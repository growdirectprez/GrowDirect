## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TOM Integration | NaN | Completion activities | NaN | NaN |
| Document title | TOM Integration Interface Specification Supply Authority Data from IDS to GFO | Document date and/or version | 2007-01-19 00:00:00 | 0.1 | Accountable | NaN | NaN |
| Comments by: | NaN | Review date | NaN | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| 1.2 Background | Reword 2nd sentence of paragraph 1. "This interface contains the details of the all SKU…." | Low | NaN | NaN | NaN | NaN | NaN |
| 1.2 Background | Add a reference to the specification that covers the flow of data from ORMS to IDS. | Low | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Timing / Cutoff constraints need to be established. | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Operational Support Requirements need to be determined. | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | We should change the narrative against Cultural / Global Consideration Requirements to state that "Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration.". | Low | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Reliability and Availability Requirements - we should state the requirements specific to this interface. | Medium | NaN | NaN | NaN | NaN | NaN |
| 3.1 Scope | Rather than write a file to a temporary location I'd like us to configure SSIS to ensure the file being written has an exclusive lock on it. This will avoid the need to rename or copy the file. The exclusive lock will prevent the RTI from picking the file up before the write is completed. ( Note: I want to perform a test on this - AH). | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 3.2 Source Message Schema | Include a reference to the Data Model. | Low | NaN | NaN | NaN | NaN | NaN |
| 3.4 Naming and Configuration | Refers to BizTalk - should be RTI. | Low | NaN | NaN | NaN | NaN | NaN |
| 4.1 Scope | File will be written with exclusive lock thereby preventing RTI from picking the reading a part written file (see also review comment 3.1 Scope). | Medium | NaN | NaN | NaN | NaN | NaN |
| 4.8 Naming and configuration | Specify the number of retry attempts and interval (Period) between them. I suggest 4 attempts at 15 minute intervals. Note that this would take an hour and therefore drives or influences the scheduled start of the SSIS package. | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | (I've moved some narrative from the Description to 2.3 and moved what were essentially non-functionals to a new section: 2.4 Non-Functional Requirements of the End to End Interface) | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 2.4 Non-Functional Requirements of the End to End Interface | We should state The Operational Support Requirement. Suggest: "The successful delivery, failure in the creation of the extract,  and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 8.2 Outstanding Issues)." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "The design of the IMOF is still being worked and will require retro-fitting to the interface." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "Specific IMOF event identifiers are yet to be defined." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "Alert numbers/identifiers are yet to be defined." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| Glossary | Include IMOF in the glossary | Enhancement | NaN | NaN | NaN | NaN | NaN |
| Document Properties | Change the author to your name. | Low | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Quality Review Summary | NaN | NaN | NaN | NaN | NaN | Quality review conclusion | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | The product reviewed has been determined to be: | NaN |
| Critical | 0 | New | 0 | NaN | NaN | Acceptable | NaN |
| High | 0 | In progress | 0 | NaN | NaN | Acceptable given agreed rework | NaN |
| Medium | 5 | Closed | 0 | NaN | NaN | A further review is necessary | NaN |
| Low | 6 | Defect raised | 0 | NaN | NaN | Formal review | NaN |
| Enhancement | 7 | Rejected | 0 | NaN | NaN | Informal review | NaN |
| Total | 18 | Total | 0 | NaN | NaN | General | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Walkthrough | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Code review | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 0 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 0 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 0 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 0 | NaN | 0 | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Abbreviation | Full Name | NaN | NaN | NaN | NaN | NaN | NaN |
| SC | Suprio Chakraborty | NaN | NaN | NaN | NaN | NaN | NaN |
| AB | Andrew Barker | NaN | NaN | NaN | NaN | NaN | NaN |
| SG | Sankar Ganesan | NaN | NaN | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |