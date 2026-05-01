**DriftPOS Architecture: A Business Analyst's Summary**

*How the platform is built, and how customers get customizations without waiting for a release*

# 1. The big idea: a small core with plug-in parts

DriftPOS is built on one consistent principle across all three of its layers: the core product is intentionally small, and almost everything that makes it useful is delivered through self-contained "modules" or "extensions" that snap into the core at runtime. Instead of one giant program where every feature is hard-wired together, the system is a thin host that discovers and loads whatever modules are present, plus a library of modules - catalog, tax, point-of-sale, and so on - that can be added, removed, or replaced individually. This matters because it shapes what the company can promise customers: new tax engines, payment integrations, or customer-specific behavior can usually be delivered as a new module rather than a change to the core.

## The three layers

DriftPOS is made up of three pieces that fit together:

* **API (the back-end server).** A .NET service that holds business logic, data, and the rules everyone else relies on. It is structured as a small "host" that loads a list of feature modules from a configuration file at startup.
* **Backoffice (the web admin app).** An Angular web application used by managers and staff. The forms users see are not hard-coded; they are assembled at runtime from data the API provides plus a layer of saved user preferences.
* **Android POS (the in-store register app).** The app installed on the physical point-of-sale terminal. Because terminals are often offline and cannot rely on a server toggle, the Android side has its own extension mechanisms that work locally on the device.

All three layers share the same philosophy: ship a stable core, and let customization happen through well-defined extension points rather than through edits to the core code. The payoff is that the same DriftPOS runs for every customer, and the per-customer differences live in clearly bounded places.

# 2. How each layer is customized

## API: modules listed in a manifest

The API has a file called modules.json that lists every feature module the system should load. At startup, the host reads the list, finds each module, and asks it to register its services, endpoints, and pages. The host itself contains no knowledge of any specific customer or feature - it just runs whatever is on the list, in the order given. Adding a capability is a matter of building a new module assembly and adding its name to the manifest; the module can ship with the main solution or be "dropped in" as an external file. Within each module, several conventions handle the wiring automatically - HTTP endpoints, validation rules, command handlers, background services, and JSON converters are all discovered by pattern. The developer drops a file in the right place and follows the contract; the host finds it. The phrase the document uses is "register, don't wire."

## Backoffice: forms built from three layers of data

The Backoffice does not ship its forms as fixed designs. Every form a user sees is assembled at runtime from three sources, layered in this order:

* **Schema metadata from the API.** Field-level rules - required, min/max, regex, data type - live in a database table called AppFieldDefinition. The same rows drive both the server's validation and the client's form rules. Editing a row changes both sides on the next request, with no deployment.
* **TypeScript schema rules.** Cross-field logic that cannot be expressed as a single field's metadata - things like "this field becomes read-only after the record is created" or "these two passwords must match" - lives in code files alongside the feature. They are part of the shipped Backoffice and require a release to change.
* **User-saved layouts.** A user with the right permission can rearrange a form: move fields between cards, hide optional fields, rename labels, and add their own regex patterns on top of the metadata rules. The result is saved per user or role, and the system applies it the next time anyone opens that form.

The hierarchy is intentional. Schema metadata is the floor and cannot be weakened by anything above it - a field marked required by the API can never be hidden by a user layout. This protects data integrity while still allowing extensive presentation-level customization without a release.

## Android: a stable core plus optional add-ons

Android terminals run a compiled app, so customization here works differently. The Android side defines a stable contract module that everything else compiles against, and then offers two extension surfaces on top of it.

* **Interceptors change behavior.** Small code packages (DEX files) can be dropped into a folder on the terminal. At app startup, the system loads them and lets them "wrap" core events such as a SKU scan or a transaction completion. An interceptor can run before the normal logic, after it, or instead of it. This is how customer-specific behavior is delivered without changing the shipped app - for example, a custom barcode parser for one chain's loyalty cards.
* **Overlays change the UI.** Modal dialogs, side sheets, and full-screen prompts are managed through a registry that any feature module can plug into. New overlays are picked up automatically at build time - a developer adds the renderer and handler files, and the framework wires them in without manual edits to the rest of the app.

The trade-off on Android is real and worth noting: the device must be restarted (or the app re-launched) to pick up a new interceptor. There is no live hot-reload. In return, the system works fully offline and survives long disconnections from the server.

# 3. What this means for the business

