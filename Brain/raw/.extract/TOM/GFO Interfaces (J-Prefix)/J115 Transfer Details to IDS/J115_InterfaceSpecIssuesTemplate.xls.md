## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | Completion activities | NaN | NaN |
| Document title | TOM Integration Interface Specification Transfer Information for PBS Order from RMS to IDS | Document date and/or version | 21/20/2007 | 0.1 | Accountable | NaN | NaN |
| Comments by: | D.Rama Krishna | Review date | NaN | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| General | Interface number is F001, not J0026 | Medium | Wrong | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| General | Please specify more information around the purpose and overview of this interface. | Medium | Unclear | Closed | Supriyo | Provided | 2006-12-28 00:00:00 |
| General | Please use the more up-to-date template supplied by Adrian, and ensure that any irrelevent information is removed or marked clearly as a placeholder. | High | Wrong | Closed | Supriyo | Changes carried out in new  template | 2006-12-28 00:00:00 |
| General | what are the  login credentials I need to use when I want to connect IDS to send data from RMS | Low | Unclear | New | Supriyo | NaN | NaN |
| General | sample data required to  start working | Medium | Missing | New | Supriyo | You need sample data for testing. For development you don't require sample data. | NaN |
| General | What is the mechanism to prevent input files/messages from being picked by  BizTalk/RTI file adapters while they are still being created? | Low | Missing | New | Supriyo | This is a message created through RIB and then will be published by RIB. Once published then the message will be picked up by JMS Adapter. | NaN |
| General | How does the destination message indicate completion? | Medium | Missing | New | Supriyo | NaN | NaN |
| General | What is the file name of source drop?Assumption: We will develop with the ability to reconfigure the source filename on the interface before moving to test/production based on environment values | Low | Missing | NaN | Supriyo | NaN | NaN |
| General | Does the naming schema on source and destination guarantee uniqueness of each file created. Will a newer version overwrite the earlier file? | Medium | Missing | New | Supriyo | NaN | NaN |
| General | Assumption: Source message files are created with Unique identifiers, so that if Biztalk is not able to process some source messages on time, they will not be overwritten\nDestination files  are created with UniqueIds and timestamp in their names so that one message doesnot override anothe | Medium | Missing | New | Supriyo | NaN | NaN |
| General | What is the expected volume of source data? Assumption:t source message file is less than 2MB | Low | Missing | New | Supriyo | NaN | NaN |
| Section 4.5 Target message schema | The Data tables(Transfer,TransferLine) are not available in the IDS database to create Target schema | Medium | Missing | New | Supriyo | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S1.2 - Background | What do you mean "business specific Store reference data"? | Medium | Unclear | Closed | Supriyo | SC 28/12/06: Corrected\nAB 02/01/07: Still present - please correct the text.\nSG 03/01/07: Corrected. | 2006-12-28 00:00:00 |
| S2.1 Description of the End-to-End Interface | The file does not contain "reference data records" | Medium | Wrong | Closed | Supriyo | Removed | 2006-12-28 00:00:00 |
| S3.1 Scope | Part of this process scope exists already (EDIDLORD.pc), and part does not - it will not be this batch job (EDIDLORD) which does any conversion. As above, please be more specific about what components are involved in this stage. | Medium | Unclear | Closed | Supriyo | Modified. | 2006-12-28 00:00:00 |
| S3.1 Scope | Why, and what component, will convert numeric data to packed decimal? | Medium | Unclear | Closed | Supriyo | this part is not required for this interface. Removed | 2006-12-28 00:00:00 |
| S3.3 | Source Platform / OS is IBM AIX | Low | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4 | What is contained in this section - it seems to be just placeholders. | Medium | Missing | Closed | Supriyo | This section will not carry much information in case of simple file drop. This section will be brifly defined about the Target location and target file specification.\nWhen filtering of records comes into account like Inventory report interface should not transfer sales data which RMS Inventory file into TIMS. | 2006-12-28 00:00:00 |
| S4.1 | What is the "shipping agent", and why is it involved in this interface? | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4.6 | What is the "TO" system? | Enhancement | Comment | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4.7 | Again - why "shipping agent"? Also, what has been written here does not make sense. | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S8.1 | Please explain why a particular assumption is relevent - in this case, what is the impact on the interface if this assumption about EOD processing is incorrect? If an assumption has led to a particular decision, please detail. | Medium | Unclear | Closed | Supriyo | Removed | 2006-12-28 00:00:00 |
| Appendices | Please ensure they are maintained - especially the change record. | Medium | Comment | Closed | Supriyo | Modified. | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 8 | NaN | NaN | NaN | NaN |
| High | 0 | In progress | 0 | NaN | NaN | NaN | NaN |
| Medium | 1 | Closed | 0 | NaN | NaN | NaN | NaN |
| Low | 1 | Defect raised | 0 | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN |
| Total | 2 | Total | 8 | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 9 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 3 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 9 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 2 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 23 | NaN | 0 | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |