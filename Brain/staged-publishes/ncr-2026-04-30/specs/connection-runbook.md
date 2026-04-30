---
title: Connection Runbook — Windows Host Stand-up
tags: [specs, counterpoint, runbook, deployment, auth]
nav_order: 55
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---

---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: github.com/NCRCounterpointAPI/APIGuide v2.4 (cloned)
----

# NCR Counterpoint API — Connection Runbook

## Governing thesis

Bringing a Counterpoint REST API server up is a Windows-on-prem exercise:
download the .exe from NCR's partner FTP, install on a Windows host with
.NET 4.5.2, register the customer's company database against it, drop a
signed APIKey XML file into the `APIKeys/` folder, prove the loop with a
single `GET /SystemInfo`. Fifteen minutes if the customer has the
registration.ini API option already paid for; an unbounded wait
otherwise. Everything else in this runbook is the disambiguation between
the four error states you actually hit (401 / 403 / 404 / 500) and the
one piece of TLS plumbing that bites every Windows 7 deployment.

## Prerequisites

| Item | Requirement | Source |
|---|---|---|
| OS | Windows 7 desktop or Windows Server 2012 R2 or newer | README.md §Requirements |
| .NET | 4.5.2 | README.md §Requirements |
| RAM | 4 GB minimum, 8 GB recommended | README.md §Requirements |
| Counterpoint version | v8.5.7.2 or v8.6.0.0 (tested matrix as of API v2.4) | README.md §Supported Counterpoint versions |
| Counterpoint API option | API user option enabled in customer's `registration.ini` (paid add-on; not all merchants have it) | README.md §Requirements + Licensing.md |
| Network | Open HTTP/HTTPS port for the API service to bind. Default port `52000`; samples use `81`. | Installing.md |
| TLD access | API service account must have read/write on the company TLD (UNC path is OK) | Installing.md §Permissions |
| SQL access | API service account must have admin on the Counterpoint SQL database (creates a `KeyValueData` table) | Installing.md §Changes to Counterpoint databases |
| Offline databases | Not supported | README.md §Requirements |

## Bring-up steps

### 1. Get NCR FTP credentials and download the test database

The test database FTP host is `files165.cyberlynk.net`, with credentials
issued by NCR per partner. Use it to pull a known-good Counterpoint test
DB + TLD if you don't already have a customer DB to point at — the public
automated test suite at `github.com/NCRCounterpointAPI/APITests` is
designed to run against this DB.

For production: skip this and point at the customer's actual DB + TLD.

### 2. Install the Counterpoint API server

Per `InstallationAndConfiguration/Installing.md`:

1. Download the latest installer from
   `https://retailchannel.radiantsystems.com/counterpoint-rest-api.htm`
   (Partner Portal credentials required).
2. Run the .exe on the target Windows host. Default install path is
   `C:\Program Files (x86)\NCR\Counterpoint API`. Override if needed.
3. The installer registers the service "NCR Counterpoint API" (visible
   in `services.msc`) and binds it to port 52000 by default with a
   self-signed cert.
4. Verify the service started: `https://<host>:52000/app/index.htm#/login`
   should load the management console.

Port collision is the most common install failure — if the service
won't start, check the Windows event log; reassign the port by editing
`<install>/CPAPI.Console.exe.config` and rebind the SSL cert to the new
port (per Installing.md §Certificates and SSL).

### 3. Configure the API server

Per `InstallationAndConfiguration/Configuring.md`:

1. Log into the management console as the default sysadmin
   (`admin` / `password` — change immediately).
2. **Add a sysadmin** for yourself (Configuration → Add Admin User).
3. **Register the company** (Configuration → Companies → Add):
   - Name: company alias (must match the alias in `companies.ini` if
     you want the alias to be portable).
   - TLD: UNC or local path to the TLD root.
   - Server / Database: SQL Server host + database name.
   - Security: Integrated or SQL — SQL creds must have admin on the DB.
4. **Designate a company admin** — one of the existing Counterpoint
   user IDs in the company. They will administer roles for that
   company.
5. **Create roles + assign endpoints + users** — Roles → Edit Roles,
   then Roles → Edit User Roles. The user ID format for company-scoped
   logins is `<company-alias>.<counterpoint-user>` (e.g. `TESTGOLF.MGR`).
6. **Install your APIKey** — drop the signed `<AppName>_key.xml` file
   into `<install>/APIKeys/`, OR call `POST /APIKey` against the
   running server. List with `GET /APIKeys` to confirm.

### 4. Verify with `GET /SystemInfo`

The smallest possible health check. No APIKey required, no registration
option required, no company prefix required.

```
curl -k -u "admin:CHANGEME" https://<host>:52000/SystemInfo
```

200 + a `SystemInfo` block with `ServerCodeVersion` and
`ServerLastStartedDateTime` means you are up. Anything else: see the
Troubleshooting section.

## Auth bootstrap

The API uses HTTP Basic + an `APIKey` request header. Three things vary
by call type:

