---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Katz/Phase II/03 - System Selection & Supply Chain Optimization/03. RFP Responses/JD Edwards Response/Appendix B.pdf.md
tags: [retail, pwc, katz, scm, rfp, 2003]
project: retail
status: unprocessed
---

# Appendix B.pdf

## Source
File: `Brain/raw/.extract/Katz/Phase II/03 - System Selection & Supply Chain Optimization/03. RFP Responses/JD Edwards Response/Appendix B.pdf.md`
Size: 297,595 bytes

## Raw content
Retail Supply Chain Management Systems RFP
A B
PPENDIX
E R D
NTITY ELATIONSHIP IAGRAMS

Accounts Payable
Data Model

| AccountsPayableLedger | A/PPaymentDetail |     |
| --------------------- | ---------------- | --- |
A/PPaymentRegister
| Key Data           | Key Data                |          |
| ------------------ | ----------------------- | -------- |
| CompanyKey   [PK1] | PaymentID   [PK1]  [FK] | Key Data |
PaymentID   [PK1]
| DocVoucherInvoiceE   [PK2] | FileLineIdentifier50   [PK2] |                 |
| -------------------------- | ---------------------------- | --------------- |
| DocumentType   [PK3]       | CompanyKey   [PK3]  [FK]     | Non-Key Data    |
| DocumentPayItem   [PK4]    | DocumentType   [PK5]  [FK]   | DocTypeMatching |
PayItemExtensionNumber   [PK5] DocVoucherInvoiceE   [PK4]  [FK] DocMatchingCheckOr
Non-Key Data DocumentPayItem   [PK6]  [FK] PayeeAddressNumber
GlBankAccount
| DocumentTypeAdjusting | PayItemExtensionNumber   [PK7]  [FK] |                     |
| --------------------- | ------------------------------------ | ------------------- |
| AddressNumber         | Non-Key Data                         | DateMatchingCheckOr |
VoidDateForGLJulian
| PayeeAddressNumber  | DocTypeMatching      | BatchNumber |
| ------------------- | -------------------- | ----------- |
| AddressNumberSentTo | PaymntAmount         |             |
| DateInvoiceJ        | AmtDiscountAvailable | BatchType   |
. DateBatchJulian
| DateServiceCurrency | AmountDiscountTaken  | PaymntAmount |
| ------------------- | -------------------- | ------------ |
| DateDueJulian       | PaymentAmountForeign |              |
CurrencyCodeFrom
| DateDiscountDueJulian    | ForeignDiscountAvail | CurrencyMode  |
| ------------------------ | -------------------- | ------------- |
| DateForGLandVoucherJULIA | ForeignDiscountTaken |               |
| FiscalYear1              | CurrencyMode         | AccountModeGL |
DateValue
| Century              | CurrencyCodeFrom     | PaymentInstrument  |
| -------------------- | -------------------- | ------------------ |
| PeriodNoGeneralLedge | CurrencyConverRateOv |                    |
| Company              | GlClass              | PostStatusPayments |
CustBankAcctNumber
| BatchNumber     | GLPostedCode         | BankTapeReconcilliationR |
| --------------- | -------------------- | ------------------------ |
| BatchType       | .GLPostCodeAlt006    |                          |
| DateBatchJulian | PeriodNoGeneralLedge | TransactionOriginator    |
UserId
| BalancedJournalEntries | FiscalYear1              |     |
| ---------------------- | ------------------------ | --- |
| PayStatusCode          | Century                  |     |
| AmountGross            | FinalPayment             |     |
| AmountOpen             | AddressNumber            |     |
| AmtDiscountAvailable   | Company                  |     |
| AmountDiscountTaken    | CostCenter               |     |
| AmountTaxable          | PurchaseOrder            |     |
| AmountTaxExempt        | NameRemark               |     |
| AmtTax2                | HistoricalCurrencyConver |     |
TaxArea1
TaxExplanationCode1
CurrencyMode
CurrencyCodeFrom
CurrencyConverRateOv
AmountCurrency
AmountForeignOpen
ForeignDiscountAvail
ForeignDiscountTaken
ForeignTaxableAmount
ForeignTaxExempt
ForeignTaxAmount
GlClass
GlBankAccount
GLPostedCode
AccountModeGL
AccountId2
CostCenter
ObjectAccount
Subsidiary
SubledgerType
Subledger
BankTransitShortId
PaymentTermsCode01
VoidFlag
CompanyKeyOriginal
OriginalDocumentType
OriginalDocumentNo
OriginalDocPayItem
CheckRoutingCode
VendorInvoiceNumber
CompanyKeyPurchase
PurchaseOrder
DocumentTypePurchase
LineNumber
OrderSuffix
SequenceNoOperations
Reference1
UnitNo
CostCenter2
NameRemark
FrequencyRecurring
RecurFrequencyOfPaym
APChecksControlField
FinalPayment
Units
UnitOfMeasure
PaymentInstrument
TaxRateArea3Withholding
TaxExplCode3Withhholding
ArApMiscCode1
ArApMiscCode2
ArApMiscCode3
ReportCodeAddBook007
FlagFor1099
DomesticEntryWMultCurrency
IdentifierShortItem

