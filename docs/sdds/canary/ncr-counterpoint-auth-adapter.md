---
id: sdd-cp-auth
title: NCR Counterpoint — Auth Adapter (Module A)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/pos-adapter-substrate.md
  - docs/sdds/canary/ncr-counterpoint-merchant-onboarding.md
---

# NCR Counterpoint — Auth Adapter (Module A)

## 1. Purpose

The Counterpoint REST API authenticates with HTTP Basic credentials plus an
`APIKey` request header. This SDD specifies:

1. `CounterpointBasicAuthFlow` — the auth flow class referenced by
   `CounterpointAdapter.auth_flow_class()` in the POSAdapter ABC.
2. Credential lifecycle: storage, rotation, error escalation.
3. The `test_connection()` implementation used by the onboarding wizard.
4. Middleware that injects credentials into every outbound request.

## 2. Counterpoint Auth Scheme

Every Counterpoint REST request requires three pieces:

| Element | HTTP component | Source |
|---|---|---|
| Username | `Authorization: Basic <base64(user:pass)>` | CP user account |
| Password | `Authorization: Basic <base64(user:pass)>` | CP user account |
| API Key | `APIKey: <key>` header | CP server settings |
| Company | URL path prefix `/<company_alias>/` | CP server config |

The `company_alias` is part of every URL path — it is not an auth token but
is required on every request and is logically coupled to the credential set.

### URL structure

```
http://<host>:<port>/<company_alias>/CPRestAPI/rest/<Entity>
```

Example:
```
http://192.168.1.100:8080/acmeGarden/CPRestAPI/rest/Documents
```

`company_alias` is case-sensitive and must match the server's configuration
exactly (confirmed at onboarding via `GET /APIVersion`).

## 3. CounterpointBasicAuthFlow

```python
from dataclasses import dataclass
from base64 import b64encode
import requests
from canary.services.pos.base import AuthFlow, AuthError


@dataclass(frozen=True)
class CounterpointCredentials:
    host: str
    port: int
    company_alias: str
    api_key: str
    username: str
    password: str

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}/{self.company_alias}/CPRestAPI/rest"

    @property
    def basic_header(self) -> str:
        token = b64encode(f"{self.username}:{self.password}".encode()).decode()
        return f"Basic {token}"


class CounterpointBasicAuthFlow(AuthFlow):
    """
    Stateless auth flow for NCR Counterpoint REST.

    No OAuth tokens to refresh, no expiry tracking — Basic auth credentials
    are valid until the CP admin changes the password. The only "flow" is:
    1. Load credentials from pos_tenant_credentials.
    2. Build request headers.
    3. On 401, escalate to credential_error state.
    """

    def __init__(self, credential_service, merchant_id: UUID, company_alias: str):
        self._cred_service = credential_service
        self._merchant_id = merchant_id
        self._company_alias = company_alias
        self._credentials: CounterpointCredentials | None = None

    def load(self) -> None:
        """Load credentials from encrypted store. Must be called before get_headers()."""
        raw = self._cred_service.load(
            self._merchant_id, "counterpoint", self._company_alias
        )
        if not raw:
            raise AuthError("No Counterpoint credentials found for tenant.")
        self._credentials = CounterpointCredentials(**raw)

    def get_headers(self) -> dict[str, str]:
        if not self._credentials:
            raise AuthError("Credentials not loaded — call load() first.")
        return {
            "Authorization": self._credentials.basic_header,
            "APIKey": self._credentials.api_key,
            "Accept": "application/json",
        }

    def get_base_url(self) -> str:
        if not self._credentials:
            raise AuthError("Credentials not loaded.")
        return self._credentials.base_url

    def on_auth_failure(self, response) -> None:
        """
        Called by the poll client when a 401 is received.
        Escalates credential_state to 'credential_error' and raises AuthError.
        """
        self._cred_service.set_error_state(
            self._merchant_id, "counterpoint", self._company_alias,
            error="HTTP 401 from Counterpoint — credentials rejected.",
        )
        raise AuthError(
            f"Counterpoint returned 401 for tenant {self._merchant_id}. "
            "Credential error state set."
        )
```

### AuthError

```python
class AuthError(Exception):
    """
    Raised when credentials are missing, invalid, or rejected by the provider.
    Distinguishes auth failures from transient network errors.
    """
```

## 4. HTTP Client Wrapper