| Call class | Authorization | APIKey header | Username format |
|---|---|---|---|
| System administration (sysadmin login) | Basic | usually absent | `admin` (no company prefix) |
| Company-level read / write | Basic | required | `<company>.<user>` |
| `POST /NSPTransaction`, `POST /Store/{StoreId}/Tokenize`, `GET /Stores/Tokenized` | Basic | NOT required | `<company>.<user>` |

### Constructing the Basic Auth header

Standard RFC 7617. The string is `<userid>:<password>`, base64-encoded,
prefixed with `Basic `. For company endpoints the user ID gets the
company prefix:

```
$ printf '%s' 'TESTGOLF.MGR:password1' | base64
VEVTVEdPTEYuTUdSOnBhc3N3b3JkMQ==

Authorization: Basic VEVTVEdPTEYuTUdSOnBhc3N3b3JkMQ==
```

Per `Basics/Requests.md`: base64 is encoding, not encryption. Do not skip
TLS.

### Registering an APIKey

Two paths. Both end with the signed XML key file in
`<install>/APIKeys/`:

**Path A — drop in the folder:** copy the `<AppName>_key.xml` you got
from NCR (the .txt sibling is the plaintext value, kept by the app
developer) into the server's `APIKeys/` directory. The cache reloads on
the next `GET /APIKeys`.

**Path B — POST it:**

```
curl -k -u "admin:CHANGEME" \
  -X POST \
  -H "Content-Type: application/xml" \
  --data-binary @AppName_key.xml \
  https://<host>:52000/APIKey
```

Then call `GET /APIKeys` to confirm. For the calling application, the
plaintext key value (from the `.txt` sibling) goes in the `APIKey`
request header on subsequent calls — never the XML file content.

### When to use sysadmin vs company-prefixed creds

- Sysadmin (`admin` etc., no prefix): SystemInfo, AdminUsers, APIKey,
  APIKeys, Database / Databases, Roles, all of `/Users` and
  `/CompanyAdmins/*`. Anything that operates the API server itself.
- Company-prefixed (`<company>.<user>`): everything else. Customers,
  documents, items, inventory, stores, gift cards, tax codes, pay codes,
  EC, Workgroup, VendorItem, tokenization.

If you cross the streams (sysadmin for a company endpoint or
company-prefixed for a sysadmin endpoint), you'll get 401 with a generic
message — not 403.

## First three smoke-test calls

All three use placeholder creds; substitute real values per tenant.

### 1. `GET /SystemInfo` — server is alive

```
curl -k -u "admin:CHANGEME" \
  -H "Accept: application/json" \
  https://localhost:52000/SystemInfo
```

Expected 200 with `ErrorCode: SUCCESS` and a `SystemInfo` object.

### 2. `GET /Store/{StoreID}` — first company-scoped call

There is **no `GET /Stores` (plural) endpoint** in this API surface.
The way to enumerate stores is to know one ID first (from
`companies.ini`, from the customer, or from a `GET /InventoryLocations`
that returns location IDs cross-referenceable to stores) and call the
single-store endpoint. For a smoke test, use a known store such as
`MAIN` from the test DB.

```
curl -k \
  -u "TESTGOLF.MGR:password1" \
  -H "APIKey: vpmk0tqApzFu5EesAMQgstBtQAEwK1ySwMZ4zwiC" \
  -H "Accept: application/json" \
  https://localhost:52000/Store/MAIN
```

Expected 200 with a `PS_STR` object. If 403, the registration option is
missing; if 404, the StoreID is not in `PS_STR`.

### 3. `GET /TaxCodes` — read against TX_COD

```
curl -k \
  -u "TESTGOLF.MGR:password1" \
  -H "APIKey: vpmk0tqApzFu5EesAMQgstBtQAEwK1ySwMZ4zwiC" \
  -H "Accept: application/json" \
  https://localhost:52000/TaxCodes
```

Expected 200 with a `TaxCodes` array of `TX_COD` records. This call is
small, cached server-side for 24h, and exercises the company-prefixed
auth + APIKey + cache path in one shot.

If all three return 200, integration is ready for adapter work to
begin.

## Troubleshooting

### Status-code disambiguation

| Code | Most common cause | What to check first |
|---|---|---|
| **401 Unauthorized** | Bad/missing Basic auth header; bad company prefix on a company endpoint; sysadmin creds on a company endpoint or vice versa | Decode the base64 of the Authorization header and confirm the username format matches the call class. |
| **403 Forbidden** | (a) APIKey header missing/invalid/expired; (b) company `registration.ini` lacks the API option; (c) per-role permissions deny this endpoint+verb to this user | Check `GET /APIKeys` for installed keys + expiry; check the registration.ini on the customer's Counterpoint host; check `GET /Role/{RoleName}` for the user's roles. |
| **404 Not Found** | Resource ID does not exist in the underlying table | For `GET /Customer/{CustNo}` → CUST_NO not in AR_CUST. For `GET /Item/{ItemNo}` → ITEM_NO not in IM_ITEM. Etc. |
| **500 Internal Server Error** | Unexpected server-side fault; commonly DB connectivity, TLD permissions, or a code defect | Check `<install>/Logfiles/CPAPI.log` (rolling, default 10-day retention); check the Counterpoint DB is reachable; check TLD UNC path is readable by the service account. |

### ServerCache invalidation

Per `Basics/Requests.md`, the API caches a small set of mostly-static
data for 24 hours: Company, Customer Control, Databases, eCommerce
Control, eCommerce Categories, Gift Card Codes, Inventory Control, Item
Categories, Items (master, not inventory), PayCodes, Stores, Stations,
Tax Codes, Workstations.

When you change one of these via the Counterpoint UI (not via the API),
the API does not know. Three ways to force a refresh:

1. Restart the service.
2. `DELETE /CACHE` — invalidates the company-scoped cache for the
   authenticated company.
3. Add header `ServerCache: no-cache` to a single call — invalidates
   the company-scoped cache before serving the call.

For TSP adapter work, prefer option 3 on the first call of each polling
window when the upstream data is known to have been edited via the
Counterpoint UI.

### Common ErrorCodes

Source: `Basics/Responses.md`. Returned in the response body alongside
HTTP status:

| ErrorCode | When | Mitigation |
|---|---|---|
| `SUCCESS` | OK on 2xx | none |
| `ERROR_MISSING_REQUIRED_DATA` | POST/PATCH/PUT body missing required field | add the field per endpoint doc |
| `ERROR_RECORD_NOT_FOUND` | GET against an ID not in the underlying table | check the ID |
| `ERROR_INVALID_APIKEY` | APIKey header value not in the server's signed-cache | reinstall the key + force-reload via `GET /APIKeys` |
| `ERROR_DOCUMENT_ALREADY_COMPLETED` | trying to mutate a posted document | only unposted (status `T`/`O`/`L`) docs accept further mutations |
| `ERROR_DOCUMENT_NOT_FULLY_PAID` | document needs full tender before close | add a `PS_DOC_PMT` row that brings the balance to zero |
| `ERROR_CARD_PAYMENT_FAILED` | Secure Pay processor rejected the card | check Monetra logs; retry with valid card |
| `ERROR_INVALID_GIFTCARD_PAYMENT` | gift card balance < amount, or expired | check `GET /GiftCard/{GiftCardNo}` |
| `ERROR_AR_PAYMENT_FAILED` | AR charge failed (over credit limit, etc.) | check `GET /Customer/{CustNo}` for credit fields |
| `ERROR_INVALID_LIN_TYP` | unknown PS_DOC_LIN.LIN_TYP value | use a valid LIN_TYP per the PS_DOC_LIN schema |
| `ERROR_NOT_PURE_ORDER` | conversion rule violated | review the document state transitions |
| `ERROR_DOCUMENT_HAS_SHIPPING_ADDRESS` / `ERROR_DOCUMENT_HAS_BILLING_ADDRESS` | trying to add a contact when one is already attached | DELETE first, then POST |
| `ERROR_INVALID_CONTACT_ID` | non-existent CONTACT_ID on PATCH/PUT/DELETE Contact | verify with `GET /Document/{DocId}` |
| `ERROR_DOCUMENT_BILLING_ADDRESS_NOT_FOUND` / `ERROR_DOCUMENT_SHIPPING_ADDRESS_NOT_FOUND` | DELETE Contact when none attached | check current document state first |
| `ERROR_INVALID_CONFIGURATION` | server-side configuration broken | check service logs and registration |
| `ERROR_UNKNOWN` | unhandled fault | read the `Message` field; escalate with the log entry |

### TLS gotchas (Windows 7)

Per `InstallationAndConfiguration/TLS1.2.md`:

- Default install gives a self-signed cert that's TLS-1.2 capable but
  browsers will warn. Add the cert to Trusted Root or accept the
  exception in dev.
- On Windows 7 with TLS 1.1 disabled and only TLS 1.2 enabled, the
  default Windows cipher order may not include a TLS 1.2 cipher Chrome
  accepts. Move `TLS_RSA_WITH_AES_128_GCM_SHA256` to the top of the
  Windows cipher list (use IIS Crypto or group policy) — NCR's
  documented workaround.
- Production: replace the self-signed cert with a CA-issued cert. Stop
  the service, unbind the self-signed cert from the port, install the
  new cert into Local Machine, bind it to the port, restart the
  service.

### Cache misbehavior after a Counterpoint UI edit

If a Canary adapter call returns stale data right after a Counterpoint
UI edit, the cache is the cause 95% of the time. Either resync with
`ServerCache: no-cache` on the first call of the next poll, or have ops
issue `DELETE /CACHE` after large overnight edits.

### Service account permissions

The most common silent failure is the service running under
`LocalSystem` while the TLD lives on a network share that
`LocalSystem` can't reach. Reconfigure the service to run under a
domain account that has read/write on the TLD UNC path and admin on
the SQL database. See Installing.md §Service Account.

## Related

- `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` — endpoint × CRDM
  × spine module map.
- `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — full OpenAPI 3.0
  spec.
- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — the
  integration SDD this runbook supports.
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — source corpus
  (README, Basics, InstallationAndConfiguration, Endpoints, Release Notes).
