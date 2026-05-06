## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Interface Number | J023 | Project name | TOM Integration | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | TOM Integration Interface Specification Advanced Shipping Notice From TIMS to RMS | Document date and/or version | 2007-01-22 00:00:00 | 0.1D | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Sec 3.1 | We are unaware that the source file is dropped on to the share in read only mode.\nWe are developing with the assumption that the file will be created in another location and dropped to the TIMS share in non read only mode OR that the file will be created in TIMS share with a read lock during creation and after creation the read lock will be released | Low | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| Sec 3.1 | The TIMS drop share and the file name created is unknown. These values will be kept configurable and will have to be reconfigured in the before moving to test/production based on environment values | Low | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| Sc 4.5 | Grouping information not provided on Target schema. Will assume the grouping as in embedded schema file | Low | Unclear | Closed | Ravindra | 2007-02-06 00:00:00 | Supriyo | 2007-02-07 00:00:00 | Use the XSD file for getting grouping info |
| Sec 4.6 | The RMS destination XML file name required is unknown. These values will be kept configurable and will have to be reconfigured in the before moving to test/production based on environment values | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Sec 4.9 | Volumes of data expected not known assuming each source message file is less than 2MB and we can get many multiple message files throughout the day | Medium | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | No codepage specified for source and destination messages. UTF-8 (65001) will be used | Low | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | Assumption: Source message files are created with Unique identifiers, so that if Biztalk is not able to process some source messages on time, they will not be overwritten\nDestination files  are created with UniqueIds and timestamp in their names so that one message doesnot override another | Low | Unclear | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | Sample messages for Source and destination were not available. So, development will proceed with dummy test messages created from the schema definitions provided in the spec. This may affect functional accuracy and quality of unit testing on the interface | Medium | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | There is no requirement to archive messages after processing, if they are sucessful. Only failed messages are archived to failed folder. The interface uses tracking of message bodies on receive port before processing so that they can be recreated in case of failure | Low | Unclear | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | Assumption: There is no requirement for ordered delivery of messages | Low | Unclear | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| General | Sample messages for Source and destination were not available. So, development will proceed with dummy test messages created from the schema definitions provided in the spec. This may affect functional accuracy and quality of unit testing on the interface | Medium | Missing | New | Ravindra | 2007-02-09 00:00:00 | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 9 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 0 | In progress | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 3 | Closed | 1 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 7 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 10 | Total | 10 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 6 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 0 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 4 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 10 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## PO Data Flow Diagram
|
|  |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |