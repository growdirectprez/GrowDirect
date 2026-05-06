## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | Completion activities | NaN | NaN |
| Document title | TOM Integration Interface Specification Goods Received Note From ORWMS/ORMS to TIMS\n\n | Document date and/or version | 2007-02-15 00:00:00 | 0.1 | Accountable | NaN | NaN |
| Comments by: | D.Rama Krishna | Review date | NaN | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| General | Interface number is F001, not J0026 | Medium | Wrong | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| General | Please specify more information around the purpose and overview of this interface. | Medium | Unclear | Closed | Supriyo | Provided | 2006-12-28 00:00:00 |
| General | Please use the more up-to-date template supplied by Adrian, and ensure that any irrelevent information is removed or marked clearly as a placeholder. | High | Wrong | Closed | Supriyo | Changes carried out in new  template | 2006-12-28 00:00:00 |
| S2.2 Architecture | Clarifiy me about XSD file routing through RTI  Adapter I think its not Possible (RMS to Biz Talk) | High | Wrong | New | Supriyo | Supriyo: The file is not XSD. It will be XML file. So I think it will not be a problem in passing it through RTI Adapter - BizTalk. | NaN |
| S3.3 Message format | Please Provide the Source message format & Hierarchy | High | Missing | New | Supriyo | Supriyo: The Interafce document will be modified accordingly. | NaN |
| S3.5 Naming and Configuration | Why  SSIS Package name included In this context? | High | Wrong | New | Supriyo | SG 12/02/07: Agreed. Corrected to BizTalk |  |
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
| Mapping Document | In the mapping documents the  elements belongs to ReceiptDtl  in the source schema mapping to  VRNHeader elements.Here VRNHeader is nonrepeatable and ReceiptDtl is Repeatable. Can u help me in this regard to. Which index I need to take and map it to the target schema. | High | Missing | New | Supriyo | Supriyo: Here you have to group the rows with same receipt\_no and receipt\_date. | NaN |
| Mapping Document Row 40 | EAN element  doesn’t have any default value to use a tag identifier in Target schema designing but my last interface (D029) have default value to use  tag identifier can you help me  in the same or I can proceed without default   value  for EAN . | Medium | Unclear | New | Supriyo | Supriyo: Leave the field blank | NaN |
| General | The source schema(ReceiptDesc) we have a record called as ReceiptDtl have element Receipt\_date it is of RIBDate datatype. I am assuming the RIBDate datatype is of full date format clarify me whether it is correct or not (yyyymmddhhmmss) | Medium | Missing | New | Supriyo | Supriyo: You are right. | NaN |
| General | The DATETIME element in the Target Shema  have the format YYYYMMDDhhmmss but it is not possible with datetime datatype  in the Target schema.If suppose we use datetime datatype the format will be 2007-02-14T10:53:11.4220458+05:30. | High | Unclear | New | supriyo | Supriyo: Could you please explain this question? I am not clear. | NaN |
| Mapping Document | The Source schema elements length is bigger than Target schema elements what action I have to take.Whether I have to minimize the Source elements equal to  Target elements or the data will come according to the Target elements. | High | Missing | New | supriyo | Supriyo: You have to truncate the field. | NaN |
| General | which record   is the root node for source schema(ReceiptDesc.xsd) | Medium | Missing | New | Supriyo | Supriyo: Please look at the grouping information as well as the XSD message. It is very clear. | NaN |
| mapping Document | if Source schema elements are bigger than target elements Truncations leads to lose of data so I am not agreeing upon Truncation I am assuming that source dataa not having  more data than secified Target element length.if the source data exceeds the length than it will give error | Medium | Unclear | New | Supriyo | NaN | NaN |
| Issues Summary | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 3 | NaN | NaN | NaN | NaN |
| High | 3 | In progress | 0 | NaN | NaN | NaN | NaN |
| Medium | 0 | Closed | 0 | NaN | NaN | NaN | NaN |
| Low | 0 | Defect raised | 0 | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN |
| Total | 3 | Total | 3 | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 1 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 2 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 0 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 3 | NaN | 0 | NaN | NaN | NaN | NaN |

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