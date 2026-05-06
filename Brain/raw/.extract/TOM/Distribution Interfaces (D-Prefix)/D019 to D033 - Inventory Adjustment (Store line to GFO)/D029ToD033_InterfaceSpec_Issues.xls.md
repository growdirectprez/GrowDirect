## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Interface Number | D019 to D033 | Project name | TOM Integration | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | TOM Integration Interface Specification Inventory Adjustment STORELINE To GFO\n | Document date and/or version | 2007-02-16 00:00:00 | 0.1D | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Sec 2.1 | Assumptiion: The stored proc JH0S00 gets stream information by passing some values of the source message (mentioned in sections 4.10, 4.11, 4.12) as attributes to it. After obtaining this stream info, Biztalk has to execute the subsequent stored procs (JIP11,JIP12,JIP13) by passing the stream information and some values of the source message to complete the processing. Also, Biztalk has to check the success/failure of the stored procs. If one of the stored procedures fails, the changes done by the executed stored procs have to be reverted back | Low | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes-If the said sp generates error then all other sp execution stpped for the ROWSET. |
| Sec 2.1 | Mechanism to update the database in GFO in Unix platform from Windows (calling the stored procedures in BizTalk) has to be mentioned in detail. We assume that the DB2 adapter mentioned would be for Windows, but not for cross-platform operation. This has to be made clear | High | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | NaN |
| Sec 2.2 | Assumption: The interface is named as ASN in the architecture diagram. We understand it to be Inventory Adjustment | Low | Comment | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes-Please change to Inventory Adjustment |
| Sec 3.1 | We are unaware that the source file is dropped on to the share in read only mode.\nWe are developing with the assumption that the file will be created in another location and dropped to the share in non read only mode OR that the file will be created in the share with a read lock during creation and after creation the read lock will be released | Low | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | The file will be created in the share with a read lock during creation and after creation the read lock will be released. |
| Sec 3.1 | The drop share and the file name created is unknown. These values will be kept configurable and will have to be reconfigured in the before moving to test/production based on environment values | Low | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Only Shareed location need to be configured.For file name it will be using a \*.dat file. |
| Sec 3.2 | No grouping hierarchy provided for the source message | Medium | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | It is a envelop type msg schema.This means the source file has one headerwith many detail records. |
| Sec 4.10 | Assumption: In the foot-print of the stored procedure, the input attribute (Store No) from Source field name would be taken from the detail records for every item number which means that the stored procedure would be executed for every item | Medium | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes |
| Sec 4.11 | Assumption: In the foot-print of the stored procedure, the input attribute (Store No, Item Number, Date of Extract, Time of Extract, Reason Code) from Source field name would be taken from details for every item number which means that the stored procedure would be executed for every item | Medium | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes |
| Sec 4.10 | Assumption: In the foot-print of the stored procedure, the input attribute (Store No, Item Number, Date of Extract, Time of Extract) from Source field name would be taken from details which means that the stored procedure would be executed for each item | Medium | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes |
| Sec 4.10 | Assumption: In the foot-print of the stored procedure, the input attribute (Store No, Item Number, Date of Extract, Time of Extract) from Source field name would be taken from details which means that the stored procedure would be executed for each item | Medium | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes |
| General | Volumes of data expected not known assuming each source message file is less than 2MB and we can get many multiple message files throughout the day | Medium | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | No the data will be 20-40 kb and the frequency depends whenever storeline goes for inventory adjustment. |
| General | No codepage specified for source and destination messages. UTF-8 (65001) will be used | Low | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | NaN |
| General | Assumption: Source message files are created with Unique identifiers, so that if Biztalk is not able to process some source messages on time, they will not be overwritten\nDestination files  are created with UniqueIds and timestamp in their names so that one message doesnot override another | Low | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | Yes for source file.There is no destination file. |
| General | Sample messages for Source and destination were not available. So, development will proceed with dummy test messages created from the schema definitions provided in the spec. This may affect functional accuracy and quality of unit testing on the interface | Medium | Missing | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | I will be sending the sample source data.For destination there will not be any sample data it is only updating the GFO table structure. |
| General | There is no requirement to archive messages after processing, if they are sucessful. Only failed messages are archived to failed folder. The interface uses tracking of message bodies on receive port before processing so that they can be recreated in case of failure | Low | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | No archieving is required for faillure it is just writing into a log file. |
| General | Assumption: There is no requirement for ordered delivery of messages | Low | Unclear | New | Ravindra | 2007-02-16 00:00:00 | NaN | NaN | You are talking it w.r.t calling order of sp.If so then after output attribute field value the next execution will start. |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 13 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 0 | In progress | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 7 | Closed | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 6 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 13 | Total | 13 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 5 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 0 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 8 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 13 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |