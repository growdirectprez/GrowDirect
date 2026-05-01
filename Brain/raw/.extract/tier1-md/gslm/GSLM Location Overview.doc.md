The Location entities contain the master reference data which define the organizational hierarchy, locations types, operational departments, and operating calendar of all locations in the Global Store Logical Model.
Assumptions:
The GSLM organizational hierarchy is a 6 level structure which should be rigid in levels 1 – 3, but can be customized as needed in levels 4 -6 to define the reporting structure of the business unit being defined.
Level 2 Market represents the attribute currently known as country code in Home Office Systems. 
Market level 2 is the point where the merchandise hierarchy connects to the organization, it is also the Level 1 of the merchandise hierarchy. 
Customers facing selling locations which may include stores, club, or web sites are referred to as Sales Outlets in the Global Store Logical model.
Location UDA’s can be defined to create customized attributes for each location type in the model
The GSLM contact method entities found in the Customer definition document are used to define address, phone number and e-mail data for a location.
The following section describes the GSLM entities and their attributes which have been modeled as part of the Location scope:
Entity Name
Description
BusinessDivision
Level 1 of the Organizational Hierarchy.  Business division represents major segments of the Walmart Business (E.g. Dvision1 - Walmart Stores, Div 18 - Sam's Club, Div 35 - International).  The GSLM organizational hierarchy is a 6 level structure, the definition of levels 4 -6  in the organizational hierarchy can vary by division, and should be defined based upon the needs of the organization being mapped to the GSLM.
Attribute
Type
Description
business_div_id
Number
Unique identification number of the business division in the GSLM merchandise and organizational hierarchies.
business_div_desc
Text
Business division description 



Entity Name
Description
Market
Level 2 of the organizational hierarchy, represents the attribute currently know as country_code in Home Office Systems.  Sample values include: US, MX, BR, K1, K2
Attribute
Type
Description
business_div_id
Number
Unique identifier of the level 1 parent in the organizational hierarchy
market_code
Number
Unique code which represents level 2 of the hierarchy (US, MX, BR, K1, etc)
market_desc
Text
Business division description 



Entity Name
Description
Country
Level 3 of the organizational hierarchy, representing geographic breakdowns within a market.  (E.g. Level 2 K1 has Honduras, Guatemala, Costa Rica, Nicaragua) as level 3 members.  Large Countries such as Brazil, China, India may need further breakdown at level 3, in this case geographic locale could be used to define an area within a country.
Attribute
Type
Description
market_code
Code
Unique identifier of the level 2 parent in the organizational hierarchy
country_code
Code
The actual international country code that would be used to identify a specific country.  This does not represent the current country_code value which has been replaced by market_code in the GSLM.
geographic_locale
Code
a subdivison of country which could be used to further breakdown a single country within level 3 of the hierarchy (E.g. Brazil:  NorthEast, SouthEast, West)



Entity Name
Description
Company
Level 4 of the organizational hierarchy, typically this would be used to represent smaller operating units within the market such as format, chain, channel, brand, etc.  
Attribute
Type
Description
country_code
Code
Unique identifier of the level 3 parent in the organizational hierarchy
company_code
Code
Unique identification number of the level 4 member in the GSLM organizational hierarchy.
company_desc
Text
Extended description of the company
base_company
Code
A recursive reference to company in the hierarchy which would allow for roll up reporting of a company if it has been split across a higher level of the organizational hierarchy.



Entity Name
Description
District
Level 5 of the organizational hierarchy, could represent a geographical area, or brand which operates in the  Each organizational level is flexible and should be defined inline with the business unit needs.
Attribute
Type
Description
company_code
Code
Unique identifier of the level 4 parent in the organizational hierarchy
district_id
Number
Unique identification number of the level 5 member in the GSLM organizational hierarchy.
district_desc
Text
Level 3  member description.



Entity Name
Description
Region
Level 6 of the organizational hierarchy, could represent a further breakdown of a geographical area.  Each organizational level is flexible and should be defined inline with the business unit needs.
Attribute
Type
Description
district_id
Number
Unique identifier of the level 5 parent in the organizational hierarchy
region_id
Number
Unique identification number of the level 6  member in the GSLM organizational hierarchy.
region_desc
Text
Level 4  member description.



Entity Name
Description
Location
The GSLM entity which describes a physical location.  Location can have contact methods assigned to them, and custom attributes can be defined by location type.
Attribute
Type
Description
business_div_id
Number
Unique identification number of the business division in the GSLM merchandise and organizational hierarchies.
country_code
Code
The country code of the Division, inherited by each sublevel of the hierarchy. 
company_id
Number
Unique identification number of the level 2 member in the GSLM organizational hierarchy.
district_id
Number
Unique identification number of the level 3  member in the GSLM organizational hierarchy.
region_id
Number
Unique identification number of the level 4  member in the GSLM organizational hierarchy.
location_id
Text
The location id, foreign key to the sales outlet and warehouse entities.  The location id number should be the store number or warehouse number that is used in other systems along with country code to define the unique location.
location_type
Code
A code value to describe the type of location associated with the location id. (E.g., Store, Warehouse, Restaurant, Convenience)



Entity Name
Description
LocationDepartment
The logical entity which defines the valid operational departments  areas which have been assigned to a location. Typically used to define the operational department of a store  (Automotive, Grocery, Sporting Goods, etc.) or warehouse (Receiving, Picking, Shipping, etc.)
Attribute
Type
Description
location_dept_id
Number
The Primary Key of the locationdepartment entity.
location_dept_desc
 Text
The description of the department
location_id
Locations
The foreign key to the location entity
dept_open_time
 Time?
The opening hours for the department in the store.
dept_closed_time
 Time?
The closing hours for the department in the store.



Entity Name
Description
LocationHolidayCalendar
The entity which defines the operating calendar for the sales outlet.
Attribute
Type
Description
location_holiday_calendar_id
 Number
The primary key of the LocationHolidayCalendar entity
location_closed_date
 DateTime
The date when a location is closed
location_closed_code
 Code
A code value used to define the reason for closing the location
location_closed_desc
 Text
The description of the reason for closure (E.g. Christmas)
location_id
Locations
The foreign key to the location entity, the unique identifier of the location to which the calendar is associated.



Entity Name
Description
SalesOutlet
The logical entity which contains the GSLM master records for all outlets where a consumer can purchase goods.  It provides the ability to distinguish between location types such as stores, clubs, websites, mobile devices, etc.
Attribute
Type
Description
business_div_id
Number
Unique identification number of the business division in the GSLM merchandise and organizational hierarchies.
country_code
Code
The country code of the Division, inherited by each sublevel of the hierarchy. 
company_id
Number
Unique identification number of the level 2 member in the GSLM organizational hierarchy.
district_id
Number
Unique identification number of the level 3  member in the GSLM organizational hierarchy.
region_id
Number
Unique identification number of the level 4  member in the GSLM organizational hierarchy.
sales_outlet_nbr
Locations
The location id, foreign key to the location entity.  The location id number is the store number used in other systems along with country code to define the unique location.
sales_outlet_type
 Code
A code value which defines the type of sales outlet.  (Club, Store, Web) 



Entity Name
Description
Warehouse
The logical entity which contains the GSLM master records for a warehouse
Attribute
Type
Description
business_div_id
Number
Unique identification number of the business division in the GSLM merchandise and organizational hierarchies.
country_code
Code
The country code of the Division, inherited by each sublevel of the hierarchy. 
company_id
Number
Unique identification number of the level 2 member in the GSLM organizational hierarchy.
district_id
Number
Unique identification number of the level 3  member in the GSLM organizational hierarchy.
region_id
Number
Unique identification number of the level 4  member in the GSLM organizational hierarchy.
warehouse_nbr
Locations
The location id, foreign key to the location entity.  The location id number is the warehouse number used in other systems along with country code to define the unique location.
warehouse_type
 Code
A code value which defines the type of warehouse. (e.g. Physical, virtual)



Entity Name
Description
LocationUserDefinedAttribute
The logical construct which allows for custom user defined attributes to be associated with any location type in the GSLM.  The is entity must be closely governed to ensure that it is not abused. 
Attribute
Type
Description
uda_id
 Number
The primary key, a globally unique identifier for the UDA
Location_type
LocationType
Foreign key to the location type entity, identifies the location type  that the UDA relates to
uda_desc
 Text
The description of the user defined attribute
data_type
Code?
 Defines the value types which are valid for this UDA. Valid types are NUM, ALPHA, DATE
single_value_ind
 Indicator?
 



Entity Name
Description
Location UserDefinedAttributeValue
The entity which contains the valid values which are possible for the user defined attribute of the merchandise.
Attribute
Type
Description
uda_value_id
 Number
The primary key, a unique identifier for the uda value.
uda_id
 UserDefinedAttributes
Foreign key to the UDA entity, defines the group of related uda values.
uda_value
 Text
The value of the uda that will be assigned to a merchandise id (E.g. the Item xref number)
uda_value_desc
 Text
The description of the value.

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
address_line_one
Text
Identifies the Address Line 1
address_line_two
Text
Identifies the Address Line 2
address_line_three
Text
Identifies the Address Line 3
address_line_four
 
Identifies the Address Line 4
city
Text
Identifies the city
county
 
Identifies the county
postal_code
Text
Identifies the zip code
province_code
Code
Identifies the State/Province code
country_code
Code
Identifies the country code










Global Store Logical Model – Location