## A worked example: a customer-specific request

The architecture document walks through a representative customer request: "Acme Corp wants their SKUs to match a custom format, the SKU field to lock after creation, the form layout rearranged for their staff, and a custom product lookup at the register that hits their internal product master before our normal lookup." None of those four pieces requires a deployment of any of the three layers. The custom SKU format is a database row in Acme's tenant - both the API and the Backoffice pick it up on the next request. The locked-after-creation behavior is already a generic pattern in the shipped Backoffice. The rearranged form layout is saved by a permitted user through the customization panel and persists for that role. The custom register-side lookup is delivered as a DEX interceptor file deployed to Acme's terminals; the shipped Android app does not change. This is the architectural payoff: the same DriftPOS host runs for Acme as for everyone else, and the differences are isolated to data rows and a single deployable extension file.

## Where each kind of change belongs

| **If you want to change…** | **It belongs in…** | **Per-tenant / no deploy?** |
| --- | --- | --- |
| A field's required-ness, range, or regex | AppFieldDefinition row (data) | Yes |
| Cross-field logic (password match, conditional read-only) | Backoffice rules file (code) | No - requires release |
| Form card order, hidden optional fields, custom labels | User-saved layout (data) | Yes (per user/role) |
| A whole new capability (tax engine, payment provider) | New API module + manifest entry | No - requires release |
| Wrap or replace a register-side event for one customer | Android interceptor DEX file | Yes (per fleet) |
| A new modal or screen on the terminal | New overlay in the Android app | No - requires release |

The first column to read is the third one. Anything marked "Yes" is a runtime change against tenant data or a fleet configuration - it does not need a release cycle. Anything marked "No" is a code change that ships to all customers. The system is deliberately designed to push as much customization as possible into the first category.

## Limitations worth being explicit about

The architecture has some honest gaps that the business should be aware of when scoping customer commitments:

* **There is no "per-tenant code" on the API.** All tenants get the same modules. Customer-specific behavior that cannot be expressed as data or as a tenant-aware setting must be handled either on the device (via an interceptor) or by gating logic on tenant identity inside a shared module.
* **Backoffice rules are global, not per-customer.** User-saved layouts are per user or role, but cross-field business rules ship in the bundle and apply everywhere. Per-role rules are achievable today by reading the user's roles inside the rule's condition, but that wiring has to be done deliberately.
* **Android extensions do not hot-reload.** A new interceptor takes effect on the next app launch, not immediately. Any "live config" feel has to be built inside the interceptor itself - typically by having it call out to the API for current settings at runtime.
* **Per-tenant Android UI is not a built-in feature.** If one customer needs a different overlay, the renderer is still in the shipped APK - the difference is gated by tenant identity inside the handler, not by registration.

## Operational implications

A few facts that affect support and operations are worth keeping in mind. Module load order matters - some modules depend on services registered by earlier ones, so the manifest order is meaningful. Each tenant has its own database, which means each gets its own database connection pool; capacity planning needs to account for this when tenant counts grow. Tenant identity is established per request, so any host instance can serve any tenant and the API scales horizontally without affinity. Background services that assume they are the only one running (such as the tenant provisioning worker) need either leader election or single-instance deployment when running in multiple replicas.

## The bottom line

DriftPOS is engineered so that the most common customer asks - new validation rules, rearranged forms, customer-specific register behavior, third-party integrations - can be answered through configuration, data changes, or isolated extensions rather than through edits to the core product. The core stays the same for every customer, which keeps maintenance and quality manageable as the customer base grows. Where the architecture has limits (per-tenant code, hot reload on devices, per-tenant UI), those limits are clearly delineated and well-understood by the engineering team. For a business analyst scoping a new customer request, the practical question is usually: which of the four extension surfaces does this fit into - a metadata change, a saved layout, a new module, or a device interceptor - and the answer determines whether the work is configuration, a release, or somewhere in between.

## What this summary leaves out

For brevity, this summary skips a number of implementation details that the original document covers: the specifics of the API host's middleware pipeline order; how JSON polymorphism is wired so that generated client code stays in sync; the reflection patterns Android interceptors use to reach app-module singletons; the exact REST endpoints the Backoffice expects for layout persistence; and the file map of reference implementations on each layer. If a specific customer commitment hinges on one of these areas, the source document is the place to look - it has worked code samples and links to canonical files for each topic.