ReceiptsHeaderFile
| CustomerLedgerFile         |                         | A/RCheckDetailFile                  |                   | Key Data                             |
| -------------------------- | ----------------------- | ----------------------------------- | ----------------- | ------------------------------------ |
| Key Data                   |                         | Key Data                            |                   |                                      |
| D o c V o u c h e r I n v  | o i c e E       [P K 1] |                                     |                   | PaymentID   [PK1]                    |
| D o c u m e n t T y p e    |       [ P K 2 ]         | P a y m e n t I D       [ P K       | 1 ]     [ F K ]   | N o n - K e y   D a ta               |
|                            |                         | F i le L i n e I d e n t i f i e r5 | 0       [ P K 2 ] | C k N u m b e r                      |
| C o m p a n y K e y        | [ P K 3 ]               | N o n - K e y   D a t a             |                   | A d d r e s s N u m b er     [ F K ] |
| D o c u m e n t P a y I t  | e m       [ P K 4 ]     | C k N u m b e r                     |                   | P a y o r A d d r e s s N u m b e r  |
| N o n - K e y   D a t a    |                         | D o c V o u c h e r I n v o         | ic e E     [F K ] | D a te M a t c h i n g C h e c k O r |
| AddressNumber  [FK]        |                         | DocumentType  [FK]                  |                   |                                      |
| DateForGLandVoucherJULIA   |                         | CompanyKey  [FK]                    |                   | DateForGLandVoucherJULIA             |
| DateInvoiceJ               |                         |                                     |                   | DateValue                            |
| BatchType                  |                         | DocumentPayItem  [FK]               |                   | GLPostedCode                         |
| BatchNumber                |                         | AddressNumber  [FK]                 |                   | PostStatusReceivables                |
|                            |                         | DocTypeMatching                     |                   | ARPostToCashManagement               |
| DateBatchJulian            |                         | DateMatchingCheckOr                 |                   | CashReceiptLoggedCash                |
| FiscalYear1                |                         | DateForGLandVoucherJULIA            |                   | GlClass                              |
| Century                    |                         | GLPostedCode                        |                   | AccountId                            |
| PeriodNoGeneralLedge       |                         | GlClass                             |                   | Century  [FK]                        |
| Company  [FK]              |                         | AccountId                           |                   | FiscalYear1  [FK]                    |
| GlClass                    |                         | Century                             |                   |                                      |
| AccountId                  |                         | FiscalYear1                         |                   | PeriodNoGeneralLedge  [FK]           |
| AddressNumberParent        |                         |                                     |                   | Company  [FK]                        |
| AddNoAlternatePayee        |                         | PeriodNoGeneralLedge                |                   | BatchType                            |
| PayorAddressNumber         |                         | Company  [FK]                       |                   | BatchNumber                          |
|                            |                         | BatchType                           |                   | DateBatchJulian                      |
| GLPostedCode               |                         | BatchNumber                         |                   | AddressNumberParent                  |
| PostStatusReceivables      |                         | DateBatchJulian                     |                   | AmountCheckAmount                    |
| BalancedJournalEntries     |                         | AddressNumberParent                 |                   | AmountOpen                           |
| PayStatusCode              |                         | RelatedPaymentID                    |                   | CurrencyCodeBase                     |
| AmountGross                |                         | RelatedPaymentLineID                |                   | CurrencyMode                         |
| AmountOpen                 |                         | PaymntAmount                        |                   |                                      |
| AmtDiscountAvailable       |                         | AmtDiscountAvailable                |                   | CurrencyCodeFrom                     |
| AmountDiscountTaken        |                         |                                     |                   | CurrencyConverRateOv                 |
| AmountTaxable              |                         | AmountDiscountTaken                 |                   | CheckAmountForeignOpen               |
| AmountTaxExempt            |                         | AMOUNT_ADJUSTMENTS                  |                   | AmountForeignOpen                    |
|                            |                         | ChargebackAmounts                   |                   | GlBankAccount                        |
| AmtTax2                    |                         | ClaimAmount                         |                   | AccountModeGL                        |
| CurrencyCodeBase           |                         | CurrencyCodeBase                    |                   | CashReceiptTranCode                  |
| CurrencyMode               |                         | CurrencyMode                        |                   | NameRemarkExplanation                |
| CurrencyCodeFrom           |                         | CurrencyCodeFrom                    |                   | GLPostCodeAlt006                     |
| CurrencyConverRateOv       |                         | CurrencyConverRateOv                |                   | PaymentInstrumentA                   |
| DomesticEntryWMultCurrency |                         | PaymentAmountForeign                |                   |                                      |
| AmountCurrency             |                         | ForeignDiscountAvail                |                   | BankTapeReconcilliationR             |
| AmountForeignOpen          |                         |                                     |                   | NameAlpha                            |
| ForeignDiscountAvail       |                         | ForeignDiscountTaken                |                   | DocumentNumberJE                     |
| ForeignDiscountTaken       |                         | ForeignChangedAmount                |                   | DocumentTypeJE                       |
|                            |                         | ForeignChargebackAmounts            |                   | DocumentCompanyJE                    |
| ForeignTaxableAmount       |                         | ForeignClaimAmount                  |                   | VoidDateForGLJulian                  |
| ForeignTaxExempt           |                         | AmountGainLoss                      |                   | VoidReasonCode                       |
| ForeignTaxAmount           |                         | DiscountAccountID                   |                   | ReceiptNSFVoidCode                   |
| TaxArea1                   |                         | ReasnCode                           |                   | DocumentNumberVoidNSFJE              |
| TaxExplanationCode1        |                         | WriteOffAccountID                   |                   | DocumentTypeVoidNSFJE                |
| DateServiceCurrency        |                         | ChargebackReasonCode                |                   |                                      |
| GlBankAccount              |                         | GLOffsetChargebacks                 |                   | DocumentCompanyVoidNSFJE             |
| AccountModeGL              |                         |                                     |                   | VoidNSFBatchType                     |
| AccountId2                 |                         |                                     |                   | BatchNumberVoidNSFReceipt            |
AccountModeGL2
A/RStatisticalSummary
Key Data
AddressNumber   [PK1]
ParentChildRelationshi   [PK2]
|     |     | A/RStatisticalHistory |     | Company   [PK3] |
| --- | --- | --------------------- | --- | --------------- |
|     |     | Key Data              |     | Non-Key Data    |
AddressNumber   [PK1]  [FK]
|     |     | Company   [PK2]  [FK] |     | EndingBalance |
| --- | --- | --------------------- | --- | ------------- |
AmountHighBalance
|                                |     | Non-Key Data          |     | DateHighBalanceJulian             |
| ------------------------------ | --- | --------------------- | --- | --------------------------------- |
|                                |     | C e n tu ry           |     | A m o u n t H ig h C re d itLimit |
| CreditandCashManagement        |     | Fi s ca lY ear1       |     | A ve r a g e D a y sL a te        |
| Key Data                       |     | PeriodNoGeneralLedge  |     | AVDN                              |
| AddressNumber   [PK1]          |     | DateEnding            |     | AmountGross                       |
| ParentChildRelationshi   [PK2] |     | PeriodDays            |     | NumberOfInvoices                  |
| Company   [PK3]                |     | EndingBalance         |     | AmountSales                       |
| Non-Key Data                   |     | DelinquentBalance     |     |                                   |
|                                |     | AmountHighBalance     |     | CreditsEntered                    |
| DateAgeAsOf                    |     |                       |     | AmtDiscountAvailable              |
| AddressNumberParent            |     | DateHighBalanceJulian |     | AmountDelinquencyFees             |
| CreditManager                  |     | DaysSalesOutstanding  |     | ChargebackAmounts                 |
| CollectionManager              |     | DaysCreditGranted     |     | NumberOfChargebacks               |
| AmountOpen                     |     | DelinquentDaysSales   |     | DateFirstInvoiceJulian            |
| NumberOfOpenInvoices           |     | AverageDaysLate       |     | DateLastInvoiceJulian             |
| OpenChargebackAmount           |     | AVDN                  |     | DateLastStatementDate             |
| NumberOfOpenChargebacks        |     | AmountGross           |     | AmtInvoicedThisYr                 |
| AmountDiscountTaken            |     | NumberOfInvoices      |     | AmtInvoicedPriorYr                |
AmountSales
| DiscountEarnable         |     | CreditsEntered        |     | PaymntAmount             |
| ------------------------ | --- | --------------------- | --- | ------------------------ |
| AmountPastDue            |     |                       |     | DiscountEarnable         |
| NumberOfPastDueInvoices  |     | AmtDiscountAvailable  |     | DiscountUnearned         |
| ChargebackPastDue        |     | AmountDelinquencyFees |     | NumberOfInvoicesPaid     |
| DiscountAvailablePastDue |     | ChargebackAmounts     |     | AmountPaidLate           |
| AmountFuture             |     | NumberOfChargebacks   |     | NumberOfInvoicesPaidLate |
| CurrentAmountDue         |     | PaymntAmount          |     | AmountDeductions         |
| NumberOfCurrentInvoices  |     | AmountDiscountTaken   |     | NumberOfDeductions       |
| CurrentChargebackAmount  |     | DiscountEarnable      |     | AmountMinorWriteOff      |
| CurrentDiscountAvailable |     | DiscountUnearned      |     | AmountBadDebt            |
NumberOfInvoicesPaid
| CurrentDiscountEarnable   |     | AmountPaidLate            |     | AmountNSF                |
| ------------------------- | --- | ------------------------- | --- | ------------------------ |
| AmtAgingCategories1       |     |                           |     | NumberOfNSF              |
| AmtAgingCategories2       |     | NumberOfInvoicesPaidLate  |     | DateLastPaid             |
| AmtAgingCategories3       |     | AmountDeductions          |     | AmountLastPaid           |
| AmtAgingCategories4       |     | NumberOfDeductions        |     | NextPeriodToProcess      |
| AmtAgingCategories5       |     | AmountMinorWriteOff       |     | NoSentReminders1         |
| AmtAgingCategories6       |     | AmountTotalActualWriteOff |     | DateLastDunningLetterJul |
| AmtAgingCategories7       |     | AmountBadDebt             |     | CurrencyCodeFrom         |
| AmtOverCreditLimit        |     |                           |     | CreditManager            |
| AmountUnapplied           |     |                           |     | CollectionManager        |
| NumberOfUnappliedReceipts |     |                           |     | UserId                   |
| CreditsEntered            |     |                           |     | ProgramId                |
| NumberOfOpenCredits       |     |                           |     | DateUpdated              |
| CurrencyCodeFrom          |     |                           |     | TimeLastUpdated          |
| OutstandingDraftAmount    |     |                           |     | WorkStationId            |
NumberOfOpenDrafts
AgingMethod
AgingDaysARCurrent
AgingDaysAR001