All Counterpoint API calls go through a single `CounterpointClient` that:
- Injects auth headers on every request
- Handles retry on transient errors (5xx, timeout) with exponential back-off
- Calls `auth_flow.on_auth_failure()` on 401
- Raises typed exceptions for 404, 429, 5xx

```python
class CounterpointClient:
    MAX_RETRIES = 3
    RETRY_BACKOFF = (1, 5, 30)   # seconds between attempts

    def __init__(self, auth_flow: CounterpointBasicAuthFlow):
        self._auth = auth_flow
        self._session = requests.Session()

    def get(self, path: str, params: dict | None = None) -> dict:
        """
        Perform GET <base_url>/<path> with auth headers.

        Returns parsed JSON body on 2xx.
        Raises:
            AuthError     — on 401
            NotFoundError — on 404
            RateLimitError— on 429
            ProviderError — on 5xx (after retries)
            NetworkError  — on timeout / connection refused
        """
        url = f"{self._auth.get_base_url()}/{path.lstrip('/')}"
        headers = self._auth.get_headers()

        for attempt, delay in enumerate(self.RETRY_BACKOFF, 1):
            try:
                resp = self._session.get(url, headers=headers, params=params, timeout=30)
            except requests.Timeout:
                if attempt == self.MAX_RETRIES:
                    raise NetworkError(f"Timeout after {attempt} attempts: {url}")
                time.sleep(delay)
                continue
            except requests.ConnectionError as exc:
                raise NetworkError(f"Connection refused: {url}") from exc

            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 401:
                self._auth.on_auth_failure(resp)   # raises AuthError
            elif resp.status_code == 404:
                raise NotFoundError(path)
            elif resp.status_code == 429:
                raise RateLimitError(resp.headers.get("Retry-After", "unknown"))
            elif resp.status_code >= 500:
                if attempt == self.MAX_RETRIES:
                    raise ProviderError(resp.status_code, resp.text[:500])
                time.sleep(delay)
            else:
                raise ProviderError(resp.status_code, resp.text[:500])

        raise ProviderError(0, "Exhausted retries")
```

## 5. test_connection() Implementation

The `CounterpointAdapter.test_connection()` method is used by the onboarding
wizard (Step 1) and the activation health-check cron.

```python
def test_connection(self, credentials: dict) -> ConnectionTestResult:
    """
    Validate that the provided credentials can reach the Counterpoint server.

    Uses GET /APIVersion — lightweight, no data side effects.
    Returns ConnectionTestResult with success flag, version string, and error.
    """
    try:
        creds = CounterpointCredentials(**credentials)
        resp = requests.get(
            f"{creds.base_url}/APIVersion",
            headers={
                "Authorization": creds.basic_header,
                "APIKey": creds.api_key,
                "Accept": "application/json",
            },
            timeout=10,
        )
    except requests.Timeout:
        return ConnectionTestResult(
            success=False,
            error="Connection timed out. Check that the server host and port are correct.",
        )
    except requests.ConnectionError:
        return ConnectionTestResult(
            success=False,
            error="Connection refused. Check host, port, and network access.",
        )

    if resp.status_code == 200:
        data = resp.json()
        return ConnectionTestResult(
            success=True,
            version=data.get("APIVersion", "unknown"),
        )
    elif resp.status_code == 401:
        return ConnectionTestResult(
            success=False,
            error=f"Authentication failed (HTTP 401). Check username, password, and API key.",
        )
    else:
        return ConnectionTestResult(
            success=False,
            error=f"Unexpected response: HTTP {resp.status_code}. {resp.text[:200]}",
        )


@dataclass
class ConnectionTestResult:
    success: bool
    version: str | None = None
    error: str | None = None
```

## 6. Credential Lifecycle

### States

Credential state lives in `app.pos_tenant_credentials.credential_state`:

| State | Meaning | Effect on poll loop |
|---|---|---|
| `active` | Credentials valid | Poll continues normally |
| `credential_error` | 401 received from provider | Poll skipped; alert surfaced to admin |
| `suspended` | Admin-suspended | Poll skipped |
| `disconnected` | Tenant disconnected | Poll never runs |

### Error escalation

On first 401:
- `credential_state → 'credential_error'`
- `error_count += 1`
- `last_error_at = now()`
- Structured log event: `cp_auth_failure`
- Admin alert (if alert routing configured for the tenant)

Poll loop will not retry on a `credential_error` credential — it checks
`credential_state` before each poll cycle and skips if not `active`.

The admin (or installer) must re-enter credentials via the settings UI to
reset back to `active`.

### Rotation

