The Global Store Interface Project will support the ability to integrate the customer database of an acquired chain’s loyalty program with the Walmart Customer Hub.  This integration will further the view of Walmart’s customer relationships globally, and supports the goal of having a single view of the customer across their business relationships with Walmart. The Global Store Logical Model and supporting XML schema will be modeled on the current Customer Hub data model; providing a standard mechanism for integrating the various customer data stores which may exist in international markets. 
 EMBED Visio.Drawing.11  
Assumptions:
The GSLM will not provide the ability to offer membership or loyalty services to a market, the intent is to capture customer profile data and provide a link for marketing and analysis between the Walmart’s global customer relationships and  in market loyalty program.
Market specific loyalty programs will define the customer offer for their registered base; the GSLM assumes that the functionality that drives the offer is resident in the non converted store systems.
The GSLM will integrate the customer, contract, contract component and related entities to support this scope.
No payment or Personal information requiring PCI or PII encryption will be stored for contacts created through loyalty program conversion.
The security requirements for International Market to Home Office data transmission as well as market specific regulations must be addressed as part of the physical integration with an international data source.
The GSLM will provide a stub out of privacy and consumer preferences that support basic opt in and contact preferences, the specific attributes for each market’s customer base would be defined as part of the physical implementation.  

The following section describes the GSLM entities and their attributes which have been modeled as part of the Customer scope:
Entity Name
Description
Customer
This entity represents a member in the system. This could be an individual or an organization.
Attribute
Type
Description
wm_customer_id
Number
The global identifier of the Customer
customer_relationship_id
CustomerType
Defines the customer type Organization or individual / person
preferred_language_type
Code
Identifies the preferred member communication language
contact_active_ind
Indicator
Indentifies if the contact is active
last_update_date
Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 



Entity Name
Description
CustomerRelationship
This entity is a logical construct which defines  the type of relationship associated with a particular Walmart customer id (organization or person).
Attribute
Type
Description
Customer_relationship_id
Number
Unique identifier of the customer relationship
customer_relationship_type
Code
Defines the type of relationship (Organization, Person)



Entity Name
Description
Organization
This entity represents a contact as an organization
Attribute
Type
Description
organization_id
CustomerRelationship
The unique organization id
contact_id
Contacts
Foreign Key to the contact
organization_name_id
OrganizationNames
Foreign Key to the organization name
organization_type
Code
type of organization



Entity Name
Description
OrgPersonBreakout
This entity defines the group of people in the person entity which are members of the organization.
Attribute
Type
Description
organization_id
Organizations
Foreign Key to the organization entity
person_id
Persons
Foreign Key to the person entity
org_role_type
Code
Defines the persons role in the organization



Entity Name
Description
Person
This entity represents a contact as a Person
Attribute
Type
Description
person_id
CustomerRelationship
 
birth_date
Date
date of birth
gender_type
Code
gender
name_type
Code
type of name
given_name_one
Text
first name
given_name_two
Text
middle name
last_name
Text
last name



Entity Name
Description
ContactMethod
This entity represents the various contact methods, email and phone
Attribute
Type
Description
contact_method_id
Number
The unique contact method id
reference_nbr
Text
contact method value, e.g. entire phone number or email address
contact_method_usage_type
Code
Identifies the contact method type
last_update_date
Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 



Entity Name
Description
EmailAddress
This entity represents an email address
Attribute
Type
Description
email_address_id
Number
The unique email address id
email_address_type
Code
Identifies the type of email
email_address
Text
actual email



Entity Name
Description
PhoneNumber
This entity represents a phone number
Attribute
Type
Description
phone_nbr_id
Number
The unique phone number id
phone_nbr_type
Code
Identifies the type of phone number
phone_area_code
Number
Identifies the phone's area code
phone_exchange
Number
Identifies the phone's exchange
phone_nbr
Number
Identifies the phone number



Entity Name
Description
Address
This entity represents an address
Attribute
Type
Description
address_id
Number
The unique address id
address_usage_type
Code
Identifies the type of address
last_update_date
Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 
address_line_one
Text
Identifies the Address Line 1
address_line_two
Text
Identifies the Address Line 2
address_line_three
Text
Identifies the Address Line 3
city
Text
Identifies the city
zip_postal_code
Text
Identifies the zip code
province_state_type
Code
Identifies the State/Province code
country_type
Code
Identifies the Country code



Entity Name
Description
BusinessRelationship
The entity defines the relationship between a customer and Walmart.
Attribute
Type
Description
business_relationship_id
Number
The unique contract id
native_key_id
NativeKeys
Foreign key to the Native Key entity, part of the composite key which defines a unique native key within a business division.
business_division_id
BusinessDivisions
Foreign key to the Business Divisions entity, part of the composite key which defines a unique native key within a business division.
last_update_date
 Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 
end_date
 Date
The date that this row of data became invalid. 
contract_lob_type
Code
1 Walmart 18 Sam's Club 1000018 Mas Club
country_type
Code
country type for this contract, e.g. this is set to US for US Clubs and PR for Porte rico



Entity Name
Description
BusinessRelationship
Component
The membership structure maps into WCC contract component structure.  E.g. currently, this contain the following components: Base, Plus, Tax-Exempt, and Cigarette Tax-Exempt.
Attribute
Type
Description
business_relationship_
component_id
Number
The unique contract component id
business_relationship_id
BusinessRelationships
Foreign Key to the owner contract id
base_ind
Indicator
Used to identify the base component of the contract. Every contract has at least one component, the base component. 
last_update_date
Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 
contract_status_type
Code
Identifies the status of the contract. For example: ″active″, ″pending″, lapse pending″, or ″cancelled″. These values are provided by the administrative source systems of the contract.
issue_date
Date
The date which the contract component was issued. 
end_date
Date
The date that this row of data became invalid. 
expiry_date
Date
The date that the type code is no longer valid. 
product_type
Code
Identifies the type of product associated with the contract (or at some level within the product family). E.g. WMT Walmart Account, Plus Advantage etc.



Entity Name
Description
BusinessRelationshipRole
The entity specifies what contacts can do with the applied contract component
Attribute
Type
Description
business_relationship_
role_id
Number
The unique contract role id
business_relationship_id
BusinessRelationships
Foreign Key to the owner contact id
business_relationship_
component_id
BusinessRelationship
Components
Foreign Key to the contract component this role applies to
native_key_id
NativeKeys
Foreign key to the Native Key entity, part of the composite key which defines a unique native key within a business division.
business_division_id
BusinessDivisions
Foreign key to the Business Divisions entity, part of the composite key which defines a unique native key within a business division.
arrangement_type
Code
contract status
recorded_start_date
Date
The date which the party’s relationship to the contract became legally effective. This is commonly the date which the party signed the contract.
role_type
Code
Identifies the type of role that a contact may have on a contract. 
start_date
Date
The date that this row of data became valid. 
end_date
Date
The date that this row of data became invalid. 
card_holder_nbr
Number
Identifies an individual on the base component, this is only used by Membership
role_desc
Text
role description, e.g. Household



Entity Name
Description
NativeKey
The entity is used to define the various unique keys that represent a customer relationship.
Attribute
Type
Description
native_key_id
Number
The native key is a system generated unique identifier for the business relationship which has been generated by a source system (e.g. SAM's membership number, walmart.com id, loyalty card number)
business_division_id
BusinessDivisions
Foreign key to the Business Divisions entity, part of the composite key which defines a unique native key within a business division.
admin_contract_id
Number
The actual text or number that is used in the administrative source system to identify a contract. 
admin_field_name_type
Code
Identifies the field name that the native key refers to, for example, policy number, policy suffix, account number, branch, and others. 
last_update_date
 Date
When a record is added or updated, this field is updated with the date and time. On subsequent updates, WCC uses this information to ensure that the update request includes a matching date and time on this field; if it does not, the update fails. 
contract_component_ind
Indicator
Describes which table the native key applies to. If the contract component indicator is ’Y’, the native key applies to the Contract Component. If the contract indicator is not ’Y’, the native key applies to the Contract. The contract ID is the value from the Contract Component (the contract component ID).





Entity Name
Description
PrivacyOption
This entity represents the various preference opt in options that customers can opt into, preferences are maintained at the business division level.  (e.g. a customer can define separate contact preferences for Sam's vs. Walmart)
Attribute
Type
Description
privacy_option_id
Number
The unique privacy option id
business_division_id
BusinessDivisions
Foreign key to the Business Divisions entity
default_opt_in_ind
Indicator
default value for this opt-in
country_type
Code
Identifies the country for this opt-in
privacy_opt_cat_type
Code
 









Global Store Logical Model – Customer