AddressBookWho'sWho
| Key Data               |                                | AddressBookMaster             |                                         |
| ---------------------- | ------------------------------ | ----------------------------- | --------------------------------------- |
| A d d r e s s N u m b  | e r      [ P K 1 ]     [ F K ] |                               |                                         |
|                        |                                | K e y   D a t a               | A d d r e s s O rganizationStructureMas |
| L i n e N u m b e r ID |       [ P K 2 ]     [ F K ]    | A d d r e s s N umber   [PK1] |                                         |
S e q u e n c e N u m b e r 7 0       [ P K 3 ]   [FK] K e y   D a t a
Non-Key Data ZipCodePostal   [PK2]  [FK] OrganizationTypeStructur   [PK1]
City   [PK3]  [FK]
S e q u e n c e N u mber52Display N o n -K e y  D a ta A d d r e s s N u m b e r P a re n t      [ P K 2 ]
N a m e M a i l i n g A d d r e s s N u m b e r     [P K 3 ]     [ F K ]
C o n t a c tT i t l e A lt e r n at e A dd r essKey N o n -K e y  D a ta
T a x I d
| Remark1        |     | NameAlpha         | SequenceNumber72Display  |
| -------------- | --- | ----------------- | ------------------------ |
| SalutationName |     |                   | BeginningEffectiveDateJu |
| NameAlpha      |     | DescripCompressed | EndingEffectiveDateJulia |
CostCenter
| DescripCompressed |     | StandardIndustryCode | NameRemark   |
| ----------------- | --- | -------------------- | ------------ |
| NameGiven         |     | LanguagePreference   | UserId       |
| NameMiddle        |     |                      | .DateUpdated |
| NameSurname       |     | AddressType1         |              |
CreditMessage
| TypeCode |     | PersonCorporationCode |     |
| -------- | --- | --------------------- | --- |
CategoryCodeWhosWh001
| C a t e g o r y C o d e | W h o s W h 0 0 2 | AddressType2 Addr.essType3 |               |
| ----------------------- | ----------------- | -------------------------- | ------------- |
| C a t e g o r y C o d e | W h o s W h 0 0 3 |                            | AddressbyDate |
A d d r e s s T y p e 4
| CategoryCodeWhosWh004 |     | A d d r e s s T y p e 5 | Key Data                    |
| --------------------- | --- | ----------------------- | --------------------------- |
| CategoryCodeWhosWh005 |     |                         | AddressNumber   [PK1]  [FK] |
CategoryCodeWhosWh006 AddressTypePayables DateBeginningEffective   [PK2]
AddressTypeReceivables
| CategoryCodeWhosWh007 |     | AddTypeCode4Purch      | Non-Key Data             |
| --------------------- | --- | ---------------------- | ------------------------ |
| CategoryCodeWhosWh008 |     | MiscCode3              | EffectiveDateExistence10 |
| CategoryCodeWhosWh009 |     |                        | AddressLine1             |
| CategoryCodeWhosWh010 |     | AddressTypeEmployee    |                          |
|                       |     | SubledgerInactiveCode  | AddressLine2             |
| SecondaryMailingN     | ame | DateBeginningEffective | AddressLine3             |
|                       | .   |                        | AddressLine4             |
AddressNumber1st .
|     |     | AddressNumber2nd | ZipCodePostal |
| --- | --- | ---------------- | ------------- |
|     |     | AddressNumber3rd | City          |
|     |     | AddressNumber4th | CountyAddress |
State
AddressNumber6th
|     |     | AddressNumber5th     | CarrierRoute      |
| --- | --- | -------------------- | ----------------- |
|     |     | ReportCodeAddBook001 | BulkMailingCenter |
Country
| AddressBookContactPhoneNumbers |     | ReportCodeAddBook002 |        |
| ------------------------------ | --- | -------------------- | ------ |
| Key Data                       |     | ReportCodeAddBook003 | UserId |
ReportCodeAddBook004
| AddressNumber   [PK1]  [FK] |     | ReportCodeAddBook005 |     |
| --------------------------- | --- | -------------------- | --- |
LineNumberID   [PK2]
| SequenceNumber70   [PK3] |     | ReportCodeAddBook006 |     |
| ------------------------ | --- | -------------------- | --- |
. ReportCodeAddBook007
| Non-Key Data    |     | ReportCodeAddBook008 | PostalCodeTransactions |
| --------------- | --- | -------------------- | ---------------------- |
| PhoneNumberType |     |                      | Key Data               |
| PhoneAreaCode1  |     | ReportCodeAddBook009 | ZipCodePostal   [PK1]  |
| PhoneNumber     |     | ReportCodeAddBook010 |                        |
|                 |     | ReportCodeAddBook011 | City   [PK2]           |
| UserId          |     | ReportCodeAddBook012 | Non-Key Data           |
ProgramId
|     |     | ReportCodeAddBook013 | State         |
| --- | --- | -------------------- | ------------- |
|     |     | ReportCodeAddBook014 | CountyAddress |
|     |     | ReportCodeAddBook015 | . Country     |
|     |     | ReportCodeAddBook016 | CarrierRoute  |
ReportCodeAddBook017
| CustomerMaster |     | ReportCodeAddBook018 |     |
| -------------- | --- | -------------------- | --- |
ReportCodeAddBook019
| Key Data              |     |                      | SupplierMaster |
| --------------------- | --- | -------------------- | -------------- |
| AddressNumber   [PK1] |     | ReportCodeAddBook020 | Key Data       |
CategoryCodeAddressBook2
Non-Key Data CategoryCodeAddressBk22 AddressNumber   [PK1]  [FK]
| ARClass             |     | CategoryCodeAddressBk23 | ZipCodePostal   [PK2]  [FK] |
| ------------------- | --- | ----------------------- | --------------------------- |
| CostCenterArDefault |     |                         | City   [PK3]  [FK]          |
CategoryCodeAddressBk24
| ObjectAcctsReceivable |     | CategoryCodeAddressBk25 | Non-Key Data |
| --------------------- | --- | ----------------------- | ------------ |
| SubsidiaryAcctsReceiv |     | CategoryCodeAddressBk26 | APClass      |
CompanyKeyARModel
|                |     | CategoryCodeAddressBk27 | CostCenterApDefault |
| -------------- | --- | ----------------------- | ------------------- |
| DocArDefaultJe |     | CategoryCodeAddressBk28 | ObjectAcctsPayable  |
DocTyArDefaultJe CategoryCodeAddressBk29 SubsidiaryAcctsPayable
| CurrencyCodeFrom |     | CategoryCodeAddressBk30 | CompanyKeyAPModel |
| ---------------- | --- | ----------------------- | ----------------- |
TaxArea1 .
|                     |     | GlBankAccount . | DocApDefaultJe   |
| ------------------- | --- | --------------- | ---------------- |
| TaxExplanationCode1 |     | TimeScheduledIn | DocTyApDefaultJe |
| AmountCreditLimit   |     | DateScheduledIn | CurrencyCodeAP   |
ArHoldInvoices
|                   |     | ActionMessageControl | TaxArea2                |
| ----------------- | --- | -------------------- | ----------------------- |
| PaymentTermsAR    |     | NameRemark           | TaxExemptReason2        |
| AltPayor          |     | CertificateTaxExempt | HoldPaymentCode         |
| SendStatementToCP |     | TaxId2               | TaxRateArea3Withholding |
PaymentInstrumentA
|                  |     | Kanjialpha       | TaxExplCode3Withhholding |
| ---------------- | --- | ---------------- | ------------------------ |
| PrintStatementYN |     | UserReservedCode | TaxAuthorityAp           |
| AutoCash         |     | UserReservedDate | PercentWithholding       |
SendInvoiceToCP
| SequenceForLedgrInq |     | UserReservedAmount    | PaymentTermsAP      |
| ------------------- | --- | --------------------- | ------------------- |
|                     |     | UserReservedNumber    | MultipleChecksYN    |
| AutocashAlgorithm   |     | UserReservedReference | PaymentInstrument   |
| StatementCycle      |     | UserId                | AddressNumberSentTo |
BalForwardOpenItem
|                      |     | ProgramId       | MiscCode1           |
| -------------------- | --- | --------------- | ------------------- |
| TempCreditMessage    |     | DateUpdated     | FloatDaysForChecks  |
| CreditCkHandlingCode |     | WorkStationId   | SequenceForLedgrInq |
| DateLastCreditReview |     | TimeLastUpdated | CurrencyCodeAmounts |
DelinquencyLetter
AmountVoucheredYtd
| LastCreditReview |     |     | AmountVoucheredPye |
| ---------------- | --- | --- | ------------------ |
DateRecallforReview
DaysSalesOutstanding

Advanced Price Adjustments
Data Model

| Item/CustomerGroupRelationship                |     |     |                     |     | SalesOrderDetailFile |     |
| --------------------------------------------- | --- | --- | ------------------- | --- | -------------------- | --- |
| Key Data                                      |     |     | FreeGoodsMasterFile |     | Key Data             |     |
| T y p e G r o u p       [ P K 1 ]     [ F K ] |     |     |                     |     |                      |     |
C o d e G r o u p       [ P K 2 ]     [ F K ] P r i c e A d j u s t m e n t S c h e d u l e K e y   D a t a C o m p a n y K e y O r d e r N o     [P K 1 ]
|     | K e y   D | a t a | P r i c e A d j u s t m e | n t T y p e       [ P K 1 ]     [ F K ] | D o c u m e n t O r d e r I | n v o ic e E     [P K 2] |
| --- | --------- | ----- | ------------------------- | --------------------------------------- | --------------------------- | ------------------------ |
G r o u p C a t e g o r y C o d e 0 1       [ P K 3 ] P r i c e A d j u s t m e n t K e y I D       [ P K 2 ] O r d e r T y p e       [ P K 3 ]
G r o u p C a t e g o r y C o d e 0 2       [ P K 4 ] P r i c e A d j u s t m e n t S c h e d u l e N      [ P K 1 ] I d e n t i f i e r 2 n d I t e m       [ P K 3 ] L i n e N u m b e r       [ P K 4 ]
G r o u p C a t e g o r y C o d e 0 3       [ P K 5 ] S e q u e n c e N u m b e r       [ P K 2 ] U n i t O f M e a s u r e A s I n p u t       [ P K 2 8 ]     [F K] N o n - K e y   D a t a
G r o u p C a t e g o r y C o d e 0 4       [ P K 6 ] P r i c e A d j u s t m e n t T y p e       [ P K 5 ]     [F K ] I d e n t i f i e r S h o r t I t e m       [ P K 4 ]    [ F K ] O r d e r S u f f i x
|     | . T y p e G | r o u p       [ P K 3 ]     [ F K ] | A d d r e s s N u m b     | e r       [ P K 5 ]     [ F K ]     | C o s t C e n t e r |     |
| --- | ----------- | ----------------------------------- | ------------------------- | ----------------------------------- | ------------------- | --- |
|     | C o d e G   | r o u p       [ P K 4 ]     [ F K ] |                           |                                     | C o m p a n y       |     |
|     | N o n -K    | e y   D a t a                       | I t e m C u s t o m e r K | e y I D       [ P K 6 ]     [ F K ] |                     |     |
. U s e rR e s e r v e d Code S a l e s D e t a i l G ro u p     [ P K 7 ]   [ F K ] C o m p a n y K e y O ri gi n a l
|     | UserReservedDate |     | S a l e s D e t a i l Va lu      | e 0 1     [ P K 8 ]    [F K] | O ri gi n a lP o S o N u m | b e r |
| --- | ---------------- | --- | -------------------------------- | ---------------------------- | -------------------------- | ----- |
|     |                  |     | SalesDetailValue02   [PK9]  [FK] |                              | OriginalOrderType          |       |
GroupCodeKeyDefinitionTable UserReservedAmount SalesDetailValue03   [PK10]  [FK] OriginalLineNumber
K e y   D a t a U s e r R e s e r v e d N u m b e r C u r r e n c y C o d e F r o m       [ P K 1 1 ]     [ F K ] C o m p a n y K e y R e l a t e d
T y p e G r o u p       [ P K 1 ] U s e r R e s e r v e d R e fe re n ce Q u a n t i t y M i n i m u m       [ P K 1 2 ]     [ F K ] R e l a t e d P o S o N u m b e r
|     | U s e r I d |     | D a t e E x p i r e d J u | l i a n 1       [ P K 1 3 ]     [ F K ] | R e l a t e d O r d e r T y p | e   |
| --- | ----------- | --- | ------------------------- | --------------------------------------- | ----------------------------- | --- |
C o d e G r o u p       [ P K 2 ] Pr o g r a m I d P r ic e A d j u s t m e n t S c h e d u l e N       [ P K 1 4]  [FK] R e l a t e d P o S o L i n e N o
N o n - K e y   D a t a S e q u e n c e N u m b e r       [ P K 1 5 ]     [ F K ] C o n t r a c t N u m b e r D i s t r ibuti
| Description001 |     |     |                          |     | ContractSupplementDistri |     |
| -------------- | --- | --- | ------------------------ | --- | ------------------------ | --- |
| GroupCodeKey01 |     |     | TypeGroup   [PK16]  [FK] |     |                          |     |
GroupCodeKey02 CodeGroup   [PK17]  [FK] ContractBalancesUpdatedY
|     |                       | .   | P ri cin g C a te g o r | y     [P K 1 8 ]   [F K] | A d d r e s s N u m b e r       |     |
| --- | --------------------- | --- | ----------------------- | ------------------------ | ------------------------------- | --- |
|     | PriceAdjustmentDetail |     | Ite m G r ou p 0 1      |   [P K 19 ]    [F K ]    | A d d r e s s N u m b e rShipTo |     |
. Key Data I t e m G r o u p 0 2       [ P K 2 0 ]     [ F K ] A d d re s s N u m b e r P a r e nt
|     |                                   |                                   | I t e m G r o u p 0 3               |   [ P K 2 1 ]     [ F K ] | D a te R e q u e st e d J | u li a n |
| --- | --------------------------------- | --------------------------------- | ----------------------------------- | ------------------------- | ------------------------- | -------- |
|     | PriceAdjustmentType   [PK1]  [FK] |                                   | ItemGroup04   [PK22]  [FK]          |                           | DateTransactionJulian     |          |
|     | IdentifierShortItem   [PK2]       |                                   | GroupCustomerPriceGp   [PK23]  [FK] |                           | PromisedDeliveryDate      |          |
|     | AddressNumber   [PK3]             |                                   | CustomerGroup01   [PK24]  [FK]      |                           | DateOriginalPromisde      |          |
|     | ItemCustomerKeyID   [PK4]         |                                   | CustomerGroup02   [PK25]  [FK]      |                           | ActualDeliveryDate        |          |
|     | SalesDetailGroup   [PK5]          |                                   | CustomerGroup03   [PK26]  [FK]      |                           | DateInvoiceJulian         |          |
|     | S a l e s D e t a                 | i l V a l u e 0 1       [ P K 6 ] |                                     |                           |                           |          |
P r i c e A d j u s t m e n t T y p e S a l e s D e t a i l V a l u e 0 2       [ P K 7 ] C u s t o m e r G r o u p 0 4       [ P K 2 7 ]  [FK] C a n c e l D a t e
K e y   D a t a S a l e s D e t a i l V a l u e 0 3       [ P K 8 ] N o n - K e y   D a t a D t F o r G L A n d V o u c h 1
|     | C u r r e n c y C | o d e F r o m       [ P K 9 ] | I t e m N o S h o r t R | e l a t e d | D a t e R e l e a s e J u l i a | n   |
| --- | ----------------- | ----------------------------- | ----------------------- | ----------- | ------------------------------- | --- |
P r i c e A d j u s t m e n t T y p e       [ PK1] . I d e n t i f i e r 3 r d I t e m D a t e P r i c e E f f e c t i v e D ate
T y p e G r o u p       [ P K 2 ]     [ F K ] U n i t O f M e a s u r e A s I n p u t       [ P K 1 0 ] U n i t s T r a n s a c t i o n Q t y D a t e P r o m i s e d P i c k J u
C o d e G r o u p       [ P K 3 ]     [ F K ] Q u a n t i t y M i n i m u m       [ P K 1 1 ] R e l a t e d P r i c e D a t e P r o m i s e d S h i p J u
N o n - K e y   D a t a D a t e E f f e c t i v e J u l i a n 1       [ P K 2 8 ]     [ F K ] A m o u n t U n i t C o s t R e f e r e n c e 1
P r i c i n g C a t e g o r y D a t e E x p i r e d J u l i a n 1       [ P K 1 2 ] R e f e r e n c e 2 V e n d o r
G r o u p C u s t o m e r P r i c e G p P r i c e A d j u s t m e n t S c h e d u l e N       [ P K 1 3]  [FK] G l C l a s s I d e n t i f i e r S h o r t I t e m
S a l e s D e t a i l G r o u p S e q u e n c e N u m b e r       [ P K 1 4 ]     [ F K ] L i n e T y p e I d e n t i f i e r 2 n d I t e m
P r e f e r n c e T y p e G r o u p       [ P K 1 5 ]     [ F K ] Q u a n t i t y P e r O r d e r e d F re e G o I d e n t i f i e r 3 r d I t e m
|     | C o d e G r o u | p       [ P K 1 6 ]     [ F K ] | P r o c e s s i n g T y p | e F r e e G o o d |     |     |
| --- | --------------- | ------------------------------- | ------------------------- | ----------------- | --- | --- |
L e v e l B r e a k T y p e P r i c i n g C a t e g o r y       [ P K 1 7 ]     [ F K ] F r e e G o o d P r o c e s s C o d e 0 1 L o c a t i o n
G l C l a s s Ite m G r o u p 0 1       [ P K 1 8 ]     [ F K ] F r e e G o o d P r o c e s s C o d e 0 0 2 L o t
| S u b l e d g e r I n f o r m a t i o n |                            |     |     |     | F r o m G r a d e |     |
| --------------------------------------- | -------------------------- | --- | --- | --- | ----------------- | --- |
| AdjustmentControlCode                   | ItemGroup02   [PK19]  [FK] |     |     |     | ThruGrade         |     |
| LineType                                | ItemGroup03   [PK20]  [FK] |     |     | .   | FromPotency       |     |
| ManualDiscount                          | ItemGroup04   [PK21]  [FK] |     |     |     | ThruPotency       |     |
AdjustmentBasedon GroupCustomerPriceGp   [PK22]  [FK] DaysPastExpiration
OrderLevelAdjustmentYN CustomerGroup01   [PK23]  [FK] DescriptionLine1
AdjustmentTaxableYN CustomerGroup02   [PK24]  [FK] DescriptionLine2
PriceAdjustmentCode01 CustomerGroup03   [PK25]  [FK] LineType
CustomerGroup04   [PK26]  [FK]
PriceAdjustmentCode02 PriceAdjustmentVariableN   [PK27]  [FK] StatusCodeNext
| PriceAdjustmentCode03 |                   |     |     |     | StatusCodeLast       |     |
| --------------------- | ----------------- | --- | --- | --- | -------------------- | --- |
| PriceAdjustmentCode04 | Non-Key Data      |     |     |     | CostCenterHeader     |     |
| PriceAdjustmentCode05 | Identifier2ndItem |     |     |     | ItemNumberRelatedKit |     |
UserReservedCode Identifier3rdItem PriceAdjustmentLedgerFile LineNumberKitMaster
| UserReservedDate | BasisCode |     | Key Data |     | ComponentNumber |     |
| ---------------- | --------- | --- | -------- | --- | --------------- | --- |
UserReservedAmount LedgType DocumentOrderInvoiceE   [PK1]  [FK] RelatedKitComponent
UserReservedNumber PriceFormulaName OrderType   [PK2]  [FK] NumbOfCpntPerParent
UserReservedReference FactorValue CompanyKeyOrderNo   [PK3]  [FK] SalesReportingCode1
UserId FreeGoodsYN LineNumber   [PK4]  [FK] SalesReportingCode2
PriceAdjustmentKeyID
|     |                  |     | SequenceNumber   [PK5] |     | SalesReportingCode3 |     |
| --- | ---------------- | --- | ---------------------- | --- | ------------------- | --- |
|     | UserReservedCode |     | Non-Key Data           |     | SalesReportingCode4 |     |
Item/CustomerKeyIDMasterFile UserReservedDate PriceAdjustmentScheduleN SalesReportingCode5
Key Data UserReservedAmount PriceAdjustmentType PurchasingReportCode1
PricingCategory   [PK1] UserReservedNumber IdentifierShortItem PurchasingReportCode2
| ItemGroup01   [PK2] |     |     | AddressNumber     |     | PurchasingReportCode3 |     |
| ------------------- | --- | --- | ----------------- | --- | --------------------- | --- |
| ItemGroup02   [PK3] |     |     | ItemCustomerKeyID |     | PurchasingReportCode4 |     |
| ItemGroup03   [PK4] | .   |     | SalesDetailGroup  |     |                       |     |
ItemGroup04   [PK5]
SalesDetailValue01
| GroupCustomerPriceGp   [PK6] |     |     | SalesDetailValue02   |     |     |     |
| ---------------------------- | --- | --- | -------------------- | --- | --- | --- |
| CustomerGroup01   [PK7]      |     |     | SalesDetailValue03   |     |     |     |
| CustomerGroup02   [PK8]      |     |     | CurrencyCodeFrom     |     |     |     |
| CustomerGroup03   [PK9]      |     |     | UnitOfMeasureAsInput |     |     |     |
| CustomerGroup04   [PK10]     |     |     | QuantityMinimum      |     |     |     |
LedgType
PriceFormulaName
BasisCode
| PriceVariableTable |     |     | F a c t o r V a l u e |     |     |     |
| ------------------ | --- | --- | --------------------- | --- | --- | --- |
K e y   D a t a
| P ri c e A d j u stmentVariableN   [PK1] |     | .   | A d ju s t m e n t B as e  | d on |     |     |
| ---------------------------------------- | --- | --- | -------------------------- | ---- | --- | --- |
| DateEffectiveJulian1   [PK2]             |     |     | A m t P r i ce P e rU n it | 2    |     |     |
AmtForPricePerUnit
| Non-Key Data         |     |     | GlClass               |     |     |     |
| -------------------- | --- | --- | --------------------- | --- | --- | --- |
| CurrencyCodeFrom     |     |     | AdjustmentReasonCode  |     |     |     |
| UnitOfMeasureAsInput |     |     | AdjustmentControlCode |     |     |     |
| AmtPricePerUnit2     |     |     | SubledgerInformation  |     |     |     |
| DateExpiredJulian1   |     |     | ManualDiscount        |     |     |     |
| UserId               |     |     | PriceOverrideCode     |     |     |     |
| ProgramId            |     |     | PriceAdjustmentKeyID  |     |     |     |
WorkStationId


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
