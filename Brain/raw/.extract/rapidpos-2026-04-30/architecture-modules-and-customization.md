Table of Contents

# []{#anchor}[]{#anchor-1}DriftPOS Architecture: Modules and Customization

DriftPOS is a three-layer system - a .NET API, an Angular Backoffice,
and an Android POS app - that shares one principle across all three: the
host is small and the modules plug in. Tenants get isolated databases,
modules get loaded by name, forms get reshaped by metadata, and the POS
device runs DEX files dropped into its cache directory. Nothing in the
core code path knows about a specific customer.

This guide is the end-to-end story. It covers how each layer is wired,
how each one is customized without touching shipped code, and how the
layers compose so that a single customization request - "give Acme Corp
a custom SKU-submit behavior with a new form layout and a new validation
rule" - can be answered without a deployment on any layer.

The first nine sections cover the API in depth. Sections 10 and 11 cover
the Backoffice and Android. Sections 12 and 13 stitch them together for
cross-layer scenarios and operational concerns. Section 14 is the file
map.

## []{#anchor-2}[]{#anchor-3}1. The shape of the system

![](media/image1.png){width="7.10451in" height="3.1564in"}

Three properties hold across all three layers:

1.  **The API host doesn't know its modules.** A module is just an
    assembly name in *modules.json*. The host reflects across loaded
    assemblies and wires whatever it finds. Adding a tax engine, a new
    tender type, or a customer-specific endpoint is a new module, not a
    code change in the host.

<!-- -->

2.  **The Backoffice doesn't hard-code its forms.** Field validation,
    visibility, readonly state, and card layouts are all driven by data
    the API returns - either schema metadata, registered TypeScript
    schema rules, or a saved *FormLayoutConfig*. A user with the right
    permission can rearrange a form without a deployment.

<!-- -->

3.  **The Android POS app extends without recompiling.**
    Compiled-once-and-shipped behavior can be wrapped, replaced, or
    supplemented by interceptor DEX files loaded at startup, and the
    entire overlay/modal surface is a registry that any feature module
    can plug into via a KSP-generated registration call.

The API is a modular monolith - a thin host (*DriftPOS.WebHost*) owns
the ASP.NET Core pipeline; everything else - entities, EF
configurations, services, validators, minimal-API endpoints, MVC
controllers, and Razor Pages - lives inside isolated module assemblies
that are discovered and wired in at startup.

![](media/image2.png){width="5.83333in" height="9.98382in"}

Every module follows the same internal layout:

*DriftPOS.Module.\<Name\>/*\
*Domain/ entities, enums, value objects*\
*Application/ services, command handlers, mappers*\
*Infrastructure/ EF configurations, hosted services, options*\
*Presentation/*\
*Api/Endpoints/ IEndpointMap implementations (minimal API)*\
*Api/Models/ request/response DTOs*\
*Pages/ Razor Pages (.cshtml + .cshtml.cs)*\
*\<Name\>ModuleInitializer.cs*

This is enforced by
[docs/dev/project_structure.rule.md](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/docs/dev/project_structure.rule.md&version=GBdevelopment).
The host has *no* knowledge of any module's internals - it only knows
the contracts in *DriftPOS.Shared.Infrastructure*.

## []{#anchor-3}[]{#anchor-4}2. The module manifest: *modules.json*

[src/DriftPOS.WebHost/modules.json](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/modules.json&version=GBdevelopment)
is a flat, ordered list of assembly names:

*\[*\
*{ \"Name\": \"DriftPOS.Module.Tenants\" },*\
*{ \"Name\": \"DriftPOS.Module.Catalog\" },*\
*{ \"Name\": \"DriftPOS.Module.Crm\" },*\
*{ \"Name\": \"DriftPOS.Module.Purchasing\" },*\
*{ \"Name\": \"DriftPOS.Module.PointOfSale\" },*\
*{ \"Name\": \"DriftPOS.Module.Sync\" },*\
*{ \"Name\": \"DriftPOS.Module.Tax\" },*\
*{ \"Name\": \"DriftPOS.Module.App\" },*\
*{ \"Name\": \"DriftPOS.Module.Reporting\" },*\
*{ \"Name\": \"DriftPOS.Module.Ui\" }*\
*\]*

The order matters: *LoadAndConfigureModules* calls each module's
*ConfigureServices* in this sequence, so a module that depends on
services registered by another (e.g. anything that uses tenant identity
expects *Tenants* first) must come after it.

Adding a module is a two-step change:

1.  Reference the module project from *DriftPOS.WebHost.csproj* (or drop
    a built DLL into the host's bin folder; see [Section
    9](#X1ac59d8b6a8494f64a683e66b67627a49a95f89)).

<!-- -->

2.  Add an entry to *modules.json*.

Removing a module is the inverse. The host code is untouched in either
case.

## []{#anchor-4}[]{#anchor-5}3. How modules are discovered and loaded

### []{#anchor-5}[]{#anchor-6}*GlobalConfiguration.EnsureModulesLoaded*

[src/Shared/DriftPOS.Shared.Infrastructure/GlobalConfiguration.cs:165](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/GlobalConfiguration.cs&version=GBdevelopment&line=165)

***public** **static** IReadOnlyList\<Module\>
EnsureModulesLoaded(string? basePath = **null**)*\
*{*\
***if** (\_modulesLoaded && Modules.Count \> 0)*\
***return** Modules;*\
\
***lock** (\_modulesLock)*\
*{*\
*var modulesPath = FindModulesJson(basePath);*\
*var moduleDefinitions =
JsonSerializer.Deserialize\<List\<ModuleDefinition\>\>(*\
*File.ReadAllText(modulesPath))!;*\
\
***foreach** (var moduleDef **in** moduleDefinitions)*\
*{*\
*var assembly = Assembly.Load(moduleDef.Name);*\
*Modules.Add(**new** Module(moduleDef.Name, **null**, assembly));*\
*}*\
\
*\_modulesLoaded = **true**;*\
*}*\
\
***return** Modules;*\
*}*

Three things to notice:

- **It reads the JSON, then Assembly.Load(name)s each one.** The CLR's
  normal probing (the host's bin directory, *AdditionalProbingPaths*,
  etc.) decides where the DLL actually comes from.
- **Lazy + idempotent.** Both the web host *and* CLI tools (codegen,
  seed-runner) call this. *\_modulesLoaded* keeps the list stable across
  calls in the same process.
- **GlobalConfiguration.Modules is the canonical list.** Other layers
  (handler discovery, endpoint discovery, codegen) read from it instead
  of re-scanning *AppDomain.CurrentDomain.GetAssemblies()*, which keeps
  the surface deterministic.

*FindModulesJson* walks a few candidate paths (CWD, app base directory,
*src/DriftPOS.WebHost/*) so the same loader works whether you're running
the API, an EF migration, or a CLI tool.

### []{#anchor-6}[]{#anchor-7}*LoadAndConfigureModules*

[GlobalConfiguration.cs:198](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/GlobalConfiguration.cs&version=GBdevelopment&line=198)

***public** **static** void LoadAndConfigureModules(IServiceCollection
services, IConfiguration configuration, \...)*\
*{*\
*EnsureModulesLoaded(basePath);*\
\
***foreach** (var module **in** Modules)*\
*{*\
*var moduleInitializerTypes = module.Assembly!*\
*.GetTypes()*\
*.Where(t =\> **typeof**(IModuleInitializer).IsAssignableFrom(t)*\
*&& !t.IsAbstract && !t.IsInterface);*\
\
***foreach** (var moduleInitializerType **in** moduleInitializerTypes)*\
*{*\
*var moduleInitializer =
(IModuleInitializer)Activator.CreateInstance(moduleInitializerType)!;*\
*moduleInitializer.ConfigureServices(services, configuration);*\
*}*\
*}*\
*}*

For each loaded assembly it reflects on every concrete
*IModuleInitializer* and calls *ConfigureServices*. The host calls this
from *AddModules*
([DependencyInjection.cs:666](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=666)).

## []{#anchor-7}[]{#anchor-8}4. The *IModuleInitializer* contract

[src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IModuleInitializer.cs&version=GBdevelopment)

***public** **interface** IModuleInitializer*\
*{*\
*void ConfigureServices(IServiceCollection services, IConfiguration
configuration);*\
*void Use(WebApplication app);*\
*void RegisterJsonPolymorphism();*\
*}*

The three methods correspond to three startup phases:

  Method                       When it runs                  Purpose
  ---------------------------- ----------------------------- --------------------------------------------------------------------------------------------------------------------------
  *ConfigureServices*          During *builder.Services*     Register DI (services, options, hosted services, named clients, EF interceptors, auth schemes, etc.)
  *Use*                        During *app.UseModules()*     Register middleware that must sit inside the pipeline (e.g. tenant resolution middleware, custom metadata handlers)
  *RegisterJsonPolymorphism*   Startup *and* codegen tools   Wire *JsonTypeInfo.PolymorphismOptions* so polymorphic types serialize identically at runtime and during code generation

A typical initializer
([CatalogModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Catalog/CatalogModuleInitializer.cs&version=GBdevelopment)):

***internal** **sealed** **class** CatalogModuleInitializer :
IModuleInitializer*\
*{*\
***public** void ConfigureServices(IServiceCollection services,
IConfiguration configuration)*\
*{*\
*services.AddTransient\<ISkuGeneratorService, SkuGeneratorService\>();*\
*services.AddScoped\<IItemService, ItemService\>();*\
*services.AddScoped\<IStockEventService, StockEventService\>();*\
\
*services.Configure\<StockProjectionListenerOptions\>(*\
*configuration.GetSection(StockProjectionListenerOptions.SectionName));*\
*services.AddHostedService\<StockProjectionListener\>();*\
\
*services.AddOptions\<AiOptions\>()*\
*.BindConfiguration(\"Ai\")*\
*.ValidateDataAnnotations()*\
*.ValidateOnStart();*\
\
*// \...*\
*}*\
\
***public** void Use(WebApplication app) { }*\
***public** void RegisterJsonPolymorphism() { /\* No-op \*/ }*\
*}*

The *Tenants* module is the heaviest user of *ConfigureServices* because
it owns identity, OpenIddict, the per-tenant *NpgsqlDataSource*, and the
tenant-resolution middleware. See
[TenantModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Tenants/TenantModuleInitializer.cs&version=GBdevelopment).

> Multiple *IModuleInitializer* implementations *per assembly* are
> allowed. The reflection scan picks them all up. Use this when a single
> module wants to split unrelated wiring (e.g. one initializer for HTTP,
> one for background services).

## []{#anchor-8}[]{#anchor-9}5. After services: discovering controllers, Razor Pages, and validators

Once modules are loaded,
[DependencyInjection.AddModules](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=666)
iterates them and folds each assembly into the MVC + Razor stack as an
*ApplicationPart*:

***foreach** (var module **in** GlobalConfiguration.Modules)*\
*{*\
*services.AddRazorPages(options =\>*\
*{*\
*options.Conventions.ConfigureFilter(**new**
IgnoreAntiforgeryTokenAttribute());*\
*options.RootDirectory = \"/Presentation/Pages\";*\
*})*\
*.AddApplicationPart(module.Assembly);*\
\
*services.AddControllers().AddApplicationPart(module.Assembly);*\
*services.AddControllersWithViews().AddApplicationPart(module.Assembly);*\
*services.AddMvc().AddApplicationPart(module.Assembly);*\
\
*services.AddValidatorsFromAssembly(*\
*module.Assembly,*\
*includeInternalTypes: **true**,*\
*filter: result =\>
result.ValidatorType.Namespace?.Contains(\".Seeding.\") != **true**);*\
*}*\
\
*services.AddEndpoints();*\
*services.AddCommandHandlers();*

This is what makes "drop a module in" actually work end-to-end:

- **Razor Pages.** *RootDirectory = \"/Presentation/Pages\"* plus
  *AddApplicationPart* means a *.cshtml* file at
  *DriftPOS.Module.Tenants/Presentation/Pages/Login.cshtml* is served at
  */Login* *as if it lived in the host project*. Examples in the wild:

<!-- -->

- - [DriftPOS.Module.Tenants/Presentation/Pages/](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Tenants/Presentation/Pages/&version=GBdevelopment) -
    sign-in, MFA, password reset, employee management
  - [DriftPOS.Module.PointOfSale/Presentation/Pages/Devices/](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.PointOfSale/Presentation/Pages/Devices/&version=GBdevelopment) -
    terminal pairing flow

<!-- -->

- **Controllers / MVC / ControllersWithViews.** Lets a module ship
  classic MVC controllers if it needs to (rare; minimal APIs are the
  default - see [Section 6](#X6ca310897a5879cffb031e665cc51b0e5a6e506)).
- **FluentValidation validators.** *AddValidatorsFromAssembly* registers
  every *AbstractValidator\<T\>* in the module so the request-pipeline
  filters can resolve them by request DTO type. The *Seeding* namespace
  is excluded because seed-time validators take constructor arguments DI
  cannot resolve.

The host's own *Pages/* folder still works for host-level views
([Pages/Error.cshtml](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/Pages/Error.cshtml&version=GBdevelopment),
shared *\_Layout.cshtml*); modules just contribute to the same pool.
*\_ViewImports.cshtml* and *\_ViewStart.cshtml* resolution follow
standard ASP.NET rules across application parts.

The host's static *Program.cs* then calls these mappers exactly once,
regardless of how many modules contributed:

*app.MapControllers();*\
*app.MapRazorPages();*

See
[Program.cs:120-121](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/Program.cs&version=GBdevelopment&line=120).

## []{#anchor-10}[]{#anchor-11}6. Minimal-API endpoints via *IEndpointMap*

Most module HTTP surface is built on minimal APIs, not controllers. The
contract:

[src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IEndpointMap.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IEndpointMap.cs&version=GBdevelopment)

***public** **interface** IEndpointMap*\
*{*\
*string Tag { **get**; }*\
*string Endpoint { **get**; }*\
*void MapEndpoints(IEndpointRouteBuilder app);*\
*}*

### []{#anchor-11}[]{#anchor-12}Discovery

*AddEndpoints*
([DependencyInjection.cs:79](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=79))
reflects across **all** loaded assemblies, finds every concrete
*IEndpointMap*, and registers each as a transient service:

*var serviceDescriptors = assemblies*\
*.SelectMany(a =\> a.GetLoadableTypes()*\
*.Where(t =\> **typeof**(IEndpointMap).IsAssignableFrom(t) &&
!t.IsInterface && !t.IsAbstract))*\
*.Select(type =\> ServiceDescriptor.Transient(**typeof**(IEndpointMap),
type));*\
\
*services.TryAddEnumerable(serviceDescriptors);*

### []{#anchor-12}[]{#anchor-13}Mapping

*UseModules*
([DependencyInjection.cs:53](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=53))
runs *Use(app)* on every initializer and then calls *MapEndpoints*,
which walks the registered *IEndpointMap*s and gives each one an
*IEndpointRouteBuilder*:

***public** **static** IApplicationBuilder MapEndpoints(**this**
WebApplication app, RouteGroupBuilder? routeGroupBuilder = **null**)*\
*{*\
***foreach** (IEndpointMap endpoint **in**
app.Services.GetRequiredService\<IEnumerable\<IEndpointMap\>\>())*\
*endpoint.MapEndpoints(routeGroupBuilder ??
(IEndpointRouteBuilder)app);*\
\
***return** app;*\
*}*

### []{#anchor-13}[]{#anchor-14}A typical endpoint map

[ItemEndpoints.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Catalog/Presentation/Api/Endpoints/v1/ItemEndpoints.cs&version=GBdevelopment):

***public** **class** ItemEndpoints : IEndpointMap*\
*{*\
***public** string Endpoint =\> \"items\";*\
***public** string Tag =\> \"Items\";*\
\
***public** void MapEndpoints(IEndpointRouteBuilder app)*\
*{*\
*var group = app.MapGroup(Endpoint)*\
*.WithTags(Tag)*\
*.WithModelBindingErrorHandling();*\
\
*group.MapGet(GetItems).WithName(\"GetItems\")\...;*\
*group.MapGet(\"{id:long}\",
GetItemById).WithName(\"GetItemById\")\...;*\
*group.MapPost(CreateItem).WithName(\"CreateItem\")\...;*\
*group.MapPut(\"{id:long}\", UpdateItem).WithName(\"UpdateItem\")\...;*\
*group.MapMethods(\"{id:long}\", \[\"PATCH\"\], PatchItem)\...;*\
*// \...*\
*}*\
*}*

Key conventions:

- **One IEndpointMap per resource family** (*Items*, *ItemBarcodes*,
  *ItemDepartments*, ...). They live under
  *Presentation/Api/Endpoints/v{n}/*.
- **Tag** controls the OpenAPI grouping shown in Swagger/ReDoc.
- **Endpoint** is the route prefix; everything else is relative to it.
- **Handlers are static-style methods** receiving services via parameter
  injection.

## []{#anchor-14}[]{#anchor-15}7. Command handlers, validators, and other auto-discovered DI

Beyond endpoints, several other registrations sweep across module
assemblies:

- **AddCommandHandlers**
  ([DependencyInjection.cs:636](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=636))
  registers every *ICommandHandler* implementation as scoped. Modules
  can drop a handler in and it's wired automatically.
- **AddValidatorsFromAssembly** registers every
  *AbstractValidator\<T\>*.
- **GlobalConfiguration.AddConvertersFromAssemblies**
  ([GlobalConfiguration.cs:57](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/GlobalConfiguration.cs&version=GBdevelopment&line=57))
  scans for *JsonConverter* types and adds them to both API and DB
  serializer options.
- **OpenTelemetry meter/source wildcards**
  ([DependencyInjection.cs:282](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=282)).
  Any *Meter*/*ActivitySource* named
  *\"DriftPOS.\<Module\>.\<Feature\>\"* is automatically captured. New
  modules need only follow the naming convention.
- **EF configurations** are picked up by the shared DbContext via
  assembly scanning over *GlobalConfiguration.Modules* (see the database
  layer docs).

In every case, the contract is the same: implement an interface or
follow a naming convention, drop the file in, and the host finds it.

## []{#anchor-16}[]{#anchor-17}8. The host pipeline, in order

[Program.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/Program.cs&version=GBdevelopment)
is intentionally short; the order matters and is annotated:

*0. UseForwardedHeaders (preserve Azure HTTPS scheme)*\
*1. UseHttpsRedirection*\
*2. UseDriftExceptionHandler*\
*3. UseSerilogRequestLogging*\
*4. UseResponseCompression*\
*5. UseResponseCaching*\
*6. UseDefaultFiles / UseStaticFiles*\
*7. UseSwagger / UseSwaggerUI / UseReDoc*\
*8. UseCors(\"ConfiguredOrigins\")*\
*9. UseRouting*\
*10. UseDriftLoggingMiddleware*\
*11. UseAuthentication*\
*12. UseAuthorization*\
*13. UseMetadataHandler*\
*14. UseModules (modules\' Use(app) + MapEndpoints)*\
*15. MapWebApp / MapControllers / MapRazorPages*\
* + Prometheus, /health, /docs*

Step 14 is where modules join the request pipeline. By then auth and
routing are wired, so module endpoints can call *RequireAuthorization*,
read tenant identity, etc., without setup.

## []{#anchor-17}[]{#anchor-18}9. Out-of-tree modules

The mechanism does not assume modules are part of the host's solution.
Any DLL placed where the runtime can probe for it - the host's bin
folder, an *AdditionalProbingPaths* location, or a custom plugin
directory - and listed in *modules.json* will be loaded by
*Assembly.Load(name)*. As
[DependencyInjection.cs:661](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=661)
puts it:

> This also allows to implement a plugin system where we can load
> modules from a directory.

Two practical paths today:

1.  **Solution-tree module.** Reference the project from
    *DriftPOS.WebHost.csproj*, add to *modules.json*. This is what every
    shipped module does.

<!-- -->

2.  **External module.** Build the module DLL against
    *DriftPOS.Shared.Infrastructure* (and any modules whose contracts it
    consumes), drop the DLL next to the host, and add the assembly name
    to *modules.json*. The host finds the *IModuleInitializer* via
    reflection and the rest of the pipeline picks up its endpoints,
    controllers, Razor Pages, validators, and JSON converters with no
    host changes.

*SampleModules/DriftPOS.Module.Avalara* is a stub demonstrating the
second path - a self-contained module that wires a third-party
*AvaTaxClient* singleton in *ConfigureServices* and contributes its own
endpoints. See
[AvalaraModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/SampleModules/DriftPOS.Module.Avalara/AvalaraModuleInitializer.cs&version=GBdevelopment).

### []{#anchor-18}[]{#anchor-19}Common API customization recipes

#### []{#anchor-19}Add a new HTTP resource

1.  Create *Presentation/Api/Endpoints/v1/MyResourceEndpoints.cs*
    implementing *IEndpointMap*.

<!-- -->

2.  Register any required services in your
    *\<Module\>ModuleInitializer.ConfigureServices*.

<!-- -->

3.  Done. Discovery and mapping are automatic.

#### []{#anchor-19}Replace a service implementation in a module

In your downstream module's *ConfigureServices*, register your
replacement *after* the upstream module has run (control via
*modules.json* order):

*services.Replace(ServiceDescriptor.Scoped\<IItemService,
MyItemService\>());*

Because the manifest order is preserved, putting your module after
*Catalog* guarantees your replacement wins.

#### []{#anchor-20}Add a Razor Page (sign-in flow, terminal pairing, etc.)

1.  Drop *MyPage.cshtml* + *MyPage.cshtml.cs* under
    *\<Module\>/Presentation/Pages/*.

<!-- -->

2.  Reference *Microsoft.AspNetCore.Mvc.RazorPages* in the module's
    csproj.

<!-- -->

3.  The host's *MapRazorPages* already picks it up via the registered
    application part - the page is reachable at */MyPage*.

For a pattern reference, see the Tenants module's [Login.cshtml +
Login.cshtml.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Tenants/Presentation/Pages/Login.cshtml&version=GBdevelopment).

#### []{#anchor-21}Plug into the request pipeline (middleware)

Implement *Use(WebApplication app)* on your initializer and call
*app.UseMiddleware\<MyMiddleware\>()*. This runs at step 14, after
auth/authz - prefer it for tenant-aware or telemetry middleware.

#### []{#anchor-22}Add a background service

Register *IHostedService* in *ConfigureServices*. The standard ASP.NET
Core host runs it. The Catalog module's *StockProjectionListener* is the
canonical example.

#### []{#anchor-22}Add a JSON polymorphic hierarchy

Override *RegisterJsonPolymorphism* on your initializer and configure
*JsonTypeInfo.PolymorphismOptions*. The hook is called both at startup
*and* by code-gen tools, so generated Kotlin/TypeScript clients stay in
sync.

#### []{#anchor-22}Add OpenAPI tags / docs

*IEndpointMap.Tag* controls the Swagger group. Add XML doc comments on
handler methods and they're surfaced via the Swashbuckle XML-comment
scan in
[DependencyInjection.cs:402](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment&line=402)
(it walks every loaded assembly's *.xml* file).

## []{#anchor-22}[]{#anchor-23}10. Backoffice: metadata-driven forms

The Backoffice is an Angular Signal Forms app, but the thing worth
understanding for the architecture is that it doesn't ship form
definitions in the traditional sense. It builds them at runtime from
three composed sources:

1.  **API-driven schema metadata** (*AppEntityDefinition* /
    *AppFieldDefinition* rows in the tenant database).

<!-- -->

2.  **Registered TypeScript schema rules** (per-entity rules files in
    the Angular bundle).

<!-- -->

3.  **User-saved FormLayoutConfig** (per-user/role layouts persisted via
    the API).

These three combine inside *EntityFormStore* to produce the form a user
sees. None of them are tied to a deployed Angular bundle; you can change
all three without shipping a new Backoffice.

![](media/image3.png){width="5.83333in" height="2.67126in"}

The order of precedence is intentional: metadata is the floor (never
weakened), schema rules layer on business logic, layouts handle
presentation and additive validation. A "broken" form is almost always a
misconfiguration in one of these three.

### []{#anchor-23}[]{#anchor-24}10.1 Metadata-driven validation

*AppFieldDefinition* is the source of truth for "what does this field
have to look like" on *both* sides of the wire. The metadata-driven
validation system on the API generates FluentValidation rules from the
rows; the Backoffice's form-schema builder reads the same rows and
produces matching client-side validators.

A representative entity definition:

*var customerEntity = **new** AppEntityDefinition*\
*{*\
*EntityName = \"Customer\",*\
*DisplayColumn = \"CustomerNumber\",*\
*LookupEndpoint = \"/customers\",*\
*AppFieldDefinitions = \[*\
***new** AppFieldDefinition*\
*{*\
*EntityName = \"Customer\",*\
*ColumnName = \"CustomerNumber\",*\
*AppDataType = AppDataType.Text,*\
*IsRequired = **true**,*\
*MinLength = 3,*\
*MaxLength = 20,*\
*ValidationRegex = \"\^CUST-\[0-9\]{3,}\$\",*\
*ValidationRegexMessage = \"Customer number must start with \'CUST-\'
followed by at least 3 digits\"*\
*},*\
***new** AppFieldDefinition*\
*{*\
*EntityName = \"Customer\",*\
*ColumnName = \"EmailAddress\",*\
*AppDataType = AppDataType.Email,*\
*ValidationRegex = @\"\^\[\\w\\.-\]+@\[\\w\\.-\]+\\.\\w+\$\",*\
*ValidationRegexMessage = \"Invalid email format\"*\
*},*\
***new** AppFieldDefinition*\
*{*\
*EntityName = \"Customer\",*\
*ColumnName = \"LoyaltyPoints\",*\
*AppDataType = AppDataType.Number,*\
*MinValue = 0,*\
*MaxValue = 1000000*\
*}*\
*\]*\
*};*

DTOs are mapped to the entity using a *\[ContractFor\]* attribute, and
endpoints opt in to the auto-generated validator with
*AddEntityValidation\<CreateCustomerDto\>(\"Customer\")* on the endpoint
group. From that point on, every API request that accepts a
*CreateCustomerDto* is validated against the metadata, and every
Backoffice form that edits a *Customer* produces the matching
client-side rules from the same rows.

The supported field-level rules cover required-ness, min/max length,
min/max value, regex with custom message, lookup validation (the value
must exist in another entity via *LookupEndpoint*), enum/list options,
and *AppDataType* (which contributes implicit rules: *Email* adds an
email pattern, *Number* rejects non-numeric input, etc.).

The reason this matters at the architecture level: **a row in
AppFieldDefinition is a per-tenant change** (the table lives in the
tenant database) that reaches both API and Backoffice on the next
request. You don't ship code, you don't redeploy, and you don't get a
Backoffice/API drift because the schema is pulled, not bundled.

### []{#anchor-24}[]{#anchor-25}10.2 Schema rules

Some rules can't be expressed as a single field's metadata - "this field
is readonly once the record exists", "this field is required only when
that other field has a specific value", "passwords must match". For
those, the Backoffice has a registry-based schema rules system. Rules
live next to the feature in a *\*.rules.ts* file:

*// features/users/employees/employee.rules.ts*\
***import** { **readonly**, required, **type** SchemaPath } **from**
\'@angular/forms/signals\';*\
***import** {*\
*ConditionalSchemaRule,*\
*SchemaBuilderOptions*\
*} **from** \'@shared/components/form/form-schema.builder\';*\
***import** { registerSchemaOptions } **from**
\'@shared/components/form/schema-options.registry\';*\
\
***const** emailPattern =
/\^\[a-zA-Z0-9.\_%+-\]+@\[a-zA-Z0-9.-\]+\\.\[a-zA-Z\]{2,}\$/;*\
\
*// Custom validators (field-specific)*\
***export** **const** employeeCustomValidators:
SchemaBuilderOptions\[\'customValidators\'\] = {*\
*email: (value: unknown) **=\>** {*\
***if** (!value) **return** \[{ kind: \'required\', message: \'Email is
required\' }\];*\
***if** (**typeof** value === \'string\' && !emailPattern.test(value))
{*\
***return** \[{ kind: \'email\', message: \'Please enter a valid email
address\' }\];*\
*}*\
***return** \[\];*\
*}*\
*};*\
\
*// Cross-field validators (multi-field)*\
***export** **const** employeeCrossFieldValidators:
SchemaBuilderOptions\[\'crossFieldValidators\'\] = \[*\
*context **=\>** {*\
***const** formValue = context.value();*\
***if** (formValue.newPassword && formValue.confirmPassword !==
formValue.newPassword) {*\
***return** \[{ kind: \'mismatch\', message: \'Passwords do not match\'
}\];*\
*}*\
***return** \[\];*\
*}*\
*\];*\
\
*// Readonly rules*\
***export** **const** employeeReadonlyRules:
SchemaBuilderOptions\[\'readonlyRules\'\] = {*\
*createdBy: () **=\>** **true**,*\
*createdOn: () **=\>** **true**,*\
*modifiedBy: () **=\>** **true**,*\
*modifiedOn: () **=\>** **true***\
*};*\
\
*// Conditional schemas (cross-field readonly/required)*\
***export** **const** employeeConditionalSchemas: Record\<string,
ConditionalSchemaRule\> = {*\
*email: {*\
*condition: (ctx, rootPath) **=\>** {*\
***const** typedPath = rootPath **as** unknown **as** { id:
SchemaPath\<number \| null\> };*\
***const** id = ctx.valueOf(typedPath.id);*\
***return** id != **null** && id !== 0; // editing existing record*\
*},*\
*schema: emailPath **=\>** **readonly**(emailPath, () **=\>**
**true**)*\
*}*\
*};*\
\
*// Combine and auto-register*\
***export** **const** employeeSchemaOptions: SchemaBuilderOptions = {*\
*customValidators: employeeCustomValidators,*\
*crossFieldValidators: employeeCrossFieldValidators,*\
*readonlyRules: employeeReadonlyRules,*\
*conditionalSchemas: employeeConditionalSchemas*\
*};*\
\
*registerSchemaOptions(\'employee\', employeeSchemaOptions);*

Rules are wired in two steps:

1.  Drop the *\*.rules.ts* file in the feature folder and call
    *registerSchemaOptions(entityName, options)*.

<!-- -->

2.  Import the file from *features/entity-rules.index.ts* so it's loaded
    at app startup.

The *EntityFormStore* looks up registered options by entity name when it
builds a form. Same mental model as the API: register, don't wire.

The *SchemaBuilderOptions* interface supports six rule types:

  Rule type                   Purpose
  --------------------------- -------------------------------------------------------------------------------------
  *customValidators*          Field-specific validation logic that's too complex for *AppFieldDefinition*
  *visibilityRules*           Show/hide a field based on form state
  *readonlyRules*             Lock a field based on form state or always
  *crossFieldValidators*      Validation that depends on multiple fields (password match, max \>= min, etc.)
  *conditionalSchemas*        Apply a sub-schema (readonly, required, pattern) when a cross-field condition holds
  *conditionalValueSchemas*   Same, but the condition is the field's own value

Two patterns worth calling out:

- **Edit-mode readonly** is the most common conditional schema: a field
  becomes readonly once the record has an *id*. This is how
  *departmentCode*, *email*, *customerNumber*, etc., are protected from
  changes after creation without making the field readonly during
  create.
- **Cross-field conditions** must call *ctx.valueOf(\...)* *inside* the
  condition function (not capture values in a closure), or the rule
  won't react when the dependency changes.

These rules ship with the Backoffice bundle; they're code, not data. The
boundary is:

- **In AppFieldDefinition** --- anything that could change per tenant or
  per deployment without redeploying the Backoffice.
- **In \*.rules.ts** --- business logic with conditions across multiple
  fields, tied to the shape of the entity itself.

### []{#anchor-25}[]{#anchor-26}10.3 User-driven form layouts

On top of metadata and rules sits the form customization system. A user
with permission opens the customization panel, drags fields between
cards, hides optional fields, renames a card, adds a regex-pattern
transform, and saves. The result is a *FormLayoutConfig* row scoped to
the user (or role), persisted via */form-layouts/{entityName}* and
cached in *localStorage* for offline use.

The data model:

***public** **class** FormLayoutConfig*\
*{*\
***public** Guid Id { **get**; **set**; }*\
***public** string EntityName { **get**; **set**; } = string.Empty;*\
***public** string LayoutName { **get**; **set**; } = string.Empty;*\
***public** string? Description { **get**; **set**; }*\
***public** bool IsDefault { **get**; **set**; }*\
***public** List\<CardLayoutConfig\> Cards { **get**; **set**; } =
\[\];*\
***public** FormLayoutMetadata? Metadata { **get**; **set**; }*\
*}*\
\
***public** **class** CardLayoutConfig*\
*{*\
***public** string CardId { **get**; **set**; } = string.Empty;*\
***public** string? CustomTitle { **get**; **set**; }*\
***public** string? CustomSubtitle { **get**; **set**; }*\
***public** int Order { **get**; **set**; }*\
***public** bool IsVisible { **get**; **set**; } = **true**;*\
***public** bool IsCollapsible { **get**; **set**; } = **true**;*\
***public** bool IsInitiallyCollapsed { **get**; **set**; }*\
***public** string Column { **get**; **set**; } = \"main\"; // \"main\"
\| \"sidebar\"*\
***public** List\<FieldLayoutConfig\> Fields { **get**; **set**; } =
\[\];*\
*}*\
\
***public** **class** FieldLayoutConfig*\
*{*\
***public** string FieldName { **get**; **set**; } = string.Empty;*\
***public** int Order { **get**; **set**; }*\
***public** bool IsVisible { **get**; **set**; } = **true**;*\
***public** bool IsUserRequired { **get**; **set**; }*\
***public** string? CustomLabel { **get**; **set**; }*\
***public** string? CustomPlaceholder { **get**; **set**; }*\
***public** string? CustomHelpText { **get**; **set**; }*\
***public** List\<FieldValidationRule\>? CustomValidationRules {
**get**; **set**; }*\
***public** string WidthHint { **get**; **set**; } = \"full\";*\
*}*\
\
***public** **class** FieldValidationRule*\
*{*\
***public** Guid Id { **get**; **set**; }*\
***public** string Type { **get**; **set**; } = \"pattern\"; //
\"pattern\" \| \"transform\"*\
***public** string Pattern { **get**; **set**; } = string.Empty;*\
***public** string? Flags { **get**; **set**; }*\
***public** string? Message { **get**; **set**; }*\
***public** string? Replacement { **get**; **set**; }*\
***public** bool IsEnabled { **get**; **set**; } = **true**;*\
*}*

The wiring on the Angular side is
*FormLayoutStore.loadLayout(entityName, columns, defaultCardStructure)*
in the form's *ngOnInit*, which loads (or creates) the layout and
exposes it as a signal. Form cards consume it via
*\<app-dynamic-form-card \[cardConfig\]=\"card\" \...\>* for the simple
case, or by checking *layoutStore.layout()* directly when the card has
custom content interleaved with fields.

The hard constraint: **schema-required fields cannot be hidden.**
*AppFieldDefinition.IsRequired* is the source of truth, and the
customization panel filters hideable fields by it. Layouts are
presentation-only; they cannot weaken the data model.

Two extra capabilities worth knowing:

- **Custom validation rules** (*FieldValidationRule*) let users add
  regex patterns for either validation (*type: \'pattern\'*) or
  transformation (*type: \'transform\'* with a *Replacement*). The form
  store applies these on top of the metadata-driven validators when the
  layout is active. This is how a tenant adds a custom SKU pattern
  without touching *AppFieldDefinition* - useful when the rule should
  only apply for one user role's view of the form.
- **Undo/redo** is built into *FormLayoutStore* (last 50 changes), so
  customization can be exploratory.

The API endpoints the Backoffice expects:

  Endpoint                                 Method   Description
  ---------------------------------------- -------- ------------------------------
  */form-layouts/{entityName}/active*      GET      Get active layout for entity
  */form-layouts/{entityName}*             GET      List all layouts for entity
  */form-layouts/id/{layoutId}*            GET      Get specific layout by ID
  */form-layouts*                          PUT      Save/update a layout
  */form-layouts/{layoutId}*               DELETE   Delete a layout
  */form-layouts/{layoutId}/set-default*   POST     Set layout as default

### []{#anchor-26}[]{#anchor-27}10.4 Backoffice customization recipes

#### []{#anchor-27}Add a new field validator that varies per tenant

Update or insert an *AppFieldDefinition* row in the tenant database with
the new *ValidationRegex* and *ValidationRegexMessage*. Both API and
Backoffice pick it up on next request. No deployment.

#### []{#anchor-28}Add a cross-field rule (e.g., max \>= min)

1.  In the entity's *\*.rules.ts*, add a function to
    *crossFieldValidators* that reads *context.value()* and returns a
    *ValidationError\[\]*.

<!-- -->

2.  Make sure the rules file is registered
    (*registerSchemaOptions(\...)*) and imported from
    *entity-rules.index.ts*.

<!-- -->

3.  Ship the Backoffice bundle.

#### []{#anchor-28}Make a field readonly after creation

In the entity's *\*.rules.ts*, add a *conditionalSchemas* entry whose
condition checks *id != null && id !== 0* and whose schema calls
*readonly(path, () =\> true)*. The pattern is identical for *email*,
*departmentCode*, *customerNumber*, etc.

#### []{#anchor-28}Reorder cards or hide optional fields per user

Open the customization panel in the form, drag/hide fields, save. The
layout is persisted as a *FormLayoutConfig* row. No code, no deployment.

#### []{#anchor-29}Add a tenant-specific regex without touching *AppFieldDefinition*

In the customization panel, add a *FieldValidationRule* with *type:
\'pattern\'*, the regex, and a message. It applies on top of the
metadata-driven validators when the layout is active.

## []{#anchor-30}[]{#anchor-31}11. Android POS: corelib + DEX + overlays

Android is the most constrained layer because it ships as an APK on a
physical terminal, often offline, and has to keep running even when the
device can't reach the API. Customization can't always be a server-side
toggle. The Android architecture solves this with three mechanisms
layered on a stable contract module.

### []{#anchor-31}[]{#anchor-32}11.1 The contract: *driftpos-corelib*

*driftpos-corelib* is a pure-Kotlin module that contains every type that
crosses the customization boundary: event classes
(*DriftInterceptorEvent*, *OnSubmitSku*, *OnPosDraftDocumentComplete*,
...), the *Interceptor\<T\>* interface, the phase/type enums, the
*InterceptorFormHandler*, the *OverlayRoute* marker interface, and the
DAO/model types that interceptors might want to interact with.

The host app and any extension module both compile against
*driftpos-corelib*. Extension modules use *compileOnly* for it - the
corelib classes come from the host's classloader at runtime, so there's
no duplication and no "two *OnSubmitSku*s" class-cast problem. From the
interceptor module's
[build.gradle.kts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-interceptors/build.gradle.kts&version=GBdevelopment&line=43):

*compileOnly(project(\":driftpos-corelib\"))*\
*compileOnly(libs.koin.core)*\
*compileOnly(kotlin(\"reflect\"))*

This corelib is the single most important Android-side asset for
compatibility. As long as it's stable, every interceptor and overlay
shipped against an older release continues to load on a newer host
build.

### []{#anchor-32}[]{#anchor-33}11.2 Interceptors: behavior extension

DriftPOS ships with a runtime-pluggable interceptor system that lets
external code "wrap" core POS events (SKU entry, document completion,
customer selection, etc.) without modifying the host app. Interceptors
are compiled into standalone DEX files, dropped into the device's cache
directory, and loaded into the running process via *DexClassLoader*. The
host app discovers them through a JSON manifest and invokes them through
a phased chain.

![](media/image4.png){width="5.83333in" height="4.31053in"}

#### []{#anchor-33}The interceptor contract

***interface** Interceptor\<TEvent : DriftInterceptorEvent\> {*\
***val** eventName: **String***\
***val** phase: InterceptorPhase // Before \| Replace \| After*\
***val** type: InterceptorType // Synchronous \| Asynchronous*\
***val** order: **Int***\
***val** enabled: **Boolean***\
***val** retryCount: **Int** **get**() = 0*\
***val** continueOnError: **Boolean** **get**() = **false***\
\
*suspend **fun** intercept(*\
*event: TEvent,*\
*formHandler: InterceptorFormHandler? = null,*\
*)*\
*}*

  Property            Purpose
  ------------------- ----------------------------------------------------------------------------------------------------
  *eventName*         Currently informational; the chain receives interceptors already filtered/ordered by the loader.
  *phase*             When the interceptor runs relative to *coreLogic* - *Before*, *Replace*, or *After*.
  *type*              *Synchronous* (awaited inline) vs *Asynchronous* (fire-and-forget launch within chain scope).
  *order*             Sort key inside a phase. Lowest first.
  *enabled*           Hard kill switch. Honored by *InterceptorLoader* at load time.
  *continueOnError*   If *true*, exceptions are logged and the chain continues. If *false*, they propagate up the chain.

All events extend *DriftInterceptorEvent* so they can flow through the
same *InterceptorChain* regardless of subtype. Concrete events live next
to their feature, e.g.:

***data** **class** OnSubmitSku(*\
***val** sku: String,*\
***var** posDraftDocument: PosDraftDocument,*\
*) : DriftInterceptorEvent(*\
*eventName = \"onSubmitSku\",*\
*eventType = POS_SCREEN_EVENT_TYPE,*\
*)*

Events are **mutable by design**. Interceptors mutate the event (or its
*posDraftDocument*) to feed information forward through the chain and
back into core logic. A SKU-scan interceptor that recognizes a
driver's-license barcode parses the customer info, attaches the customer
to the document, and clears the SKU on the event so the host's normal
lookup becomes a no-op.

#### []{#anchor-33}Phases

***enum** **class** InterceptorPhase { Before, After, Replace }*

*InterceptorChain* groups loaded interceptors into three buckets and
runs them in this order:

*\[Before, sorted by order\] -\> Replace OR coreLogic -\> \[After,
sorted by order\]*

- **Before** - run in *order* ascending, all of them, before the core
  operation.
- **Replace** - if any interceptor declares *Replace*, it executes
  *instead of* *coreLogic*. Only the first match is used
  (*interceptors.find { \... }*), so it is effectively "replace once or
  not at all".
- **After** - run in *order* ascending after either *Replace* or
  *coreLogic* completes.

This shape is what makes the system useful for both observation
(Before/After) and behavior substitution (Replace).

#### []{#anchor-33}Form handler bridge

An optional bridge lets a backgrounded interceptor request UI input from
the host:

***interface** InterceptorFormHandler {*\
*suspend **fun** requestInput(formData: FormData): FormResponse*\
*}*

The host supplies the implementation when it dispatches the event.
Interceptors call *formHandler?.requestInput(\...)* and suspend until
the user submits or cancels.

#### []{#anchor-33}End-to-end SKU-submit flow

Walking through a SKU submit on a device that has a driver's-license
interceptor deployed:

1.  **App startup.** Koin builds
    *EventDispatcher\<DriftInterceptorEvent\>*. Its constructor calls
    *InterceptorLoader.loadInterceptors(context)*, which reads
    *assets/interceptors.json*, looks for the matching *.dex* in
    *cacheDir/interceptors/* for each enabled entry, builds a
    *DexClassLoader* per file, instantiates the interceptor class with
    its no-arg constructor, and returns a
    *List\<Interceptor\<DriftInterceptorEvent\>\>*.

<!-- -->

2.  **User scans a barcode into the SKU input.** POS code constructs
    *OnSubmitSku(sku, draft)* and calls
    *eventDispatcher.processForEvent(event, coreLogic = { \...normal SKU
    lookup\... }, formHandler = \...)*.

<!-- -->

3.  **processForEvent** notifies plain subscribers, then either invokes
    *coreLogic* directly (no interceptors) or builds an
    *InterceptorChain* and calls *start()*.

<!-- -->

4.  **InterceptorChain.start() -\> proceedBefore()** iterates Before
    interceptors in *order*. The DL interceptor (Before, Synchronous,
    *order=1*) runs, decides this is an AAMVA scan, parses the fields,
    finds-or-creates a *Customer* via Koin/reflection, attaches the
    customer to the document, and clears the SKU on the event.

<!-- -->

5.  **proceedBeforeOrReplace()** runs *coreLogic* (no Replace
    interceptor present). With the SKU cleared, the host's normal SKU
    resolution is a no-op for this scan.

<!-- -->

6.  **proceedAfter()** iterates After interceptors. None for this event,
    chain ends.

<!-- -->

7.  **Control returns to the caller.** The customer is attached to the
    document, and the user sees the customer card populate without ever
    leaving the SKU field.

#### []{#anchor-33}Reaching app-module types from a DEX

Interceptor modules can compile against corelib but not against the app
module. The pattern when an interceptor needs an app-module singleton
(e.g., *DbProvider*, *CustomerInteract*):

1.  Implement *KoinComponent* and grab the global Koin context:
    *GlobalContext.get()*.

<!-- -->

2.  Resolve the app-module class by name with
    *Class.forName(\"com.rapidpos.driftpos\...\")* (resolved via the
    parent classloader).

<!-- -->

3.  Look up the singleton in Koin: *koin.get\<Any\>(theClass.kotlin,
    null, null)*.

<!-- -->

4.  For suspend functions, find the *KFunction* via *kotlin-reflect* and
    invoke with *callSuspend(\...)*.

***val** dbProviderClass =
Class.forName(\"com.rapidpos.driftpos.data.local.DbProvider\")*\
***val** dbProvider = koin.**get**\<Any\>(dbProviderClass.kotlin,
**null**, **null**)*\
***val** getFunc = dbProviderClass.kotlin.memberFunctions.first {
it.name == \"get\" }*\
*getFunc.callSuspend(dbProvider)*

Where corelib types are involved (DAOs, models), the cast can be direct
because both sides see the same class:

*daoMethod.invoke(database) **as**?
com.driftpos.corelib.dao.CustomerDao*

The rule of thumb: **typed against corelib, reflective against the app
module.**

#### []{#anchor-33}Building and deploying a DEX

[driftpos-interceptors/build.gradle.kts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-interceptors/build.gradle.kts&version=GBdevelopment)
ships a custom *BuildInterceptorDexTask* that:

1.  Runs *assembleRelease* to produce the module's AAR.

<!-- -->

2.  Extracts *classes.jar* from the AAR.

<!-- -->

3.  Locates the highest-versioned *d8* (or *d8.bat* on Windows) in
    *\$ANDROID_HOME/build-tools/*.

<!-- -->

4.  Invokes d8 to convert the JAR into *classes.dex*.

<!-- -->

5.  Renames it to the configured *dexFileName*
    (e.g. *drivers-license-scan.dex*) and emits to
    *build/outputs/interceptors/*.

*./gradlew :driftpos-interceptors:buildInterceptorDex*

The resulting DEX must end up in
*\<cacheDir\>/interceptors/\<fileName\>* on the target device, and the
manifest entry's *fileName* must match.

#### []{#anchor-33}Operational gotchas

- **No hot reload.** Interceptors are loaded once when *EventDispatcher*
  is constructed. Changing *interceptors.json* or replacing a DEX
  requires the dispatcher to be recreated.
- **Manifest != deployment.** The presence of an entry in
  *interceptors.json* does not create the file; the loader skips entries
  whose *fileName* is not in *cacheDir/interceptors/*. A deployment
  pipeline must put the DEX there.
- **enabled = false is honored at load time only.** Toggling *enabled*
  after loading has no effect.
- **retryCount is unused.** The interface declares it, but
  *InterceptorChain* does not retry. Treat it as advisory until that
  wiring lands.
- **One Replace per chain.** If multiple interceptors declare *Replace*
  for the same event, only the first found is used. Order is not
  deterministic relative to manifest position; this is unsafe in
  practice. Avoid declaring more than one *Replace* per event.
- **Events are mutable.** Interceptors are expected to mutate *event*
  (e.g. set *posDraftDocument*, clear *sku*) to influence downstream
  Before, the *coreLogic* closure, and After. Treat shared event state
  as a small, explicit protocol.
- **Security boundary.** Anything with write access to
  *cacheDir/interceptors/* can inject code that runs with the app's
  classloader and Koin singletons. The DEX directory is private to the
  app's process on Android, but any deployment mechanism that writes
  there is effectively a code-push channel and should be authenticated.

### []{#anchor-33}[]{#anchor-34}11.3 Overlays: UI extension

The overlay system covers the other half of Android customization: not
*what happens* when an event fires, but *what the user sees* on top of
the POS screen. It's a stack-based, composable-driven layer that any
feature can push to via *OverlayScope.push(entry)*.

*User Action -\> OverlayHostAction -\> OverlayDispatcher -\>
OverlayMutation -\> OverlayReducer -\> OverlayHostState -\> OverlayHost
(Compose)*

#### []{#anchor-34}Core types

  Type                     Purpose
  ------------------------ --------------------------------------------------------------------------------
  *OverlayRoute*           Marker interface; concrete data class per overlay carrying the state to render
  *OverlayEntry*           Wraps a route with *id*, *shell*, *dismissPolicy*, *transition*, *chrome*
  *OverlayHostState*       *ImmutableList\<OverlayEntry\>* - the stack; topmost entry is visible
  *OverlayHostAction*      *Dismiss* / *Confirm* / *Back* / *ChildIntent*
  *OverlayMutation*        *Push* / *ReplaceTop* / *Pop* / *ClearAll*
  *OverlayScope*           Public API: *push*, *replaceTop*, *dismiss*, *showError*, *showConfirm*
  *OverlayIntentHandler*   Per-feature handler; *handle(overlayId, intent): Boolean*

#### []{#anchor-34}Shell types

  Shell           Default size         Description
  --------------- -------------------- -----------------------------------------------
  *Dialog*        520.dp width         Centered modal dialog
  *BottomSheet*   720.dp max width     Bottom sheet with optional drag handle
  *SideSheet*     42% width fraction   Right-aligned side panel with slide animation
  *Fullscreen*    fills screen         Full-screen overlay

#### []{#anchor-34}Auto-registration: the scaling property

Two things make the overlay system scale across customizations:

1.  **Renderers are auto-registered at build time.** Any *object*
    annotated with *\@ScreenOverlay* and implementing
    *OverlayRouteRenderer\<T\>* is picked up by the KSP processor
    (*OverlayProcessor*), which generates
    *GeneratedOverlayModule.registerAll()*. The app's *onCreate* calls
    that one method and every renderer in every feature module is wired
    into *OverlayRouteRendererRegistry*.

<!-- -->

2.  **Handlers are auto-registered at runtime.** Any concrete
    *OverlayIntentHandler* declared as a Koin singleton is discovered by
    the KSP processor (*processHandlers*) and registered with the
    *OverlayDispatcher* from
    *GeneratedOverlayHandlerModule.registerAll(dispatcher)*. There's no
    *\@OverlayHandler* annotation, no constructor wiring in
    *PosScreenViewModel*, and no manual *dispatcher.register(\...)*
    call - just declare the Koin single.

The startup wiring is two lines:

*// DriftPOSApplication.onCreate()*\
*GeneratedOverlayModule.registerAll() // renderers*\
\
*// DbProvider.initializeServices()*\
*GeneratedOverlayHandlerModule.registerAll(dispatcher) // handlers*

A feature module ships a complete overlay - route, intents, renderer,
handler, entry factory - and it *just works* at runtime. The
*OverlayHost* reads directly from *OverlayDispatcher.state* (not from
*PosScreenUiState*), so pushing or popping an overlay does not recompose
transaction lines, totals, or the header.

#### []{#anchor-34}How to add a new overlay

1.  Define a route - data class implementing *OverlayRoute* (carries
    overlay state).

<!-- -->

2.  Define intents - sealed interface for user actions within the
    overlay.

<!-- -->

3.  Create an entry factory - configures shell, chrome, dismiss policy,
    transition.

<!-- -->

4.  Create a renderer - *object* annotated with *\@ScreenOverlay*,
    implements *OverlayRouteRenderer\<T\>*.

<!-- -->

5.  Create a handler - implements *OverlayIntentHandler*, declared as a
    Koin *single*.

<!-- -->

6.  Show - the handler's entry-point method calls
    *overlayScope.push(entry)*.

What you do *not* need to do:

- No *\@OverlayHandler* annotation (discovery is by supertype).
- No constructor param in *PosScreenViewModel*.
- No *overlayDispatcher.register()* call in *init{}*.
- No *PosScreenModule* changes for the handler.

### []{#anchor-34}[]{#anchor-35}11.4 Android customization recipes

#### []{#anchor-35}Wrap a POS event with custom logic per fleet

Build an interceptor module against *driftpos-corelib*, declare the
right *phase* / *type* / *order*, implement *intercept(\...)*. Run
*./gradlew :\<module\>:buildInterceptorDex*. Deploy the DEX to
*cacheDir/interceptors/\<fileName\>* and add an entry to
*assets/interceptors.json*. No APK rebuild.

#### []{#anchor-36}Replace a POS event entirely

Same as above, but set *phase = Replace*. Only one Replace interceptor
per event; the chain runs *Replace* instead of *coreLogic*. Use
sparingly.

#### []{#anchor-36}Add a new modal / overlay

Add a *\@ScreenOverlay* renderer object and an *OverlayIntentHandler*
Koin single. KSP wires both at build time. No edits to the dispatcher,
the view model, or DI modules outside of declaring the Koin single.

#### []{#anchor-36}Customer-specific UI without forking the app

Today, customer-specific overlay behavior is gated by tenant identity
inside the handler (e.g. an *if (currentTenant == \...)* check before
pushing the overlay). Renderers themselves are compiled into the APK;
per-tenant compilation isn't supported.

## []{#anchor-37}[]{#anchor-38}12. Cross-layer customization

Putting all three layers together, here is what "customize this for Acme
Corp" looks like end to end.

### []{#anchor-38}[]{#anchor-39}12.1 Worked example: a custom SKU-submit policy

Acme wants three things:

1.  **API**: SKUs must match a regex specific to their numbering scheme.

<!-- -->

2.  **Backoffice**: When editing an Item for Acme, the SKU field is
    readonly after creation, and a custom card layout puts
    SKU/UPC/internal-code together at the top.

<!-- -->

3.  **Android**: When a SKU is scanned at the register, run an
    Acme-specific lookup against their internal product master before
    falling back to the local DB.

Nothing about this should require a deployment of any of the three.

![](media/image5.png){width="5.83333in" height="1.38393in"}

Step by step:

1.  **Update AppFieldDefinition** for *Item.Sku* in Acme's database. Set
    *ValidationRegex* to their pattern and a useful
    *ValidationRegexMessage*. The next API request that hits *POST
    /items* for Acme will reject mismatched SKUs (the metadata-driven
    validation system generates a FluentValidator from the row, wired in
    via *AddEntityValidation\<CreateItemDto\>(\"Item\")* on the
    endpoint), and the next form-load in the Backoffice will use the
    same regex on the client side. *Zero deployments.*

<!-- -->

2.  **Save a FormLayoutConfig** for Acme's "Item" entity via the
    customization panel. SKU readonly-after-creation lives in the Item
    rules file already (it's a generic edit-mode-readonly pattern from
    §10.2) - the layout adds the card reordering on top. *Zero
    deployments.*

<!-- -->

3.  **Build and deploy acme-sku-lookup.dex** to Acme's terminals. The
    DEX implements *Interceptor\<OnSubmitSku\>* with *phase = Before*
    and *type = Synchronous*, calls Acme's product master API (or a
    cached local mirror), mutates the event's *posDraftDocument*, and
    lets the host's *coreLogic* run normally if it didn't find a match.
    Deploy by writing the file to *cacheDir/interceptors/* on each
    terminal and updating *assets/interceptors.json*. *Zero APK
    changes.*

The first two are runtime data changes; the third is a code-push to a
defined extension surface. The DriftPOS host - on all three layers - is
identical for Acme as it is for everyone else.

### []{#anchor-40}[]{#anchor-41}12.2 Where each customization mechanism belongs

  If you want to...                                                        Use this                                               Layer        Per-tenant?
  ------------------------------------------------------------------------ ------------------------------------------------------ ------------ ---------------------
  Change a regex / range / required-ness on a field                        *AppFieldDefinition* row                               API + BO     Yes
  Add a cross-field rule, conditional readonly, password-confirm           *\*.rules.ts* registered via *registerSchemaOptions*   Backoffice   No (code)
  Reorder cards / hide optional fields / add transform regex               *FormLayoutConfig* saved by a user                     Backoffice   Yes (per user/role)
  Replace a service implementation (e.g., *IItemService*)                  New module after the original in *modules.json*        API          No (deploy)
  Add a new HTTP resource                                                  New *IEndpointMap* in any module                       API          No (deploy)
  Add a whole capability (third-party tax provider, payment integration)   New module assembly + *modules.json* entry             API          No (deploy)
  Wrap or replace a POS event (SKU submit, document complete, ...)         Interceptor DEX in cacheDir/interceptors/              Android      Yes (per fleet)
  Add a modal / overlay (dialog, side sheet, fullscreen)                   *\@ScreenOverlay* renderer + *OverlayIntentHandler*    Android      No (deploy)

The "per-tenant" column is the one to read first. Anything marked yes is
a runtime change against tenant data or fleet configuration; anything
marked no is a code change in a module that ships to everyone. The
system is built to push as much customization as possible into the first
column.

### []{#anchor-42}[]{#anchor-43}12.3 What each layer does NOT solve

Worth being explicit about the gaps, because they're the things that
bite when a customer asks for something just past what the system
supports today.

- **Per-tenant code on the API.** There is no "load this assembly only
  for Acme" mechanism. *modules.json* is global. Customer-specific
  business logic that can't be expressed as data or as an opt-in module
  setting has to be handled in an interceptor on the device, in a
  customization at the data layer, or by gating the new module's
  behavior on tenant identity at runtime.
- **Per-user code on the Backoffice.** Layouts are per user/role; rules
  and validators are not. Adding role-conditional schema rules is doable
  today by reading the user's roles inside the rule's *condition*, but
  that information has to be wired into the rule context.
- **Hot-reload of interceptors.** DEX files are loaded once at
  *EventDispatcher* construction. A new DEX dropped on disk takes effect
  on the next app launch. Any "live config" feel has to be implemented
  inside the interceptor (the interceptor reads its own config from the
  API at runtime).
- **Per-tenant Android UI customizations.** Renderers are compiled into
  the APK. An overlay that's shown only for Acme has to be gated by
  tenant identity inside the handler, not by registration.

### []{#anchor-43}[]{#anchor-44}12.4 When a layer is the wrong place

The hardest architecture decision in this system is which layer to solve
a given problem at. A few rules of thumb that hold up in practice:

- **Validation that's true regardless of UI** belongs in
  *AppFieldDefinition*. It will be enforced on the server and reflected
  on the client without effort. Don't put it in *\*.rules.ts*; you'll
  have to mirror it on the API.
- **Business logic that depends on tenant configuration but not on which
  device is running** belongs in a module on the API, gated by
  configuration or by tenant claims. The Android side will see
  consistent behavior across terminals automatically.
- **Per-terminal behavior** (hardware-specific, fleet-specific,
  integration with on-device peripherals) belongs in an Android
  interceptor. The API and Backoffice should not know.
- **A new screen or modal** belongs in the layer that owns the workflow.
  If it's a config screen, it's a Backoffice route. If it's a
  register-time prompt, it's an Android overlay. If it's both, you're
  describing two screens that happen to share a domain.
- **A new "thing the system can do"** (a tax engine, a payment
  processor, a loyalty program) belongs in a new API module that defines
  the contract, with the Backoffice and Android consuming it through the
  existing surfaces.

The mistakes that recur:

- Putting cross-field rules in *AppFieldDefinition* (they don't fit; the
  metadata is per-field).
- Putting per-tenant business behavior in shipped Backoffice code
  (you'll be redeploying for every customer).
- Putting hardware integration in API endpoints the device polls
  (latency and offline both lose).
- Building a feature as an interceptor when it should be a first-class
  POS event (the chain is for extension, not invention; new events go in
  corelib).

## []{#anchor-44}[]{#anchor-45}13. Operational notes

### []{#anchor-45}[]{#anchor-46}API host

- **Module load order is the manifest order.** The reflection scans
  inside *LoadAndConfigureModules* and *AddModules* iterate
  *GlobalConfiguration.Modules* in the order JSON deserialization
  produced them.
- **A missing modules.json is fatal.** *FindModulesJson* throws
  *FileNotFoundException* listing the paths it tried.
- **Assembly.Load failures bubble up.** If an assembly is named in
  *modules.json* but isn't on the probing path, startup fails fast with
  a *FileNotFoundException* from the CLR.
- **Re-loads are idempotent within a process.** *\_modulesLoaded*
  short-circuits subsequent calls; this matters for tools that share the
  loader (codegen, EF design-time, seed-runner).
- **Tools share the same loader.** *DriftPOS.Tool.CodeGen*,
  *DriftPOS.Tool.SemanticCatalog*, and *DriftPOS.Tool.SeedRunner* all
  call *EnsureModulesLoaded* so they see exactly the assemblies the
  running API would see.
- **ValidateScopes = true; ValidateOnBuild = true** is enabled in all
  environments
  ([Program.cs:11](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/Program.cs&version=GBdevelopment&line=11)).
  A module that registers a captive dependency or a missing service will
  fail at *builder.Build()* rather than on the first request.

### []{#anchor-46}[]{#anchor-47}Backoffice rule troubleshooting

- **Rules not applying.** Verify the entity name matches exactly
  (case-sensitive); confirm *registerSchemaOptions()* is called; ensure
  the rules file is imported in *entity-rules.index.ts*; check the
  browser console for warnings about missing fields.
- **Conditional schema not working.** Use *conditionalSchemas* (not
  *readonlyRules*) for cross-field conditions. Verify the field name
  matches the entity property name. Check that the condition function
  returns a boolean.
- **Form not updating reactively.** Ensure *ctx.valueOf()* is called
  inside the condition function (not captured in a closure). The
  condition must return a boolean synchronously.

### []{#anchor-47}[]{#anchor-48}Android interceptor pitfalls

Repeated here because they're the most common production bugs:

- DEX loaded once at startup; toggling *enabled* or replacing the file
  requires a process restart.
- Multiple *Replace* interceptors per event are unsafe - first found
  wins, order is not deterministic.
- Async interceptors are scoped, not background - the chain still awaits
  the surrounding *coroutineScope*.
- *cacheDir/interceptors/* is a code-push channel; treat any deployment
  mechanism that writes there as a trust boundary.

### []{#anchor-48}[]{#anchor-49}Cross-layer scaling

- **Database-per-tenant** means each Npgsql pool is
  per-connection-string. With N tenants, you have N pools - watch
  *pg_stat_activity* to verify total connections stay under PostgreSQL's
  *max_connections* and tune *TenantMaxPoolSize* / *TenantMinPoolSize*
  accordingly.
- **Tenant identity is per-request, not per-process.** Any host instance
  can serve any tenant; sessions are server-side via *ITicketStore*.
  Horizontal scale-out is safe.
- **Hosted services that assume singleton ownership** (the tenant
  provisioning background service, replication listeners, projection
  workers) need leader election or a single-instance deployment slot
  when running multiple host replicas.

## []{#anchor-49}[]{#anchor-50}14. File map

### []{#anchor-50}[]{#anchor-51}API (DriftPOS.API)

  Concern                              File
  ------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Module manifest                      [modules.json](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/modules.json&version=GBdevelopment)
  Host pipeline                        [Program.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/Program.cs&version=GBdevelopment)
  Service registration orchestration   [DependencyInjection.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/DriftPOS.WebHost/DependencyInjection.cs&version=GBdevelopment)
  Module loader                        [GlobalConfiguration.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/GlobalConfiguration.cs&version=GBdevelopment)
  Initializer contract                 [IModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IModuleInitializer.cs&version=GBdevelopment)
  Endpoint contract                    [IEndpointMap.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Shared/DriftPOS.Shared.Infrastructure/Hosting/IEndpointMap.cs&version=GBdevelopment)
  Reference initializer (light)        [CatalogModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Catalog/CatalogModuleInitializer.cs&version=GBdevelopment)
  Reference initializer (heavy)        [TenantModuleInitializer.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Tenants/TenantModuleInitializer.cs&version=GBdevelopment)
  Reference endpoint map               [ItemEndpoints.cs](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Catalog/Presentation/Api/Endpoints/v1/ItemEndpoints.cs&version=GBdevelopment)
  Reference Razor Pages                [DriftPOS.Module.Tenants/Presentation/Pages/](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/Modules/DriftPOS.Module.Tenants/Presentation/Pages/&version=GBdevelopment)
  Out-of-tree sample                   [DriftPOS.Module.Avalara](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/src/SampleModules/DriftPOS.Module.Avalara/&version=GBdevelopment)
  Module structure rule                [project_structure.rule.md](https://dev.azure.com/RapidPOSDevOps/DriftPOS.API/_git/DriftPOS.API?path=/docs/dev/project_structure.rule.md&version=GBdevelopment)

### []{#anchor-51}[]{#anchor-52}Backoffice (DriftPOS.Backoffice)

  Concern                   File
  ------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Schema builder            [form-schema.builder.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form/form-schema.builder.ts&version=GBdevelopment)
  Schema options registry   [schema-options.registry.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form/schema-options.registry.ts&version=GBdevelopment)
  Entity form store         [entity-form.store.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form/entity-form.store.ts&version=GBdevelopment)
  Central rules import      [entity-rules.index.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/features/entity-rules.index.ts&version=GBdevelopment)
  Form layout store         [form-layout.store.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form-customization/services/form-layout.store.ts&version=GBdevelopment)
  Form layout service       [form-layout.service.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form-customization/services/form-layout.service.ts&version=GBdevelopment)
  Customization panel       [customization-panel.component.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form-customization/components/customization-panel.component.ts&version=GBdevelopment)
  Dynamic form card         [dynamic-form-card.component.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form-customization/components/dynamic-form-card.component.ts&version=GBdevelopment)
  Field validation editor   [field-validation-editor.component.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/shared/components/form-customization/components/field-validation-editor.component.ts&version=GBdevelopment)
  Reference rules file      [item-department.rules.ts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.Backoffice/_git/DriftPOS.Backoffice?path=/src/app/features/items/item-departments/item-department.rules.ts&version=GBdevelopment)

### []{#anchor-52}[]{#anchor-53}Android (DriftPOS.APP)

  Concern                        File
  ------------------------------ -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Interceptor contract           [Interceptor.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/Interceptor.kt&version=GBdevelopment)
  Phase enum                     [InterceptorPhase.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorPhase.kt&version=GBdevelopment)
  Type enum                      [InterceptorType.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorType.kt&version=GBdevelopment)
  Manifest schema                [InterceptorConfig.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorConfig.kt&version=GBdevelopment)
  Form-handler bridge            [InterceptorFormHandler.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorFormHandler.kt&version=GBdevelopment)
  Loader (DEX -\> instance)      [InterceptorLoader.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorLoader.kt&version=GBdevelopment)
  Chain (Before/Replace/After)   [InterceptorChain.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/intercept/InterceptorChain.kt&version=GBdevelopment)
  Event base class               [DriftInterceptorEvent.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/abstraction/DriftInterceptorEvent.kt&version=GBdevelopment)
  Dispatcher (entry point)       [EventDispatcher.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/event/EventDispatcher.kt&version=GBdevelopment)
  POS events                     [PosScreenEvent.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-corelib/src/main/java/com/driftpos/corelib/event/PosScreenEvent.kt&version=GBdevelopment)
  Reference interceptor (DL)     [DriversLicenseScanInterceptor.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-interceptors/src/main/java/com/driftpos/interceptors/DriversLicenseScanInterceptor.kt&version=GBdevelopment)
  DEX build pipeline             [driftpos-interceptors/build.gradle.kts](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-interceptors/build.gradle.kts&version=GBdevelopment)
  Overlay route                  [OverlayRoute.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-facets/src/main/java/com/rapidpos/driftpos/facets/overlay/model/OverlayRoute.kt&version=GBdevelopment)
  Overlay dispatcher             [OverlayDispatcher.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-facets/src/main/java/com/rapidpos/driftpos/facets/overlay/host/OverlayDispatcher.kt&version=GBdevelopment)
  Overlay reducer                [OverlayReducer.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-facets/src/main/java/com/rapidpos/driftpos/facets/overlay/host/OverlayReducer.kt&version=GBdevelopment)
  Overlay host (Compose)         [OverlayHost.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-facets/src/main/java/com/rapidpos/driftpos/facets/overlay/host/OverlayHost.kt&version=GBdevelopment)
  Renderer registry              [OverlayRouteRendererRegistry.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-facets/src/main/java/com/rapidpos/driftpos/facets/overlay/renderers/OverlayRouteRendererRegistry.kt&version=GBdevelopment)
  *\@ScreenOverlay* annotation   [ScreenOverlay.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/driftpos-annotations/src/main/java/com/rapidpos/driftpos/annotations/ScreenOverlay.kt&version=GBdevelopment)
  KSP overlay processor          [OverlayProcessor.kt](https://dev.azure.com/RapidPOSDevOps/DriftPOS.APP/_git/DriftPOS.APP?path=/overlay-processor/src/main/java/com/rapidpos/driftpos/overlay/processor/OverlayProcessor.kt&version=GBdevelopment)
