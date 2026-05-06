## Review comments
| Unnamed: 0 | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | Unnamed: 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| Programme name | TOM | Project name | TOM Integration | NaN | Completion activities | NaN | NaN |
| Document title | J0052 - Item-Region Interface Specification | Document date and/or version | 2007-01-19 00:00:00 | 0.1 | Accountable | NaN | NaN |
| Comments by: | Adrian Hinks | Review date | 2007-02-09 00:00:00 | NaN | Communicate | NaN | NaN |
| NaN | NaN | NaN | NaN | NaN | Inform | NaN | NaN |
| Location | Description | Severity | Type | Status | Responsible | Next step | When (d mmm yyyy) |
| 2.2 Requirements for the end-to-end interface | Timing/Cut-off Constraints - we need to establish what time GFO requires this file. Wethen need to establish what time we need to schedule this extract to start in order to complete in time. | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.2 Requirements for the end-to-end interface | Security Requirements- state the following: "The interface executes within a secure private domain.No additional security considerations are required. | Low | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Operational Support Requirements - we should state the requirement as: "The due start time and due delivery time of this interface must be defined as IMOF events.These events will be monitored. Alerts will be generated should the interface fail to start, fail to deliver, or deliver late." | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Operational Support Requirements - we should make a statement about recovery / restart. We need to agree this with the GFO team. As a starting point I would suggest that if the extract stage has run successfully but we are unable to deliver to GFO (for example due to network problems) we should provide a resubmission mechanism for the file that enables us to just retry the delivery step rather than re-run the entire interface. We need to agree with the GFO team to understand how much time can pass prior to a re-run being needed i.e. if the network is down for 18 hours it is more likely that we would need to regenerate the file; where as if the network has only been down for 2 hours, the extract should suffice. | Medium | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Cultural/Global Requirements - We should change the narrative against Cultural / Global Consideration Requirements to state that "Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration.". | Low | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Cultural/Global Consideration Requirements - Remove the word Consideration from this title. | NaN | NaN | NaN | NaN | NaN | NaN |
| 2.3 Requirements for the end-to-end interface | Reliability and Availability Requirements - we should state the requirements specific to this interface. I would expect this to be along the lines of the interface is expected to be available at to produce the interface at the sheduled time. We should also establish from the consumer (i.e. GFO),  the impact of non-delivery of the file. This will enable us to understand the availability and reliability requirement. For example, GFO may be able to operate on the previous days data if we are unable to deliver. | Medium | NaN | NaN | NaN | NaN | NaN |
| 3.1 Scope | Rather than write a file to a temporary location I'd like us to configure SSIS to ensure the file being written has an exclusive lock on it. This will avoid the need to rename or copy the file. The exclusive lock will prevent the RTI from picking the file up before the write is completed. | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 3.1 Scope | We should state the name(s) of the consolidated services that are called in order to produce this interface (I accept this is easier said than done at present). | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 3.2 Source Message Schema | We should list the Consolidated Services called and the Common Forms returned. | Low | NaN | NaN | NaN | NaN | NaN |
| 3.4 Formatting Process (New Section) | This is a new section which should be be added after section 3.3. Here we should state the processing that takes place to combine data from the consolidated services to the file format required. You should also move the mappings currently defined in Section 4.4 into this section. | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 3.5 Target Schema (New Section) | This is a new section which should be be added after section 3.4. Show the target schema in this section i.e. the file format GFO is expecting. | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 3.6 Environment and Security Context (Previously Section 3.4) | We should state: "To be determined once environments and user accounts are clarified". | Low | NaN | NaN | NaN | NaN | NaN |
| 4.1 Scope | As we have moved the mapping into Section 3, this section should now cover the transport of the file from the integration layer to GFO. The Data Validation, Filtering, and Mapping are therefore redundant in the context of this section, in this interface spec. | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 4.2 Message Transport Details (Replaces 4.2 Data Validation) | Move the Message Transport Details from section 4.6 to our renamed section 4.2. | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 4.3 RTI Configuration (New Section) | We should attempt to specify the RTI configuration. There's an template for  RTI configuration in one of the sections in Prasanth's interface spec (J076 I think). Copy from there and we can discuss. | High | NaN | NaN | NaN | NaN | NaN |
| 4.4 Error Handling and Recovery (New Section) | Here we should specify what happens to the file when we are unable to deliver it. We should also describe how the file will be resubmitted after a failed delivery attempt. At a basic level this would involve moving the file from the error location back into the RTI source folder. | High | NaN | NaN | NaN | NaN | NaN |
| 4.5 Environment and Security Context (Previously Section 4.7) | We should state: "To be determined once environments and user accounts are clarified". | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 6 Deliverables (Previously Section 6 Testing Deliverables) | (Refer to change I've made in the document). | NaN | NaN | NaN | NaN | NaN | NaN |
| 7 Deployment | (Refer to change I've made in the document). | NaN | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "The design of the IMOF is still being worked and will require retro-fitting to the interface." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "Specific IMOF event identifiers are yet to be defined." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "Alert numbers/identifiers are yet to be defined." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Record a note to the effect that "Alert numbers/identifiers are yet to be defined." | Enhancement | NaN | NaN | NaN | NaN | NaN |
| 8.2 Outstanding Issues | Security Context yet to be identified. | Enhancement | NaN | NaN | NaN | NaN | NaN |
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
| High | 2 | In progress | 0 | NaN | NaN | Acceptable given agreed rework | NaN |
| Medium | 4 | Closed | 0 | NaN | NaN | A further review is necessary | NaN |
| Low | 5 | Defect raised | 0 | NaN | NaN | Formal review | NaN |
| Enhancement | 13 | Rejected | 0 | NaN | NaN | Informal review | NaN |
| Total | 24 | Total | 0 | NaN | NaN | General | NaN |
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