CP does not issue short-lived tokens. Password rotation is an admin action:
1. Admin updates password in Counterpoint server
2. Admin enters new password in Canary settings UI
3. `CredentialService.rotate()` stores new encrypted blob, resets
   `credential_state = 'active'`, zeroes `error_count`

No automated rotation — CP has no refresh-token mechanism.

## 7. Security Constraints

- Credentials are never stored in plaintext anywhere in the application layer.
- The `CounterpointCredentials` dataclass is frozen and never serialized to
  JSON or logged. Its fields are redacted in all `__repr__` / `__str__` output.
- `password` and `api_key` fields are excluded from all log output via
  `structlog` bound context. Logging middleware enforces `REDACT_FIELDS = {"password", "api_key", "Authorization"}`.
- The Basic auth header is generated at request time from the decrypted blob —
  never cached in memory between requests.
- TLS is not enforced in the client (Counterpoint often runs HTTP-only on a
  LAN). A future hardening pass may add HTTPS enforcement with a per-tenant
  opt-out for on-prem deployments.

## 8. File Structure

```
canary/services/pos/
├── base.py                  # POSAdapter ABC, AuthFlow, CanonicalEvent, PollResult
├── registry.py              # register_adapter, get_adapter
└── counterpoint/
    ├── __init__.py
    ├── adapter.py           # CounterpointAdapter (implements POSAdapter)
    ├── auth.py              # CounterpointBasicAuthFlow, CounterpointCredentials
    ├── client.py            # CounterpointClient (HTTP wrapper)
    ├── parsers/
    │   ├── __init__.py
    │   ├── document.py      # parse_cp_transaction()
    │   ├── customer.py      # parse_cp_customer()
    │   ├── item.py          # parse_cp_item()
    │   └── pay_code.py      # parse_cp_pay_codes()
    └── adapters/
        ├── __init__.py
        ├── store_station.py # StoreStationAdapter.seed()
        ├── item_catalog.py  # ItemCatalogAdapter.full_sync()
        ├── customer.py      # CustomerRosterAdapter.full_sync()
        └── pay_code.py      # PayCodeAdapter.seed()
```

## 9. Acceptance Criteria

**AC-A-01 — Valid credentials:** `test_connection()` with correct credentials
returns `ConnectionTestResult(success=True, version="<version string>")`.

**AC-A-02 — Wrong password:** `test_connection()` with wrong password returns
`ConnectionTestResult(success=False, error="Authentication failed (HTTP 401)...")`.
The raw 401 is surfaced — not masked.

**AC-A-03 — Network failure:** `test_connection()` with an unreachable host
returns `ConnectionTestResult(success=False, error="Connection refused...")`.
No unhandled exception escapes.

**AC-A-04 — Auth header injection:** Every `CounterpointClient.get()` call
includes both `Authorization: Basic <...>` and `APIKey: <key>` headers.
Verified via requests mock in unit tests.

**AC-A-05 — 401 poll escalation:** When the poll client receives HTTP 401,
`credential_state` transitions to `credential_error` and the `cp_auth_failure`
event is logged. Subsequent poll cycles skip this tenant without retrying.

**AC-A-06 — No plaintext log:** `structlog` output for any Counterpoint auth
event contains no `password`, `api_key`, or `Authorization` field values.
Verified by scanning test log output for those field names.

## 10. Open Questions

| ID | Question | Impact |
|---|---|---|
| A-OQ-01 | Does NCR Counterpoint enforce per-user API permission levels? Some CP deployments limit which entities a non-admin API user can access. The test account used for sandbox should match the permission level the installer will provision in production. | Scope of readable endpoints |
| A-OQ-02 | HTTP vs HTTPS: do any Rapid POS garden-center deployments use SSL on the Counterpoint REST endpoint? If yes, the client must handle certificate validation (and potentially self-signed cert bypass). | TLS handling in client |
| A-OQ-03 | APIKey vs per-user key: is the APIKey a server-wide static key (same for all API users on the server) or per-user? If per-user, the credential bundle grows by one field and rotation scope changes. | Credential model completeness |

---

## Related

- `docs/sdds/canary/pos-adapter-substrate.md` — AuthFlow ABC; pos_tenant_credentials; CredentialService
- `docs/sdds/canary/ncr-counterpoint-merchant-onboarding.md` — test_connection() call in onboarding wizard; Step 1 UI
- `Brain/wiki/ncr-counterpoint-api-reference.md` — API endpoint reference (auth section)
