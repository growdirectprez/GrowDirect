## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | Completion activities | NaN | NaN |
| Document title | TOM Integration Interface Specification Purchase Order Data from RMS to TIMS | Document date and/or version | 2007-01-03 00:00:00 | 0.3 | Accountable | NaN | NaN |
| Comments by: | Andy Barker | Review date | 2007-01-04 00:00:00 | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| General | Interface number is F001, not J0026 | Medium | Wrong | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| General | Please specify more information around the purpose and overview of this interface. | Medium | Unclear | Closed | Supriyo | Provided | 2006-12-28 00:00:00 |
| General | Please use the more up-to-date template supplied by Adrian, and ensure that any irrelevent information is removed or marked clearly as a placeholder. | High | Wrong | Closed | Supriyo | Changes carried out in new  template | 2006-12-28 00:00:00 |
| Date / Versioning | Please ensure that the version numbering and dates are kept up-to-date. Version 0.1 has already been reviewed - this version should have been 0.2. | High | Wrong | In progress | Supriyo | SG 03/01/07: Changed to 0.3\nAB 04/01/07: List of reviewers is not supposed to be a list of versions - just  a list of the people who are to review, and their positions.\nSG 09/01/07: Modified. | 2007-01-03 00:00:00 |
| General | Please update to match with details in high level interface overview (process steps, technology etc.) provided in email today. | High | Comment | New | Sankar G | SG 09/01/07: The Archecture of this Interface will stay in BizTalk. Changes added in respective locations | 2007-01-09 00:00:00 |
| S1.1 | The interface is for both US and Turkey. | High | Missing | In progress | Supriyo | SG 03/01/07: We have sent the Source Message Difference document. We have mentioned about filed size differences and functionality differences.\nAB 04/01/07: As agreed, this document is supposed to be generic across US and Turkey - with possible different mapping documents for the two deployments.\nSG 09/01/07: Source format specification is different amoung US and Turkey. Only section 1.1, 3.3 and 3.4 will go for change. | 2007-01-03 00:00:00 |
| S1.2 - Background | What do you mean "business specific Store reference data"? | Medium | Unclear | Closed | Supriyo | SC 28/12/06: Corrected\nAB 02/01/07: Still present - please correct the text.\nSG 03/01/07: Corrected. | 2006-12-28 00:00:00 |
| S2.1 Description of the End-to-End Interface | The file does not contain "reference data records" | Medium | Wrong | Closed | Supriyo | Removed | 2006-12-28 00:00:00 |
| S2.1 Description of the End-to-End Interface | It is not clear what components are involved in each part of the end-to-end processing - can it be made more specific? See sheet "PO Data Flow Diagram" for a diagram to include & base description around. | Medium | Unclear | In progress | Supriyo | SC 28/12/06: PO Data Flow Diagram included\nAB 02/01/07: E2E description required around the diagram - please provide.\nSG 03/01/07: Explained in the section 2.1. The picture will explain diagrammatically.\nAB 04/01/07: This will need updating based on the overview spreadsheet.\nSG 09/01/07: The Archecture of this Interface will stay in BizTalk. Changes added | 2006-12-28 00:00:00 |
| S3.1 Scope | Part of this process scope exists already (EDIDLORD.pc), and part does not - it will not be this batch job (EDIDLORD) which does any conversion. As above, please be more specific about what components are involved in this stage. | Medium | Unclear | Closed | Supriyo | Modified. | 2006-12-28 00:00:00 |
| S3.1 Scope | Why is an indicator file needed, if XCOM is used? Please give more details around this indicator file - if it is really required. | High | Unclear | Closed | Supriyo | SG 03/01/07: Yes you are correct. I have changed the text. | 2007-01-03 00:00:00 |
| S3.1 Scope | What is "another pipe delimitted file"? This implies that there is a second pipe-delimitted file - what is this, and how is it different from the target TIMS pipe-delimitted file? | High | Unclear | Closed | Supriyo | SG 03/01/07: Yes you are correct. I have changed the text. | 2007-01-03 00:00:00 |
| S3.1 Scope | Why, and what component, will convert numeric data to packed decimal? | Medium | Unclear | Closed | Supriyo | this part is not required for this interface. Removed | 2006-12-28 00:00:00 |
| S3.2 Source Message Schema | This is available and should be included in this document - specifying V10 and V12 if there are differences. | Medium | Missing | In progress | Supriyo | SC 28/12/06: We are checking it. Consider this document only for US for time-being\nSG 03/01/07: We have send our analysis on differences\nAB 04/01/07: Please include a comment that the Turkey source will be different, and that it will be detailed in the Turkey mapping document.\nSG 09/01/07: Source format specification is different amoung US and Turkey. Only section 1.1, 3.3 and 3.4 will go for change. | 2006-12-28 00:00:00 |
| S3.2 Source Message Schema | The text at the top of this section does not make sense - what is it trying to explain? | Medium | Unclear | Closed | Supriyo | SG 03/01/07: Modified. | 2007-01-03 00:00:00 |
| S3.3 | Source Platform / OS is IBM AIX | Low | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S3.3 | Source physical location has been supplied in email. | Medium | Missing | Closed | Supriyo | SC 28/12/06: E-mail not availalble. Please send it again.\nAB 02/01/07: Email originally sent 19/12/06, resent.\nSG 03/01/07: Email is not specifing the windows path where XCOM will dispatch the file\nAB 4/1/07: XCOM not needed now - see points above about using RTI. | 2006-12-28 00:00:00 |
| S4 | What is contained in this section - it seems to be just placeholders. | Medium | Missing | Closed | Supriyo | This section will not carry much information in case of simple file drop. This section will be brifly defined about the Target location and target file specification.\nWhen filtering of records comes into account like Inventory report interface should not transfer sales data which RMS Inventory file into TIMS. | 2006-12-28 00:00:00 |
| S4.1 | What is the "shipping agent", and why is it involved in this interface? | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4.1 | What file is monitored by Biztalk? Please expand this section. | Medium | Unclear | Closed | Supriyo | SG 03/01/07: Modified. | 2007-01-03 00:00:00 |
| S4.6 | What is the "TO" system? | Enhancement | Comment | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4.1 | RIB is not involved. | High | Wrong | New | NaN | SG 09/01/07: Correccted. | 2007-01-09 00:00:00 |
| S4.6 | What "following message format"? | Medium | Unclear | In progress | Supriyo | SG 03/01/07: will be prepared | 2007-01-04 00:00:00 |
| S4.7 | Again - why "shipping agent"? Also, what has been written here does not make sense. | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| S4.9 | Why will messaging happen through Shipping Agent? | Medium | Unclear | In progress | Supriyo | SG 03/01/07: Changed to BizTalk\nAB 04/01/07: As above, see updates to interface approach.\nSG 09/01/07: Again approach changed back to BizTalk. Necessary changes have been carried out. | 2007-01-03 00:00:00 |
| S5 | Why is this section included - what does it cover? | Medium | Unclear | Closed | Supriyo | SC 28/12/06: This section will be incorporated where the intermediate storage in the interface like inventory report interface.\nAB 02/01/07: I don't understand the above comment - please can you explain? If a section is included as part of the template, but is not relevant for the specific interface, please state clearly why - within that section of the document.\nSG 03/01/07: This section will require when the data is getting stored in IDS (Integration Data Store). And further processed to transform into file for other systems. | 2006-12-28 00:00:00 |
| S8.1 | Please explain why a particular assumption is relevent - in this case, what is the impact on the interface if this assumption about EOD processing is incorrect? If an assumption has led to a particular decision, please detail. | Medium | Unclear | Closed | Supriyo | Removed | 2006-12-28 00:00:00 |
| S8.1 | Why is this assumption included, and what is the impact of it? | Medium | Unclear | In progress | Supriyo | SG 01/01/07: This one of the pre-requist for BizTalk messaging.\nAB 04/01/07: Please explain the inclusion of this assumption, and put that explanation into the document. \nSG 09/01/07: Details added | 2007-01-03 00:00:00 |
| S8.2 | Issues:\n1. Agree - we are waiting on confirmation\n2. These documents are not mentioned in the document. Therefore, without some more context - this issue does not make sense.\n3. Has been emailed - please can you update this.\n4. TBD | Medium | Unclear | Closed | Supriyo | SC 28/12/06: elaborated.\nSG 03/01/07: I agree that we don’t necessarily to know when and where the signature file is getting generated. But only we need to know where the file will get copied. I will remove from the issue list.\nAB 4/1/07: All file locations should be run-time configurable, so not knowing the exact location at this time should not hold up development. | 2006-12-28 00:00:00 |
| Appendices | Please ensure they are maintained - especially the change record. | Medium | Comment | Closed | Supriyo | Modified. | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Quality Review Summary | NaN | NaN | NaN | NaN | NaN | Quality review conclusion | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | The product reviewed has been determined to be: | NaN |
| Critical | 0 | New | 2 | NaN | NaN | Acceptable | NaN |
| High | 7 | In progress | 7 | NaN | NaN | Acceptable given agreed rework | NaN |
| Medium | 21 | Closed | 21 | NaN | NaN | A further review is necessary | NaN |
| Low | 1 | Defect raised | 0 | NaN | NaN | Formal review | NaN |
| Enhancement | 1 | Rejected | 0 | NaN | NaN | Informal review | NaN |
| Total | 30 | Total | 30 | NaN | NaN | General | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Walkthrough | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Code review | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 4 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 5 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 18 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 3 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 30 | NaN | 0 | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Abbreviation | Full Name | NaN | NaN | NaN | NaN | NaN | NaN |
| SC | Suprio Chakraborty | NaN | NaN | NaN | NaN | NaN | NaN |
| AB | Andrew Barker | NaN | NaN | NaN | NaN | NaN | NaN |
| SG | Sankar Ganesan | NaN | NaN | NaN | NaN | NaN | NaN |

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