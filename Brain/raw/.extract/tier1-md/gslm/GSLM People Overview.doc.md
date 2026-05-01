The Global Store Interface Project could support the ability to integrate a centralized data store of associate information from an international country with the Global HR database.  Associate data in the GSLM will be limited to contact details, emergency contacts, associate language, work area and line managers.  
Assumptions:
The GSLM will leverage many of the customer entities that define a person and their contact methods as the basis for the associate profile.
The GSLM will not support time and attendance functions for international markets.
The GSLM will not support payroll and employee benefits for international markets.
The Customer elements of the GSLM structure can be utilized to support associate discount card information if desired.
Use Cases:
Create Walmart associate WIN for international employee
Add associate profile to Global HR database
Define employee manager and assigned work areas in Global HR database

The following section describes the GSLM entities and their attributes which have been modeled as part of People scope:

Entity Name
Description
Associate
The Associate entity describes the Wal-Mart associate
Attribute
Type
Description
person_id
Number
Unique identifier for a person
associate_win
Number
Unique identifier of a Wal-mart associate
national_id
Text
Government issued Id number for the person (e.g. SSN, National Insurance)
associate_userid
Text
Associates userid
associate_employee_id
 
Foreign key to the native key entity, the unique identifier of the associate assigned by the international / acquired company.
associate_charge_store 
Locations
Foreign key to sales outlet table, the store to which the associates expenses are charged.
associate_charge_division 
Number
The Division the employee is assigned to.
associate_work_store
Locations
Location where the associate is currently assigned
associate_manager
Associates
Unique identifier for a person, which manages the associate
associate_org_hire_date
Date?
The date the associate was hired originally
associate_hire_date
Date?
The hire date for the associates current work period
associate_work_status
Code?
The work status of the associate
associate_type_code
Code?
The type of associate, full time, peak time or temporary 
associate_type_eff_date
Date?
The date the associate type became effective for the associate 
rehire_eligible
Indicator
Indicates if an employee is eligible for rehire
pay_type_code
Code?
The pay type of the associate, hourly, salary, salary exempt. 
pay_type_eff_date
Date?
The date the current pay type was effective for the associate 
pay_band_nbr
Code?
salary plan of the associate
tax_marital_code
Code?
The marital status of associate for tax reporting 
pay_frequency_code
Code?
The pay interval for the associate (weekly, monthly, ect.)
loa_eff_date 
 Date?
Leave of absence start date
loa_return_date 
Date?
Leave of absence return date
loa_code 
 Code?
Leave of absence reason code
loa_desc 
 Text?
Leave of absence extended description
termination_date 
 Date?
Date the employee was terminated
termination_reason_code 
 Code?
The termination reason code from the corresponding HR system 
termination_reason_desc 
 Text?
Termination comments / description
mgmt_training_date
Date
Management training date of the employee
poistion_number
Number
The home office position number the associate is assigned in.
super_position_number
Number
This is the position number of the supervisor of the associate.
supervisor_comment
Text
Supervisor comments



Entity Name
Description
 
AssociateLanguage
The AssociateLanguage entity describes the languages an employee can converse in
 
Attribute
Type
Description
associate_win
Number
Unique identifier for a person
language_code
Code
The code for a specific language
proficiency_level_code
Code
The proficiency level of the associate with the language



Entity Name
Description
 
AssociateWorkArea
The departments that the associate works in
 
Attribute
Type
Description
associate_win
Number
Unique identifier for a person
sales_outlet
Number
The sales outlet identifier
sales_outlet_dept_id
Number
The department within the sales outlet that this associate works
department_entry_date 
Date?
The date a store associate was assigned to their current department 
job_code 
 Code
The job number for the associate used to define the job function of the associate.
job_desc 
 Text?
Description of job 
job_code_eff_date 
 Date?
The date the job number was active for the associate
job_type_seq_nbr 
 Number?
Sequence number used when an associate is assigned more than one job. This occurs either when an associate has a primary and secondary jobs or when an associate is in more than one hr source type.
job_end_date
Date?
The date the job assignment is no longer valid for the associate.  The date the associate moves to a new job or transferred or terminated. 
hr_org_id 
 Code?
The organizational area of the company as aligned to the human resource division.



Entity Name
Description
 
AssociateEmergencyContact
The contact details of an associate in case of emergency
 
Attribute
Type
Description
associate_win
Number
Unique identifier for a person
associate_contact
Number
Unique identifier for the associates' contact
associate_contact_relationship
Code
A relationship code, specifying the relationship between associate and contact









Global Store Logical Model – People



