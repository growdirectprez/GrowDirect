## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TIMS Integration | NaN | Completion activities | NaN | NaN |
| Document title | IKB Valid Mod Range Information to GPM | Document date and/or version | 22/03/2007 | 0.3 | Accountable | NaN | NaN |
| Comments by: | Upasana | Review date | 22/03/2007 | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| General | Interface number is F001, not J0026 | Medium | Wrong | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| General | Please specify more information around the purpose and overview of this interface. | Medium | Unclear | Closed | Supriyo | Provided | 2006-12-28 00:00:00 |
| General | Please use the more up-to-date template supplied by Adrian, and ensure that any irrelevent information is removed or marked clearly as a placeholder. | High | Wrong | Closed | Supriyo | Changes carried out in new  template | 2006-12-28 00:00:00 |
| Interface specification document | The Data Model of GPM is not known,Shall we make dummy databse/Table to store GPM data. | Medium | Unclear | New | Upasana | NaN | 22/03/2007 |
| NaN |  | NaN | NaN | NaN | NaN | NaN | NaN |
| Mapping document | In IKB table (CSG\_Mods\_Extract) column Store\_No datatype varchar32 is mapped to GPM Holding table STOREID datatype Integer | High | Wrong | New | Upasana | NaN | 22/03/2007 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Requirements for the End-to-End Interface | Since Audit and traceability components are still in the process of development,at this point of time  the ‘placeholder’ in the code / configurations may need rework in future. | Enhancement | Missing | New | Upasana | NaN | 19/02/2007 |
| Mapping document | In IKB table (CSG\_Mods\_Extract) column Module\_Number datatype varchar32 is mapped to GPM Holding table ModNumber datatype Integer | High | Wrong | New | Upasana | NaN | 22/03/2007 |
| S3.1 Scope | Part of this process scope exists already (EDIDLORD.pc), and part does not - it will not be this batch job (EDIDLORD) which does any conversion. As above, please be more specific about what components are involved in this stage. | Medium | Unclear | Closed | Supriyo | NaN | Modified. |
| Mapping document | "Source Field size exceeds the Destination field size, then data will be truncated to fit to Destination field size"………..But what if filed is Primary key or rerquired/Unique key.Truncating the data means loss of data. | High | Unclear | New | Upasana | NaN | 22/03/2007 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S3.1 Scope | Why, and what component, will convert numeric data to packed decimal? | Medium | Unclear | Closed | Supriyo | this part is not required for this interface. Removed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S3.3 | Source Platform / OS is IBM AIX | Low | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S4 | What is contained in this section - it seems to be just placeholders. | Medium | Missing | Closed | Supriyo | This section will not carry much information in case of simple file drop. This section will be brifly defined about the Target location and target file specification.\nWhen filtering of records comes into account like Inventory report interface should not transfer sales data which RMS Inventory file into TIMS. | 2006-12-28 00:00:00 |
| S4.1 | What is the "shipping agent", and why is it involved in this interface? | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S4.6 | What is the "TO" system? | Enhancement | Comment | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S4.7 | Again - why "shipping agent"? Also, what has been written here does not make sense. | Medium | Unclear | Closed | Supriyo | Changed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| S8.1 | Please explain why a particular assumption is relevent - in this case, what is the impact on the interface if this assumption about EOD processing is incorrect? If an assumption has led to a particular decision, please detail. | Medium | Unclear | Closed | Supriyo | Removed | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Appendices | Please ensure they are maintained - especially the change record. | Medium | Comment | Closed | Supriyo | Modified. | 2006-12-28 00:00:00 |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Severity | Total | Status | Total | NaN | NaN | NaN | NaN |
| Critical | 0 | New | 5 | NaN | NaN | NaN | NaN |
| High | 3 | In progress | 0 | NaN | NaN | NaN | NaN |
| Medium | 1 | Closed | 0 | NaN | NaN | NaN | NaN |
| Low | 0 | Defect raised | 0 | NaN | NaN | NaN | NaN |
| Enhancement | 0 | Rejected | 0 | NaN | NaN | NaN | NaN |
| Total | 4 | Total | 5 | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Type | Total | Time | Hours | NaN | NaN | NaN | NaN |
| Missing | 0 | Preparation | NaN | NaN | NaN | NaN | NaN |
| Wrong | 2 | Conduct | NaN | NaN | NaN | NaN | NaN |
| Unclear | 2 | Completion | NaN | NaN | NaN | NaN | NaN |
| Out of scope | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Comment | 0 | NaN | NaN | NaN | NaN | NaN | NaN |
| Total | 4 | NaN | 0 | NaN | NaN | NaN | NaN |

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