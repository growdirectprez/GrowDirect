## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Interface Number | S077 | Project name | TOM Integration | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | TOM Integration Interface Specification on Actual Range in Store from GFO to Store Range\n | Document date and/or version | 26/03/2007 | 0.1D | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Sec 3.1 | We are unaware that the source file is dropped on to the share in read only mode.\nWe are developing with the assumption that the file will be created in another location and dropped to the share in non read only mode OR that the file will be created in the share with a read lock during creation and after creation the read lock will be released | Low | Missing | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| Sec 3.2 & 4.5 | Assumption: As the source message schema doesn't define whether the detail records is 1 or many, it as assumed as 1 by default. And, the target message schema defines that the detail records are many. As the details in the source message schema is assumed as one single record, the same would be reflected in the target message schema | Medium | Missing | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| Sec 3.2 | In the source message schema, the field 'JLCXB-ON-PROMOTION' should start at position 57. But, it has no positional specification. | Medium | Missing | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| Sec 3.2 | The date format for the fields 'JLCXB-STKD-PROD-STDT', 'JLCXB-STKD-PROD-ENDT', 'JLCXB-ACTL-RNGE-IN-DT' and 'JLCXB-ACTL-RNGE-OUT-DT' in the source message would be of "YYYY-MM-DD" | Medium | Missing | Closed | Ravindra | 2007-03-27 00:00:00 | Nitin | 2007-03-28 00:00:00 | NaN |
| Sec 3.2 | What actually is the RecordType mentioned in the table header of the Source message schema. We assume that it has nothing to do with the interface development. Please clarify | Low | Comment | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| Sec 3.4 | The source physical location is a shared location on Unix platform. As we don't have any Unix system, as of now, we assume the source location as a shared location on the Windows platform. This value will be kept configurable and will have to be reconfigured before moving to test/production based on environment values | Low | Comment | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| Sec 4.5 | The date format for the fields 'Stock Start Date', 'Stock End Date', 'Actual Range In Date' and 'Actual Range Out Date' in the target message would be of "YYYY-MM-DD" | Medium | Missing | Closed | Ravindra | 2007-03-27 00:00:00 | Nitin | 2007-03-28 00:00:00 | NaN |
| Sec 3.4 & 4.7 | As the RTI has enriched functionality for archiving the source messages and as there is scope for desired naming conventions of the target messages, the BizTalk RTI file adapter would be used in the configuration of the application instead of the BizTalk file adapter | Low | Comment | Closed | Ravindra | 2007-03-27 00:00:00 | Nitin | 2007-03-28 00:00:00 | NaN |
| General | Volumes of data expected not known assuming each source message file is less than 2MB and we can get many multiple message files throughout the day | Medium | Missing | New | Ravindra | 2007-03-26 00:00:00 | NaN | NaN | NaN |
| General | No codepage specified for source and destination messages. UTF-8 (65001) will be used | Low | Missing | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| General | Sample messages for Source and destination were not available. So, development will proceed with dummy test messages created from the schema definitions provided in the spec. This may affect functional accuracy and quality of unit testing on the interface | Medium | Missing | New | Ravindra | 2007-03-26 00:00:00 | NaN | NaN | NaN |
| General | Assumption: There is no requirement for ordered delivery of messages | Low | Unclear | Closed | Ravindra | 2007-03-26 00:00:00 | Nitin | 2007-03-27 00:00:00 | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 2 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 0 | In progress | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 6 | Closed | 10 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 6 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 12 | Total | 12 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 8 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 0 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 1 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 3 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 12 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |