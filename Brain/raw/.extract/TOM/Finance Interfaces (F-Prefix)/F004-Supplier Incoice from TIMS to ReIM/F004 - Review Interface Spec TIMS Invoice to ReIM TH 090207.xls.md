## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | Completion activities | NaN | NaN |
| Document title | TOM Integration Interface Specification TIMS Invoice to ReIM | Document date and/or version | 2007-02-08 00:00:00 | ? | Accountable | NaN | NaN |
| Comments by: | Thomas Harper | Review date | 2007-02-09 00:00:00 | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| 3 | This section needs to say that  files in Windows will have CRLF terminating each record and that records in Unix files should be terminated CR - otherwise Unix can'r read the file properly. This affects the schema for the output record. This should also be made clear in the mapping spreadsheet. | Critical | Missing | New | NaN | SG 090207: Agreed. Line delimiter is specified in 4.2 validation section. Going forward all the inteface specification documents will reflect the Line Delimiters | NaN |
| 2 | Keep the swin lanes to show the message flow but this also needs a context dgm showing what is happening at a high level. | High | Missing | New | NaN | SG 090207: Agreed. Context diagram diagram uploaded later part of the day. After sending the mail to Tom | NaN |
| 3.5 | What is this SSIS table doing here? Are we saving the Invoices to the IDS? | Medium | Out of scope | New | NaN | SG 090207: Agreed. Changed to BizTalk | NaN |
| 4.8 | What are the details for the Orchestration | Critical | Missing | New | NaN | SG 090207: Agreed. This section will be updated by Developers | NaN |
| 4.5 | How should the output be encoded?  UTF-8? | Critical | Missing | New | NaN | SG 090207: Agreed. Output character set is mentioned in the mapping document. | NaN |
| 7 | Deployment - The interface should be delivered as an msi together with a Binding file so location changes can be made at installation time. A Release Note will also be needed. | Critical | Missing | New | NaN | SG 090207: Agreed. This will be done by the developers. | NaN |
| 5 | I think you can get rid of this section altogether for this spec | Medium | Wrong | New | NaN | SG 090207: Agreed. This is part of the template. If we remove this the numbering of the other sectiions will get disturbed. | NaN |
| Appendix B | EDI810 is a batch program not a file | Low | Wrong | New | NaN | SG 090207: This is EDI batch process. This has been modified in the Glossary | NaN |
| 3.2 | How is the input file named? This will effect the bindings on the receive | High | Missing | New | NaN | SG 090207: Not yet received from ITS | NaN |
| 4.5 | How is the output file named? | High | Missing | New | NaN | SG 090207: To be confirmed from RMS side. | NaN |
| 4.5 | Target Message Schema - needs a comment to say this is correct  for rel xx.xx of ReIM | Medium | Unclear | New | NaN | SG 090207: This has been specified in the reference document section. | NaN |
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
| Critical | 3 | New | 9 | NaN | NaN | Acceptable | NaN |
| High | 2 | In progress | 0 | NaN | NaN | Acceptable given agreed rework | NaN |
| Medium | 3 | Closed | 0 | NaN | NaN | A further review is necessary | NaN |
| Low | 1 | Defect raised | 0 | NaN | NaN | Formal review | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | Informal review | NaN |
| Total | 9 | Total | 9 | NaN | NaN | General | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Walkthrough | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | Code review | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 5 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 2 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 1 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 1 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 9 | NaN | 0 | NaN | NaN | NaN | NaN |

## Options
| Severity | Type | Status |
| --- | --- | --- |
| Critical | Missing | New |
| High | Wrong | In progress |
| Medium | Unclear | Closed |
| Low | Out of scope | Defect raised |
| Enhancement | Comment | Rejected |