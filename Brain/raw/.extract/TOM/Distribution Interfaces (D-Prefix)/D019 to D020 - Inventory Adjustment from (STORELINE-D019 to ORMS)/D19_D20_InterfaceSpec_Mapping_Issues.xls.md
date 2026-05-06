## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Interface Number | D019\_D020 | NaN | NaN | NaN | NaN | NaN | NaN |
| Document title | D019\_D020 TOM Integration Interface Specification STORELINE To ORMS | Document date and/or version | 15/02/2007 | 1 | NaN | NaN | NaN | NaN | NaN |
| Location | Description | Severity | Type | Status | Opened by | Open Date (dd/mmm/yyyy) | Closed By | Close Date (dd/mmm/yyyy) | Comments |
| Sec 3.4 Message Transport details | The format of the source filename is given in mapping spec.,but the source location is not known.We will develop with the ablity to reconfigure the location and filename | Low | Missing | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 4.7 Message Transport details | The format of the destination filename given in mapping spec is "tsc\_invadjupld\_{store number}\_{yyyymmddhhmmss}\_{xxxxxxxxxxxxx}", where is a random number xxxxxxxxxxxxx?.  However the destination location is not known.We will develop with the ablity to reconfigure the location and filename | Low | Missing | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 3.7 | The volume of the source data is not known. We assume that each source message file is less than 2MB and we can get many multiple message files throughout the day | Medium | Missing | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 4.6 | The sample data for destination message is not given. Development will proceed with as per dummy test messages created from the schema definitions provided in the spec | Medium | Missing | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| General | String datatype is used for date time fields. Developing using the same type. But please review if the type should be DATE instead | Low | Wrong | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 2.1 and Sec 3.4 | Sec 2.1 indicates Source File is picked up using RTI file adapter but Sec 3.4 says it should be FTP. Developing with the assumption that we are using RTI file adapter for picking source files | Low | Wrong | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 2.1 and Sec 3.4 | Sec 2.1 indicates Source File is dropped to shared location using RTI file adapter using RTI File Adapter. However the Source Platform for Storeline is IBM AIX. We can't use a Windows File protocols to read data from AIX directories unless we go via CIFS or use FTP to pick up the source file | Medium | Wrong | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 4.7 | Sec 4.7 indicates Target File is dropped to shared location using FTP. However the target message is a RMS RIB message. We can't send a message to RIB using FTP. We are assuming this will eventually be done using a JMS adapter and are current configuring the destination to use a RTI File Adapter to drop the file | Medium | Wrong | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| Sec 4.9 | Requires the file to be written to a failed folder location in case of failure. Biztalk will persist messages in the MessageBox and in case of failure they can be resumed from the message box after fixing the issue which cause failure. In the worst case the whole process may need to be restarted using the original source file. However we are not building any mechanism to archive original source files. This should be done as a separate prestep before sending the file to the interface for processing. Please discuss with architect arounf this. | Medium | Unclear | New | Palanivel.P | 15/02/2007 | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 9 | NaN | NaN | NaN | NaN | NaN | NaN |
| High | 0 | In progress | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Medium | 5 | Closed | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Low | 4 | Defect raised | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 9 | Total | 9 | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN | NaN | NaN |
| Missing | 4 | Preparation | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Wrong | 4 | Conduct | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Unclear | 1 | Completion | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 9 | NaN | 0 | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |