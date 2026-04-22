---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/SSO Overview v2.docx
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# SSO Overview v2.docx

## Source
File: `/Users/gclyle/secure/SSO Overview v2.docx`
Size: 12,879 bytes

## Raw content
Federated Identity Management Capabilities in Secure.

10/23/2018

#

Contents

[1 Introduction 3](#_Toc528077016)

[2 Security Assertion Markup Language (SAML) 2.0 Authentication 3](#_Toc528077017)

[3 Secure Platform Authentication 4](#_Toc528077018)

[4 SSO Assignment of User Roles and Responsibilities 4](#_Toc528077019)

[5 Manual Assignment of Roles and Responsibilities 4](#_Toc528077020)

[6 SAML 3.0 Service Provider Initiated Authentication Workflow 5](#_Toc528077021)

[7 Sample SAML 2.0 Assertion 6](#_Toc528077022)

[8 OpenID Connect (OIDC) Authentication 8](#_Toc528077023)

[9 Sample OpenID Connect Token 9](#_Toc528077024)

# Control

## Version

|  |  |  |  |
| --- | --- | --- | --- |
| Document Version | Author | Date | Notes |
| 1.0 | Jerry Caldwell | 09/13/2018 | Initial Version |
| 2.0 | Geoff Lyle | 10/23/2018 | Updates |

## Reviewers

|  |  |  |
| --- | --- | --- |
| Reviewed By | Position | Date |
| Nathan Smith | SVP Product Strategy |  |
| David West | SVP Operations |  |
| Raymond Kelly | VP, Security & Compliance |  |
| Kenny Vu | Engineering Manager |  |
| Jerry Boersma | SVP, Engineering |  |
| Geoff Lyle | VP Program Management |  |

# Introduction

Federated Identity Management describes the technologies, standards and use-cases which serve to enable the portability of identity information across otherwise autonomous security domains. The goal of identity federation is to enable users of one domain to securely access data or systems of another domain seamlessly, and without the need for completely redundant user administration. Federation is enabled using open industry standards and/or openly published specifications, such that multiple parties can achieve interoperability for common use-cases. Typical use-cases involve things such as cross-domain, web-based Single Sign-On (SSO), cross-domain user account provisioning, cross-domain entitlement management and cross-domain user attribute exchange.

Use of identity federation standards can reduce cost by eliminating the need to scale one-off or proprietary solutions. It can increase security and lower risk by enabling an organization to identify and authenticate a user once, and then use that identity information across multiple systems, including external partner websites. It can improve privacy compliance by allowing the user to control what information is shared, or by limiting the amount of information shared. And lastly, it can drastically improve the end-user experience by eliminating the need for new account registration through automatic "federated provisioning" or the need to redundantly login through cross-domain single sign-on.

# ![Image result for sp initiated sso flow](data:image/jpeg;base64...)Security Assertion Markup Language (SAML) 2.0 Authentication

Note: With SAML 2.0, there is no need for the SP and IDP to communicate directly. All authorizations are handled through user browser redirects.

# Secure Platform Authentication

Appriss Retail offers Just in Time Provisioning via SAML2 and OpenID Connect. These protocols allow user management to be handled by the customer's Active Directory and provides the end users with a Single Sign On (SSO) experience.  As we have developed our own proprietary Service Provider layer, we are able to interface with any 3rd party Identity Provider that supports SAML2 and, or OIDC.

The minimum data we can accept to authenticate a user and initiate access to Secure are:

* UserName – The unique Active Directory network id for the use
* given\_name - The users’ first name
* family\_name - The users’ last name
* email - The unique email address assigned to the user by the organization

# SSO Assignment of User Roles and Responsibilities

The Secure authentication claim can support assignment of permissions groups referred to as application Roles configured to control the level of access an individual user has in the application. Additional permissions supported in the claim can define the span of control a user has to location groups typically defined by levels of the organizational hierarchy (Market, Region, District) down to specific retail locations and to team-based restrictions that can be used to define operational job responsibilities. These claim attributes should be provided in the SAML 2.0 Assertion in the following nodes:

* Roles – One or more application permission groups to which the user is assigned
* Stores – One or more location groups to which defines the users operational span of control
* Group – One or more operational teams that may exist within the organization (Loss Prevention, Merchandising)

# Manual Assignment of Roles and Responsibilities

The user permissions and span of control definitions described in Section 3 are not always managed within the Active Directory configuration of the Identity provider. In this case permissions can be managed manually within the application by the organization’s system administrator where the SSO process only handles authentication. Alternatively, Secure can ingest details such as location restrictions and teams from a nightly feed and call out to an internal application service to assign the correct restrictions or group membership during the authentication process.  This is referred to as Flat-file Provisioning. For this method, a security file is created by the customer, and transferred via secure transfer during the nightly process. After receipt, the file is processed, and provides additional data for the login process. Flat file provisioning is not a real-time solution, changes made to the user’s permissions would not be available to Secure until a new file is received and processed.

Note: Flat file provisioning is specific to each account and may incur additional Time and Materials costs to configure this capability, Appriss technical consultants will work with the organizations networking team to understand the capabilities of their Identify Management solution and determine the level of effort to integrate using manual provisioning.

# SAML 3.0 Service Provider Initiated Authentication Workflow

At Appriss, we support SP initiated authentication. The flow would involve the following steps:

1. User's browser request access to a protected resource
2. The SSO Web Agent intercepts the call, determines that the user needs to be authenticated and issues a redirect back to the user's browser
3. The user's browser accesses the SSO server, being redirected by the SSO Web Agent
4. The SSO Server determines that the user should be authenticated via Federation SSO, selects an IdP, creates a SAML 2.0 AuthnRequest message, saves the operational state in the SSO server store and redirects the user's browser to the IdP with the SAML message and a string referencing the operational state at the SP
5. The user's browser accesses the IdP SAML 2.0 service with the AuthnRequest message. Once the IdP receives the SAML 2.0 AuthnRequest message, the server will determine if the user needs to be challenged (not authenticated yet, session timed out...). After the possible identification of the user, the Federation SSO flow will resume.
6. The IdP creates an SSO Response with a SAML 2.0 Assertion containing user information as well as authentication data, and redirects the user's browser to the SP with the message and the RelayState parameter
7. The user's browser presents the SSO response to the SP server
8. The SP validates the SAML 2.0 Assertion and creates an SSO session for the user. The SSO server will then redirect the user's browser back to the resource originally requested
9. The user's browser requests access to the resource. This time the SSO Web Agent grants access to the resource
10. The Web Application returns a response to the user's browser

# Sample SAML 2.0 Assertion

<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="\_8e8dc5f69a98cc4c1ff3427e5ce34606fd672f91e6" Version="2.0" IssueInstant="2014-07-17T01:01:48Z" Destination="http://sp.example.com/demo1/index.php?acs" InResponseTo="ONELOGIN\_4fee3b046395c4e751011e97f8900b5273d56685">

<saml:Issuer>http://idp.example.com/metadata.php</saml:Issuer>

<samlp:Status>

<samlp:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>

</samlp:Status>

<saml:Assertion xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" ID="\_d71a3a8e9fcc45c9e9d248ef7049393fc8f04e5f75" Version="2.0" IssueInstant="2014-07-17T01:01:48Z">

<saml:Issuer>http://idp.example.com/metadata.php</saml:Issuer>

<saml:Subject>

<saml:NameID SPNameQualifier="http://sp.example.com/demo1/metadata.php" Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient">\_ce3d2948b4cf20146dee0a0b3dd6f69b6cf86f62d7</saml:NameID>

<saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">

<saml:SubjectConfirmationData NotOnOrAfter="2024-01-18T06:21:48Z" Recipient="http://sp.example.com/demo1/index.php?acs" InResponseTo="ONELOGIN\_4fee3b046395c4e751011e97f8900b5273d56685"/>

</saml:SubjectConfirmation>

</saml:Subject>

<saml:Conditions NotBefore="2014-07-17T01:01:18Z" NotOnOrAfter="2024-01-18T06:21:48Z">

<saml:AudienceRestriction>

<saml:Audience>http://sp.example.com/demo1/metadata.php</saml:Audience>

</saml:AudienceRestriction>

</saml:Conditions>

<saml:AuthnStatement AuthnInstant="2014-07-17T01:01:48Z" SessionNotOnOrAfter="2024-07-17T09:01:48Z" SessionIndex="\_be9967abd904ddcae3c0eb4189adbe3f71e327cf93">

<saml:AuthnContext>

<saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:Password</saml:AuthnContextClassRef>

</saml:AuthnContext>

</saml:AuthnStatement>

<saml:AttributeStatement>

<saml:Attribute Name="username" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">jdoe</saml:AttributeValue>

</saml:Attribute>

<saml:Attribute Name="givenname" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">John</saml:AttributeValue>

</saml:Attribute>

<saml:Attribute Name="surname" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">Doe</saml:AttributeValue>

</saml:Attribute>

<saml:Attribute Name="EmailAddress" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">john.doe@example.com</saml:AttributeValue>

</saml:Attribute>

<saml:Attribute Name="roles" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">administrators</saml:AttributeValue>

<saml:AttributeValue xsi:type="xs:string">everyone</saml:AttributeValue>

<saml:AttributeValue xsi:type="xs:string">store managers</saml:AttributeValue>

</saml:Attribute>

<saml:Attribute Name="stores" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">

<saml:AttributeValue xsi:type="xs:string">120</saml:AttributeValue>

<saml:AttributeValue xsi:type="xs:string">315</saml:AttributeValue>

<saml:AttributeValue xsi:type="xs:string">619</saml:AttributeValue>

</saml:Attribute>

</saml:AttributeStatement>

</saml:Assertion>

</samlp:Response>

**M**ust Have

**S**hould Have

**C**ould Have

# OpenID Connect (OIDC) Authentication

![Secure OIDC Single Sign-on Flow](data:image/png;base64...)

The Authentication Flow in OpenID Connect works as follows:

1. The user attempts to start a session with your client app and is redirected to the OpenID Provider (OneLogin), passing in the client ID, which is unique for that application.
2. The OpenID Provider authenticates and authorizes the user for a particular application instance. So far, it looks like the Implicit flow.
3. A one-time-use code is passed back to the web server using a predefined Redirect URI.
4. The web server passes the code, client ID, and client secret to the OpenID Provider’s token endpoint, and the OpenID Provider validates the code and returns a one-hour access token.
5. The web server uses the access token to get further details about the user (if necessary) and establishes a session for the user.

# Sample OpenID Connect Token

{

"sub": "00uid4BxXw6I6TV4m0g3",

"name":"John Doe",

"nickname":"Jimmy",

"given\_name":"John",

"family\_name":"Doe",

"groups": [

"administrators",

"everyone",

"store managers"

],

"preferred\_username":"jdoe",

"profile":"https://example.com/john.doe",

"zoneinfo":"America/Los\_Angeles",

"locale":"en-US",

"updated\_at":1311280970,

"email":"john.doe@example.com",

“stores”:[

“120”,

“315”,

“619”

],

"email\_verified":true,

"address" : { "street\_address":"123 Hollywood Blvd.", "locality":"Los Angeles", "region":"CA", "postal\_code":"90210", "country":"US" },

"phone\_number":"+1 (425) 555-1212"

}

**M**ust Have

**S**hould Have

**C**ould Have

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
