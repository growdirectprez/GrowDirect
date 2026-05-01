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

C C C D L C A A C S M D D D D C C C C C C C C C C C C C C C C C C C C K N e d d t o o o e o o e e e e a a a a a a a a a a a a a a a a a a a a o a e o v d d s s s s m u s s s s t t t t t t t t t t t t t t t t t t t t d t e e e e e e e e e e e e e e e e e e e e y e n t t t c c c c c r r e n e C C C p e e g g g g g g g g g g g g g g g g g g g g l - r r r r r D O t l K i i i i i a s s y o o o o o o o o o o o o o o o o o o o o A e e e p p p p p a f s s e n r r r r r r r r r r r r r r r r r r r r n n n C t t t t c D y y y y y y y y y y y y y y y y y y y y t i i i i N N y y o o o o t t t c a C C C C C C C C C C C C C C C C C C C C o e e e e u u o n n n n D m r r r t o o o o o o o o o o o o o o o o o o o o m m u 0 0 0 0 a M T a d d d d d d d d d d d d d d d d d d d d p n 0 1 1 1 i y b b l t a [ e e e e e e e e e e e e e e e e e e e e C r t a 1 0 0 0 p P e e s e s C C C C C C C C C C C C C C C C C C C C 0 0 0 e c a K r r s t o o o o o o o o o o o o o o o o o o o o e C J 2 3 4 n s 1 o s s s s s s s s s s s s s s s s s s s s r e o d ] t t t t t t t t t t t t t t t t t t t t b d d C C C C C C C C C C C C C C C C C C C C C A e t t t t t t t t t t t t t t t t t t t t o r 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 n 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 s 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 olid . W C D C L C P P D A A R W W W N N S M Q C D D D D D D D D D U U U U U K N o r a d v t o i o r e e u u r e e e e e e e e e s s s s s u o o s o o o a i e i e o c e m e e e e e y d t s s m s m m s s s m m m s s s e v p r r r r n i y w a n P r c t t o i i i i i i r r r r r r k k k k e u a r r r r r r e C C a d o b b o o o R R R R R e t - a C H C C S e e e e e e u D o H i e K t L g a C e e C C C o s e e l e e e e e c d d d d d d r i i H e W o e e a o o n s e r e z c r r n n h n a a a a s s s s s H H H C C C d O O n u n n t N e a e u t Q o y e e e e e t G t a l p p p o C Q t c r t t o o o a a a e e d O r u f f u e e e r r r r r P i i i u D r E M s C r u u u c c c p p p r r o v v v v v C u r k m r o r r A f e e s i i i a e e e e e m r r r i i i d M E U f C a e a t t t c c c u o s s s s u r y y y l b t d d d d d e [ p t u f c i i i D t a e p S S S p d e a P e S S S t t t f i e D A N R C a h y y y e l i n l e t s T a i c h h h K o h h h r z S S S c i m H a u e o t t i n y i i i i y i i i e a e e 1 i f f f m f f f h h h t m f d t o e t t t o e t t t e e r t r y n ] 1 2 3 i i i e 1 2 3 i u F s e f f f u b e r o c t t t e r H i 1 2 3 n e s n y l s n e t r o c u e rs W C C C K o a a o e s l l r e e y t k C n n C D d d e e a a a n n t r r t a Y M t e e r e o r a R n r [ t e P h s K [ o P 1 u [ K P ] r c 2 K [ e F ] 3 . U K ] n ] its C C U C C C D I S T A t K e y e t a o n a a o o o e p m q p s i l l s c t e e L y e t O t u u a N C n n C i O n m e D c f d d u e e M e i n p a t e a a m n n y T . c e t e n r r M t t a e y b Y M r e e a t a p N O e e r e r s o t A e r o s u a i r n S o d l s O r r [ t t n e h P e a h [ p C o P r g K [ [ I e r P P o e n K 1 [ t [ r P K d F v K P K a ] 1 o e K i i t 8 K 6 1 l t i [ e i o 1 F ] ] c 0 9 n e 1 K ] ] [ [ [ [ P P s E ] F F ] [ [ K K K F K F [ F 1 1 K [ ] K ] [ P K 5 P 3 ] ] K ] ] ] K 1 1 [ [ 4 F F 2 ] K K ] ] ] [ [ F F K K ] ] . S D I S T A P C C C O O T I I C L A D O I T L P P J A C S D D D D B E t t t n K N o e e e i a y y i h e t a u a a d l e n o a a a o e r a a a a r r n p m s a o e i b o p d d p m m m b o q r t y y d g d t c t t t s s t t t t e e p c L o i e e e e e e e e y C n e e e e e o P P c u t c p u r i i I r e N N N k n n C i L n g g g e T R S C d - B O r r R a r a r n m a F e D o o T c K T S O n g i o u u u t o o o s r e e t t p l e o e a t n o l S t i i p R i a i a a i H e y o n n e s a e m u m m r r r i m o n n r n t q m T s o c u e i i i n e r t p i M N n o t t g d y a e e e f n h t o t g a i u t e y n C S b b b f t e r i s e s g e p t r o D t s s s i i f u S M n a H a p e N D O x n C i e e e C i C R a t r o m l o W W W e r m a L e t e A c e t s g r r r y h c m o a i o d o r a o a r S 2 3 o t i h t e t s d l t M o o o n b O u t i d e e n t d t t i n r o S n c a i n h u i e o r r r e n e s d e d o t [ e m p r d n C k k k t o s r P s r n 1 e r i K N J o I p e O O O K C r o J n S K u t i l u t r t R i u K d r r r v i o a l t s 5 o m i d d d l o e a d o i t i ] n t e e e a i i n b o e u c r r r n e n W t 0 0 0 e [ [ i P n P r s 0 0 0 E o g K 1 2 3 K I [ 4 7 [ n P [ P ] P ] s [ [ [ K K P P P t K r 6 3 K K K u 1 ] ] c 8 9 1 ] t ] ] 0 [ ] F [ [ F F K [F K K ] K ] ] ]
CategoryCodeCostCt021 CostCenterAlt [PK4] ParentSegmentNumber [PK17] [FK] ShiftCodeRequested
CategoryCodeCostCt022 UnitOfMeasure [PK5] Non-Key Data ShiftCodeStart
C s C C C C C C T T T d a a a a a a a a a a f x x x t t t t t t t s e e e e e e e A E A d g g g g g g g r n r e e o o o o o o o ti a a r r r r r r r t y y y y y y y y 1 C C C C C C C o o o o o o o d d d d d d d e e e e e e e C C C C C C C o o o o o o o s s s s s s s t t t t t t t C C C C C C C t e e e e e e 0 n n n n n n 2 t t t t t t 3 e e e e e e r r r r r r 2 2 2 2 2 3 5 6 7 8 9 0 C S W W R R R R R R N h o e e e e e e o o o i s s s s s s s f r r n t t o o o o o o k k C C - C C u u u u u u K o e r r r r r r e e e c c c c c c d n n n e e e e e e y e t t t e U U U U U U e e D r r r n n n n n n T a E U i i i i i i y t t t t t t t f t s s s s s s a p f il i 0 0 0 0 0 0 e i c z 0 0 0 0 0 0 i a e 1 2 3 4 5 6 t n io c n y . C C A H Q U D D D c a a o n a a e u t p p l i t t s a i d t e e o s c a a n C R S n T r c c t i i o M t p e r i i t a t t a y d t y y q e r i T n o M M e u t s s r n e s a o e a L s a n d s c i t g s n s e e ti a e a e o d g C c 1 n J t e u Q o io C l n i t n a y o tr n d o e l S L P P P N C M Q R R e h e e e e r u u u o e a i r r r x n n e v f c c c w d t t M L e u C e e e O t S a H e i n n n a o m p b i H o t t t z c d e O O C o e e u h o e r r O u f p a r i u C S n O s m e t r v e t o i s v o r a e u S m a e n n r l t l t a r d p a i a l o a t a l p n i e n v p r d t a e d e a l P P d r l d l a
T T a a x x E D x e p d l u a c n t a io ti n o C n o C d o e d s e 1 1 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 0 0 7 8 S R e u t n u M pL a a ch b i o n r e H A rs c S tu t a d l r
T T T a a a x x x D D D e e e d d d u u u c c c t t t i i i o o o n n n C C C o o o d d d e e e s s s 2 3 4 R R R e e e s s s o o o u u u r r r c c c e e e U U U n n n i i i t t t s s s 0 0 0 0 1 1 9 0 1 R S O e u p t n e u L r p a a L t b i a o o b n r o A S r c h H t r u o in a u k l r a s g A e ctual
T T a a x x D D e e d d u u c c t t i i o o n n C C o o d d e e s s 5 6 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 1 1 2 3 U U n n i i t t s s T Q r u a a n n s t a it c y t C io a n n Q c t e y led
T T T a a a x x x D D D e e e d d d u u u c c c t t t i i i o o o n n n C C C o o o d d d e e e s s s 7 8 9 R R R e e e s s s o o o u u u r r r c c c e e e U U U n n n i i i t t t s s s 0 0 0 1 1 1 4 5 6 U U R n n a i i t t t e s s P Q Q ie u u c a a e n n w t t i i t t o y y r S M k h o i v p e p d e T d
T D a is x t D rib e u d t u e c T t a io x n C C o o d d e e 0 s 0 1 1 0 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 1 1 7 8 U U n n i a tO cc fM tD e ir a e s c u tL re a A b s o I r n H p r u s t
D D i i s s t t r r i i b b u u t t e e T T a a x x C C o o d d e e 0 0 0 0 2 3 . R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 1 2 9 0 U U n n a a c c c c t t S M e a t c u h p i L n a e b H o o r u H r r s s
D D D i i i s s s t t t r r r i i i b b b u u u t t t e e e T T T a a a x x x C C C o o o d d d e e e 0 0 0 0 0 0 4 5 6 R R R e e e s s s o o o u u u r r r c c c e e e U U U n n n i i i t t t s s s 0 0 0 2 2 2 1 2 3 U U U n n n a a a c c c c c c t t t D D D i i i r r r e e e c c c t t t L S M a e a b t c u o h p r A A A m m m t t t
D D i i s s t t r r i i b b u u t t e e T T a a x x C C o o d d e e 0 0 0 0 7 8 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 2 2 4 5 U M n e i s tN sa u g m e b N e o r
D D i i s s t t r r i i b b u u t t e e T T a a x x C C o o d d e e 0 0 0 1 9 0 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 2 2 6 7 P O u b r j c e h c a tA s c in c g o C un o t stCenter
TaxOrDedCompStat01 ResourceUnits028 Subsidiary
T T a a x x O O r r D D e e d d C C o o m m p p S S t t a a t t 0 0 2 3 R R e e s s o o u u r r c c e e U U n n i i t t s s 0 0 2 3 9 0 P C r o im m a p r a y n L y a K s e tV y e R n e d la o t r e N d o
TaxOrDedCompStat04 RelatedPoSoNumber
TaxOrDedCompStat05 RelatedOrderType
TaxOrDedCompStat06 RelatedPoSoLineNo
TaxOrDedCompStat07
TaxOrDedCompStat08
TaxOrDedCompStat09
TaxOrDedCompStat10
PostingEditCostCenter
AllocaSummarizaMeth
InvstmtSummarizaMeth
GlBankAccount
AllocationLevel
LaborLoadingMethod
LaborLoadingFactor
GlObjectAcctLabor
GlObjctAcctLaborPrem
GlObjAcctLaborBurden
SubsidiaryBurdnCstCde
UnitsTotal
SubledgerInactiveCode
Supervisor
ContractType1
CertifiedJob
CostCenterSubsequent
BillingTypeCostCenter
PercentComplete
PerCompleteAggregate
AmtCostToCompleteOb
IntComputationCodeAr
IntComputationCodeRev
DatePlannedStartJ

.
C o s t C e n t e r M a s te r C r o s s S e g m e n t E d i t i n g R u l e s C o n f i g u r e d I t e m S e g m e n t s S h o p F l o o r C o n t r o l R o u t i n g I n s t r u c t
| N o n - K e y   D a t a | K e y   D a t a | K e y   D a t a | K e y   D a t a |
| ----------------------- | --------------- | --------------- | --------------- |
C o s t C e n t e r T y p e I t e m N u m b e r S h o r t K i t       [ P K 1 ]   [ F K ] I t e m N u m b e r S h o r t K i t      [ P K 1 ] I t e m N u m b e r S h o r t K i t       [ P K 7 ]     [ F K ]
D e s c r i p C o m p r e s s e d C o s t C e n t e r       [ P K 2 ]     [ F K ] C o s t C e n t e r       [ P K 2 ] S e q u e n c e N o O p e r a t i o n s       [ P K 3 ]
L C e o v m e p l O a f n D y e t a i l C c C o de A A t t o o R S e u q l e N N u u m m b b e e r r             [ [ P P K K 4 3 ] ] P a r e n t S e g m e n t N u m b e r     [ P K3] T y p e O p e r a t i o n C o d e       [ P K 4 ]
A d d r e s s N u m b e r P a r e n t S e g m e n t N u m b e r      [ P K 5 ]   [ FK] N o n - K e y   D a t a A to L i n e T y p e       [ P K 5 ]     [ F K ]
A d d r e s s N u m b e r J o b A r N o n - K e y   D a t a I d e n t i f i e r 2 n d I t e m P a r e n t S e g m e n t N u m b e r       [ P K 6 ]     [ F K ]
C o u n t y I d e n t i f i e r 2 n d I t e m I d e n t i f i e r 3 r d I t e m C o s t C e n t e r       [ P K 8 ]     [ F K ]
S t a t e I d e n t i f i e r 3 r d I t e m E f f e c t i v e F r o m D a t e A t o R u l e N u m b e r       [ P K 9 ]     [ F K ]
M o d e l A c c o u n t s a n d C o n s o l id E f f e c t i v e F r o m D a t e E f f e c t i v e T h r u D a t e A t o S e q N u m b e r       [ P K 1 0 ]     [ F K ]
D e s c r i p t i o n 0 0 1 E f f e c t i v e T h r u D a t e D e s c r i p t i o n L i n e 1 C o m p a n y K e y O r d e r N o       [ P K 1 1 ]     [ F K ]
| D e s c r i p t i o n 0 1 0 0 2 | A T O S e g m e n t P r o d u c t F a m ilyN | D R a e t q a u I t i r e e m d T o B e | N o n - K e y   D a t a |
| ------------------------------- | -------------------------------------------- | --------------------------------------- | ----------------------- |
| D e s c r i p t i o n 0 1 0 0 3 | C o s t C e n t e r H e a d e r              | S y s t e m C o d e                     | O r d e r T y p e       |
| D e s c r i p t i o n 0 1 0 0 4 | R e l a t i o n s h i p                      | U s e r D e f i n e d C o d e s         | O r d e r S u f f i x   |
C C a a t t e e g g o o r r y y C C o o d d e e C C o o s s t t C C t t 0 0 0 0 1 2 S e l e c t i o n V a l u e A t o I f V a l u e F o r E n t r y D e f a u l t T I t e y p m e N R u o m u b t i n e g r 2 n d K i t
C a t e g o r y C o d e C o s t C t 0 0 3 A n d O r S e l e c t i o n L o w e r A l l o w e d V a l u e D d I t e m N u m b e r 3 r d K i t
| C a t e g o r y C o d e C o s t C t 0 0 4 | A n d O r S e l e c t i o n B e g i n n in g                                | A l l o w e d V a l u e U p p e r | C o s t C e n t e r A l t   |
| ----------------------------------------- | --------------------------------------------------------------------------- | --------------------------------- | --------------------------- |
| C a t e g o r y C o d e C o s t C t 0 0 5 | A C n h d i l d O S r S e g e m l e e c t n i o t N n u E m n d b i e n r g | . N u m e r i c Y N               | L i n e I d e n t i f i e r |
C a t e g o r y C o d e C o s t C t 0 0 6 S e l e c t i o n V a l u e A t o T h e n D a t a I t e m S i z e A u t o L o a d D e s c r i p t i o n
C a t e g o r y C o d e C o s t C t 0 0 7 R e q u i r e d T o B e D a t a D i s p l a y D e c i m a l s D e s c r i p t i o n L i n e 1
C a t e g o r y C o d e C o s t C t 0 0 8 S e g m e n t D e l i m i t e r A d d r e s s N u m b e r O p e r a t i o n S t a t u s C o d e W o
| C a t e g o r y C o d e C o s t C t 0 0 9 | R e l a t i o n s h i p V a l u e | A D T i s O p l S a a y I v t e e S m e N g u m m e b n e t r | I n s p e c t i o n C o d e |
| ----------------------------------------- | --------------------------------- | ------------------------------------------------------------- | --------------------------- |
C a t e g o r y C o d e C o s t C t 0 1 0 . C u s t o m M e s s a g e T e x t S t r i n g o r C u s t o m F o r m a t T i m e B a s i s C o d e
C a t e g o r y C o d e C o s t C t 0 1 1 A t o L i n e T y p e S p a c e s B e f o r e S e g m e n t I n f o r L a b o r O r M a c h i n e
| C C a a t t e e g g o o r r y y C C o o d d e e C C o o s s t t C C t t 0 0 1 1 2 3 | M e s s a g e N o                     | A T O P r i n t S e g m e n t N u m b e r       | P P a a y y P P o o i i n n t t C S t o a d t u e s |
| ----------------------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| C a t e g o r y C o d e C o s t C t 0 1 4                                           | I d e n t i f i e r S h o r t I t e m | A T O P r i n t S e g m e n t D e s c r i p t i | J o b C a t e g o r y                               |
C a t e g o r y C o d e C o s t C t 0 1 5 C U o s e s t r C R e e n s e t e r r v A e l d t C o d e A T O P r i n t S e g m e n t V a l u e A d d r e s s N u m b e r
| C a t e g o r y C o d e C o s t C t 0 1 6 | U s e r R e s e r v e d D a t e | A T O P r i n t S e g m e n t V a l u e D e s c | C r i t i c a l R a t i o |
| ----------------------------------------- | ------------------------------- | ----------------------------------------------- | ------------------------- |
C a t e g o r y C o d e C o s t C t 0 1 7 U s e . r R e s e r v e d A m o u n t S p a c e s A f t e r S e g m e n t I n f o r m S l a c k T i m e R a t i o
C a t e g o r y C o d e C o s t C t 0 1 8 U s e r R e s e r v e d N u m b e r R e t u r n a n d S t a r t N e w L i n e D a t e T r a n s a c t i o n J u l i a n
C a t e g o r y C o d e C o s t C t 0 1 9 U s e r R e s e r v e d R e f e r e n c e D e r i v e d C a l c u l a t i o n R o u n d D a t e R e q u e s t e d J u l i a n
| C a t e g o r y C o d e C o s t C t 0 2 0 | P r o g r a m I d | U U p s e d r a R t e e C s e a r t v e e g d o C r y o C d o e d e | D a t e S t a r t |
| ----------------------------------------- | ----------------- | ------------------------------------------------------------------- | ----------------- |
C a t e g o r y C o d e C o s t C t 0 2 1 W o r k S t a t i o n I d U s e r R e s e r v e d D a t e D a t e C o m p l e t i o n
C a t e g o r y C o d e C o s t C t 0 2 2 U s e r I d U s e r R e s e r v e d A m o u n t B e g i n n i n g H h M m S s
C s d a f t s e d g o r y C o d e C o s t C t 0 2 3 D a t e U p d a t e d U s e r R e s e r v e d N u m b e r E S n h d i f t i n C g o H d h e M R e m q S u s e s t e d
| C a t e g o r y C o d e C o s t C e n t e r 2 5 | T i m e O f D a y       | U s e r R e s e r v e d R e f e r e n c e | S h i f t C o d e S t a r t |
| ----------------------------------------------- | ----------------------- | ----------------------------------------- | --------------------------- |
| CategoryCodeCostCenter26                        |                         | UserId                                    | ShiftCodeCompleted          |
| CategoryCodeCostCenter27                        |                         | ProgramId                                 | LeadtimeOverlap             |
| CategoryCodeCostCenter28                        |                         | WorkStationId                             | PercentOfOverlap            |
| CategoryCodeCostCenter29                        |                         | DateUpdated                               | PercentOperationalPl        |
| CategoryCodeCostCenter30                        |                         | TimeOfDay                                 | PercentCumulativePla        |
| TaxArea                                         |                         |                                           | NextOperation               |
| TaxEntity                                       | ItemMaster              |                                           | CrewSize                    |
| TaxArea1                                        | N o n - K e y   D a t a |                                           | MoveHours                   |
T T a a x x E D x e p d l u a c n t a io ti n o C n o C d o e d s e 1 1 Id e n t if ie r 2 n d It e m . Q Ru u n e M ue a H ch o i u n r e s Standard
| TaxDeductionCodes2 | Identifier3rdItem |     | RunLaborStandard  |
| ------------------ | ----------------- | --- | ----------------- |
| TaxDeductionCodes3 | DescriptionLine1  |     | SetupLaborHrsStdr |
| TaxDeductionCodes4 | DescriptionLine2  |     | RunMachineActual  |
| TaxDeductionCodes5 | SearchText        |     | RunLaborActual    |
T a x D e d u c t i o n C o d e s 6 S e a r c hT e x t C o m p re s s ed S e t u p L a b o r H o u r s A ctual
T a x D e d u c t i o n C o d e s 7 S a le s R e p o r tin g C o d e 1 AssemblyInclusionsRules O p e r a ti o n S h r in k a g e
TaxDeductionCodes8 SalesReportingCode2 Key Data UnitsTransactionQty
TaxDeductionCodes9 SalesReportingCode3 CostCenter   [PK1]  [FK] ItemNumberShortKit   [PK2]  [FK] UnitsQuantityCanceled
TaxDeductionCodes10 DistributeTaxCode001 SalesReportingCode4 SalesReportingCode5 AtoLineType   [PK3] UnitsQuantityShipped UnitsQuantityMovedT
| DistributeTaxCode002 | SalesReportingCode6 | AtoRuleNumber   [PK4] | RatePiecework |
| -------------------- | ------------------- | --------------------- | ------------- |
DistributeTaxCode003 SalesReportingCode7 AtoSeqNumber   [PK5] UnitOfMeasureAsInput
DistributeTaxCode004 SalesReportingCode8 ParentSegmentNumber   [PK11]  [FK] UnacctDirectLaborHrs
DistributeTaxCode005 SalesReportingCode9 CompanyKeyOrderNo   [PK6] UnacctSetupLaborHrs
DistributeTaxCode006 SalesReportingCode10 Non-Key Data UnacctMachineHours
DistributeTaxCode007 PurchasingReportCode1 Identifier2ndItem UnacctDirectLaborAmt
DistributeTaxCode008 PurchasingReportCode2 Identifier3rdItem UnacctDirectSetupAmt
| DistributeTaxCode009                  | PurchasingReportCode3                       | IdentifierShortItem                    |     |
| ------------------------------------- | ------------------------------------------- | -------------------------------------- | --- |
| DistributeTaxCode010                  | PurchasingReportCode4 PurchasingReportCode5 | BranchComponent                        |     |
| TaxOrDedCompStat01 TaxOrDedCompStat02 | PurchReportingCode6                         | DescriptionLine1                       |     |
| TaxOrDedCompStat03                    | PurchReportingCode7                         | AndOrSelection AndOrSelectionBeginning |     |
| TaxOrDedCompStat04                    | PurchReportingCode8                         | AndOrSelectionEnding                   |     |
| TaxOrDedCompStat05                    | PurchReportingCode9                         | ATOSegmentProductFamilyN               |     |
| TaxOrDedCompStat06                    | PurchReportingCode10                        | CostCenterHeader                       |     |
| TaxOrDedCompStat07                    | CommodityCode                               | Relationship                           |     |
T a x O r D e d C o m p S t a t 0 8 P r o d u c t G r o u p F rom S e l e c t i o n V a l u e A to If S a le s O rd erDetailFile
| T a x O r D e d C o m p S t a t 0 9 | D is p a t c h G rp        | S e q u e n c e N o O p e ra tions | K e y  D a ta |
| ----------------------------------- | -------------------------- | ---------------------------------- | ------------- |
| T a x O r D e d C o m p S t a t 1 0 | P r ic in g C a t e g o ry | U n i tP r i c e E n t e r e d     |               |
PostingEditCostCenter RepriceBasketPriceCat OrderRepriceCategory AmountMemoCost1 CompanyKeyOrderNo   [PK1] DocumentOrderInvoiceE   [PK2]
AllocaSummarizaMeth InvstmtSummarizaMeth Buyer LineType OrderType   [PK3]
GlBankAccount DrawingNumber MessageNo QtyRequiredStandard LineNumber   [PK4]
| AllocationLevel    | RevisionNumber        | UnitOfMeasure      | Non-Key Data |
| ------------------ | --------------------- | ------------------ | ------------ |
| LaborLoadingMethod | DrawingSize           | FixedOrVariableQty | OrderSuffix  |
| LaborLoadingFactor | VolumeCubicDimensions | IssueTypeCode      | CostCenter   |
| GlObjectAcctLabor  | Carrier               | LeadtimeOffsetDays | Company      |
GlObjctAcctLaborPrem PreferCarrierPurchasin CompanyKeyOriginal
GlObjAcctLaborBurden ShippingConditionsCode OriginalPoSoNumber
| SubsidiaryBurdnCstCde            |     |                             | OriginalOrderType                  |
| -------------------------------- | --- | --------------------------- | ---------------------------------- |
| UnitsTotal                       |     |                             | OriginalLineNumber                 |
| SubledgerInactiveCode Supervisor |     |                             | CompanyKeyRelated                  |
| ContractType1                    |     |                             | RelatedPoSoNumber RelatedOrderType |
| CertifiedJob                     |     |                             | RelatedPoSoLineNo                  |
| CostCenterSubsequent             |     |                             | ContractNumberDistributi           |
| BillingTypeCostCenter            |     |                             | ContractSupplementDistri           |
| PercentComplete                  |     |                             | ContractBalancesUpdatedY           |
| PerCompleteAggregate             |     | ConfiguredStringHistoryFile | AddressNumber                      |
| AmtCostToCompleteOb              |     | Key Data                    | AddressNumberShipTo                |
IntComputationCodeAr ConfiguredString   [PK1] AddressNumberParent
IntComputationCodeRev D a t e P l a n n e d S t a r t J Non-Key Data DateRequestedJulian
D a t e A c t u a l S t a r t J I t e m N u m b e r S h o r t K i t D P r a o t e m T i s r a e n d s D a e c l i t v i o e n r y J D u l a i a t e n
D a t e P l a n n e d C o m p l e t e J C o s t C e n t e r D a t e O r i g i n a l P r o m i s d e
D a t e A c t u a l C o m p l e t e J L o c a t i o n . A c t u a l D e l i v e r y D a t e
D a t e O t h e r 5 J L C o o t n f i g u r e d S t r i n g I D D a t e I n v o i c e J u l i a n
| D a t e O t h e r 6 J |     | A T O S e g m e n t P r o d u c t F a milyN | C a n c e l D a t e |
| --------------------- | --- | ------------------------------------------- | ------------------- |
D t e F i n a l P a y m n t J u l i a n C o m p a n y K e y O r d e r N o D t F o r G L A n d V o u c h 1
A m t C o s t A t C o m p l e t i o n D o c u m e n t O r d e r I n v o i c e E D a t e R e l e a s e J u l i a n
A m t P r o f i t A t C o m p l e t i o n O r d e r T y p e D a t e P r i c e E f f e c t i v e D a te
E q u a l E m p l o y m e n t O p p o rt L i n e N u m b e r D a t e P r o m i s e d P i c k J u
E U q s e u r i p I d m e n t R a t e C o d e A d d r e s s N u m b e r D a t e P r o m i s e d S h i p J u
P r o g r a m I d I d e n t i f i e r S h o r t I t e m R R e e f f e e r r e e n n c c e e 1 2 V e n d o r
D a t e U p d a t e d B r a n c h C o m p o n e n t I d e n t i f i e r S h o r t I t e m
| W o r k S t a t i o n I d    |     | D a t e R e q u e s t e d J u l i a n                         | I d e n t i f i e r 2 n d I t e m |
| ---------------------------- | --- | ------------------------------------------------------------- | --------------------------------- |
| Ti m e L a s t U p d a t e d |     | A U m n i o t P u r n i c t M e E e n m t e o r C e o d s t 1 | I d e n t i f i e r 3 r d I t e m |
UserId
ProgramId
WorkStationId
DateUpdated
TimeOfDay
.

PPATMessageDetailFile
| Key Data                     | AddressBookMaster     |                 |     |
| ---------------------------- | --------------------- | --------------- | --- |
| KeyValueSerialNumber   [PK1] | Key Data              |                 |     |
| AddressNumber   [PK2]        | AddressNumber   [PK1] | JDEMMailFilters |     |
Key Data
| Non-Key Data             | Non-Key Data         |                             |     |
| ------------------------ | -------------------- | --------------------------- | --- |
| NameAlpha                | AlternateAddressKey  | AddressNumberParent   [PK1] |     |
| MailBoxDesignator        | TaxId                | AddressNumber   [PK2]       |     |
|                          | NameAlpha            | Non-Key Data                |     |
| DateTickler              |                      | MailBoxDesignator           |     |
| CommandFlagPPAT          | DescripCompressed    |                             |     |
| StatusElectronicMailMess | CostCenter           |                             |     |
| SequenceNumber52Display  | StandardIndustryCode |                             |     |
| ActionMessageControl     | LanguagePreference   |                             |     |
AddressType1
MiscCode3
| TimeLastUpdated | CreditMessage | .   |     |
| --------------- | ------------- | --- | --- |
PersonCorporationCode
AddressType2
AddressType3
. AddressType4
AddressType5
AddressTypePayables
AddressTypeReceivables
AddTypeCode4Purch
| PPATMessageControlFile | MiscCode3 |     |     |
| ---------------------- | --------- | --- | --- |
AddressTypeEmployee
| Key Data                     | SubledgerInactiveCode  |     |     |
| ---------------------------- | ---------------------- | --- | --- |
| KeyValueSerialNumber   [PK1] | DateBeginningEffective |     |     |
Non-Key Data
AddressNumber1st
| AddressNumber   | AddressNumber2nd |     |     |
| --------------- | ---------------- | --- | --- |
| NameAlpha       | AddressNumber3rd |     | .   |
| SntFrm          | AddressNumber4th |     |     |
| CallFromCompany | AddressNumber6th |     |     |
TimeLogLedgerFile
| AallFromPhone     | AddressNumber5th     |     | Key Data                 |
| ----------------- | -------------------- | --- | ------------------------ |
| MailBoxDesignator | ReportCodeAddBook001 |     |                          |
| DateTickler       | ReportCodeAddBook002 |     | AddressNumber   [PK1]    |
| DateUpdated       | ReportCodeAddBook003 |     | DateScheduledOut   [PK2] |
TimeScheduledOut   [PK3]
| TimeLastUpdated         | ReportCodeAddBook004 |     | Non-Key Data   |
| ----------------------- | -------------------- | --- | -------------- |
| WorkStationId           | ReportCodeAddBook005 |     |                |
| SequenceNumber52Display | ReportCodeAddBook006 |     | NameAlpha      |
| PPATBriefMassage        | ReportCodeAddBook007 |     | TypePpatAction |
| AddressNumberParent     | ReportCodeAddBook008 |     | NameRemark     |
DateScheduledIn
| CategoryCodePPAT01       | ReportCodeAddBook009     |     |                 |
| ------------------------ | ------------------------ | --- | --------------- |
| CategoryCodePPAT02       | ReportCodeAddBook010     |     | TimeScheduledIn |
| MessageType1             | ReportCodeAddBook011     |     | TimeEntered     |
| MessageType2             | ReportCodeAddBook012     |     | UserId          |
| MessageType3             | ReportCodeAddBook013     |     | ProgramId       |
| UserId                   | ReportCodeAddBook014     |     | DateUpdated     |
| ProgramId                | ReportCodeAddBook015     |     | WorkStationId   |
| ActionMessageControl     | ReportCodeAddBook016     |     | TimeLastUpdated |
| TimeEntered              | ReportCodeAddBook017     |     |                 |
| StatusElectronicMailMess | ReportCodeAddBook018     |     |                 |
| PhoneExtension           | ReportCodeAddBook019     |     |                 |
| BaseMemberName           | ReportCodeAddBook020     |     |                 |
| SystemCode               | CategoryCodeAddressBook2 |     |                 |
| DocumentOrderInvoiceE    | CategoryCodeAddressBk22  |     |                 |
| OrderSuffix              | CategoryCodeAddressBk23  |     |                 |
| OrderType                | CategoryCodeAddressBk24  |     |                 |
| LineNumber               | CategoryCodeAddressBk25  |     |                 |
CompanyKeyOrderNo CategoryCodeAddressBk26 WorkflowMessageSecurity
Key Data
| TemplateID | CategoryCodeAddressBk27 |     |                       |
| ---------- | ----------------------- | --- | --------------------- |
| MiscCode3  | CategoryCodeAddressBk28 |     | AddressNumber   [PK1] |
LevelIndented CategoryCodeAddressBk29 . WorkflowGroup   [PK2]
KeyValueSerialNumber CategoryCodeAddressBk30 WorkflowUser   [PK3]
| Version                    | GlBankAccount        |     | MailBoxDesignator   [PK4] |
| -------------------------- | -------------------- | --- | ------------------------- |
| TemplateSubstitutionValues | TimeScheduledIn      |     | Non-Key Data              |
| ApplicationID              | DateScheduledIn      |     | UserId                    |
| FormID                     | ActionMessageControl |     | WorkStationId             |
|                            | NameRemark           |     | DateUpdated               |
|                            | CertificateTaxExempt |     | TimeOfDay                 |
|                            | TaxId2               |     | ProgramId                 |
Kanjialpha
UserReservedCode
UserReservedDate
.
UserReservedAmount
UserReservedNumber
UserReservedReference
UserId
| JDEMMultiLevelMessage        | ProgramId       |     |     |
| ---------------------------- | --------------- | --- | --- |
| Key Data                     | DateUpdated     |     |     |
| KeyValueSerialNumber   [PK1] | WorkStationId   |     |     |
| KeyValueSerialNumber   [PK2] | TimeLastUpdated |     |     |
Non-Key Data
PPATBriefMassage
DateTickler
LevelIndented
AddressNumber
AddressNumberParent
TemplateSubstitutionValues
TemplateID
FormID
ApplicationID
Version
FunctionName
SourceLineNumber

EmployeeMasterInformation
Key Data
| HRHistoryConstants | AddressNumber   [PK1]  [FK] |     |     |
| ------------------ | --------------------------- | --- | --- |
CostCenterHome   [PK12]  [FK]
| Key Data                               | P a y Ty p e H S P        | [P K 3 ]     [ F K ]  |                          |
| -------------------------------------- | ------------------------- | --------------------- | ------------------------ |
| D a ta F i le L ib r ar y      [P K 1] | Jo b C a te g o ry      [ | P K 1 3 ]     [ F K ] | Select Data for Tracking |
H rS u b S y s te m      [ P K 2]
| Non-Key Data | JobStep   [PK7]  [FK] |     |     |
| ------------ | --------------------- | --- | --- |
ChangeReason   [PK11]  [FK]
| EmployeeHistory     | DatePayStops   [PK14]  [FK]      |     |     |
| ------------------- | -------------------------------- | --- | --- |
| EmpHistoryPrompt001 | PayGrade   [PK4]  [FK]           |     |     |
| EmpHistoryPrompt002 | SalaryDataLocality   [PK5]  [FK] |     |     |
| EmpHistoryPrompt003 | DateEffective   [PK2]  [FK]      |     |     |
AutoReqPrompt
| PositionControlPrompt | JobType   [PK6]  [FK] |     |     |
| --------------------- | --------------------- | --- | --- |
DataItem   [PK8]  [FK]
| EmpHistoryPrompt006                   | TurnoverData   [PK9]  [FK]     |                        |     |
| ------------------------------------- | ------------------------------ | ---------------------- | --- |
| EmpHistoryPrompt007                   | DateEffectiveOn   [PK10]  [FK] |                        |     |
| EmpHistoryPrompt008                   | FileName   [PK15]  [FK]        |                        |     |
| E m p H i s t o r y P r o m p t 0 0 9 | S e q u e n c e N u m          | berView   [PK16]  [FK] |     |
E m p H i s t o r y P r o m p t 0 1 0 E m p l o y e e TurnoverAnalysis
| U se r Id | N o n - K e y   D a ta |     | K e y   D a t a |
| --------- | ---------------------- | --- | --------------- |
NameAlpha
| ProgramId     | SocialSecurityNumber |     | DataItem   [PK1]  [FK]     |
| ------------- | -------------------- | --- | -------------------------- |
| DateUpdated   | EmployeeNumberThird  |     | TurnoverData   [PK2]  [FK] |
| WorkStationId |                      |     | ChangeReason   [PK3]  [FK] |
FlexCreditsPerDollar SexMaleFemale DateEffectiveOn   [PK4]  [FK]
UseAssignmentWindow MaritalStatusTax AddressNumber   [PK9]  [FK]
| PayRateSource | MaritalStatusTaxState |     | PayTypeHSP   [PK5]  [FK] |
| ------------- | --------------------- | --- | ------------------------ |
ResidencyStatus12
StepProgressionRateSourc EarnIncomeCredStatus PayGrade   [PK6]  [FK]
PositionBudgetEditSalary NumberOfDependents SalaryDataLocality   [PK7]  [FK]
| PositionBudgetEditFTE |     |     | DateEffective   [PK8]  [FK] |
| --------------------- | --- | --- | --------------------------- |
PositionBudgetEditHours EmploymentStatus CostCenterHome   [PK10]  [FK]
PositionBudgetEditHeadct EmployeeClassification JobCategory   [PK11]  [FK]
| PayRangeEdit | TaxAreaResidence |     | JobStep   [PK12]  [FK] |
| ------------ | ---------------- | --- | ---------------------- |
TaxAreaWork
SalaryDefaultSource SchoolDistrictCode DatePayStops   [PK13]  [FK]
SalaryIncreasesinProject S t a t e H o m e JobType   [PK14]  [FK]
| SalaryDisplay |                      |     | Non-Key Data     |
| ------------- | -------------------- | --- | ---------------- |
|               | S t a t e W o rk ing |     | EffectOnTurnover |
LocationHome
|     | LocationWorkCity   |     | UserId      |
| --- | ------------------ | --- | ----------- |
|     | LocationWorkCounty |     | ProgramId   |
|     | CompanyHome        |     | DateUpdated |
CostCenter
EmpoyeeJobs
| Key Data                         | ControlGroup     |     |                               |
| -------------------------------- | ---------------- | --- | ----------------------------- |
| AddressNumber   [PK1]  [FK]      | RoutingCodeCheck |     |                               |
| CostCenterHome   [PK2]  [FK]     |                  |     | HRHistory                     |
| JobCategory   [PK3]  [FK]        |                  |     | Key Data                      |
| JobStep   [PK4]  [FK]            |                  |     | FileName   [PK1]  [FK]        |
| DatePayStops   [PK5]  [FK]       |                  |     | AddressNumber   [PK2]  [FK]   |
| SalaryDataLocality   [PK9]  [FK] |                  |     | DataItem   [PK3]  [FK]        |
| PayGrade   [PK8]  [FK]           |                  |     | DateEffectiveOn   [PK4]  [FK] |
PayTypeHSP   [PK7]  [FK]
ChangeReason   [PK16]  [FK]
| ChangeReason   [PK15]  [FK]    |     |     | SequenceNumberView   [PK5]  [FK] |
| ------------------------------ | --- | --- | -------------------------------- |
| DateEffectiveOn   [PK16]  [FK] |     |     | PayTypeHSP   [PK6]  [FK]         |
| DateEffective   [PK6]  [FK]    |     |     | PayGrade   [PK7]  [FK]           |
| JobType   [PK10]  [FK]         |     |     | SalaryDataLocality   [PK8]  [FK] |
| DataItem   [PK11]  [FK]        |     |     | DateEffective   [PK9]  [FK]      |
TurnoverData   [PK12]  [FK]
CostCenterHome   [PK10]  [FK]
| FileName   [PK13]  [FK]           |     |     | JobCategory   [PK11]  [FK] |
| --------------------------------- | --- | --- | -------------------------- |
| SequenceNumberView   [PK14]  [FK] |     |     | JobStep   [PK12]  [FK]     |
Non-Key Data Multiple Employee Job History DatePayStops   [PK13]  [FK]
| PositionID         |                        |     | JobType   [PK14]  [FK]      |
| ------------------ | ---------------------- | --- | --------------------------- |
|                    | Key Data               |     | TurnoverData   [PK15]  [FK] |
| PrimaryJobFlag     | AddressNumber   [PK1]  |     |                             |
| DatePayStarts      | CostCenterHome   [PK2] |     | Non-Key Data                |
| UnionCode          | JobCategory   [PK3]    |     | HistoryData                 |
| RtSalary           | JobStep   [PK4]        |     | UserId                      |
| RtHourly           |                        |     | DateUpdated                 |
| DefaultAutoPayType | DatePayStops   [PK5]   |     | ProgramId                   |
SalaryDataLocality   [PK6]
| ShiftCode | PayGrade   [PK7] |     | WorkStationId |
| --------- | ---------------- | --- | ------------- |
WorkersCompInsurCode PayTypeHSP   [PK8] NumericValueOfHistory
ChangeReason   [PK9]
DateEffectiveOn   [PK10]
DateEffective   [PK11]
JobType   [PK12]
DataItem   [PK13]
TurnoverData   [PK14]
FileName   [PK15]
SequenceNumberView   [PK16]

| ShopFloorControlPartsList | WorkOrderMasterFile           |               |     |                          |
| ------------------------- | ----------------------------- | ------------- | --- | ------------------------ |
|                           | Key Data                      | AccountLedger |     | AssetAccountBalancesFile |
| Key Data                  | DocumentOrderInvoiceE   [PK1] | Key Data      |     | Key Data                 |
DocumentOrderInvoiceE   [PK5]  [FK] CategoriesWorkOrder001   [PK2]  [FK] AccountId   [PK1]
UniqueKeyIDInternal   [PK1] CompanyKey   [PK1] Century   [PK2]
| CategoriesWorkOrder001   [PK2]  [FK] | CategoriesWorkOrder002   [PK3]  [FK] | DocumentType   [PK2] |     |     |
| ------------------------------------ | ------------------------------------ | -------------------- | --- | --- |
CategoriesWorkOrder002   [PK3]  [FK] CategoriesWorkOrder003   [PK4]  [FK] DocVoucherInvoiceE   [PK3] FiscalYear1   [PK3]
CategoriesWorkOrder003   [PK4]  [FK] Non-Key Data DateForGLandVoucherJULIA   [PK4] FiscalQtrFutureUse   [PK4]
Non-Key Data OrderType JournalEntryLineNo   [PK5] LedgerType   [PK5]
O r d e r T y p e O r d e r S u f f ix L i n e E x t e n s i o n C o d e       [P K 6 ] S u b l e d g e r      [ P K 6 ]
O r d e r S u ff ix R e l a t e d O r d e r Ty p e A c c o u n tI d       [ P K 9 ]     [ F K ] A s s e tI te m N u m b e r     [P K 7]
T y p e B il l R e l a t e d P o S o N u m ber S u b l e d g e r       [ P K 1 3 ]     [ F K ] S u b l e d g e r T y p e       [ P K 8 ]
F i x e d O r V a riableQty Li n e N u m b e r S u b l e d g e r T y p e      [ P K 1 4 ]    [F K] N o n - K e y   D a ta
IssueTypeCode PegToWorkOrder LedgerType   [PK7]  [FK] Company
C o p r o d u ct s B y p r oducts P a re n tW oNumber C e n tu ry     [ P K 1 0 ]   [F K ] A m t B e g in n i n gB a la n c e Py
C o m p o n e n t T y p e Ty p e W o Fi s ca lY e a r 1     [P K 1 1 ]   [FK] A m o u n tN e t P o st in g 0 0 1
ComponentNumber PriorityWo FiscalQtrFutureUse   [PK12]  [FK] AmountNetPosting002
FromPotency Description001 AssetItemNumber   [PK8]  [FK] AmountNetPosting003
| ThruPotency | StatusCommentWo | Non-Key Data |     | AmountNetPosting004 |
| ----------- | --------------- | ------------ | --- | ------------------- |
|             | Company         | GLPostedCode |     | AmountNetPosting005 |
| FromGrade   | CostCenter      | BatchNumber  |     | AmountNetPosting006 |
ThruGrade C o s tC e nterAlt B a t c h T y p e A m o u n t N N.e t P o s t i n g 0 0 7
C o m p a n y K e y R e la te d Lo c a tio n D a t e B a tc h Julian A m o u n t e t P o s t i n g 0 0 8
R e lat e d P o S o N u m b e r AisleLocation DateBatchSystemDateJuliA AmountNetPosting009
| RelatedOrderType     | Bin.Location      |                 |     | AmountNetPosting010 |
| -------------------- | ----------------- | --------------- | --- | ------------------- |
| RelatedPoSoLineNo    | StatusCodeWo      | BatchTime       |     | AmountNetPosting011 |
| SequenceNoOperations |                   | Company         |     | AmountNetPosting012 |
| BubbleSequence       | DateStatusChanged | AcctNoInputMode |     |                     |
| ResourcePercent      | Subsidiary        | AccountModeGL   |     | AmountNetPosting013 |
| PercentOfScrap       | AddressNumber     | CostCenter      |     | AmountNetPosting014 |
ReworkPercent AddNoOriginator ObjectAccount AmtPriorYrNetPosti
| AsIsPercent | AddressNumberManager | Subsidiary |     | AmountWtd |
| ----------- | -------------------- | ---------- | --- | --------- |
PercentCumulativePla Supervisor PeriodNoGeneralLedge AmtOriginalBeginBud
StepScrapPercent AddNoAssignedTo CurrencyCodeFrom AmtProjectedOverUnder
LeadtimeOffsetDays AddressNumberInspector CurrencyConverRateOv PercentComplete
ComponentItemNoShort NextAddressNumber HistoricalCurrencyConver UnitsProjectedFinal
ComponentItemNo2nd DateTransactionJulian HistoricalDateJulian BudgetRequested
| ComponentThirdNumber | DateStart              | AmountField           |     | BudgetApproved             |
| -------------------- | ---------------------- | --------------------- | --- | -------------------------- |
|                      | DateRequestedJulian    | Units                 |     | CostCenter                 |
|                      | DateWoPlanCompleted    | UnitOfMeasure         |     | ObjectAccount              |
|                      | DateCompletion         | GlClass               |     | Subsidiary                 |
|                      | DateAssignedTo         | ReverseOrVoidRV       |     |                            |
|                      | DateAssignToInspector  | NameAlphaExplanation  |     |                            |
|                      | PaperPrintedDate       | NameRemarkExplanation |     | AssetMasterFileDONOTDELETE |
|                      | CategoriesWorkOrder004 | Reference1JeVouchIn   |     | Key Data                   |
ShopFloorControlRoutingInstruct CategoriesWorkOrder005 Reference2 AssetItemNumber   [PK1]
Key Data CategoriesWorkOrder006 Reference3AccountReconci Non-Key Data
|     | CategoriesWorkOrder007 | DocumentPayItem |     |     |
| --- | ---------------------- | --------------- | --- | --- |
DocumentOrderInvoiceE   [PK1]  [FK] CategoriesWorkOrder008 OriginalDocumentNo Company
ItemNumberShortKit   [PK7] CategoriesWorkOrder009 OriginalDocumentType ParentNumber
SequenceNoOperations   [PK3] CategoriesWorkOrder010 OriginalDocPayItem SerialTagNumber
TypeOperationCode   [PK4] Reference1 CompanyKeyPurchase UnitNumber
AtoLineType   [PK5] Reference2Vendor CompanyKeyOriginal SequenceNumber1
ParentSegmentNumber   [PK6] AmountOriginalDollars . MajorClass
CategoriesWorkOrder001   [PK8]  [FK] DocumentTypePurchase SubClass
CategoriesWorkOrder002   [PK9]  [FK] CrewSize AddressNumber ClassCode3
CategoriesWorkOrder003   [PK10]  [FK] RateDistribuOrBill CheckNumber ClassCode4
N o n - K e y   D a t a P a y D e d u c t B e n e f i t T y p e D a t e C h e c k J C l a s s C o d e 5
O r d e r T y p e A m t C h n g T o O r i g i n a l D D a t e C h e c k C l e a r e d C o s t C e n t e r
O r d e r S u f f i x H o u r s O r i g i n a l S e r i a l T a g N u m b e r D e s c r i p t i o n 0 0 1
T y p e R o u t i n g H r s C h n g T o O r i g i n a l H o B a t c h R e a r E n d P o s t C o d e D e s c r i p t i o n 0 1 0 0 2
I t e m N u m b e r 2 n d K i t A m o u n t A c t u a l R e c o n c i l e d R O r B l a n k D e s c r i p t i o n 0 1 0 0 3
I t e m N u m b e r 3 r d K i t H o u r s A c t u a l D e s c C o m p r e s s e d
C o s t C e n t e r A l t I d e n t i f i e r S h o r t I t e m D a t e A c q u i r e d
L i n e I d e n t i f i e r I d e n t i f i e r 3 r d I t e m D a t e D i s p o s a l
A u t o L o a d D e s c r i p t i o n I d e n t i f i e r 2 n d I t e m E q u i p m e n t S t a t u s
|     | A s s e t I t e m N u m b e r |     |     | N e w O r U s e d O n A c q u i s i t |
| --- | ----------------------------- | --- | --- | ------------------------------------- |
D e s c r i p t i o n L i n e 1 U n i t N u m b e r S t a t u s H i s t o r y F i l e A m t E s t S a l v a g e V a
O p e r a t i o n S t a t u s C o d e W o U n i t s T r a n s a c t i o n Q t y K e y   D a t a A m o u n t R e p l a c e m e n t C o s t
I n s p e c t i o n C o d e U n i t s Q u a n B a c k o r H e l d R e c o r d N u m b e r       [ P K 1 ] A m t L a s t Y e a r s R e p l a c e
T i m e B a s i s C o d e U n i t s Q u a n t i t y C a n c e l e d T y p e O f R e c       [ P K 2 ] A s s e t C o s t A c c t C o s t C e n
L a b o r O r M a c h i n e U n i t s Q u a n t i t y S h i p p e d D a t e B e g i n n i n g E f f e c t i v e       [ P K 3 ] A s s e t C o s t A c c t O b j e c t
P a y P o i n t C o d e Q u a n t i t y S h i p p e d T o D a t e T i m e B e g i n n i n g       [ P K 4 ] A s s e t C o s t A c c t S u b s i d
P a y P o i n t S t a t u s . U n i t O f M e a s u r e A s I n p u t E q u i p m e n t W o r k O r d e r S       [ P K 5 ] A c c u m D e p r e A c c t C c
| J o b C a t e g o r y | M e s s a g e N o | D o c u m e n t O r d e r | I n v o i c e E       [ P K 9 ]     [ F K ] |     |
| --------------------- | ----------------- | ------------------------- | ------------------------------------------- | --- |
A d d r e s s N u m b e r B e g i n n i n g H h M m S s C a t e g o r i e s W o r k O r d e r 0 0 1       [ P K 6 ]     [ F K ] A c c u m D e p r e A c c t O b j
C r i t i c a l R a t i o T y p e B i l l A c c u m D e p r e A c c t S u b
S l a c k T i m e R a t i o T y p e R o u t i n g C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 7 ]     [ F K ] D e p r e c i a t i o n E x p e n s e C c
D a t e T r a n s a c t i o n J u l i a n W o P i c k L i s t P r i n t e d C a t e g o r i e s W o r k O r d e r 0 0 3       [ P K 8 ]     [ F K ] D e p r e c i a t i o n E x p e n s e O b j
D a t e R e q u e s t e d J u l i a n P o s t i n g E d i t A s s e t I t e m N u m b e r       [ P K 1 0 ]     [ F K ] D e p r e c i a E x p e n s e S u b s i d
D a t e S t a r t V a r i a n c e F l a g N o n - K e y   D a t a A s s e t R e v e n u e C o s t C n t r
D a t e C o m p l e t i o n B i l l O f M a t e r i a l N . D a t e E n d i n g E f f e c t i v e A s s e t R e v e n u e O b j e c t
B e g i n n i n g H h M m S s R o u t e S h e e t N T i m e E n d i n g A s s e t R e v e n u e S u b s i d i a r y
E n d i n g H h M m S s S t a t u s H o u r s A s s e t I t e m C u r r e n t Q u a n
S h i f t C o d e R e q u e s t e d W o F l a s h M e s s a g e C u m u l a t i v e H o u r s A s s e t I t e m O r i g Q u a n
S h i f t C o d e S t a r t W o O r d e r F r e e z e C o d e L i f e t i m e F u e l M e t e r . T a x E n t i t y
S h i f t C o d e C o m p l e t e d I n d e n t e d C o d e L i f e t i m e H o u r M e t e r A m t I n v T a x C r Y t d
L e a d t i m e O v e r l a p S e q u e n c e C o d e L i f e t i m e M i l e M e t e r A m t I n v T a x C r P y e
P e r c e n t O f O v e r l a p A m t M i l e s O r H o u r s U n i t N a m e R e m a r k F i n a n c i n g M e t h o d
P e r c e n t O p e r a t i o n a l P l D a t e S c h e d u l e d T i c k l e r U s e r I d I t c O w n e d F l a g
P e r c e n t C u m u l a t i v e P l a A m t P r o j e c t e d O v e r U n d e r P r o g r a m I d P u r c h a s e O p t i o n
N e x t O p e r a t i o n P e r c e n t C o m p l e t e W o r k S t a t i o n I d A m t P u r c h a s e O p t i o n P r i c
C r e w S i z e L e a d t i m e L e v e l D a t e U p d a t e d P u r O p t i o n C r e d i t P e r c e n
M o v e H o u r s L e a d t i m e C u m T i m e L a s t U p d a t e d A m t P u r c h a s e O p t i o n M a x i
Q u e u e H o u r s U n a c c t D i r e c t L a b o r H r s A d d r e s s N u m b e r L e s s o r
|     | L o t |     |     | D a t e C o n t r a c t |
| --- | ----- | --- | --- | ----------------------- |
R u n M a c h i n e S t a n d a r d L o t P o t e n c y D a t e E x p i r e d J u l i a n
R u n L a b o r S t a n d a r d L o t G r a d e A m o u n t M o n t h l y P a y m e n t
S e t u p L a b o r H r s S t d r C r i t i c a l R a t i o P r i o r i t y 1 N a m e R e m a r k
R u n M a c h i n e A c t u a l C r i t i c a l R a t i o P r i o r i t y 2 N a m e R e m a r k s L i n e 2
R u n L a b o r A c t u a l D o c u m e n t T y p e I n s u r a n c e P o l i c y N u m b e r
S e t u p L a b o r H o u r s A c t u al S u b l e d g e r I n a c t i v e C o d e I n s u r a n c e C o m p a n y
O p e r a t i o n S h r i n k a g e C o m p a n y K e y R e l a t e d P o l i c y R e n e w a l M o n t h
| U n i t s T r a n s a c t i o n Q t y | B i l l R e v i s i o n L e v e l |     |     |     |
| ------------------------------------- | --------------------------------- | --- | --- | --- |
U n i t s Q u a n t i t y C a n c e l e d R o u t i n g R e v i s i o n L e v e l A m o u n t I n s u r a n c e P r e m i u m
U n i t s Q u a n t i t y S h i p p e d D r a w i n g C h a n g e A m o u n t I n s u r a n c e V a l u e
U n i t s Q u a n t i t y M o v e d T R o u t i n g C h a n g e E c o I n s u r a n c e V a l u e I n d e x
R a t e P i e c e w o r k N e w P a r t N u m b e r R e q u i r e d U s e r I d
U n i t O f M e a s u r e A s I n p u t D t L a s t C h a n g e d

FixedAssetConstants
| Key Data |     | .   |     |     |     |
| -------- | --- | --- | --- | --- | --- |
SupplementalDataCategory   [PK1]
AssetAccountBalancesFile
Key Data
| CompanyConstants                                                          |                                                                         |                                                                                 | AccountId   [PK1]                                                       |                                               |     |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------- | --- |
| Key Data                                                                  |                                                                         |                                                                                 | Century   [PK2] FiscalYear1   [PK3]                                     |                                               |     |
| Company   [PK1]                                                           |                                                                         |                                                                                 | FiscalQtrFutureUse   [PK4]                                              |                                               |     |
| Non-Key Data                                                              |                                                                         |                                                                                 | LedgerType   [PK5]  [FK]                                                |                                               |     |
| N a m e                                                                   |                                                                         |                                                                                 | S u b l e d g e r       [ P K 6 ]                                       |                                               |     |
| A l t e r n a t e C o m p a n y N a m e                                   |                                                                         |                                                                                 | C o m p a n y       [ P K 1 3 ]                                         | [ F K ]                                       |     |
| D a t e f i s c a l y e a r b e g i n s j                                 |                                                                         |                                                                                 | A s s e t I t e m N u m b e r                                           | [ P K 7 ]     [ F K ]                         |     |
| P e r i o d N u m b e r C u r r e n t                                     | A s s e t M a s t e r F i l e                                           |                                                                                 | S S u u b p l p e l d e g m e e r n T t y a p l D e   a     t [ a P C K | a 8 t e ] g o r y       [ P K 9 ]     [ F K ] |     |
| W o r k e r s C o m p P r e m B a s e 1                                   | K e y   D a t a                                                         |                                                                                 | D e p r e c i a t i o n C a t e g o                                     | r y C o d e       [ P K 1 0 ]     [F K ]      |     |
| C S e u a r r r e c n h c T y y C p o e n S v e e c r u Y r N i t y A R   | A s s e t I t e m N u m b e r       [                                   | P K 1 ]                                                                         | A s s e t C o s t A c c t O b j e                                       | c t D       [ P K 1 1 ]     [ F K ]           |     |
| W o r k e r s C o m p P r e m B a s e 2                                   | S D u e p p p r e l e c m i a e t i o n n t a C l D a a t e t a g C o r | a y t C e g o o d r e y             [ [ P P K K 9 8 ] ]         [ [ F F K K ] ] | A s s e t A c c t S u b s i d i a r                                     | y D e       [ P K 1 2 ]     [ F K ]           |     |
| U s e C c F r A s s e t C s t F l a g                                     | N o n - K e y   D a t a                                                 |                                                                                 | N o n - K e y   D a t a                                                 |                                               |     |
| U s e C c F o r D e p r e E x p F l g                                     | P a r e n t N u m b e r                                                 |                                                                                 | A m t B e g i n n i n g B a l a n                                       | c e P y                                       |     |
| U s e C c F r A c c u m D e p r e F l                                     | S e r i a l T a g N u m b e r                                           |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 1                                           |     |
| U s e C c F o r R e v B i l l F l a g                                     | U n i t N u m b e r                                                     |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 2                                           |     |
| C B o o o m k M T o e T t h a o x d I t d O r R e m 1                     | S e q u e n c e N u m b e r 1                                           |                                                                                 | A A m m o o u u n n t t N N e e t t P P o o s s t t i i n n g g 0 0     | 0 0 3 4                                       |     |
| T a x Y e a r B e g i n M o n t h                                         | M a j o r C l a s s                                                     |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 5                                           |     |
| T a x Y e a r B e g i n M o n t h O l d                                   | S u b C l a s s                                                         |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 6                                           |     |
| D a t e N e w T a x Y e a r E n d J                                       | C C l l a a s s s s C C o o d d e e 3 4                                 |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 7                                           |     |
| G l I n t e r f a c e F l g P r o p E q                                   | C l a s s C o d e 5                                                     |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 0 8                                           |     |
| A d d r e s s B o o k I n t e r f a c e                                   | C o s t C e n t e r                                                     | .                                                                               | A m o u n t N e t P o s t i n g 0                                       | 0 9                                           |     |
| N u m b e r O f P e r i o d s N o r m a l                                 | . D e s c r i p t i o n 0 0 1                                           |                                                                                 | A A m m o o u u n n t t N N e e t t P P o o s s t t i i n n g g 0 0     | 1 1 0 1                                       |     |
| F P i e s r c i o a d l D N a o t e F P i n a a t n t e c r i n a l R e p | D e s c r i p t i o n 0 1 0 0 2                                         |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 1 2                                           |     |
| F i n a n c i a l R e p o r t i n g Y e a r                               | D e s c r i p t i o n 0 1 0 0 3                                         |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 1 3                                           |     |
| C u r r e n c y C o d e F r o m                                           | D D e a s t e c A C c o q m u p i r r e e d s s e d                     |                                                                                 | A m o u n t N e t P o s t i n g 0                                       | 1 4                                           |     |
| S y m b l U s e T o D e f i n P E I                                       | D a t e D i s p o s a l                                                 |                                                                                 | A m t P r i o r Y r N e t P o s t i                                     |                                               |     |
| S y m b l U s e T o D e f i n P E U                                       | E q u i p m e n t S t a t u s                                           |                                                                                 | A m o u n t W t d                                                       |                                               |     |
| S y m b l U s e T o D e f i n S e r i a                                   | N e w O r U s e d O n A c q u                                           | i s i t                                                                         | A A m m t t O P r r o i g j e i n c a t e l B d e O g v i n e B r U u   | n d d e r                                     |     |
| D P r e i n l i n t S q t u a e t e n m c y e L n e t t Y t e N r         | A m t E s t S a l v a g e V a                                           |                                                                                 | P e r c e n t C o m p l e t e                                           |                                               |     |
| A u t o C a s h                                                           | A m o u n t R e p l a c e m e n                                         | t C o s t                                                                       | U n i t s P r o j e c t e d F i n a l                                   |                                               |     |
| A u t o c a s h A l g o r i t h m                                         | A A m s s t e L t a C s o t Y s t e A a c r c s t R C e o p s l t a C   | c e e n                                                                         | B u d g e t R e q u e s t e d                                           |                                               |     |
| A g i n g M e t h o d                                                     | A s s e t C o s t A c c t O b j e c                                     | t                                                                               | B u d g e t A p p r o v e d                                             |                                               |     |
| A g i n g D a y s A R C u r r e n t                                       | A s s e t C o s t A c c t S u b s i                                     | d                                                                               | C o s t C e n t e r                                                     |                                               |     |
| A g i n g D a y s A R 0 0 1                                               | A c c u m D e p r e A c c t C c                                         |                                                                                 | O S u b b j e s c i d t A i a c r c y o u n t                           |                                               |     |
| A A g g i i n n g g D D a a y y s s A A R R 0 0 0 0 2 3                   | A c c u m D e p r e A c c t O b                                         | j                                                                               | L i f e M o n t h s                                                     |                                               |     |
| A g i n g D a y s A R 0 0 4                                               | A c c u m D e p r e A c c t S u                                         | b                                                                               | D e p r e c i a t i o n M e t h o d                                     |                                               |     |
| A g i n g D a y s A R 0 0 5                                               | D D e e p p r r e e c c i i a a t t i i o o n n E E x x p p e e n n s s | e e C O c b j                                                                   | D e p r e c i a t i o n I n f o r m a                                   | t i o n                                       |     |
| A g i n g D a y s A R 0 0 6                                               | D e p r e c i a E x p e n s e S u                                       | b s i d                                                                         | M e t h o d                                                             |                                               |     |
| A g i n g D a y s A R 0 0 7                                               | A s s e t R e v e n u e C o s t C                                       | n t r                                                                           | S c h e d u l e M e t h o d 9                                           |                                               |     |
| F i n a n c i a l R e p o r t Y e a r 5 2                                 | A s s e t R e v e n u e O b j e c                                       | t                                                                               | C D o a m t e p D M e p e r t e h S o d t a I t r d t e O d r R         | e m                                           |     |
| P N e u r m i o b d e N r O o F f P i n e a r n i o c d i a s l 5 5 2 2   | A s s e t R e v e n u e S u b s i                                       | d i a r y                                                                       | U s e r I d                                                             |                                               |     |
| P e r c e n t a g e F a c t o r                                           | A s s e t I t e m C u r r e n t Q u                                     | a n                                                                             | D t L a s t C h a n g e d                                               |                                               |     |
B a s e A g i n g D a t e A T a s s x e E t n I t t e i t m y O r i g Q u a n P r o g r a m I d L o c a t i o n T r a c k i n g T a b l e
D a t e A g e A s O f A m t I n v T a x C r Y t d C u r r e n c y C o d e F r o m K e y   D a t a
P e r i o d N o A r A m t I n v T a x C r P y e D a t e U p d a t e d A s s e t I t e m N u m b e r       [ P K 9 ]     [ F K ]
P e r i o d N o A p F i n a n c i n g M e t h o d W o r k S t a t i o n I d T r a n s f e r N u m b e r       [ P K 1 ]
D D a a t t e e A A R P F F i i s s c c a a l l Y Y e e a a r r B B e e g g i i n n s s J J I t c O w n e d F l a g N S u e p x t p N l e u m m e b n e t r a V l D a l a u t e a   C     a [ P t e K g 2 o ] r y       [ P K 3 ]     [ F K ]
A d d r e s s N u m b e r P u r c h a s e O p t i o n D e p r e c i a t i o n C a t e g o r y C o d e       [ P K 4 ]     [ F K ]
S i g n a t u r e B l o c k A m t P u r c h a s e O p t i o n P r i c C o m p a n y       [ P K 5 ]     [ F K ]
P r i n t C o m p a n y N a m e P A u m r t O P p u t r i c o h n a C s r e e O d i p t P t i e o r n c M e n a x i A s s e t C o s t A c c t O b j e c t D       [ P K 6 ]     [ F K ]
F o r F u t u r e U s e F l a g 1 A d d r e s s N u m b e r L e s s o r A s s e t A c c t S u b s i d i a r y D e       [ P K 7 ]     [ F K ]
F o r F u t u r e U s e F l a g 2 D a t e C o n t r a c t L e d g e r T y p e       [ P K 8 ]     [ F K ]
U s e r I d D a t e E x p i r e d J u l i a n N o n - K e y   D a t a
|     | AmountMonthlyPayment                                  |     |     |     | LocationHistOrSched CostCenterLocation |
| --- | ----------------------------------------------------- | --- | --- | --- | -------------------------------------- |
|     | NameRemark                                            |     |     |     | DateBeginningEffective                 |
|     | NameRemarksLine2 I n s u r a n c e P o l ic yN u mber |     |     |     | D a t e E nd i ng                      |
|     | I n s u r a n c e C o m p an y                        |     |     | .   | N a m e R e m ark                      |
|     | PolicyRenewalMonth                                    |     |     |     | DtLastChanged                          |
|     | AmountInsurancePremium                                |     |     |     | UserId                                 |
|     | AmountInsuranceValue                                  |     |     |     | ProgramId WorkStationId                |
|     | InsuranceValueIndex                                   |     |     |     | EquipmentRateCode                      |
|     | UserId DtLastChanged                                  |     |     |     | Quantity                               |
|     | CostCenterLocation                                    |     |     |     | EquipmentStatus                        |
D e f a u l t A c c o u n t i n g C o n s t a n t s S t a t e C o s t C e n t e r
| K e y   D a t a | P r o g r a m I d |     |     |     | S u b s id i a r y |
| --------------- | ----------------- | --- | --- | --- | ------------------ |
C o m p a n y       [ P K 1 ]     [ F K ] D a t e B e g i n n i n g E f f e c t i v e O b j e c t A c c o u n t
A s s e t C o s t A c c t O b j e c t D       [ P K 2 ]     [ F K ] D a t e E x p e c t e d R e t u r n P a r e n t H i s t o r y T T i i m m e e S S t t a a m m p p B E e n g d i i n n n g i n g
A s s e t A c c t S u b s i d i a r y D e       [ P K 3 ]     [F K ] A N c a t m i o e n E M x e p s l a s a n g a e t i o C n o n t r o l K e y   D a t a M e t e r O r i g i n a l R e a d i n g
A s s e t I t e m N u m b e r       [ P K 4 ]     [ F K ] N a m e R e m a r k E x p la n a t ion A s s e t I t e m N u m b e r      [ P K 1 ]     [ F K ] M e t e r C u r r e n t R e a d i n g
L e d g e r T y p e       [ P K 5 ]     [ F K ] A d d r e s s N u m b e r P a r e n t N u m b e r       [ P K 2 ] E q u i p m e n t R a t e T a b le
S D u e p p p r e l e c m i a e t i o n n t a C l D a a t e t a g C o r a y t C e g o o d r e y             [ [ P P K K 7 6 ] ]         [ [ F F K K ] ] C l a s s C o d e 6 D a t e B e g i n n i n g E f f e c t i v e       [ P K 3 ] E q u i p m e n t R a t e G r o u p
N o n - K e y   D a t a C l a s s C o d e 7 D S u a p t e p E l e n m d i e n n g t E a f l D f e a c t t a i v C e a     t   e [P g K o r 4 y ]       [ P K 5 ]     [ F K ] A m o u n t A c t u a l B i l l e d
M a j o r C l a s s C l a s s C o d e 8 . D e p r e c i a t i o n C a t e g o r y C o d e       [ P K 6 ]     [ F K ] A B i i s n l L e o L c o a c t a i o t i n o n
SubClass C ClassCode0 l a s s C o d e 9 Company   [PK7]  [FK] Subledger
AccumDepreAcctCc StandardFuelConsumptio AssetCostAcctObjectD   [PK8]  [FK] SubledgerType
AccumDepreAcctObj . DisposalAccumDepreCc AssetAcctSubsidiaryDe   [PK9]  [FK] TransferActionCode
| AccumDepreAcctSub                            | DisposalAccumDepreObj               |     | LedgerType   [PK10]  [FK] |     |     |
| -------------------------------------------- | ----------------------------------- | --- | ------------------------- | --- | --- |
| DepreciationExpenseCc                        | DisposalAccumDepreSub               |     | Non-Key Data              |     |     |
| DepreciationExpenseObj DepreciaExpenseSubsid | UnitNo                              |     | DateUpdated               |     |     |
| AssetRevenueCostCntr                         | ItemNumberShortKit ItemNumber2ndKit |     | UserId ProgramId          |     |     |
| AssetRevenueObject                           | AfeNumber                           |     |                           |     |     |
| AssetRevenueSubsidiary                       | JobCategory                         |     |                           |     |     |
| DtLastChanged                                | JobStep                             |     |                           |     |     |
| UserId                                       | UnionCode                           |     |                           |     |     |
| ProgramId DateUpdated                        | SubledgerInactiveCode               |     |                           |     |     |
| WorkStationId                                | DateUpdated                         |     |                           |     |     |
| TimeLastUpdated                              | . WorkStationId TimeLastUpdated     |     |                           |     |     |
| Subledger                                    | CategoryCodeFA0                     |     |                           |     |     |
| SubledgerType                                | CatagoryCodeFA                      |     |                           |     |     |
| DeprExpenseSubledgerDeri                     | CategoryCodeFA2                     |     |                           |     |     |
CategoryCodeFA3
CategoryCodeFA4
|                                                                                               | CategoryCodeFA5 C a t e g o r y C o d e F A 6 |     | ProductionScheduleMasterFile                        |                                                                                                     |     |
| --------------------------------------------------------------------------------------------- | --------------------------------------------- | --- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --- |
|                                                                                               | C a t e g o r y C o d e F A 7                 |     | . K e y   D a t a                                   |                                                                                                     |     |
| D e f a u l t D e p r e c i a t i o n C o n s t a n t s                                       | C a t e g o r y C o d e F A 8                 |     | A s s e t I t e m N u m                             | b e r       [ P K 1 ]     [ F K ]                                                                   |     |
| K e y   D a t a                                                                               | C a t e g o r y C o d e F A 9                 |     | S D u e p p p r e l e c m i a e t i o n n t a C l D | a a t e t a g C o r a y t C e g o o d r e y             [ [ P P K K 3 2 ] ]         [ [ F F K K ] ] |     |
| C o m p a n y       [ P K 1 ]                                                                 |                                               |     | C o m p a n y       [ P K                           | 4 ]                                                                                                 |     |
| A s s e t C o s t A c c t O b j e c t D       [ P K 2 ]                                       |                                               |     | A s s e t C o s t A c c t                           | O b j e c t D       [ P K 5 ]                                                                       |     |
| A L e s d s e g t e A r T c c y t p S e u     b   [ s P i d K i a 4 r ] y D e       [ P K 3 ] |                                               |     | A s s e t A c c t S u b s                           | i d i a r y D e       [ P K 6 ]                                                                     |     |
| A s s e t I t e m N u m b e r       [ P K 5 ]     [ F K ]                                     |                                               |     | L e d g e r T y p e       [                         | P K 7 ]                                                                                             |     |
| S u p p l e m e n t a l D a t a C a t e g o r y       [ PK6]  [FK]                            |                                               |     | N o n - K e y   D a t a                             |                                                                                                     |     |
| DepreciationCategoryCode   [PK7]  [FK]                                                        |                                               |     | ScheduleMethod9                                     |                                                                                                     |     |
| Non-Key Data                                                                                  |                                               |     | Description001                                      |                                                                                                     |     |
| D e p r e c i a t i o n M e t h o d                                                           |                                               |     | U U n n i i t t O s C f M u r e r e a n s u t M r e | o P r o d u c t                                                                                     |     |
| L i f e M o n t h s                                                                           |                                               |     | U n i t s P r o d u c e d                           | P r i o r Y r                                                                                       |     |
| D M e e p t h r e o c d i a t i o n I n f o r m a tio n                                       |                                               |     | U n i t s P r o d u c e d                           | Y r T o D t e                                                                                       |     |
| S c h e d u l e M e t h o d 9                                                                 |                                               |     | U n i t s T o t a l                                 |                                                                                                     |     |
| C o m p M e t h o d It d O rR e m                                                             |                                               |     | P r i o r Y e a r R e v i s                         | i o n s                                                                                             |     |
| D t L a s t C h a n g e d                                                                     |                                               |     | C u r r e n t Y e a r R e                           | v i s i o n s                                                                                       |     |
| U s e r I d                                                                                   |                                               |     | D U t s L e a r I s d t C h a n g e                 | d                                                                                                   |     |
| P r o g r a m I d                                                                             |                                               |     | P r o g r a m I d                                   |                                                                                                     |     |
D WorkStationId a t e U p d a t e d
TimeLastUpdated
MajorClass
AssetDepreciationCategor
SubledgerType
Subledger

ItemMaster
|     |     | Non-Key Data | ItemBranchFile |     |
| --- | --- | ------------ | -------------- | --- |
Non-Key Data
Identifier2ndItem
|     |     | Identifier3rdItem | Identifier2ndItem |     |
| --- | --- | ----------------- | ----------------- | --- |
Identifier3rdItem
DescriptionLine1
|     |     | D e sc ri p ti o n Line2 | S a l e s R e p o r t | i n g C o d e 1 |
| --- | --- | ------------------------ | --------------------- | --------------- |
CategoryCodeKeyPositionFile S a l e s R e p o r t i n g C o d e 2
| Key Data |     | Se a rc h T e x t | SalesReportingCode3 |     |
| -------- | --- | ----------------- | ------------------- | --- |
SearchTextCompressed
VersionKeyDefinition   [PK1] SalesReportingCode1 SalesReportingCode4
| Non-Key Data |     |     | SalesReportingCode5 |     |
| ------------ | --- | --- | ------------------- | --- |
SalesReportingCode2
| KeyPostionCode001 |     | SalesReportingCode3 | SalesReportingCode6 |     |
| ----------------- | --- | ------------------- | ------------------- | --- |
SalesReportingCode7
| KeyPostionCode002 |     | SalesReportingCode4 |                       |     |
| ----------------- | --- | ------------------- | --------------------- | --- |
| KeyPostionCode003 |     | SalesReportingCode5 | SalesReportingCode8   |     |
| KeyPostionCode004 |     |                     | SalesReportingCode9   |     |
|                   |     | SalesReportingCode6 | SalesReportingCode10  |     |
| KeyPostionCode005 |     | SalesReportingCode7 |                       |     |
| KeyPostionCode006 |     | SalesReportingCode8 | PurchasingReportCode1 |     |
. PurchasingReportCode2
| KeyPostionCode007 |     | SalesReportingCode9  |                       |     |
| ----------------- | --- | -------------------- | --------------------- | --- |
| KeyPostionCode008 |     | SalesReportingCode10 | PurchasingReportCode3 |     |
| KeyPostionCode009 |     |                      | PurchasingReportCode4 |     |
PurchasingReportCode1
KeyPostionCode010 PurchasingReportCode2 PurchasingReportCode5
| KeyPostionCode011 |     |                       | PurchReportingCode6 |     |
| ----------------- | --- | --------------------- | ------------------- | --- |
|                   |     | PurchasingReportCode3 | PurchReportingCode7 |     |
| KeyPostionCode012 |     | PurchasingReportCode4 |                     |     |
| KeyPostionCode013 |     | PurchasingReportCode5 | PurchReportingCode8 |     |
PurchReportingCode9
| KeyPostionCode014 |     | PurchReportingCode6  |                      |     |
| ----------------- | --- | -------------------- | -------------------- | --- |
| KeyPostionCode015 |     | PurchReportingCode7  | PurchReportingCode10 |     |
| KeyPostionCode016 |     |                      | CommodityCode        |     |
|                   |     | PurchReportingCode8  | ProductGroupFrom     |     |
| KeyPostionCode017 |     | PurchReportingCode9  |                      |     |
| KeyPostionCode018 |     |                      | DispatchGrp          |     |
|                   |     | PurchReportingCode10 | PrimaryLastVendorNo  |     |
| KeyPostionCode019 |     | CommodityCode        |                      |     |
|                   |     | ProductGroupFrom     | AddressNumberPlanner |     |
Buyer
DispatchGrp
|     | .   |     | GlCategory |     |
| --- | --- | --- | ---------- | --- |
CountryOfOrigin
ReorderPointInput
ForecastSummaryFile
Key Data
| VersionKeyDefinition   [PK1]  [FK] |     |     |     | .   |
| ---------------------------------- | --- | --- | --- | --- |
ForecastType   [PK2]
KeyValueCategoryCodes001   [PK3]
KeyValueCategoryCodes002   [PK4]
KeyValueCategoryCodes003   [PK5]
| KeyValueCategoryCodes004   [PK6] |     | ForecastFile                      |     |     |
| -------------------------------- | --- | --------------------------------- | --- | --- |
| KeyValueCategoryCodes005   [PK7] |     | Key Data                          |     |     |
| KeyValueCategoryCodes006   [PK8] |     | IdentifierShortItem   [PK1]  [FK] |     |     |
KeyValueCategoryCodes007   [PK9] CostCenter   [PK2]  [FK] ForecastPrices
KeyValueCategoryCodes008   [PK10] DateRequestedJulian   [PK3] Key Data
KeyValueCategoryCodes009   [PK11]
|     |     | AddressNumber   [PK4]  [FK] | CostCenter   [PK1] |     |
| --- | --- | --------------------------- | ------------------ | --- |
KeyValueCategoryCodes010   [PK12] ForecastType   [PK5]  [FK] IdentifierShortItem   [PK2]
| Company   [PK13] |     | CalendarYear   [PK6] |     |     |
| ---------------- | --- | -------------------- | --- | --- |
AddressNumber   [PK3]
IdentifierShortItem   [PK14] EffectiveFromDate   [PK7]  [FK] ForecastType   [PK4]
| A d d re s s N u m | b e r      [ P K 1 5 ] | E ff e c t iv e T h r u D ate   [PK8]  [FK] |                 |                                   |
| ------------------ | ---------------------- | ------------------------------------------- | --------------- | --------------------------------- |
|                    |                        | .                                           | E f f e c t i v | e F r o m D a t e       [ P K 5 ] |
D a te R e q u e st e d J u l i a n     [P K16] N o n - K e y   D a t a E f f e c t i v e T h r uD a t e       [ P K 6 ]
| Non-Key Data |     | Identifier2ndItem |     |     |
| ------------ | --- | ----------------- | --- | --- |
Non-Key Data
| UnitsTransactionQty |     | Identifier3rdItem | AmtPricePerUnit2 |     |
| ------------------- | --- | ----------------- | ---------------- | --- |
UnitsTransactionQty
DateUpdated
|     |     | AmountExtendedPrice | TimeOfDay |     |
| --- | --- | ------------------- | --------- | --- |
ForecastAmount
|     | .   |                  | WorkStationId |     |
| --- | --- | ---------------- | ------------- | --- |
|     |     | ForecastQuantity | UserId        |     |
OrderType
BypassForcingYN
| ForecastSummaryWorkFile |     | Revised |     |     |
| ----------------------- | --- | ------- | --- | --- |
DateUpdated
Key Data
| IdentifierShortItem   [PK1]  [FK] |     | UserId |     |     |
| --------------------------------- | --- | ------ | --- | --- |
WorkStationId
| CostCenter   [PK2] |     | ProgramId |     |     |
| ------------------ | --- | --------- | --- | --- |
ForecastType   [PK3]  [FK]
.
SummaryForecastKey   [PK4]
VersionKeyDefinition   [PK5]  [FK]
KeyValueCategoryCodes001   [PK6]  [FK]
KeyValueCategoryCodes002   [PK7]  [FK]
KeyValueCategoryCodes003   [PK8]  [FK]
KeyValueCategoryCodes004   [PK9]  [FK]

CostCenterMaster
| D a t e F i s c a l P a t t e r n | s   | K e y   D a t a |     | A c c o u n t M a s t e r |                           |     |
| --------------------------------- | --- | --------------- | --- | ------------------------- | ------------------------- | --- |
| K e y   D a t a                   |     |                 |     |                           | A c c o u n t L e d g e r |     |
F i s c a l D a t e P a t t e r n       [ P K 1 ] C o s t C e n t e r       [ P K 1 ] K e y   D a t a K e y   D a t a
D a t e f i s c a l y e a r b e g i n s j       [ P K 2] N o n - K e y   D a t a A c c o u n t I d       [ P K 1 ] C o m p a n y K e y       [ P K 1 ]
|     |     | C o s t C e n t e r T y p e |     | N o n - K e y   D a t a | D o c u m e n t T y p e |       [ P K 2 ] |
| --- | --- | --------------------------- | --- | ----------------------- | ----------------------- | --------------- |
F i s c a l Q t r F u t u r e U s e       [ P K 3 ] D e s c r i p C o m p r e s s e d C o m p a n y     [ F K ] D o c V o u c h e r I n v o i c e E       [ P K 3 ]
N o n - K e y   D a t a L e v e l O f D e t a i l C c C o d e C o s t C e n t e r     [ F K ] D a t e F o r G L a n d V o u c h e r J U L I A   [PK4]
| F i s c a l Y e a r 1 |     | C o m p a n y     [ F K ] |     |     |     |     |
| --------------------- | --- | ------------------------- | --- | --- | --- | --- |
D a t e E n d o f P e r i o d 0 1 J u A d d r e s s N u m b e r     [ F K ] O b j e c t A c c o u n t     [ F K ] J o u r n a l E n t r y L i n e N o       [ P K 5 ]
D a t e E n d o f P e r i o d 0 2 J u S u b s i d i a r y L i n e E x t e n s i o n C o d e       [ P K 7 ]
D a t e E n d o f P e r i o d 0 3 J u A d d r e s s N u m b e r J o b A r A c c o u n t N u m b e r 3 r d L e d g e r T y p e       [ P K 6 ]     [ F K ]
D a t e E n d o f P e r i o d 0 4 J u C o u n t y D e s c r i p t i o n 0 0 1 N o n - K e y   D a t a
|     |     | S t a t e |     | L e v e l O f D e t a i l A c c t C d e | G L P o s t e d C o d e |     |
| --- | --- | --------- | --- | --------------------------------------- | ----------------------- | --- |
D a t e E n d o f P e r i o d 0 5 J u M o d e l A c c o u n t s a n d C o n s o l id B u d g e t P a t t e r n C o d e B a t c h N u m b e r     [ F K ]
D a t e E n d o f P e r i o d 0 6 J u D e s c r i p t i o n 0 0 1 P o s t i n g E d i t B a t c h T y p e     [ F K ]
| D a t e E n d o f P e r i o d | 0 7 J u | D e s c r i p t i o n 0 1 0 0 | 2   | B i l l a b l e Y N |     |     |
| ----------------------------- | ------- | ----------------------------- | --- | ------------------- | --- | --- |
D a t e E n d o f P e r i o d 0 8 J u D e s c r i p t i o n 0 1 0 0 3 C u r r e n c y C o d e F r o m D a t e B a t c h J u l i a n
D a t e E n d o f P e r i o d 0 9 J u D e s c r i p t i o n 0 1 0 0 4 U n i t O f M e a s u r e D a t e B a t c h S y s t e m D a t e J u l i A
D a t e E n d o f P e r i o d 1 0 C a t e g o r y C o d e C o s t C t 0 0 1 B a t c h T i m e
D a t e E n d o f P e r i o d 1 1 C a t e g o r y C o d e C o s t C t 0 0 2 C a t e g o r y C o d e G l 0 0 1 C o m p a n y
D a t e E n d o f P e r i o d 1 2 C a t e g o r y C o d e G l 0 0 2 A c c t N o I n p u t M o d e
D a t e E n d o f P e r i o d 1 3 J C a t e g o r y C o d e C o s t C t 0 0 3 C a t e g o r y C o d e G l 0 0 3 A c c o u n t M o d e G L
|     |     | C a t e g o r y C o d e C | o s t C t 0 0 4 | C a t e g o r y C o d e G l 0 0 4 | A c c o u n t I d     [ F K ] |     |
| --- | --- | ------------------------- | --------------- | --------------------------------- | ----------------------------- | --- |
D a t e E n d o f P e r i o d 1 4 C a t e g o r y C o d e C o s t C t 0 0 5 C a t e g o r y C o d e G l 0 0 5 C o s t C e n t e r
D a t e P a t t e r n T y p e C a t e g o r y C o d e C o s t C t 0 0 6 C a t e g o r y C o d e G l 0 0 6 O b j e c t A c c o u n t
| U s e r I d |     | C a t e g o r y C o d e C | o s t C t 0 0 7 | C a t e g o r y C o d e G l 0 0 7 | .   |     |
| ----------- | --- | ------------------------- | --------------- | --------------------------------- | --- | --- |
P r o g r a m I d C a t e g o r y C o d e C o s t C t 0 0 8 C a t e g o r y C o d e G l 0 0 8 S u b s i d i a r y
|     |     | C a t e g o r y C o d e C | o s t C t 0 0 9 | C a t e g o r y C o d e G l 0 0 9 | S u b l e d g e r     [ F K ] |             |
| --- | --- | ------------------------- | --------------- | --------------------------------- | ----------------------------- | ----------- |
|     |     | C a t e g o r y C o d e C | o s t C t 0 1 0 | .                                 | S u b l e d g e r T y p e     |     [ F K ] |
. C a t e g o r y C o d e C o s t C t 0 1 1 C a t e g o r y C o d e G l 0 1 0 P e r i o d N o G e n e r a l L e d g e
|     |     |                           |                 | C a t e g o r y C o d e G l 0 1 1 | C e n t u r y     [ F K ]     |                   |
| --- | --- | ------------------------- | --------------- | --------------------------------- | ----------------------------- | ----------------- |
|     |     | C a t e g o r y C o d e C | o s t C t 0 1 2 | C a t e g o r y C o d e G l 0 1 2 | F i s c a l Y e a r 1     [ F | K ]               |
|     |     | C a t e g o r y C o d e C | o s t C t 0 1 3 | C a t e g o r y C o d e G l 0 1 3 | F i s c a l Q t r F u t u r e | U s e     [ F K ] |
C o m p a n y C o n s t a n t s C a t e g o r y C o d e C o s t C t 0 1 4 C a t e g o r y C o d e G l 0 1 4 C u r r e n c y C o d e F r o m     [ F K ]
K e y   D a t a . C a t e g o r y C o d e C o s t C t 0 1 5 C a t e g o r y C o d e G l 0 1 5 C u r r e n c y C o n v e r R a t e O v
C o m p a n y       [ P K 1 ] C a t e g o r y C o d e C o s t C t 0 1 6 C a t e g o r y C o d e G l 0 1 6 H i s t o r i c a l C u r r e n c y C o n v e r
| N o n - K e y   D a t a |     | C a t e g o r y C o d e C | o s t C t 0 1 7 | C a t e g o r y C o d e G l 0 1 7 |                               |           |
| ----------------------- | --- | ------------------------- | --------------- | --------------------------------- | ----------------------------- | --------- |
|                         |     | C a t e g o r y C o d e C | o s t C t 0 1 8 | C a t e g o r y C o d e G l 0 1 8 | H i s t o r i c a l D a t e J | u l i a n |
N a m e C a t e g o r y C o d e C o s t C t 0 1 9 C a t e g o r y C o d e G l 0 1 9 A m o u n t F i e l d
A l t e r n a t e C o m p a n y N a m e C a t e g o r y C o d e C o s t C t 0 2 0 U n i t s
D a t e f i s c a l y e a r b e g i n s j     [ F K ] C a t e g o r y C o d e C o s t C t 0 2 1 C a t e g o r y C o d e G l 0 2 0 U n i t O f M e a s u r e
P e r i o d N u m b e r C u r r e n t C a t e g o r y C o d e G l 0 2 1 G l C l a s s
W o r k e r s C o m p P r e m B a s e 1 C a t e g o r y C o d e C o s t C t 0 2 2 C a t e g o r y C o d e G l 0 2 2 R e v e r s e O r V o i d R V
C u r r e n c y C o n v e r Y N A R C a t e g o r y C o d e C o s t C t 0 2 3 C a t e g o r y C o d e G l 0 2 3 N a m e A l p h a E x p l a n a t i o n
S e a r c h T y p e S e c u r i t y s d f s d O b j e c t A c c o u n t A l t e r n a t e N a m e R e m a r k E x p l a n a t i o n
W o r k e r s C o m p P r e m B a s e 2 C a t e g o r y C o d e C o s t C e n t e r 2 5 S u b s i d i a r y A l t e r n a t e . R e f e r e n c e 1 J e V o u c h I n
| U s e C c F r A s s e t C s t | F l a g | C a t e g o r y C o d e C | o s t C e n t e r 2 6 |     |     |     |
| ----------------------------- | ------- | ------------------------- | --------------------- | --- | --- | --- |
U s e C c F o r D e p r e E x p F l g C a t e g o r y C o d e C o s t C e n t e r 2 7 R e f e r e n c e 2
|     |     | C a t e g o r y C o d e C | o s t C e n t e r 2 8 |     | R e f e r e n c e 3 A c c | o u n t R e c o n c i |
| --- | --- | ------------------------- | --------------------- | --- | ------------------------- | --------------------- |
U s e C c F r A c c u m D e p r e F l C a t e g o r y C o d e C o s t C e n t e r 2 9 D o c u m e n t P a y I t e m
U s e C c F o r R e v B i l l F l a g C a t e g o r y C o d e C o s t C e n t e r 3 0 O r i g i n a l D o c u m e n t N o
C o m M e t h o d I t d O r R e m 1 O r i g i n a l D o c u m e n t T y p e
B o o k T o T a x T a x A r e a O r i g i n a l D o c P a y I t e m
T a x Y e a r B e g i n M o n t h T a x E n t i t y C o m p a n y K e y P u r c h a s e
T a x Y e a r B e g i n M o n t h O l d T a x A r e a 1 C o m p a n y K e y O r i g i n a l
D a t e N e w T a x Y e a r E n d J T a x E x p l a n a t i o n C o d e 1 D o c u m e n t T y p e P u r c h a s e
G l I n t e r f a c e F l g P r o p E q T a x D e d u c t i o n C o d e s 1 A d d r e s s N u m b e r
| A d d r e s s B o o k I n t e r | f a c e | T a x D e d u c t i o n C | o d e s 2 | C h a r t o f A c c o u n t s R e f e r enceFile |                       |     |
| ------------------------------- | ------- | ------------------------- | --------- | ------------------------------------------------ | --------------------- | --- |
|                                 |         | T a x D e d u c t i o n C | o d e s 3 | K e y   D a t a                                  | C h e c k N u m b e r |     |
N u m b e r O f P e r i o d s N o r m a l T a x D e d u c t i o n C o d e s 4 O b j e c t A c c o u n t       [ P K 1 ] D a t e C h e c k J
|     |     | T a x D e d u c t i o n C | o d e s 5 |                               | D a t e C h e c k C l e a | r e d |
| --- | --- | ------------------------- | --------- | ----------------------------- | ------------------------- | ----- |
|     | .   | T a x D e d u c t i o n C | o d e s 6 | C o m p a n y       [ P K 2 ] | S e r i a l T a g N u m b | e r   |
N o n - K e y   D a t a
|                                   |         | TaxDeductionCodes7              |             | Description001                        |     |     |
| --------------------------------- | ------- | ------------------------------- | ----------- | ------------------------------------- | --- | --- |
| A d d r e s s B o o k M a s       | t e r   | T a x D e d u c t i o n C       | o d e s 8   | L e v e l O f D e t a il A cctCde     |     |     |
|                                   |         | T a x D e d u c t i o n C       | o d e s 9   | P o s t i n g E d i t                 |     |     |
| K e y   D a t a                   |         | T a x D e d u c t i o n C       | o d e s 1 0 | U n it O f M e a s u r e              |     |     |
| A d d r e s s N u m b e r         | [ P K1] | D is t rib u t e T a x C o      | d e 0 0 1   |                                       |     |     |
| Non-Key Data                      |         | DistributeTaxCode002            |             |                                       |     |     |
| A lte r nateAddressKey            |         | D i s t r i b u t e T a x C o   | d e 0 0 3   |                                       |     |     |
| Ta xI d                           |         | D i s t r i b u t e T a x C o   | d e 0 0 4   |                                       | .   | .   |
| NameAlpha                         |         | DistributeTaxCode005            |             |                                       |     |     |
| DescripCompressed                 |         | DistributeTaxCode006            |             | BatchControlRecords                   |     |     |
| CostCenter                        |         | DistributeTaxCode007            |             | Key Data                              |     |     |
| S t a n d a r d I n d u s t r y C | o d e   | D i s t r i b u t e T a x C o   | d e 0 0 8   | B a t c h T y p e       [ P K 1 ]     |     |     |
| L a n g u a g e P r e f e r e n   | c e     | . D i s t r i b u t e T a x C o | d e 0 0 9   | B a t c h N u m b e r       [ P K 2 ] |     |     |
A d d r e s s T y p e 1 D i s t r i b u t e T a x C o d e 0 1 0 A c c o u n t B a l a n c e s
| C r e d i t M e s s a g e |     | T a x O r D e d C o m p | S t a t 0 1 | N o n - K e y   D a t a |     |     |
| ------------------------- | --- | ----------------------- | ----------- | ----------------------- | --- | --- |
P e r s o n C o r p o r a t i o n C o d e T a x O r D e d C o m p S t a t 0 2 B a t c h S t a t u s K e y   D a t a
A d d r e s s T y p e 2 T a x O r D e d C o m p S t a t 0 3 B a t c h A p p r o v e d F o r P o s t A c c o u n t I d       [ P K 1 ]
A d d r e s s T y p e 3 T a x O r D e d C o m p S t a t 0 4 A m o u n t B a t c h E x p e c t e d C e n t u r y       [ P K 2 ]
|     |     | T a x O r D e d C o m p | S t a t 0 5 | U s e r I d | F i s c a l Y e a r 1     |   [ P K 3 ] |
| --- | --- | ----------------------- | ----------- | ----------- | ------------------------- | ----------- |
A d d r e s s T y p e 4 D a t e B a t c h J u l i a n F i s c a l Q t r F u t u r e U s e       [ P K 4 ]
A d d r e s s T y p e 5 T a x O r D e d C o m p S t a t 0 6 N o O f D o c u m e n t s E x p e c t e d L e d g e r T y p e       [ P K 5 ]
A d d r e s s T y p e P a y a b l e s T a x O r D e d C o m p S t a t 0 7 S u b l e d g e r       [ P K 6 ]
A d d r e s s T y p e R e c e i v a b l es T a x O r D e d C o m p S t a t 0 8 B a l a n c e D o c u m e n t s A m t s S u b l e d g e r T y p e       [ P K 7 ]
A d d T y p e C o d e 4 P u r c h T a x O r D e d C o m p S t a t 0 9 B a l a n c e d J o u r n a l E n t r i e s C u r r e n c y C o d e F r o m       [ P K 8 ]
| M i s c C o d e 3 |     | T a x O r D e d C o m p | S t a t 1 0 | A m o u n t E n t e r e d |     |     |
| ----------------- | --- | ----------------------- | ----------- | ------------------------- | --- | --- |
AddressTypeEmployee PostingEditCostCenter AmountDocumentsEntered Non-Key Data
SubledgerInactiveCode AllocaSummarizaMeth AuthorizedUserId Company
DateBeginningEffective InvstmtSummarizaMeth PostOutOfBalance AmtBeginningBalancePy
AddressNumber1st GlBankAccount IncludeBatchonIntegrityf AmountNetPosting001
AmountNetPosting002
| AddressNumber2nd |     | AllocationLevel      |     |     | AmountNetPosting003 |     |
| ---------------- | --- | -------------------- | --- | --- | ------------------- | --- |
| AddressNumber3rd |     | LaborLoadingMethod   |     |     | AmountNetPosting004 |     |
| AddressNumber4th |     | LaborLoadingFactor   |     |     |                     |     |
| AddressNumber6th |     | GlObjectAcctLabor    |     |     | AmountNetPosting005 |     |
| AddressNumber5th |     | GlObjctAcctLaborPrem |     |     | AmountNetPosting006 |     |

PayrollGeneralConstants EstablishmentConstantFile
Key Data Key Data
Company [PK1] CostCenter [PK1]
Non-Key Data Non-Key Data
GlInterfaceKeyGl CommonPaycycleGroup
GlInterfaceAcctPayabl EstablishmentType
ConsecutiveSubmission CostCenterIdNumber
PeInterfaceFlag CountyCodeSui
WorkHoursPerDay CountyTaxIdNumber
WorkDaysPerWeek RoutingCodeCheck
WorkWeeksPerYear DateBeginningEffective
WorkHoursPerYear DateEndingEffective
TaxArrearage JobCategory
CostCenterSearch TipAllocationMethod
SubsidiarySearch RateTipAllocationPer
BatchControlRequireGl AverageDaysPerMonth
ManagemntApprovalInput MinWageRate
Subsidiary DenominationMinimum
UserId BurdenDistrRule
ProgramId StMnimumWage
DateUpdated UserId
ModeEmployeeNumber ProgramId
CountryForPayroll DateUpdated
PayrollFiscalPeriod
PrInterfaceInvMgmt
FiscalYear1
DenominationMinimum
AnnualLeaveHours
LaborPremiumDistr
BurdenOverrideRule
LastCheckNumberPr
LastBankAdviseNo
LastPayslipNumber
TipProcessingFlag
CanadianPayrollFlag
CycleControlFlag
InterestRateStandard
MaximumDeferralRate
CompanyRetirementPlan
ExemptionType
AcctPayableMgmtAppr
BatchControlMgmtAppr
AcctRecMgmtAppr
DbaPeriodProcessing
SpendingAcctControl
SuiCalculationSwitch
CalculateVDITax

ItemBranchFile
Key Data
CostCenter   [PK2]  [FK]
SystemCode   [PK6]  [FK]
Lot   [PK7]  [FK]
IdentifierShortItem   [PK8]  [FK]
L o ca t i o n      [P K 9]  [FK]
|     | It e m C o st F ile |     | .   |     | N o n - K e y   D a ta |
| --- | ------------------- | --- | --- | --- | ---------------------- |
N o n -K e y  D ata
|     | I d e n t i f i e r 2 n d I t e m |                   |         | .                         | I d e n t i f i e r 2 n d I t e m     |
| --- | --------------------------------- | ----------------- | ------- | ------------------------- | ------------------------------------- |
|     | I d e n t i f i e r 3 r d I t e m |                   |         |                           | I d e n t i f i e r 3 r d I t e m     |
|     | L o t G r a d e                   |                   |         |                           | S a l e s R e p o r t i n g C o d e 1 |
|     |                                   |                   | I t e m | M a s t e r               | S a l e s R e p o r t i n g C o d e 2 |
|     | A m o u n t U n i t C o s         | t                 | N o n   | - K e y   D a t a         | S a l e s R e p o r t i n g C o d e 3 |
|     | C o s t i n g S e l e c t i o     | n P u r c h a s i |         |                           | S a l e s R e p o r t i n g C o d e 4 |
|     | C o s t i n g S e l e c t i o     | n I n v e n t o r | I d e n | t i f i e r 2 n d I t e m | S a l e s R e p o r t i n g C o d e 5 |
I t e m L o c a t i o n F i l e U s e r R e s e r v e d C o d e I d e n t i f i e r 3 r d I t e m S a l e s R e p o r t i n g C o d e 6
K e y   D a t a U s e r R e s e r v e d D a t e D e s c r i p t i o n L i n e 1 S a l e s R e p o r t i n g C o d e 7
| L o t       [ P K 1 ]     [ F K ] | U s e r R e s e r v e d A | m o u n t | D e s | c r i p t i o n L i n e 2 |     |
| --------------------------------- | ------------------------- | --------- | ----- | ------------------------- | --- |
C o s t C e n t e r       [ P K 2 ]     [ F K ] U s e r R e s e r v e d N u m b e r S e a r c h T e x t S a l e s R e p o r t i n g C o d e 8
I d e n t i f i e r S h o r t I t e m       [ P K 3 ]  [FK] U s e r R e s e r v e d R e f e r e n c e S e a r c h T e x t C o m p r e s s e d S a l e s R e p o r t i n g C o d e 9
L o c a t i o n       [ P K 4 ]     [ F K ] U s e r I d . S a l e s R e p o r t i n g C o d e 1 S a l e s R e p o r t i n g C o d e 1 0
|     | . P r o g r a m I d |     | S a l e | s R e p o r t i n g C o d e 2 | P u r c h a s i n g R e p o r t C o d e 1 |
| --- | ------------------- | --- | ------- | ----------------------------- | ----------------------------------------- |
S y s t e m C o d e       [ P K 5 ]     [ F K ] P u r c h a s i n g R e p o r t C o d e 2
N o n - K e y   D a t a W o r k S t a t i o n I d S a l e s R e p o r t i n g C o d e 3 P u r c h a s i n g R e p o r t C o d e 3
P r i m a r y B i n P S D a t e U p d a t e d . S a l e s R e p o r t i n g C o d e 4 . P u r c h a s i n g R e p o r t C o d e 4
G l C a t e g o r y T i m e O f D a y S a l e s R e p o r t i n g C o d e 5 P u r c h a s i n g R e p o r t C o d e 5
L o t S t a t u s C o d e S a l e s R e p o r t i n g C o d e 6 P u r c h R e p o r t i n g C o d e 6
| D a t e L a s t R e c e i p t 1 |     |     | S a l e | s R e p o r t i n g C o d e 7 |     |
| ------------------------------- | --- | --- | ------- | ----------------------------- | --- |
Q t y O n H a n d P r i m a r y U n S a l e s R e p o r t i n g C o d e 8 P u r c h R e p o r t i n g C o d e 7
|     |     |     | S a l e | s R e p o r t i n g C o d e 9 | P u r c h R e p o r t i n g C o d e 8 |
| --- | --- | --- | ------- | ----------------------------- | ------------------------------------- |
Q t y B a c k o r d e r e d I n P r i S a l e s R e p o r t i n g C o d e 1 0 P u r c h R e p o r t i n g C o d e 9
Q t y O n P u r c h a s e O r d e r P r P u r c h a s i n g R e p o r t C o d e 1 P u r c h R e p o r t i n g C o d e 1 0
Q u a n t i t y O n W o R e c e i p t P u r c h a s i n g R e p o r t C o d e 2 C o m m o d i t y C o d e
Q t y 1 O t h e r P r i m a r y U n P r o d u c t G r o u p F r o m
Q t y 2 O t h e r P r i m a r y U n P u r c h a s i n g R e p o r t C o d e 3 D i s p a t c h G r p
Q t y O t h e r P u r c h a s i n g 1 P u r c h a s i n g R e p o r t C o d e 4 P r i m a r y L a s t V e n d o rN o
Q t y H a r d C o m m i t t e d P u r c h a s i n g R e p o r t C o d e 5 A d d r e s s N u m b e r P l a n n e r
| Q u a n t i t y S o f t C o m m i t t e d |     |     | P u r c | h R e p o r t i n g C o d e 6 |     |
| ----------------------------------------- | --- | --- | ------- | ----------------------------- | --- |
Q t y O n F u t u r e C o m m i t . P u r c h R e p o r t i n g C o d e 7 B u y e r
|     |     |     | P u r c | h R e p o r t i n g C o d e 8 | G l C a t e g o r y |
| --- | --- | --- | ------- | ----------------------------- | ------------------- |
W o r k O r d e r S o f t C o m m i t P u r c h R e p o r t i n g C o d e 9 C o u n t r y O f O r i g i n
Q u a n t i t y O n W o r k o r d e r P u r c h R e p o r t i n g C o d e 1 0 R e o r d e r P o i n t I n p u t
Q t y I n T r a n P r i m a r y U n C o m m o d i t y C o d e R e o r d e r Q u a n t i t y I n p u t
Q t y I n I n s p P r i m a r y U n R e o r d e r Q u a n t i t y M a x i m u m
| Q u a n t i t y O n L o a n T o M a | L o c a t i o n M a | s t e r | P r o d | u c t G r o u p F r o m |     |
| ----------------------------------- | ------------------- | ------- | ------- | ----------------------- | --- |
| QuantityInboundWareh                | Key Data            |         |         |                         |     |
QuantityOutboundWare
CostCenter   [PK1]
Location   [PK2]
Non-Key Data
AisleLocation
BinLocation .
|           | CategoryCodeLocation003 |                           |                         |            | InventoryConstants                      |
| --------- | ----------------------- | ------------------------- | ----------------------- | ---------- | --------------------------------------- |
| .         | CategoryCodeLocation004 |                           |                         |            | Key Data                                |
|           | CategoryCodeLocation005 |                           |                         |            | SystemCode   [PK1]                      |
|           | CategoryCodeLocation006 |                           |                         |            | CostCenter   [PK2]                      |
|           | CategoryCodeLocation007 |                           |                         |            | Non-Key Data                            |
|           | CategoryCodeLocation008 |                           | ItemCostComponentAddOns |            | GLExplanation                           |
|           | C a t e g o r y C o     | d e L o c a t i o n 0 0 9 | K e                     | y  D a t a | . S y m T o I d e n t i fy S h r tI n v |
| LotMaster | C a t e g o r y C o     | d e L o c a t i o n 0 1 0 |                         |            |                                         |
Key Data LocationLevelOfDetail C o s tC e n t erAlt   [PK2] S y m T o I d e n t L o n g In v N
|             | StorageType |     | CostType   [PK6]         |     | SymToIdent3rdInvNu |
| ----------- | ----------- | --- | ------------------------ | --- | ------------------ |
| Lot   [PK1] |             |     | CostCenter   [PK7]  [FK] |     | SymToIdentCustomer |
CostCenter   [PK2] LocationCharacteristics SystemCode   [PK8]  [FK] DelimiterSegment
I d e n t i f i e r S h o r t I t e m       [ P K 3] H o l d C o d e L o c a t i o n N o n - K e y   D a t a S e p a r a t o r L o c a t i o n
N o n - K e y   D a t a F r e e z e R u l e I d e n t i f i e r 2 n d I t e m N u m b e r C h a r a c t e r s A i s
D e s c r i p t i o n L o t N e t t a b l e A l l o c a t a b l e N u m b e r C h a r a c t e r s B i n
L o t S t a t u s C o d e M i n i m u m U t i l i z a t i o n P e r c e n ta g e I d e n t i f i e r 3 r d I t e m N u m b e r C h a r a c t e r s C o d 0 3
I d e n t i f i e r 2 n d I t e m M i n i m u m P i c k P e r c e n t a g e L o t G r a d e N u m b e r C h a r a c t e r s C o d 0 4
|     | C o d e L o c a t i | o n T a x S t a t | A m | t C u r r e n t S t a n d a r d U n t |     |
| --- | ------------------- | ----------------- | --- | ------------------------------------- | --- |
I d e n t i f i e r 3 r d I t e m M e t h o d M o v e A m t S t d M f g C o s t S i m N u m b e r C h a r a c t e r s C o d 0 5
P r i m a r y L a s t V e n d o r N o P a l l e t T y p e S t a n d a r d C o s t R o l l u p N u m b e r C h a r a c t e r s C o d 0 6
C o m p a n y K e y O r d e r N o A m t S t d R o l l u p S i m N u m b e r C h a r a c t e r s C o d 0 7
D o c u m e n t O r d e r I n v o i c e E C a r t o n i z e F l a g S t a n d a r d F a c t o r C o d e F r o N u m b e r C h a r a c t e r s C o d 0 8
O r d e r T y p e M i x C o n t a i n e r s Y N S t a n d a r d F a c t o r C o d e S im N u m b e r C h a r a c t e r s C o d 0 9
V e n d o r L o t N u m b e r I te m M u l t i p l e D a t e s S t a n d a r d F a c t o r F r o z e n N u m b e r C h a r a c t e r s C o d 1 0
L o t P o t e n c y M a x i m u m N u m b e r O f I t e m s J u s t i f y A i s l e
L o t G r a d e S t a g i n g L o c a t i o n Y N S t a n d a r d F a c t o r S i m J u s t i f y B i n
D a t e L a y e r E x p i r a t i o n C o d e L o c a t i o n V e r i f i c a S t a n d a r d R a t e C o d e F r o J u s t i f y C o d e 3
|     | P u t a w a y C o | n f i r m a t i o n R e q u ir e d | S t a | n d a r d R a t e C o d e S i m |     |
| --- | ----------------- | ---------------------------------- | ----- | ------------------------------- | --- |
S e r i a l N u m b e r L o t P i c k i n g C o n f i r m a t i o n R e q u i r e d S t a n d a r d R a t e F r o z e n J u s t i f y C o d e 4
D a t e U s e r D e f i n e d D a t 0 0 1 A l l o w P u t a w a y Y N S t a n d a r d R a t e S i m J u s t i f y C o d e 5
D a t e U s e r D e f i n e d D a t 0 0 2 A l l o w P i c k Y N S t a n d a r d P r o c e s s i n g F la g J u s t i f y C o d e 6
D a t e U s e r D e f i n e d D a t 0 0 3 U s e r I d J u s t i f y C o d e 7
| D a t e U s e r D e f i n e d D a t 0 0 4 | A l l o w R e p l e | n i s h m e n t Y N | P r o | g r a m I d |     |
| ----------------------------------------- | ------------------- | ------------------- | ----- | ----------- | --- |
WorkStationId
DateUpdated

| CompanyConstantsJobCost |     |     |                   |     | AccountMaster |     |               |     |     |
| ----------------------- | --- | --- | ----------------- | --- | ------------- | --- | ------------- | --- | --- |
|                         |     |     | ExtendedJobMaster |     |               |     | AccountLedger |     |     |
| Key Data                |     |     | Key Data          |     | Key Data      |     | Key Data      |     |     |
Company   [PK1]  [FK] CostCenter   [PK1] AccountId   [PK1] CompanyKey   [PK1]
Non-Key Data
|     |     |     | Non-Key Data |     | Non-Key Data |     | DocumentType   [PK2] |     |     |
| --- | --- | --- | ------------ | --- | ------------ | --- | -------------------- | --- | --- |
WeeklyFiscalDatePat BudgetStartCentury Company DocVoucherInvoiceE   [PK3]
DateFiscalYearWeekly BudgetStartFiscalYear CostCenter DateForGLandVoucherJULIA   [PK4]
NumberOfPeriodsWeekly ObjectAccount JournalEntryLineNo   [PK5]
PeriodNumberCurrentW BudgetThruCentury LineExtensionCode   [PK6]
|     |     |     | BudgetThruFiscalYear |     | Subsidiary |     |     |     |     |
| --- | --- | --- | -------------------- | --- | ---------- | --- | --- | --- | --- |
DateJobCostMonthly ReportCodeSelection1 AccountNumber3rd Subledger   [PK12]  [FK]
DateJobCostWeekly ReportCodeSelection2 Description001 SubledgerType   [PK13]  [FK]
FileMaintOptions ReportCodeSelection3 LevelOfDetailAcctCde LedgerType   [PK7]  [FK]
| BudgetAuditTrail |     |     |     |     | BudgetPatternCode |     | Century   [PK9]  [FK] |     |     |
| ---------------- | --- | --- | --- | --- | ----------------- | --- | --------------------- | --- | --- |
ProjectionAuditTrail JobCostFutureConst6 FiscalYear1   [PK10]  [FK]
|     |     |     | JobCostFutureConst7 |     | PostingEdit |     |     |     |     |
| --- | --- | --- | ------------------- | --- | ----------- | --- | --- | --- | --- |
JobCostProjections JobCostFutureConst8 BillableYN FiscalQtrFutureUse   [PK11]  [FK]
CommitmentRelief JobCostFutureConst9 CurrencyCodeFrom CurrencyCodeFrom   [PK14]  [FK]
| CommittedDisplay      |     |     |                       |     | UnitOfMeasure                 |     | AccountId   [PK8]  [FK] |                        |            |
| --------------------- | --- | --- | --------------------- | --- | ----------------------------- | --- | ----------------------- | ---------------------- | ---------- |
| JobCostFutureConst1   |     |     |                       |     | CategoryCodeGl001             |     | Non-Key Data            |                        |            |
| JobCostFutureConst2   |     |     |                       |     | CategoryCodeGl002             |     | GLPostedCode            |                        |            |
|                       | .   |     |                       | .   | CategoryCodeGl003             |     | BatchNumber             |                        |            |
|                       |     |     |                       |     | CategoryCodeGl004             |     | BatchType               |                        |            |
|                       |     |     |                       |     | C a t e g o r y C o d e G l 0 | 0 5 | D a                     | t e B a t c h J u l ia | n          |
|                       |     |     |                       | .   | C a t e g o r y C o d e G l 0 | 0 6 |                         |                        |            |
|                       |     |     |                       |     |                               |     | D a                     | t e B a t c h S y s te | mDateJuliA |
|                       |     |     |                       |     | CategoryCodeGl007             |     | BatchTime               |                        |            |
| CompanyConstants      |     |     | CostCenterMaster      |     | CategoryCodeGl008             |     | Company                 |                        |            |
| Key Data              |     |     | Key Data              |     | CategoryCodeGl009             |     | AcctNoInputMode         |                        |            |
| Company   [PK1]  [FK] |     |     |                       |     | CategoryCodeGl010             |     | AccountModeGL           |                        |            |
|                       |     |     | CostCenter   [PK1]    |     | CategoryCodeGl011             |     |                         |                        |            |
| Non-Key Data          |     |     | Company   [PK2]  [FK] |     |                               |     | CostCenter              |                        |            |
| Name                  |     |     | Non-Key Data          |     | CategoryCodeGl012             |     | ObjectAccount           |                        |            |
A l t e r n a t e C o m p a n y N a m e C a t e g o r y C o d e G l 0 1 3 S u b s i d ia r y
D a t e f i s c a l y e a r b e g i n s j C o s t C e n t e r T y p e C a t e g o r y C o d e G l 0 1 4 P e r i o d N o G e n e r a l L e d g e
|                   |                     |     | D e s c r i p | C o m p r e s s e d      | C a t e g o r y C o d e G l 0 | 1 5 | C u | r r e n c y C o n v e | r R a te O v |
| ----------------- | ------------------- | --- | ------------- | ------------------------ | ----------------------------- | --- | --- | --------------------- | ------------ |
| P e r i o d N u m | b e r C u r r e n t |     | L e v e l O   | f D e t a i lC c C o d e | C a t e g o r y C o d e G l 0 | 1 6 |     |                       |              |
W o r k e r s C o m p P r e m B a s e1 A d d r e s s N u m b e r H i s t o r i c a l C u r r e n c y C o n v er
C u r r e n c y C o n v e r Y N A R A d d r e s s N u m b e r J o b A r C a t e g o r y C o d e G l 0 . 1 7 H i s t o r i c a l D a t e J u li a n
| SearchTypeSecurity   |     |     |                          |     |     |     | AmountField           |     |     |
| -------------------- | --- | --- | ------------------------ | --- | --- | --- | --------------------- | --- | --- |
|                      |     |     | County                   |     |     |     | Units                 |     |     |
| WorkersCompPremBase2 |     |     | State                    |     |     |     |                       |     |     |
| UseCcFrAssetCstFlag  |     |     | ModelAccountsandConsolid |     |     |     | UnitOfMeasure         |     |     |
| UseCcForDepreExpFlg  |     |     | Description001           |     |     |     | GlClass               |     |     |
| UseCcFrAccumDepreFl  |     |     | Description01002         |     |     |     | ReverseOrVoidRV       |     |     |
| UseCcForRevBillFlag  |     |     |                          |     |     |     | NameAlphaExplanation  |     |     |
|                      |     |     | Description01003         |     |     |     | NameRemarkExplanation |     |     |
| ComMethodItdOrRem1   |     |     | Description01004         |     |     |     |                       |     |     |
B o o k T o T a x C a t e g .o r y C o d e C o s t C t 0 0 1 R e f e r e n c e 1 J e V o u c h I n
T a x Y e a r B e g i n M o n t h C a t e g o r y C o d e C o s t C t 0 0 2 A c c o u n t B a l a n c e s R e f e r e n c e 2
T a x Y e a r B e g i n M o n t h O ld C a t e g o r y C o d e C o s t C t 0 0 3 R e f e r e n c e 3 A c c o u n t R e c onci
D a t e N e w T a x Y e a r E n d J K e y   D a t a D o c u m e n t P a y I t e m
|                     |                     |     | C a t e g o | r y C o d e C o s t C t 0 0 4 | A c c o u n t I d       [ P K 1 | ]   | O r | i g i n a l D o c u m | e n t N o |
| ------------------- | ------------------- | --- | ----------- | ----------------------------- | ------------------------------- | --- | --- | --------------------- | --------- |
| G l I n t e r f a c | e F l g P r o p E q |     | C a t e g o | r y C o d e C o s t C t 0 0 5 | C e n t u r y       [ P K 2 ]   |     |     |                       |           |
A d d r e s s B o o k I n t e r f a c e C a t e g o r y C o d e C o s t C t 0 0 6 O r i g i n a l D o c u m e n t T y p e
N u m b e r O f P e r i o d s N o r m al C a t e g o r y C o d e C o s t C t 0 0 7 F i s c a l Y e a r 1       [ P K 3 ] O r i g i n a l D o c P a y I t e m
F i s c a l D a t e P a t t e r n C a t e g o r y C o d e C o s t C t 0 0 8 F i s c a l Q t r F u t u r e U s e       [ P K 4 ] C o m p a n y K e y P u r c h a s e
P e r i o d N o F i n a n c i a l R e p L e d g e r T y p e       [ P K 5 ] C o m p a n y K e y O r i g i n a l
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 0 9 | S u b l e d g e r       [ P K 6 | ]                   | D o       | c u m e n t T y p e | P u r c h a s e |
| ------------------------ | ----------------------------- | --- | --------------------- | ----------------------------- | ------------------------------- | ------------------- | --------- | ------------------- | --------------- |
| F i n a n c i a l R      | e p o r t i n g Y e a r       |     | C a t e g o           | r y C o d e C o s t C t 0 1 0 | S u b l e d g e r T y p e       |   [ P K 7 ]         |           |                     |                 |
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 1 1 |                                 |                     | A d       | d r e s s N u m b e | r               |
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 1 2 | C u r r e n c y C o d e F r     | o m       [ P K 8 ] | C h       | e c k N u m b e r   |                 |
|                          |                               |     |                       |                               | N o n -K e y  Data              |                     | DateCheck | J                   |                 |
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 1 3 | C o m p a n y                   |                     |           | .                   | .               |
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 1 4 |                                 |                     |           |                     |                 |
|                          |                               |     | CategoryCodeCostCt015 |                               | AmtBeginningBalancePy           |                     |           |                     |                 |
| ProfitRecognitionHistory |                               |     | CategoryCodeCostCt016 |                               | AmountNetPosting001             |                     |           |                     |                 |
| Key Data                 |                               |     | CategoryCodeCostCt017 |                               | AmountNetPosting002             |                     |           |                     |                 |
|                          |                               |     |                       |                               | A m o u n t N e t P o s t i     | n g 0 0 3           |           |                     |                 |
| V e r s i o n       [    | P K 1 ]                       |     | C a t e g o           | r y C o d e C o s t C t 0 1 8 | A m o u n t N e t P o s t i     | n g 0 0 4           |           |                     |                 |
| C o s t C e n t e        | r       [ P K 2 ]     [ F K ] |     | C a t e g o           | r y C o d e C o s t C t 0 1 9 |                                 |                     |           |                     |                 |
| S u b l e d g e r        |       [ P K 3 ]               |     | C a t e g o           | r y C o d e C o s t C t 0 2 0 | A m o u n t N e t P o s t i     | n g 0 0 5           |           |                     |                 |
| S u b l e d g e r        | T y p e       [ P K 4 ]       |     | C a t e g o           | r y C o d e C o s t C t 0 2 1 | A m o u n t N e t P o s t i     | n g 0 0 6           |           |                     |                 |
|                          |                               |     | C a t e g o           | r y C o d e C o s t C t 0 2 2 | A m o u n t N e t P o s t i     | n g 0 0 7           |           |                     |                 |
D a t e E f f e c t i v e       [ P K 5 ] A m o u n t N e t P o s t i n g 0 0 8 D r a w R e p o r t i n g M a s t e r F i l e
| T y p e O f R e | c o r d       [ P K 6 ]   |     | C a t e g o | r y C o d e C o s t C t 0 2 3 | A m o u n t N e t P o s t i | n g 0 0 9 |           |       |     |
| --------------- | ------------------------- | --- | ----------- | ----------------------------- | --------------------------- | --------- | --------- | ----- | --- |
| C o m p a n y   |     [ P K 7 ]     [ F K ] |     | s d f s d   |                               |                             |           | K e y   D | a t a |     |
N o n - K e y   D a t a C a t e g o r y C o d e C o s t C e n t e r 2 5 A m o u n t N e t P o s t i n g 0 1 0 D o c u m e n t T y p e       [ P K 1 ]     [ F K ]
|                 |                   |     | C a t e g o | r y C o d e C o s t C e n t e r 2 6 | A m o u n t N e t P o s t i | n g 0 1 1 | D o c V o | u c h e r I n v o i c e | E       [ P K 2 ]     [ F K ] |
| --------------- | ----------------- | --- | ----------- | ----------------------------------- | --------------------------- | --------- | --------- | ----------------------- | ----------------------------- |
| M e t h o d P r | o f i t R e c o g | .   | C a t e g o | r y C o d e C o s t C e n t e r 2 7 | A m o u n t N e t P o s t i | n g 0 1 2 |           |                         |                               |
N e x t N u m b e r V a l u e A m o u n t N e t P o s t i n g 0 1 3 D a te F o r G L a n d V o u c h e r J U L I A      [ P K3]  [FK]
D e f e r r e d P r o f i t R e c o n g n i C a t e g o r y C o d e C o s t C e n t e r 2 8 A m o u n t N e t P o s t i n g 0 1 4 J o u r n a l E n t r y L i n e N o       [ P K 4 ]    [ F K ]
P r o f i t T h r e s h o l d P e r c e n t C a t e g o r y C o d e C o s t C e n t e r 2 9 S u b l e d g e r       [ P K 1 2 ]     [ F K ]
|                    |     |     | CategoryCodeCostCenter30 |     |     |     | SubledgerType   [PK13]  [FK]    |     |     |
| ------------------ | --- | --- | ------------------------ | --- | --- | --- | ------------------------------- | --- | --- |
| CostOriginalBudget |     |     | TaxArea                  |     |     |     | AccountId   [PK14]  [FK]        |     |     |
| RevnOriginalBudget |     |     | TaxEntity                |     |     |     |                                 |     |     |
| CostChanges        |     |     |                          |     |     |     | CompanyKey   [PK5]  [FK]        |     |     |
| RevnChanges        |     |     | TaxArea1                 |     |     |     | LineExtensionCode   [PK6]  [FK] |     |     |
ActualCostToDate TaxExplanationCode1 LedgerType   [PK7]  [FK]
|     |     |     | TaxDeductionCodes1 |     |     |     | Century   [PK8]  [FK] |     |     |
| --- | --- | --- | ------------------ | --- | --- | --- | --------------------- | --- | --- |
ActualRevnToDate TaxDeductionCodes2 FiscalYear1   [PK9]  [FK]
| CostProjectedFinal    |     |     | TaxDeductionCodes3 |     |     |     |                                   |     |     |
| --------------------- | --- | --- | ------------------ | --- | --- | --- | --------------------------------- | --- | --- |
| CostProjectedFinalAdj |     |     |                    |     |     |     | FiscalQtrFutureUse   [PK10]  [FK] |     |     |
RevnProjectedFinal TaxDeductionCodes4 CurrencyCodeFrom   [PK11]  [FK]
| RevnProjectedFinalAdj |     |     | TaxDeductionCodes5 |     |     |     | Non-Key Data |     |     |
| --------------------- | --- | --- | ------------------ | --- | --- | --- | ------------ | --- | --- |
TaxDeductionCodes6
| StoredMaterials      |     |     | TaxDeductionCodes7  |     |     |     | Company       |     |     |
| -------------------- | --- | --- | ------------------- | --- | --- | --- | ------------- | --- | --- |
| JobToDateEarnedCost  |     |     |                     |     |     |     | CostCenter    |     |     |
| JobToDateEarnedReven |     |     | TaxDeductionCodes8  |     |     |     | Subsidiary    |     |     |
| CostEarnedPriorYr    |     |     | TaxDeductionCodes9  |     |     |     | ObjectAccount |     |     |
| RevnEarnedPriorYr    |     |     | TaxDeductionCodes10 |     |     |     |               |     |     |
DistributeTaxCode001

MenuMasterFile
MenuSelectionsFile
| Key Data | Key Data |     |
| -------- | -------- | --- |
MenuIdentification   [PK1]
MenuIdentification   [PK1]  [FK]
Non-Key Data
MenuSelection   [PK2]
| SystemCode       | Non-Key Data |     |
| ---------------- | ------------ | --- |
| MenuAdvancedOper | JobToExecute |     |
MenuTechnicalOperMenu
SelectionBatchDesignatio
| LevelOfMenu | HelpStartKey |     |
| ----------- | ------------ | --- |
ClientMenuDisplayStyle
OptionCode
| TextIconDisplay | OptionKey |                      |
| --------------- | --------- | -------------------- |
| ClientMenuType  |           | MenuTextOverrideFile |
Versionconsolidated
| UserId | RunTimeMessage | Key Data |
| ------ | -------------- | -------- |
ProgramId
| .           | MenuSelectionHighlight | MenuIdentification   [PK1]  [FK] |
| ----------- | ---------------------- | -------------------------------- |
| DateUpdated |                        | MenuSelection   [PK2]  [FK]      |
MenutoExecute
| WorkStationId     | MenuSelectionType        | LanguagePreference   [PK3] |
| ----------------- | ------------------------ | -------------------------- |
| TimeLastUpdated   | .                        |                            |
|                   | MenuCountryRegionCodes   | Non-Key Data               |
| AuthorizationMask | SystemCodeApplicationOve | MenuText                   |
JobMask
|               | ProcessingOptionIdentifi | UserId    |
| ------------- | ------------------------ | --------- |
| KnowledgeMask | ApplicationIdentifier    | ProgramId |
DepartmentMask
|               | FormIdentifier | DateUpdated |
| ------------- | -------------- | ----------- |
| FutureUseMask | IconIdentifier |             |
WorkStationId
|     | RunMinimized | TimeLastUpdated |
| --- | ------------ | --------------- |
SelectionConsequences.
UserId
ProgramId
DateUpdated
MenuPathFile
WorkStationId
|     | TimeLastUpdated   | Key Data                         |
| --- | ----------------- | -------------------------------- |
|     | AuthorizationMask | MenuIdentification   [PK1]  [FK] |
|     | JobMask           | MenuSelection   [PK2]  [FK]      |
|     | KnowledgeMask     | PathType   [PK3]                 |
|     | DepartmentMask    | Non-Key Data                     |
|     | FutureUseMask     | Path                             |
|     | ObjectName        | UserId                           |
FormName
ProgramId
DateUpdated
WorkStationId
TimeLastUpdated

|                           | CrossReferenceFieldRelationship      | TableConversionJDEScheduler |
| ------------------------- | ------------------------------------ | --------------------------- |
| VersionsList              | Key Data                             | Key Data                    |
| Key Data                  | NameObject   [PK1]  [FK]             |                             |
| ProgramId   [PK1]         |                                      | NameObject   [PK1]  [FK]    |
|                           | FileFormatName   [PK2]               | ReleaseNumber   [PK2]       |
| V e r si o n     [P K 2 ] | D a ta F l d N a m e       [ P K 3 ] |                             |
N a m e O b je c t    [ PK3] Pr im a r y O b j ec t       [ P K 4 ] Non-Key Data
CnvType
| Non-Key Data | PrimaryAttr   [PK5]    | ConversionTypeSeq |
| ------------ | ---------------------- | ----------------- |
| REPORT_ID    | Description001   [PK6] |                   |
| Version_ID   | KeySequence   [PK7]    | ProgramName       |
Version
| VersionTitle     | FunctionName   [PK8] | ConversionGroup       |
| ---------------- | -------------------- | --------------------- |
| UserExclusive12  | Application   [PK9]  |                       |
| UserId           | Non-Key Data         | UserReservedNumber    |
| DateLastChanged  |                      | UserReservedReference |
|                  | ID                   | UserReservedCode      |
| DateLastExecuted |                      | ProgramId             |
PROCESSING_OPTION_TEMPLATE_ID .
| ProcessingOptionIdentifi |     | WorkStationId |
| ------------------------ | --- | ------------- |
UserId
| UBEOptionCode |     | DateUpdated |
| ------------- | --- | ----------- |
VERSION_LIST_MODE
| VERSION_TEXT_ID  |                            | TimeLastUpdated |
| ---------------- | -------------------------- | --------------- |
|                  | ObjectLibrarianMasterTable | .               |
| Check_Out_Status | Key Data                   |                 |
Check_Out_Date
| User .               | NameObject   [PK1] |                     |
| -------------------- | ------------------ | ------------------- |
| Version_Availability | Non-Key Data       | FormInformationFile |
Key Data
| EnvironmentName | MemberDescription       |                          |
| --------------- | ----------------------- | ------------------------ |
| MachineKey      | SystemCode              | FormName   [PK1]         |
| ProcOptData     | SystemCodeReporting     | NameObject   [PK2]  [FK] |
|                 | FunctionCodeOpenSystems | Non-Key Data             |
|                 | FunctionUse             | FormIdentifier           |
|                 | PrefixFile              | MemberDescription        |
SourceLanguage
FormProcessType
|     | AnsiYN         | ReleaseNumber |
| --- | -------------- | ------------- |
|     | ObjectCatagory | Entry         |
CommonLibFileYOrN
| ObjectLibrarianStatusDetail |                           | Point                           |
| --------------------------- | ------------------------- | ------------------------------- |
| Key Data                    | C o p y D a t a W ithFile | S ys t e m C o d e              |
|                             | O m it O p t i o n        | Fu n c t ion C o d eOpenSystems |
| NameObject   [PK1]  [FK]    | OptionalDataFile          | Application                     |
| MachineKey   [PK2]          | Application               | .                               |
| CodePath   [PK3]            |                           | ID                              |
|                             | ID                        | HELP_ID                         |
| Non-Key Data                | CurrencyLogicType         | HelpFileName                    |
| EnvironmentName .           | BusinessFunctionLocation  |                                 |
VersionJDE
| UserId       | GlobalBuildOption | ModificationFlag  |
| ------------ | ----------------- | ----------------- |
| DateModified | NameTextFile      | MergeOption       |
| VersionJDE   | TypeText          | CategoriesForm001 |
SarNumberModify
|                       | GenericTextFutureUse | CategoriesForm002 |
| --------------------- | -------------------- | ----------------- |
| StatusCodeOpenSystems | JDETextYN            | CategoriesForm003 |
DevelopmentProgressCd ProcessingOptionIDEveres CategoriesForm004
| ModificationFlag | MemberIdAlt |     |
| ---------------- | ----------- | --- |
CategoriesForm005
| MergeOption         | BaseMemberName   | UserId    |
| ------------------- | ---------------- | --------- |
| ReleaseNumber       | ParentDLLLibrary | ProgramId |
| ModificationComment | ParentObject     |           |
WorkStationId
| ProgramId     | PackageCollection     | DateUpdated     |
| ------------- | --------------------- | --------------- |
| WorkStationId | ObjectLibrarianCode01 | TimeLastUpdated |
| DateUpdated   | ObjectLibrarianCode02 |                 |
TimeLastUpdated
ObjectLibrarianCode03
ObjectLibrarianCode04
|     | ObjectLibrarianCode05 | .   |
| --- | --------------------- | --- |
ProgramId
UserId
|     | WorkStationId | ObjectLibrarianFunctionDetail |
| --- | ------------- | ----------------------------- |
| .   | DateUpdated   | Key Data                      |
CrossReferenceRelationships NameObject   [PK1]  [FK]
Key Data TimeLastUpdated
FunctionName   [PK2]
NameObject   [PK1]  [FK] Non-Key Data
MemberDescription
EVENT_DESCRIPTION_ID
. BusinessFunctionID
DS_Template_ID
VersionJDE
ModificationFlag
| CheckoutLogTable | .                                | MergeOption              |
| ---------------- | -------------------------------- | ------------------------ |
| Key Data         | ObjectLibrari anObjectRelationsh |                          |
| UserId   [PK1]   | Key Data                         | BusinessFunctionCategory |
BusinessFunctionCat2
DateUpdated   [PK2] NameObject   [PK1]  [FK] BusinessFunctionCat3
| TimeLastUpdated   [PK3] | FunctionCodeOpenSystems   [PK2] |     |
| ----------------------- | ------------------------------- | --- |
NameObject   [PK4]  [FK] RelatedNameObject   [PK3] BusinessFunctionCat4
BusinessFunctionCat5
| Non-Key Data        | Non-Key Data | UserId    |
| ------------------- | ------------ | --------- |
| SubmittalStatusCode | VersionJDE   | ProgramId |
ActionCode1
|                         | ModificationFlag | WorkStationId   |
| ----------------------- | ---------------- | --------------- |
| Description001          | MergeOption      | DateUpdated     |
| FunctionCodeOpenSystems | ProgramId        | TimeLastUpdated |
| Application             | UserId           |                 |
| ID                      | WorkStationId    |                 |
| Descript80Characters    | DateUpdated      |                 |
TimeLastUpdated

|                                 |     |                    |     |     | PrimaryIndexHeader |     |     | TableColumns |     |
| ------------------------------- | --- | ------------------ | --- | --- | ------------------ | --- | --- | ------------ | --- |
| ReportDesignAidSpecificationInf |     | PrimaryIndexDetail |     |     | Key Data           |     |     | Key Data     |     |
Key Data Key Data TableIDEverest   [PK1]  [FK] TableIDEverest   [PK1]  [FK]
NameObject   [PK7]  [FK] TableIDEverest   [PK1]  [FK] NameObject   [PK3]  [FK] NameObject   [PK2]  [FK]
REPORT_ID   [PK1] NameObject   [PK4]  [FK] IndexIdentifierEverest   [PK2] DataDictionaryIdentifier   [PK3]
R e c o r d T y p e E v e re s t       [ P K 2 ] I n d e x I d e n t if i e r E v e r e s t       [ P K 2 ]    [FK] N o n - K e y   D a t a D D O b j e c t N a m e E v er e s t     [ PK4]
G e n e r i c I D 1 E v e r e s t       [ P K 3 ] D a t a D i c t i o n a r y Id e n t i f i e r      [ P K 3 ] D e s c r i p t i o n N o n - K e y   D a ta
G E V e n E e R r E i c S I D T 2 W E E v e V r E e N s t T           [   P [ P K K 4 5 ] ] N o n - K e y   D a t a P r i m a r y T a b l e F la g E v e r es t P r o g r a m S e q u e n c e
G e n e r i c I D 3 E v e r e s t       [ P K 6 ] D e s c r i p t i o n U n i q u e K e y s S Q L C o l u m n N a m e E v e r e s t
N o n - K e y   D a ta D D O b j e c t N a m e E v e r e s t N u m b e r o f I n d e x D e ta i ls E v er C o l u m n I D E v e r e s t
|     |     | K e y C o l u m n S e | q u e n c e E v e r e s t |     | . V e r | s i o n J D E |     | V e r s i o n J | D E |
| --- | --- | --------------------- | ------------------------- | --- | ------- | ------------- | --- | --------------- | --- |
ControlID R e p o rt D e s ignBlob SortOrderEverest ModificationFlag ModificationFlag
Ve r s io n J D E C o m p a r is o nFieldEverest M e r g e O p t io n . M e r g e O p t io n
ModificationFlag Ve ModificationFlag r si o n J D E Fl a g F u tu r e U se1 Fl a g F u tu r e U se1
| MergeOption    |     | MergeOption    |     |     | FlagFutureUse2 |     |     | FlagFutureUse2 |     |
| -------------- | --- | -------------- | --- | --- | -------------- | --- | --- | -------------- | --- |
| FlagFutureUse1 |     | FlagFutureUse1 |     |     |                |     |     |                |     |
| FlagFutureUse2 |     | FlagFutureUse2 |     |     |                |     |     |                |     |
TableHeader
|     |     |     | ObjectLibrarianMasterTable |     |     |     |     | Key Data |     |
| --- | --- | --- | -------------------------- | --- | --- | --- | --- | -------- | --- |
ReportDesignAidTextInformation Key Data TableIDEverest   [PK1]
| Key Data                 |     |     | NameObject   [PK1] |     |     |     |     | NameObject   [PK2]  [FK] | .   |
| ------------------------ | --- | --- | ------------------ | --- | --- | --- | --- | ------------------------ | --- |
| NameObject   [PK5]  [FK] |     |     | Non-Key Data       |     |     |     |     | Non-Key Data             |     |
| REPORT_ID   [PK1]        |     |     | MemberDescription  |     |     |     |     | TotalNumberofColumnsinTa |     |
| TextIDEverest   [PK2]    |     |     | SystemCode         |     |     |     |     | TotalNumberofPrimaryIndi |     |
LanguagePreference   [PK3] SystemCodeReporting TotalNumberofForeignIndi
| SystemCode   [PK4]                                |     |     | FunctionCodeOpenSystems   |                            |     |                                         |     | VersionJDE                  |     |
| ------------------------------------------------- | --- | --- | ------------------------- | -------------------------- | --- | --------------------------------------- | --- | --------------------------- | --- |
| Non-Key Data                                      |     |     | FunctionUse               |                            |     |                                         |     | ModificationFlag            |     |
| ReportDesignBlob                                  |     | .   | PrefixFile                |                            |     |                                         |     | MergeOption                 |     |
| V e r s i o n J D E                               |     |     | .S o u r ce Language      |                            |     |                                         |     | F l a g F u t u r e U s e 1 |     |
| M o d i f ic a t io nFlag                         |     |     | A ObjectCatagory n si Y N |                            |     |                                         |     | F l a g F u t u r e U s e 2 |     |
| MergeOption                                       |     |     | CommonLibFileYOrN         |                            |     |                                         |     |                             |     |
| FlagFutureUse1                                    |     |     | CopyDataWithFile          |                            |     |                                         |     |                             |     |
| FlagFutureUse2                                    |     |     | OmitOption                |                            |     |                                         |     |                             |     |
|                                                   |     |     | OptionalDataFile          |                            |     | BusinessViewSpecifications              |     |                             |     |
|                                                   |     |     | Application               |                            |     | Key Data                                |     |                             |     |
|                                                   |     |     | ID                        |                            |     | NameObject   [PK2]  [FK]                |     |                             |     |
|                                                   |     |     | C u rr e n c              | y L o g i c T y p e        |     | B u s in e s s V ie w IDEverest   [PK1] |     |                             |     |
| JDEBLCBehaviorInformation                         |     | .   | Bu s i n e s              | s F u n c t io n L ocation |     | N o n - K e y  D a ta                   |     |                             |     |
| K e y   D a t a                                   |     |     | G l o b a l B             | u i l d O p t i o n        | .   | B u s in e s s V i e w B lob            |     |                             |     |
| N a m e O b j e c t       [ P K 2 ]     [ F K ]   |     |     | N a m e T                 | e x t F i l e              |     | V e r s i o n J D E                     |     |                             |     |
| B e h a v i o r I D E v e r e s t       [ P K 1 ] |     |     | T y p e T e               | x t                        |     | M o d i f i c a t i o n F l a g         |     |                             |     |
| N o n - K e y   D a t a                           |     | .   | G e n e r i c             | T e x t F u t u r e U s e  |     | M e r g e O p t i o n                   |     |                             |     |
S o u r c e F i l e N a m e E v e r e s t J D E T e x t Y N F l a g F u t u r e U s e 1 . F o r m s D e s i g n A i d / S o f t w a r eVersions
R e p o r t D e s i g n B l o b P r o c e s s i n g O p t i o n I D E v eres F l a g F u t u r e U s e 2 K e y   D a t a
V e r s i o n J D E M e m b e r I d A l t N a m e O b j e c t      [ P K 2 ]     [ F K ]
M o d i f i c a t i o n F l a g B a s e M e m b e r N a m e A p p li c a t i o n      [ P K 1 ]     [ F K ]
M e r g e O p t i o n P a r e n t D L L L i b r a r y N o n - K e y   D a t a
| F l a g F u t u r e U s e 1 |     |     | P a r e n t O | b j e c t |     |     |     |     | I D |
| --------------------------- | --- | --- | ------------- | --------- | --- | --- | --- | --- | --- |
F l a g F u t u r e U s e 2 P O a b c j e k c a t g L e i b C r a o r l l i e a c n t C i o o n d e 0 1 F o r m s D e s i g n B l o b
|                       |     |     | ObjectLibrarianCode02 |            |     |                          |                       |     | VersionJDE       |
| --------------------- | --- | --- | --------------------- | ---------- | --- | ------------------------ | --------------------- | --- | ---------------- |
|                       |     |     | ObjectLibrarianCode03 |            |     |                          |                       |     | ModificationFlag |
|                       |     |     | ObjectLibrarianCode04 |            |     | DataStructureTemplates   |                       |     | MergeOption      |
|                       |     |     | ObjectLibrarianCode05 |            |     | Key Data                 |                       |     | FlagFutureUse1   |
|                       |     |     | ProgramId             |            |     | NameObject   [PK3]  [FK] |                       |     | FlagFutureUse2   |
|                       |     |     | U s e r I d           |            |     | E V E R E S T T M P      | L I D      [ P K 1 ]  |     |                  |
| M e d i a O b j e c t |     |     | W o r k S ta          | t i o n Id |     | E V E R E S T T M P      | L N M       [ P K 2 ] |     |                  |
K e y   D a t a D a t e U p d a te d N o n - K e y   D a t a .
| N a m e O b j e c t       [ P K 5 ]    [ F K ]    |       |                                           | Ti m e L a | s t U p d ated |     |                                                         |                         |     |     |
| ------------------------------------------------- | ----- | ----------------------------------------- | ---------- | -------------- | --- | ------------------------------------------------------- | ----------------------- | --- | --- |
| T e x t T y p e E v e r e s t       [ P K 1 ]     |       |                                           |            |                |     | . D E v a e t a n S t R t r u u l c e t s u B r e l o T | b e m p l a t e T y p e |     |     |
| T e x t I D E v e r e s t      [ P K 2 ]          | E v e | n t R u l esLinkTable                     |            |                |     | V e r s i o n J D E                                     |                         |     |     |
| L a n g u a g e P r e f e r e n c e       [ P K3] | K e   | y   D a t a .                             |            |                |     | M o d i f i c a t i o n F l a                           | g                       |     |     |
| S y s t e m C o d e       [ P K 4 ]               | N a m | e O b j e c t       [ P K 7 ]     [ F K ] |            |                |     | M e r g e O p t io n                                    |                         |     |     |
| N o n - K e y   D a t a                           | E V E | R E S T P T       [ P K 1 ]               |            |                |     | F l a g F u t u r e U s e                               | 1                       |     |     |
| E v e n t R u l e s B l o b                       | A p p | l i c a t i o n       [ P K 2 ]           |            |                | .   | F l a g F u t u r e U s e                               | 2                       |     |     |
V e r s i o n J D E F R M I D E V E R E S T       [ P K 3 ] F o r m s D e s i g n A i d /S o f t w a r eVers2
| M M o e d r g i f e i c O a p t i t o i o n n F l a g | C o n | t r o l I D       [ P K 4 ] |     |     |     |     |     |     |     |
| ----------------------------------------------------- | ----- | --------------------------- | --- | --- | --- | --- | --- | --- | --- |
F l a g F u t u r e U s e 1 E V E R E S T W E V E N T       [P K 5] K e y   D a t a
F l a g F u t u r e U s e 2 E V E R E S T E R I D 3       [ P K 6 ] N a m e O b j e c t      [ P K 2 ]    [ F K ]
|     | N o           | n - K e y   D a t a |     |     |     |     |     | A p p li c a | t i o n      [ P K 1 ] |
| --- | ------------- | ------------------- | --- | --- | --- | --- | --- | ------------ | ---------------------- |
|     | EVERESTEVSPEC |                     |     |     |     |     |     | Non-Key Data |                        |
|     | ID            |                     |     |     |     |     |     | ID.          |                        |
E v e n t R u l esSpecificationTable E v e n t R u l e s B l o b F o r m s D e s i g nB l ob
| K e y   D a t a | V e r | s i o n J D E |     |     |     |     |     | V e r s i o | n J D E |
| --------------- | ----- | ------------- | --- | --- | --- | --- | --- | ----------- | ------- |
E V E R E S T E V S P E C      [P K 1] M o d i f i c a t i o n F l a g M M o e d r g i f e ic O a p t i t o io n n F la g
E V E R E S T E V S E Q     [ P K 2] . M e r g e O p t io n Fl a g F u tu r e U se1
N am eO bj e ct      [ P K 3 ]    [ F K ] Fl a g F u tu r e U se1 F o rm s D e signAidTextInformation FlagFutureUse2
| EV ER ES T P T       [P K 4 ]     [F K ] | FlagFutureUse2 |     |     | .   |     | K e y  D a ta |     |     |     |
| ---------------------------------------- | -------------- | --- | --- | --- | --- | ------------- | --- | --- | --- |
Application   [PK5]  [FK]
| FRMIDEVEREST   [PK6]  [FK]  |     |                                 |     |     |     | NameObject   [PK5]  [FK] Application   [PK1] |     |     |     |
| --------------------------- | --- | ------------------------------- | --- | --- | --- | -------------------------------------------- | --- | --- | --- |
| ControlID   [PK7]  [FK]     |     |                                 |     |     |     | TextIDEverest   [PK2]                        |     |     |     |
| EVERESTWEVENT   [PK8]  [FK] |     |                                 |     |     |     | LanguagePreference   [PK3]                   |     |     |     |
| EVERESTERID3   [PK9]  [FK]  |     | FormsDesignAidSpecificationInfo |     |     |     | SystemCode   [PK4]                           |     |     |     |
| Non-Key Data                |     | Key Data                        |     |     |     | Non-Key Data                                 |     |     |     |
| EventRulesBlob              |     | NameObject   [PK7]  [FK]        |     |     |     | ID                                           |     |     |     |
| VersionJDE                  |     | Application   [PK1]             |     |     |     | FormsDesignBlob                              |     |     |     |
| ModificationFlag            |     | RecordTypeEverest   [PK2]       |     |     |     | VersionJDE                                   |     |     |     |
| MergeOption                 |     | GenericID1Everest   [PK3]       |     |     |     | ModificationFlag                             |     |     |     |
| FlagFutureUse1              |     | GenericID2Everest   [PK4]       |     |     |     | MergeOption                                  |     |     |     |
| FlagFutureUse2              |     | EVERESTWEVENT   [PK5]           |     |     |     | FlagFutureUse1                               |     |     |     |
|                             |     | GenericID3Everest   [PK6]       |     |     |     | FlagFutureUse2                               |     |     |     |
Non-Key Data
ControlID
ID
FormsDesignBlob
VersionJDE
ModificationFlag
MergeOption
FlagFutureUse1
FlagFutureUse2

DataItemMaster
Key Data
DataItem   [PK1]
DataItemAlphaDescriptions
Non-Key Data
|     |     | SystemCode | Key Data |     |
| --- | --- | ---------- | -------- | --- |
DataItem   [PK1]  [FK]
. SystemCodeReporting
|     |     | GlossaryGroup | LanguagePreference   [PK2] |     |
| --- | --- | ------------- | -------------------------- | --- |
SystemCodeReporting   [PK3]
UserId
|     |     | ProgramId | . ScreenName   [PK4] |     |
| --- | --- | --------- | -------------------- | --- |
|     | .   |           | Non-Key Data         |     |
DateUpdated
|     |     | WorkStationId | DescriptionAlpha |     |
| --- | --- | ------------- | ---------------- | --- |
.
|                      |     | TimeLastUpdated | DescCompressed |     |
| -------------------- | --- | --------------- | -------------- | --- |
| DataFieldDisplayText |     |                 |                | .   |
Key Data
DataItem   [PK1]  [FK]
| LanguagePreference   [PK2]  |     |                                 | MediaObjectsstorage |     |
| --------------------------- | --- | ------------------------------- | ------------------- | --- |
| SystemCodeReporting   [PK3] |     |                                 | Key Data            |     |
| Non-Key Data                |     | DataFieldSpecifications(OneWorl |                     |     |
NameObject   [PK1]
| ColTitle1XrefBuild |     | Key Data | GenericTextKey   [PK2] |     |
| ------------------ | --- | -------- | ---------------------- | --- |
DataItem   [PK1]  [FK]
| ColTitle2XrefBuild |     |               | LanguagePreference   [PK3] |     |
| ------------------ | --- | ------------- | -------------------------- | --- |
| ColTitle3XrefBuild |     | Non-Key Data  | Non-Key Data               |     |
| DescriptionRow     |     | DataItemClass |                            |     |
GenericTextProcOptions
|     |     | DataItemType | CreatedByUser |     |
| --- | --- | ------------ | ------------- | --- |
DataItemSize
DateQuestionEntered
|     |     | DataFileDecimals | TimeEnteredProg |     |
| --- | --- | ---------------- | --------------- | --- |
DataFieldParent
RecordUpdateByUserNa
|     |     | NumberOfArrayElements | DateUpdated |     |
| --- | --- | --------------------- | ----------- | --- |
ValueForEntryDefault
TimeOfDay
DataDictionaryErrorMessageInfor JustifyLeftOrRghtCde DateEffectiveJulian1
DataDisplayDecimals
| Key Data         |     |                  | DateExpiredJulian1 |     |
| ---------------- | --- | ---------------- | ------------------ | --- |
| DataItem   [PK1] |     | DataDisplayRules | PrintBeforeYN      |     |
DataDisplayParameters
| Non-Key Data |     |                           | GenericTextTemplateFlag |                  |
| ------------ | --- | ------------------------- | ----------------------- | ---------------- |
|              |     | D a t a E d i t R u l e s | G e n e r icT e x       | t F i le F l a g |
P r o g r a m N a m e D a t a E d i t O p 1 M e d i a O b j e c t L e n g t h O f T e x t
E r r o r L e v e l
D a t a S t r u c t u r e T e m p l a t e I D D a t a E d i t O p 2 M e d i a O b j e c t L e n g t h I m a g e O b j e c t s
|                         |                      | H e l p T e x t P r o g r a m | M e d i a O b j e c | t L e n g t h O L E O b j e c t |
| ----------------------- | -------------------- | ----------------------------- | ------------------- | ------------------------------- |
| D a t a S t r u c t u r | e O b je c t N a m e | H e l p L i s t P r o g r a m |                     |                                 |
D a t a D i c t i o n a r y I d e n t i f i e r M e d i a O b j e c t L e n g t h M is c O b j e c t s
|     |     | N e x t N u m b e r i n g I ndexNo | M e d i a O b j e c | t L e n g t h F u t u r e O b j e c t s |
| --- | --- | ---------------------------------- | ------------------- | --------------------------------------- |
SystemCodeNextNumbe
MediaObjectVariableLengthColumn
ReleaseNumber
UserId
DateUpdated
ProgramId
WorkStationId
TimeLastUpdated
DataDictionarySmartFields
DataItemLong
|     |     | DataTypeOneWorld | Key Data         |     |
| --- | --- | ---------------- | ---------------- | --- |
|     |     | ControlType      | DataItem   [PK1] |     |
|     |     | SecurityFlag .   | Non-Key Data     |     |
UpperCaseOnly
SmartFColValueBF
|     |     | AllowBlankEntry | SmartFColValueMap |     |
| --- | --- | --------------- | ----------------- | --- |
DataEditRulesOW
SmartFColHeaderBF
|     |     | EditRulesSpec1OW | SmartFColHeaderMap |     |
| --- | --- | ---------------- | ------------------ | --- |
EditRulesSpec2OW
DataDisplayRulesOW
DataDisplayParmsOW
DisplayBehaviorIDEverest
DispBusFunctionObjectName
EditBehaviorIDEverest
EditBusFuncObjectName
SearchFormIDEverest
SearchFormObjectName
BusinessViewIDEverest
BusinessViewObjectName
PlatformFlag
DataDictionaryIdentifier
AutoInclude

PayGrade/SalaryRangeTable
| Address Book          | EmployeeMasterInformation   | Key Data                         |     |
| --------------------- | --------------------------- | -------------------------------- | --- |
| Key Data              |                             | PayGrade   [PK1]  [FK]           |     |
| AddressNumber   [PK1] | Key Data                    | SalaryDataLocality   [PK2]  [FK] |     |
|                       | AddressNumber   [PK1]  [FK] | PayTypeHSP   [PK3]  [FK]         |     |
CostCenterHome   [PK12]  [FK]
|                                 | PayTypeHSP   [PK3]  [FK]                      | DateEffective   [PK4]  [FK]  |                |
| ------------------------------- | --------------------------------------------- | ---------------------------- | -------------- |
|                                 | JobCategory   [PK13]  [FK]                    | AddressNumber   [PK5]  [FK]  |                |
|                                 | J o b S t e p     [ P K 7 ]     [ F K ]       | CostCenterHome   [PK6]  [FK] |                |
| Organization@AddressNumberParen |                                               | J o b C a t e g o ry     [   | P K 7 ]   [FK] |
|                                 | C h a n g e R e a s o n       [ P K 11]  [FK] | J o b St e p      [P K 8     | ]    [F K ]    |
|                                 | DatePayStops   [PK14]  [FK]                   | ChangeReason   [PK9]  [FK]   |                |
|                                 | PayGrade   [PK4]  [FK]                        | DatePayStops   [PK10]  [FK]  |                |
SalaryDataLocality   [PK5]  [FK]
|                                 | DateEffective   [PK2]  [FK]                       | JobType   [PK11]  [FK]            |                          |
| ------------------------------- | ------------------------------------------------- | --------------------------------- | ------------------------ |
|                                 | J o b T y p e      [ P K 6 ]     [ F K ]          | DataItem   [PK12]  [FK]           |                          |
| EmployeeMasterAdditionalInforma |                                                   | T u r n o v e r D a t a           | [P K 1 3]    [F K ]      |
|                                 | D a ta I te m       [ P K 8 ]     [ F K ]         | D a t e E ff e c ti v e O         | n     [P K 1 4 ]   [F K] |
| Key Data                        | TurnoverData   [PK9]  [FK]                        | FileName   [PK15]  [FK]           |                          |
| AddressNumber   [PK1]           | DateEffectiveOn   [PK10]  [FK]                    | SequenceNumberView   [PK16]  [FK] |                          |
| P a y T y p e H S P     [ P K2] | F i le N a m e     [ P K 1 5 ]   [ F K]           |                                   |                          |
| P a y G r a d e     [P K 3 ]    | S e q u e nc e N u m b e r V i ew    [PK16]  [FK] | Non-Key Data                      |                          |
| SalaryDataLocality   [PK4]      | Non-Key Data                                      | MinimumSalaryAmount               |                          |
|                                 |                                                   | M i d p oi n tS a la ry           | A m o u n t              |
| DateEffective   [PK5]           | NameAlpha                                         | M a x im u m S a la               | r yA m o u n t           |
| Non-Key Data                    | SocialSecurityNumber                              | FourthQuartileAmount              |                          |
| MaritalStatusActual             | EmployeeNumberThird                               |                                   |                          |
| CountryBirth                    | SexMaleFemale                                     | OtherSalaryAmount                 |                          |
|                                 | MaritalStatusTax                                  | NameRemark                        |                          |
| Nationality1st                  |                                                   | SourceOfSalaryData                |                          |
| Nationality2nd                  | MaritalStatusTaxState                             | PayStep                           |                          |
| Nationality3rd                  | ResidencyStatus12                                 | AmountStep                        |                          |
| DataProtectionCode              | EarnIncomeCredStatus                              | RangeSpreadPercent                |                          |
| DateDataProtection              | NumberOfDependents                                |                                   |                          |
| DateUpdated                     | EmploymentStatus                                  | UserId                            |                          |
| UserId                          | EmployeeClassification                            | ProgramId                         |                          |
DateUpdated
|     | TaxAreaResidence | WorkStationId |     |
| --- | ---------------- | ------------- | --- |
TaxAreaWork
SchoolDistrictCode
|     | StateHome |     | Job Supplemental Data |
| --- | --------- | --- | --------------------- |
StateWorking
LocationHome
LocationWorkCity
PayrollTaxAreaProfile
Key Data
| TaxAreaWork   [PK1]    |     | Jobinformation |     |
| ---------------------- | --- | -------------- | --- |
| PayrollTaxType   [PK2] |     | Key Data       |     |
JobType   [PK1]
Non-Key Data
| DescripCompressed  |     | JobStep   [PK2]            |     |
| ------------------ | --- | -------------------------- | --- |
| DescriptionAlpha   |     | AddressNumber   [PK3]      |     |
| StatutoryCode01    |     | PayGrade   [PK4]           |     |
| AddressNumberPayee |     | SalaryDataLocality   [PK5] |     |
PayTypeHSP   [PK5]
| CoEmployeePaidTax |     | DateEffective   [PK6] |     |
| ----------------- | --- | --------------------- | --- |
PrintOnPaycheckYN
| UserId                |                                  | Non-Key Data         |     |
| --------------------- | -------------------------------- | -------------------- | --- |
| ProgramId             |                                  | JobGroup             |     |
| DateUpdated           | Supplemental Data                | Description001       |     |
| OccTaxWhFrequency     |                                  | PayFrequency         |     |
|                       | Key Data                         | JobCategoryEeo       |     |
| SuiReportingLevel     | SupplementalDatabaseCode   [PK1] |                      |     |
| SchoolDistrictCode    | TypeofData   [PK2]               | WorkersCompInsurCode |     |
| TaxArrearageRules     | SuppDataAlphaKey1   [PK3]        | FloatCode            |     |
| TaxPriority           | CompanyKey   [PK4]               | FlsaExemptYN         |     |
| TaxAdjustmentLimit    | SuppDataAlphaKey2   [PK5]        | BenefitGroupCode     |     |
| TaxCategoryCode       |                                  | UnionCode            |     |
| BenefitDeductionTable | CostCenter   [PK6]               | JobEvaluationMethod  |     |
|                       | SuppDataNumericKey1   [PK7]      | DateJobEvaluation    |     |
| GenerateVoucherFlag   | SuppDataNumericKey2   [PK8]      |                      |     |
|                       | UserDefinedCode   [PK9]          | JobEvaluationPoints  |     |
|                       | DateEffectiveRates   [PK10]      | EvalFactorDegrees001 |     |
|                       | AddressNumber   [PK11]  [FK]     | EvalFactorDegrees002 |     |
EvalFactorDegrees003
|     | RequisitionNumber   [PK12]  [FK] | EvalFactorDegrees004 |     |
| --- | -------------------------------- | -------------------- | --- |
|     | JobStep   [PK13]  [FK]           | EvalFactorDegrees005 |     |
PayGrade   [PK14]  [FK]
|     | SalaryDataLocality   [PK15]  [FK] | EvalFactorDegrees006 |     |
| --- | --------------------------------- | -------------------- | --- |
|     | PayTypeHSP   [PK16]  [FK]         | EvalFactorDegrees007 |     |
|     | JobType   [PK17]  [FK]            | EvalFactorDegrees008 |     |
|     | DateEffective   [PK18]  [FK]      | EvalFactorDegrees009 |     |
EvalFactorDegrees010
|     | Non-Key Data | JobEvalFactorPnts001 |     |
| --- | ------------ | -------------------- | --- |
UnitsTransactionQty
|     | DateEndingEffective | JobEvalFactorPnts002 |     |
| --- | ------------------- | -------------------- | --- |
AmountUserDefined
AmountUserDefined2

|                      | ItemMaster        |     |     |     | CoProductsPlanning/CostingTable |
| -------------------- | ----------------- | --- | --- | --- | ------------------------------- |
| WorkCenterMasterFile | Non-Key Data      |     |     |     | Key Data                        |
| Key Data             | Identifier2ndItem |     |     |     | CostCenterAlt   [PK1]           |
CostCenter   [PK1] Identifier3rdItem ItemCostComponentAddOns IdentifierShortItem   [PK2]  [FK]
Non-Key Data DescriptionLine1 Key Data BranchComponent   [PK3]
| DispatchGroup | DescriptionLine2 |     |     |     | EffectiveThruDate   [PK4] |
| ------------- | ---------------- | --- | --- | --- | ------------------------- |
CostCenterAlt SearchText CostCenterAlt   [PK2] ItemNumberShortKit   [PK5]
Location SearchTextCompressed Location   [PK3]  [FK] CostCenter   [PK6]  [FK]
| CriticalWorkCenter | SalesReportingCode1 |     | Lot   [PK4]  [FK] |     |     |
| ------------------ | ------------------- | --- | ----------------- | --- | --- |
PrimeLoadCode SalesReportingCode2 LedgType   [PK5]  [FK] Non-Key Data
PayPointCode SalesReportingCode3 CostType   [PK6] FeatureCostPercent
DemoCalcCapacity SalesReportingCode4 CostCenter   [PK7]  [FK] EffectiveFromDate
AddressNumber SalesReportingCode5 SystemCode   [PK8]  [FK] FeaturePlannedPercent
AverageQueueTimeHours SalesReportingCode6 IdentifierShortItem   [PK9]  [FK] UserId
R e s o u r c e O f f s e t S a l e s R e p o r t i n g C o d e 7 Non-Key Data ProgramId
W o r k H o u r P e r D a y S a l e s R e p o r t i n g C o d e 8 I d e n t i f i e r 2 n d I t e m W o r k S t a t io n Id
W o r k C e n t e r E f f i c i e n c y S a l e s R e p o r t i n g C o d e 9 I d e n t i f i e r 3 r d I t e m D a t e U p d a t e d
W o r k C e n t e r U t i l i z a t i o n S a l e s R e p o r t i n g C o d e 1 0 L o t G r a d e Ti m e O f D a y
| N u m b e r O f E m p l o y e e s   | P u r c h a s i n g R e p o r t C o d e 1 |                                   | A m t C               | u r r e n t S t a n d a r d U n t |     |
| ----------------------------------- | ----------------------------------------- | --------------------------------- | --------------------- | --------------------------------- | --- |
|                                     |                                           |                                   | A m t S               | t d M f g C o s t S i m           | .   |
| N u m b e r O f M a c h i n e s     | P u r c h a s i n g R e p o r t C o d e 2 |                                   | S t a n               | d a r d C o s t R o l l u p       |     |
| S t a n d a r d Q u e u e H o u r s | P u r c h a s i n g R e p o r t C o d e 3 |                                   | A m t S               | t d R o l l u p S i m             |     |
| M o v e H o u r s                   | P u r c h a s i n g R e p o r t C o d e 4 |                                   | S t a n               | d a r d F a c t o r C o d e F r o |     |
| Q u e u e H o u r s                 | P u r c h a s i n g R e p o r t C o d e 5 |                                   | S t a n               | d a r d F a c t o r C o d e S im  |     |
| C r e w S i z e                     | P u r c h R e p o r t i n g C o d e 6     |                                   | S t a n               | d a r d F a c t o r F r o z e n   |     |
| D e s i r e d H o u r s S h i f t 1 | P u r c h R e p o r t i n g C o d e 7     |                                   | S t a n               | d a r d F a c t o r S i m         |     |
| D e s i r e d H o u r s S h i f t 2 | P u r c h R e p o r t i n g C o d e 8     | B i l l o f M a t e r i a l M a s | t e r F i l e S t a n | d a r d R a t e C o d e F r o     |     |
| D e s i r e d H o u r s S h i f t 3 | P u r c h R e p o r t i n g C o d e 9     | K e y   D a t a                   | S t a n               | d a r d R a t e C o d e S i m     |     |
D e m o C a p i c i t y S h i f t 1 P u r c h R e p o r t i n g C o d e 1 0 T y p e B i l l       [ P K 1 ] S t a n d a r d R a t e F r o z e n .
| D e m o C a p i c i t y S h i f t 2       | C o m m o d i t y C o d e                 | I t e m N u m b e r S h o           | r t K i t       [ P K 2 ] S t a n     | d a r d R a t e S i m              |                |
| ----------------------------------------- | ----------------------------------------- | ----------------------------------- | ------------------------------------- | ---------------------------------- | -------------- |
| D e m o C a p i c i t y S h i f t 3       | P r o d u c t G r o u p F r o m           | C o s t C e n t e r A l t       [   | P K 3 ] S t a n                       | d a r d P r o c e s s i n g F la g |                |
| D e s i r e d C a p i c i t y S h i f t 1 | D i s p a t c h G r p                     | I d e n t i f i e r S h o r t I t e | m       [ P K 8 ]     [ F K ] U s e r | I d                                |                |
| D e s i r e d C a p i c i t y S h i f t 2 | P r i c i n g C a t e g o r y             | C o m p o n e n t N u m             | b e r       [ P K 4 ] P r o g         | r a m I d                          |                |
| D e s i r e d C a p i c i t y S h i f t 3 | R e p r i c e B a s k e t P r i c e C a t | S u b s t i t u t e I t e m S e     | q u e n c e N u       [ P K5] W o r k | S t a t i o n I d                  |                |
| U s e r R e s e r v e d D a t e           | O r d e r R e p r i c e C a t e g o r y   | U n i t s B a t c h Q u a n         | t i t y       [ P K 6 ] D a t e       | U p d a t e d                      |                |
| U s e r R e s e r v e d A m o u n t       | B u y e r                                 | C o p r o d u c t s B y p r o       | d u c t s       [ P K 7 ]             | .                                  |                |
| U s e r R e s e r v e d N u m b e r       | D r a w i n g N u m b e r                 | C o s t C e n t e r       [ P K     | 9 ]     [ F K ]                       |                                    |                |
| U s e r R e s e r v e d R e f e r e n ce  | R e v i s i o n N u m b e r               | N o n - K e y   D a t a             |                                       |                                    |                |
| U s e r R e s e r v e d C o d e           | D r a w i n g S i z e                     | ItemNumber2ndKit                    |                                       |                                    |                |
| UserId                                    | VolumeCubicDimensions                     | ItemNumber3rdKit                    |                                       |                                    |                |
| ProgramId                                 | Carrier                                   | Identifier2ndItem                   |                                       |                                    | ItemBranchFile |
DateUpdated PreferCarrierPurchasin Identifier3rdItem Key Data
| TimeOfDay | ShippingConditionsCode | BranchComponent |     |     |     |
| --------- | ---------------------- | --------------- | --- | --- | --- |
WorkStationId ShippingCommodityClass PartialsAllowedYN CostCenter   [PK2]  [FK]
|     | UnitOfMeasurePrimary   | QtyRequiredStandard       |     |     | SystemCode   [PK3]  [FK] |
| --- | ---------------------- | ------------------------- | --- | --- | ------------------------ |
|     | UnitOfMeasureSecondary | U n i t O f M e a s u r e |     |     | Non-Key Data             |
C o s t C e n t e r M a s t e r U n i t O f M e a s u r e P u r c h a s U n i t O f M e a s u r e A s I n p u t I d e n t i f i e r 2 n d I t e m
. U n i t O f M e a s u r e P r i c i n g F i x e d o r V a r i a b l e B a t c h S i z e I d e n t i f i e r 3 r d I t e m
K e y   D a t a U n i t O f M e a s u r e S h i p p i n g E f f e c t i v e F r o m D a t e S a l e s R e p o r t i n g C o d e 1
C o s t C e n t e r       [ P K 1 ] U n i t O f M e a s u r e P r o d u c t io n E f f e c t i v e T h r u D a t e S a l e s R e p o r t i n g C o d e 2
N o n - K e y   D a t a U n i t O f M e a s u r e A l l o c a t i o n E f f e c t i v e F r o m S e r i a l N o S a l e s R e p o r t i n g C o d e 3
C o s t C e n t e r T y p e U n i t O f M e a s u r e W e i g h t E f f e c t i v e T h r u S e r i a l N o S a l e s R e p o r t i n g C o d e 4
D e s c r i p C o m p r e s s e d U n i t O f M e a s u r e V o l u m e I s s u e T y p e C o d e S a l e s R e p o r t i n g C o d e 5
L e v e l O f D e t a i l C c C o d e U n i t O f M e a s u r e S t o c k i R e q u i r e d Y N S a l e s R e p o r t i n g C o d e 6
C o m p a n y U n i t o f M e a s u r e V o l u m e o r W eI O p t i o n a l I t e m K i t S a l e s R e p o r t i n g C o d e 7
A d d r e s s N u m b e r C y c l e C o u n t C a t e g o r y D e f a u l t C o m p o n e n t S a l e s R e p o r t i n g C o d e 8
A d d r e s s N u m b e r J o b A r G lC a t e g o r y C o m p o n e n t C o s t i n g M e t h o d S a l e s R e p o r t i n g C o d e 9
C o u n t y P r i c e L e v e l S a l e s R e p o r t i n g C o d e 1 0
S t a t e L e v e l P u r c h a s i n g P r i c e C o s t M e t h o d P u r c h a s i n g P u r c h a s i n g R e p o r t C o d e 1
M o d e l A c c o u n t s a n d C o n s olid C o s t L e v e l O r d e r W i t h Y N P u r c h a s i n g R e p o r t C o d e 2
D e s c r i p t i o n 0 0 1 P o t e n c y P r i c i n g F i x e d O r V a r i a b l e Q t y P u r c h a s i n g R e p o r t C o d e 3
D e s c r i p t i o n 0 1 0 0 2 C h e c k A v a i l a b i l i t y Y N C o m p o n e n t T y p e P u r c h a s i n g R e p o r t C o d e 4
D e s c r i p t i o n 0 1 0 0 3 B u l k P a c k e d F l a g F r o m P o t e n c y P u r c h a s i n g R e p o r t C o d e 5
D e s c r i p t i o n 0 1 0 0 4 L a y e r C o d e S o u r c e T h r u P o t e n c y P u r c h R e p o r t i n g C o d e 6
C a t e g o r y C o d e C o s t C t 0 0 1 C o n s t a n t F u t u r e U s e 1 F r o m G r a d e P u r c h R e p o r t i n g C o d e 7
C a t e g o r y C o d e C o s t C t 0 0 2 T h r u G r a d e P u r c h R e p o r t i n g C o d e 8
C a t e g o r y C o d e C o s t C t 0 0 3 S e q u e n c e N o O p e r a t i o n s P u r c h R e p o r t i n g C o d e 9
C a t e g o r y C o d e C o s t C t 0 0 4 B u b b l e S e q u e n c e P u r c h R e p o r t i n g C o d e 1 0
C a t e g o r y C o d e C o s t C t 0 0 5 F e a t u r e P l a n n e d P e r c e n t C o m m o d i t y C o d e
C a t e g o r y C o d e C o s t C t 0 0 6 F e a t u r e C o s t P e r c e n t P r o d u c t G r o u p F r o m
C a t e g o r y C o d e C o s t C t 0 0 7 R e s o u r c e P e r c e n t D i s p a t c h G r p
C a t e g o r y C o d e C o s t C t 0 0 8 P e r c e n t O f S c r a p P r i m a r y L a s t V e n d o rN o
C a t e g o r y C o d e C o s t C t 0 0 9 R e w o r k P e r c e n t A d d r e s s N u m b e r P l a n n e r
C a t e g o r y C o d e C o s t C t 0 1 0 A s I s P e r c e n t B u y e r
C a t e g o r y C o d e C o s t C t 0 1 1 P e r c e n t C u m u l a t i v e P l a G l C a t e g o r y
| CategoryCodeCostCt012    |     |     |     |     | CountryOfOrigin        |
| ------------------------ | --- | --- | --- | --- | ---------------------- |
| CategoryCodeCostCt013    |     |     |     |     | ReorderPointInput      |
| CategoryCodeCostCt014    |     |     |     |     | ReorderQuantityInput   |
| CategoryCodeCostCt015    |     |     |     |     | ReorderQuantityMaximum |
| CategoryCodeCostCt016    |     |     |     |     | ReorderQuantityMinimum |
| CategoryCodeCostCt017    |     |     |     |     | OrderMultiples         |
| CategoryCodeCostCt018    |     |     |     |     | ServiceLevel           |
| CategoryCodeCostCt019    |     |     |     |     | SafetyStockDaysSupply  |
| CategoryCodeCostCt020    |     |     |     |     | ShelfLifeDays          |
| CategoryCodeCostCt021    |     |     |     |     | CheckAvailabilityYN    |
| CategoryCodeCostCt022    |     |     |     |     | LayerCodeSource        |
| CategoryCodeCostCt023    |     |     |     |     | LotStatusCode          |
| sdfsd                    |     |     |     |     | ConstantFutureUse1     |
| CategoryCodeCostCenter25 |     |     |     |     | ConstantFutureUse2     |
| CategoryCodeCostCenter26 |     |     |     |     | StandardPotency        |
| CategoryCodeCostCenter27 |     |     |     |     | FromPotency            |
| CategoryCodeCostCenter28 |     |     |     |     | ThruPotency            |
| CategoryCodeCostCenter29 |     |     |     |     | StandardGrade          |
| CategoryCodeCostCenter30 |     |     |     |     | FromGrade              |
| TaxArea                  |     |     |     |     | ThruGrade              |
| TaxEntity                |     |     |     |     | ComponentType          |
| TaxArea1                 |     |     |     |     | MarginMaintenancePer   |
| TaxExplanationCode1      |     |     |     |     | PricingCategory        |
| TaxDeductionCodes1       |     |     | .   |     | RepriceBasketPriceCat  |
| TaxDeductionCodes2       |     |     |     |     | OrderRepriceCategory   |
| TaxDeductionCodes3       |     |     |     |     | BackordersAllowedYN    |
TaxDeductionCodes4
TaxDeductionCodes5
TaxDeductionCodes6
TaxDeductionCodes7
TaxDeductionCodes8
TaxDeductionCodes9
.

AccountLedger
| ItemMaster        |     |     | ItemBranchFile    |     | ItemLocationFile |     |                    |     |     |     |
| ----------------- | --- | --- | ----------------- | --- | ---------------- | --- | ------------------ | --- | --- | --- |
| Non-Key Data      |     |     | Non-Key Data      |     | Non-Key Data     |     | Key Data           |     |     |     |
| Identifier2ndItem |     |     | Identifier2ndItem |     | PrimaryBinPS     |     | CompanyKey   [PK1] |     |     |     |
DocumentType   [PK2]
| Identifier3rdItem |     |     | Identifier3rdItem   |     | GlCategory    |     |                            |     |     |     |
| ----------------- | --- | --- | ------------------- | --- | ------------- | --- | -------------------------- | --- | --- | --- |
| DescriptionLine1  |     | .   | SalesReportingCode1 |     | LotStatusCode |     | DocVoucherInvoiceE   [PK3] |     |     |     |
DescriptionLine2 SalesReportingCode2 DateLastReceipt1 DateForGLandVoucherJULIA   [PK4]
| SearchText           |     |     | SalesReportingCode3 |     | QtyOnHandPrimaryUn   |     | JournalEntryLineNo   [PK5] |     |                 |     |
| -------------------- | --- | --- | ------------------- | --- | -------------------- | --- | -------------------------- | --- | --------------- | --- |
| SearchTextCompressed |     |     |                     |     |                      |     | LineExtensionCode   [PK6]  |     |                 |     |
|                      |     |     | SalesReportingCode4 |     | QtyBackorderedInPri  |     |                            |     |                 |     |
| SalesReportingCode1  |     |     | SalesReportingCode5 |     | QtyOnPurchaseOrderPr |     | OrderType   [PK28]  [FK]   |     |                 |     |
| SalesReportingCode2  |     |     | SalesReportingCode6 |     | QuantityOnWoReceipt  |     | LineNumber   [PK29]  [FK]  |     |                 |     |
|                      |     |     |                     |     |                      | .   |                            |     | AccountBalances |     |
|                      |     |     |                     |     |                      |     |                            | .   | Key Data        |     |
AccountId   [PK1]
.
| W o r k O rd erMasterFile |     |     |                     |     |     |     |     |     | Century   [PK2] |                        |
| ------------------------- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --------------- | ---------------------- |
|                           |     |     | PurchaseOrderHeader |     |     |     |     |     | F i s c a l Y   | e a r 1      [ P K 3 ] |
K e y   Da ta PurchaseOrderDetailFile F i s c a l Q tr F u t u r e U s e    [PK4]
DocumentOrderInvoiceE   [PK1] Key Data Key Data LedgerType   [PK5]
| C a t e g o r i e s W o | r k O r d e r 0 0 1       | [ P K 2 ]     [ F K ] | C o m p a n yK | e y O r d e r N o      |  [P K 1 ]   [F K ]     | C o m p a n yK | e y O r d e r N | o     [P K 1 ]   [F K ] |               |                      |
| ----------------------- | ------------------------- | --------------------- | -------------- | ---------------------- | ---------------------- | -------------- | --------------- | ----------------------- | ------------- | -------------------- |
|                         |                           |                       | D o cu m e n   | tO r d e r In v o ic e | E     [P K 2 ]   [F K] |                |                 |                         | . S u b l e d | g e r      [ P K 6 ] |
C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 3 ]     [ F K ] D o cu m e n tO r d e r In v o ic e E     [P K 2 ]   [F K] S u b l e d g e r T y p e      [PK7]
C a te g o ri e s W o rkOrder003   [PK4]  [FK] . O r d e r T y p e      [ P K 3 ]   [FK] . O r d e r T y p e      [ P K 3 ]    [ F K ] . C u rr e n c y C o d e From   [PK8]
N o n -K e y   D a ta O r d e r S u ff ix       [P K 4 ] O r d e r S u ff ix       [P K 4 ]     [F K ] N o n - K e y  D a t a
|     |     |     | A d d re s s N | u m b e r     [P K 5 | ]    [ F K ] | L i n e N u m b | e r    [ P K 5 ] |     |     |     |
| --- | --- | --- | -------------- | -------------------- | ------------ | --------------- | ---------------- | --- | --- | --- |
O r d e r T y p e Ty p e A d d re s s N u m b e r     [ P K 6 ]   [FK] C om p a n y
O r d e r S u ff ix A d d r e s sN u m b e r     [P K9]  [FK] Am tB e g i nningBalancePy
RelatedOrderType Non-Key Data UnitOfMeasureAsInput   [PK12]  [FK] AmountNetPosting001
| RelatedPoSoNumber |     |     | CostCenter |     |     | UnitsTransactionQty   [PK13]  [FK] |     |     |     |     |
| ----------------- | --- | --- | ---------- | --- | --- | ---------------------------------- | --- | --- | --- | --- |
LineNumber
SupplierPrice/CatalogFile
O r d e r A d d ressInformation
|     |     |     |     |     | K e y  D a t a |     |     | .   |     |     |
| --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- |
K e y   D a t a C o s tC e n t er   [PK1] PurchaseOrderReceiverFile
| DocumentOrderInvoiceE   [PK1] |     |     |     |     | AddressNumber   [PK2]       |     | .   | Key Data                 |     |     |
| ----------------------------- | --- | --- | --- | --- | --------------------------- | --- | --- | ------------------------ | --- | --- |
| OrderType   [PK2]             |     |     |     |     | IdentifierShortItem   [PK3] |     |     | MatchType   [PK1]        |     |     |
| CompanyKeyOrderNo   [PK3]     |     |     |     |     |                             |     |     | NoOfLinesOnOrder   [PK6] |     |     |
CatalogName   [PK4]
TypeAddressNumber   [PK4] CurrencyCodeFrom   [PK5] DocVoucherInvoiceE   [PK7]
Non-Key Data UnitOfMeasureAsInput   [PK6] CompanyKeyOrderNo   [PK8]
| N a m e M a i l in | g   |     |     |     | U n i t s T ra n s a c t | io n Q ty       [P K 7 ] |     |       | [ F K ]                     |     |
| ------------------ | --- | --- | --- | --- | ------------------------ | ------------------------ | --- | ----- | --------------------------- | --- |
|                    |     |     |     | .   | D a t e E x p ir e d J   | u li a n1      [ P K 8 ] |     | Docum | e n tO rderInvoiceE   [PK9] |     |
Ad d r e ss L i n e 1
| AddressLine2      |     |     |     |     | Non-Key Data                    |     |     |                            | [FK] |     |
| ----------------- | --- | --- | --- | --- | ------------------------------- | --- | --- | -------------------------- | ---- | --- |
| AddressLine3      |     |     |     |     |                                 |     |     | OrderType   [PK10]  [FK]   |      |     |
| AddressLine4      |     |     |     |     |                                 |     |     | OrderSuffix   [PK11]  [FK] |      |     |
|                   |     |     |     | .   |                                 |     |     | LineNumber   [PK12]  [FK]  |      |     |
|                   |     |     |     |     | P.O.DetailLedgerFileFlexibleVer |     |     | Non-Key Data               |      |     |
| AddressBookMaster |     |     |     |     | Key Data                        |     |     | AddressNumber              |      |     |
| Key Data          |     |     |     |     |                                 |     |     | AssociatedLine             |      |     |
CompanyKeyOrderNo   [PK1]
| AddressNumber   [PK1] |     |     |     |     | [FK]                  |     |     | WrittenBy                |     |     |
| --------------------- | --- | --- | --- | --- | --------------------- | --- | --- | ------------------------ | --- | --- |
| Non-Key Data          |     |     |     |     | DocumentOrderInvoiceE |     |     | ContractNumberDistributi |     |     |
| AlternateAddressKey   |     |     |     |     | [PK2]  [FK]           |     |     | ContractSupplementDistri |     |     |
ContractBalancesUpdatedY
| TaxId             |     |     |     |     | OrderType   [PK3]  [FK]   |     |     | IdentifierShortItem |     |     |
| ----------------- | --- | --- | --- | --- | ------------------------- | --- | --- | ------------------- | --- | --- |
| NameAlpha         |     |     |     |     | OrderSuffix   [PK4]  [FK] |     |     |                     |     |     |
| DescripCompressed |     |     |     |     | LineNumber .  [PK5]  [FK] |     |     | Identifier2ndItem   |     |     |
| CostCenter        |     |     |     |     | LedgerType   [PK6]        |     |     | Identifier3rdItem   |     |     |
CostCenterItem
| StandardIndustryCode |                         |     |     |     | NumberChangeOrder   [PK7] |                       |     | Location        |                               |     |
| -------------------- | ----------------------- | --- | --- | --- | ------------------------- | --------------------- | --- | --------------- | ----------------------------- | --- |
| LanguagePreference   |                         |     |     |     | DateUpdated   [PK8]       |                       |     |                 |                               |     |
| AddressType1         |                         |     |     |     |                           |                       |     | Lot             |                               |     |
| CreditMessage        |                         |     |     | .   |                           |                       |     |                 |                               |     |
| S u p p l i e r M    | a s t e r               |     |     |     | A c c o u n t s P a       | y a b l e L e d g e r |     | I t e m L e d g | e r F i l e                   |     |
| K e y   D a t a      |                         |     |     |     | K e y   D a t a           |                       |     |                 |                               |     |
| A d d r e s s N      | u m b e r       [ P K 1 | ]   |     |     |                           |                       |     | K e y   D a t   | a                             |     |
|                      |                         |     |     |     | C o m p a n y K e         | y       [ P K 1 ]     |     | O r d e r T y p | e       [ P K 5 ]     [ F K ] |     |
N o n - K e y   D a t a D o c V o u c h e r I n v o i c e E       [ P K 2 ] D o c u m e n t O r d e r I n v o i c e E      [P K 4]
| A P C l a s s     |                     |     |     |     | D o c u m e n t T | y p e       [ P K 3 ] |     |       |     |     |
| ----------------- | ------------------- | --- | --- | --- | ----------------- | --------------------- | --- | ----- | --- | --- |
| C o s t C e n t e | r A p D e f a u l t |     |     |     |                   |                       |     | [ F K | ]   |     |
O b je c t A c c t s P a y a b l e D o c u m e n t P a y I t e m       [ P K 4 ] C o m p a n y K e y O r d e r N o       [ P K 3 ]
|                     |                        |     |     |     | P a y I t e m E x t     | e n s i o n N u m b e r       [P | K 5 ] | [ F K         | ] .                               |     |
| ------------------- | ---------------------- | --- | --- | --- | ----------------------- | -------------------------------- | ----- | ------------- | --------------------------------- | --- |
| S u b s i d i a r y | A c c t s P a y a b le |     |     |     | L i n e N u m b e       | r       [ P K 1 0 ]     [ F K ]  |       | L i n e N u m | b e r       [ P K 6 ]     [ F K ] |     |
| C o m p a n y       | K e y A P M o d e l    |     |     |     | O r d e r S u f f i x   |     [ P K 9 ]     [ F K ]        |       |               |                                   |     |
D o c A p D e f a u l t J e C o m p a n y K e y O r d e r N o       [ P K 6 ]    [F K ] U n i q u e K e y I D I n t e r n a l       [ P K 1 ]
| D o c T y A p D     | e f a u l t J e         |          |     |     |                         |                                     |     | O r d e r S u f     | f i x       [ P K 2 ]     [ F K ] |     |
| ------------------- | ----------------------- | -------- | --- | --- | ----------------------- | ----------------------------------- | --- | ------------------- | --------------------------------- | --- |
|                     |                         |          |     |     | D o c u m e n t O       | r d e r I n v o i c e E       [ P K | 7 ] | N o n - K e y       |   D a t a                         |     |
| C u r r e n c y C   | o d e A P               |          |     |     | [ F K ]                 |                                     |     |                     |                                   |     |
| TaxArea2            |                         |          |     |     | OrderType   [PK8]  [FK] |                                     |     | NoOfLinesOnOrder    |                                   |     |
| T a x E x e m p     | t R e a s o n 2         |          |     |     |                         |                                     |     | I d e n t i f i e r | S h o r t I t e m                 |     |
| H o l d P a y m     | e n t C o d e           |          |     |     | N o n - K e y   D       | a t a                               |     | I d e n t i f i e r | 2 n d I t e m                     |     |
|                     |                         |          |     |     | D o c u m e n t T       | y p e A d ju s t i n g              |     | I d e n t i f i e r | 3 r d I t e m                     |     |
| T a x R a t e A     | r e a 3 W i t h h o l d | i n g    |     |     | A d d r e s s N u m     | b e r                               |     |                     |                                   |     |
| T a x E x p l C     | o d e 3 W i t h h h o   | l d i ng |     |     | P a y e e A d d r e     | s s N u m b e r                     |     | C o s t C e n       | t e r                             |     |
| T a x A u t h o     | r i t y A p             |          |     |     |                         |                                     |     | L o c a t i o n     |                                   |     |
| P e r c e n t W     | i t h h o l d i n g     |          |     |     | A d d r e s s N u m     | b e r S e n t T o                   |     | L o t               |                                   |     |
| P a y m e n t T     | e r m s A P             |          |     |     | D a t e I n v o i c e   | J                                   |     | P a r e n t L o     | t                                 |     |
|                     |                         |          |     |     | D a t e S e r v i c e   | C u r r e n c y                     |     | S t o r a g e U     | n i t N u m b e r                 |     |
| M u l t i p l e C h | e c k s Y N             |          |     |     | D a t e D u e J u l     | i a n                               |     |                     |                                   |     |
| P a y m e n t I n   | s t r u m e n t         |          |     |     |                         |                                     |     | S e q u e n c       | e N u m b e r L ocati             |     |
| A d d r e s s N     | u m b e r S e n t T o   |          |     |     | D a t e D i s c o u     | n t D u e J u l i a n               |     | T r a n s a c t     | i o n L i n e N r                 |     |
| M i s c C o d e     | 1                       |          |     |     | D a t e F o r G L a     | n d V o u c h e r JULIA             |     | F r o m T o         |                                   |     |
|                     |                         |          |     |     | F i s c a l Y e a r 1   |                                     |     | L o t M a s t e     | r C a r d e x Y N                 |     |
| F l o a t D a y s   | F o r C h e c k s       |          |     |     | C e n t u r y           |                                     |     |                     |                                   |     |
| S e q u e n c e     | F o r L e d g r I n q   |          |     |     | P e r i o d N o G e     | n e r a lL e d g e                  |     | L o t S t a t u s   | C o d e                           |     |
| C u r r e n c y C   | o d e A m o u n t s     |          |     |     |                         |                                     |     | L o t P o t e n     | c y                               |     |
| AmountVoucheredYtd  |                         |          |     |     | C o m p a n y           |                                     |     |                     |                                   |     |

RequisitionInformation
Key Data
RequisitionActivity
| RequisitionNumber   [PK1] | Employee Master |     |     |
| ------------------------- | --------------- | --- | --- |
Key Data
| JobStep   [PK4]  [FK] | RequisitionNumber   [PK1]  [FK] |     |     |
| --------------------- | ------------------------------- | --- | --- |
PayGrade   [PK6]  [FK]
| SalaryDataLocality   [PK7]  [FK] | AddressNumber   [PK2]  [FK] |     |     |
| -------------------------------- | --------------------------- | --- | --- |
JobStep   [PK3]  [FK]
PayTypeHSP   [PK8]  [FK]
| AddressNumber   [PK5]  [FK] | PayGrade   [PK4]  [FK] |     |     |
| --------------------------- | ---------------------- | --- | --- |
SalaryDataLocality   [PK5]  [FK]
JobType   [PK2]  [FK]
| DateEffective   [PK3]  [FK] | PayTypeHSP   [PK6]  [FK] |     |     |
| --------------------------- | ------------------------ | --- | --- |
JobType   [PK7]  [FK]
Non-Key Data
|                | DateEffective   [PK8]  [FK] | Address Book          |     |
| -------------- | --------------------------- | --------------------- | --- |
| CostCenter     | Non-Key Data                |                       |     |
| PositionID     |                             | Key Data              |     |
| Description001 | DateAvailableToBegin        | AddressNumber   [PK1] |     |
CandidateRequisitionStat
FiscalYear1
| DateRequisitioned | CRS |     |     |
| ----------------- | --- | --- | --- |
UserId
AddNoRequestedBy
| RequisitionStatus | ProgramId |     |     |
| ----------------- | --------- | --- | --- |
DateUpdated
TypeRequisition
| AmountExpectedSalary | WorkStationId |     |     |
| -------------------- | ------------- | --- | --- |
UserComboGuideRequired
BudgetedFte
BudgetedPositionHours
JobCategory
PayGradeStep
DateEffectiveFrom
DateEffectiveThru
DateBeginningEffective
FlsaExemptYN
| AddNoApprovedBy |     | ApplicantMaster |     |
| --------------- | --- | --------------- | --- |
| DateApproved    |     | Key Data        |     |
Description01002
AddressNumber   [PK1]  [FK]
| Descript240Characters |     | JobStep   [PK7]  [FK] |     |
| --------------------- | --- | --------------------- | --- |
| CategoryCodeReqn001   |     | JobType   [PK2]  [FK] |     |
CategoryCodeReqn002
PayGrade   [PK3]  [FK]
| CategoryCodeReqn003 |     | SalaryDataLocality   [PK4]  [FK] |     |
| ------------------- | --- | -------------------------------- | --- |
CategoryCodeReqn004
|                     | Supplemental Data                       | PayTypeHSP   [PK5]  [FK]    |     |
| ------------------- | --------------------------------------- | --------------------------- | --- |
| CategoryCodeReqn005 |                                         | DateEffective   [PK6]  [FK] |     |
| U s e rI d          | K e y   D a ta                          |                             |     |
|                     | S u p p l e m entalDatabaseCode   [PK1] | Non-Key Data                |     |
Pr o g r amId
| DateUpdated         | TypeofData   [PK2]        | NameAlpha            |     |
| ------------------- | ------------------------- | -------------------- | --- |
|                     | SuppDataAlphaKey1   [PK3] | ApplicantStatus      |     |
| WorkStationId       |                           | SocialSecurityNumber |     |
| CostCenterHome      | CompanyKey   [PK4]        |                      |     |
|                     | SuppDataAlphaKey2   [PK5] | CostCenter           |     |
| CategoryCodeReqn006 |                           | PositionID           |     |
CostCenter   [PK6]
|     | SuppDataNumericKey1   [PK7] | JobCategory |     |
| --- | --------------------------- | ----------- | --- |
JobCategoryEeo
SuppDataNumericKey2   [PK8]
|     | UserDefinedCode   [PK9] | MinorityEeo |     |
| --- | ----------------------- | ----------- | --- |
SexMaleFemale
DateEffectiveRates   [PK10]
|     | AddressNumber   [PK11]  [FK]     | I9Status |     |
| --- | -------------------------------- | -------- | --- |
|     | RequisitionNumber   [PK12]  [FK] | Veteran  |     |
DisabledVeteran
JobStep   [PK13]  [FK]
|     | PayGrade   [PK14]  [FK] | Handicapped |     |
| --- | ----------------------- | ----------- | --- |
CategoryCodeAplcnt005
SalaryDataLocality   [PK15]  [FK]
|     | PayTypeHSP   [PK16]  [FK] | CategoryCodeAplcnt006 |     |
| --- | ------------------------- | --------------------- | --- |
CategoryCodeAplcnt007
JobType   [PK17]  [FK]
|                 | DateEffective   [PK18]  [FK] | CategoryCodeAplcnt008  |                       |
| --------------- | ---------------------------- | ---------------------- | --------------------- |
|                 |                              | C a t e g o r y C o    | d e A p l c n t 0 0 9 |
| Jobinformation  | Non-Key Data                 |                        |                       |
|                 | UnitsTransactionQty          | C a t e g o r y C o    | d e A p l c n t 0 1 0 |
| Key Data        |                              | CategoryCodeApplcnt001 |                       |
| JobType   [PK1] | DateEndingEffective          |                        |                       |
|                 | AmountUserDefined            | CategoryCodeApplcnt002 |                       |
| JobStep   [PK2] |                              | CategoryCodeApplcnt003 |                       |
AddressNumber   [PK3] AmountUserDefined2 CategoryCodeApplcnt004
NameRemark
| PayGrade   [PK4] |     | CategoryCodeApplcnt005 |     |
| ---------------- | --- | ---------------------- | --- |
SalaryDataLocality   [PK5] NameRemarksLine2 CategoryCodeApplcnt006
UpdatedDate
| PayTypeHSP   [PK5]    |                 | CategoryCodeApplcnt007 |     |
| --------------------- | --------------- | ---------------------- | --- |
| DateEffective   [PK6] | DaysUserDefined | CategoryCodeApplcnt008 |     |
DocumentOrderInvoiceE
| Non-Key Data |                 | CategoryCodeApplcnt009 |     |
| ------------ | --------------- | ---------------------- | --- |
| JobGroup     | UdcEquivalentWw | CategoryCodeApplcnt010 |     |
UserId
| Description001 | ProgramId | DateBirth       |     |
| -------------- | --------- | --------------- | --- |
| PayFrequency   |           | DateApplication |     |
WorkStationId
| JobCategoryEeo       | DateUpdated | DateRecruitingEnd    |     |
| -------------------- | ----------- | -------------------- | --- |
| WorkersCompInsurCode |             | DateFirstInterview   |     |
|                      | TimeOfDay   | DateAvailableToBegin |     |
FloatCode
| FlsaExemptYN |     | RtSalaryAsking |     |
| ------------ | --- | -------------- | --- |
HoursAvailToWork
BenefitGroupCode
| UnionCode |     | UserId |     |
| --------- | --- | ------ | --- |
ProgramId
JobEvaluationMethod
| DateJobEvaluation    |     | DateUpdated    |     |
| -------------------- | --- | -------------- | --- |
| JobEvaluationPoints  |     | WorkStationId  |     |
| EvalFactorDegrees001 |     | CostCenterHome |     |
EvalFactorDegrees002
EvalFactorDegrees003
EvalFactorDegrees004
EvalFactorDegrees005

Demand/SupplyInclusionRules
Key Data
BranchRelationshipsMasterFile
| ResourceVersion   [PK1] |     |     |     | Key Data |
| ----------------------- | --- | --- | --- | -------- |
OrderType   [PK2]
| LineType   [PK3] |     |     |     | CostCenterAlt   [PK1] |
| ---------------- | --- | --- | --- | --------------------- |
IdentifierShortItem   [PK2]  [FK]
| StatusLine   [PK4] |     |     |     | BranchComponent   [PK3] |
| ------------------ | --- | --- | --- | ----------------------- |
GenericReportCode   [PK4]
BranchLevel   [PK5]
ItemMaster
BranchSequence   [PK6]
| Non-Key Data      |     |     |     | CostCenter   [PK7]  [FK] |
| ----------------- | --- | --- | --- | ------------------------ |
| Identifier2ndItem |     |     |     | Location   [PK8]  [FK]   |
Identifier3rdItem
|                  |     | ItemBranchFile    |     | Lot   [PK9]  [FK]       |
| ---------------- | --- | ----------------- | --- | ----------------------- |
| DescriptionLine1 |     |                   |     | LedgType   [PK10]  [FK] |
| DescriptionLine2 |     | Non-Key Data      |     | Non-Key Data            |
| SearchText       |     | Identifier2ndItem |     |                         |
ExcludeIncludeCode
| SearchTextCompressed |     | Identifier3rdItem   |     | AvailabilityCheck |
| -------------------- | --- | ------------------- | --- | ----------------- |
| SalesReportingCode1  |     | SalesReportingCode1 |     |                   |
EffectiveFromDate
| SalesReportingCode2     |               | SalesReportingCode2 |                       | EffectiveThruDate       |
| ----------------------- | ------------- | ------------------- | --------------------- | ----------------------- |
| SalesReportingCode3     |               | SalesReportingCode3 |                       | T.ransitLeadtime        |
| S a l e s R e p o r t i | n g C o d e 4 | S a l e s R e p     | o r t i n g C o d e 4 |                         |
|                         |               |                     | r.                    | S o u r ce P e r ce n t |
| S a l e s R e p o r t i | n g C o d e 5 | S a l e s R e p     | o t i n g C o d e 5   | P e rc e n tT o F ill A |
| SalesReportingCode6     |               | SalesReportingCode6 |                       | PercentMarkup           |
| SalesReportingCode7     |               | SalesReportingCode7 |                       |                         |
FixedMarkupAmount
| SalesReportingCode8  |     | SalesReportingCode8  |     | UnitExtended |
| -------------------- | --- | -------------------- | --- | ------------ |
| SalesReportingCode9  |     | SalesReportingCode9  |     |              |
| SalesReportingCode10 |     | SalesReportingCode10 |     | UserId       |
ProgramId
| PurchasingReportCode1 |                     | PurchasingReportCode1 |                         | DateUpdated       |
| --------------------- | ------------------- | --------------------- | ----------------------- | ----------------- |
| P u r c h a s i n g R | e p o r t C o d e 2 | P u r c h a s i n     | g R e p o r t C o d e 2 |                   |
| P u r c h a s i n g R | e p o r t C o d e 3 | P u r c h a s i n     | g R e p o r t C o d e 3 | T im e O .f D a y |
W or k S t at io nId
PurchasingReportCode4
PurchasingReportCode5
PurchReportingCode6
| MPS/MRP/DRPMessageFile |     | PurchReportingCode7 |     |     |
| ---------------------- | --- | ------------------- | --- | --- |
PurchReportingCode8 CoProductsPlanning/CostingTable
Key Data
UniqueKeyIDInternal   [PK1] Key Data
CostCenterAlt   [PK1]
Non-Key Data
IdentifierShortItem IdentifierShortItem   [PK2]  [FK]
. BranchComponent   [PK3]
| CostCenter |     |     | .   | EffectiveThruDate   [PK4] |
| ---------- | --- | --- | --- | ------------------------- |
CostCenterAlt
MessageCde ItemNumberShortKit   [PK5]
CostCenter   [PK6]  [FK]
ActionMessageControl
HoldCode Location   [PK7]  [FK]
Lot   [PK8]  [FK]
CompanyKeyOrderNo LedgType   [PK9]  [FK]
DocumentOrderInvoiceE
OrderType Non-Key Data
FeatureCostPercent
LineNumber
OrderSuffix EffectiveFromDate
DescriptionLine1 FeaturePlannedPercent
. UserId
QuantityTransaction
PrimaryLastVendorNo ProgramId
DateRequestedJulian MPS/MRP/DRPLowerLevelRequiremen WorkStationId
Key Data DateUpdated
DateStart
| DateRecommendedStart   |     | UniqueKeyIDInternal   [PK1] |     | TimeOfDay              |
| ---------------------- | --- | --------------------------- | --- | ---------------------- |
| DateRecommendedComplet |     | Non-Key Data                |     |                        |
| DateUpdated            |     | IdentifierShortItem         |     |                        |
| TimeOfDay              |     | CostCenter                  |     |                        |
| UserId                 |     | DateRequestedJulian         |     |                        |
| WorkStationId          |     | LeadtimeOffsetDays          |     |                        |
| ProgramId              |     | ItemNumberShortKit          |     | MPS/MRP/DRPSummaryFile |
Key Data
CostCenterAlt
|     |     | UnitsTransactionQty   |     | IdentifierShortItem   [PK1] |
| --- | --- | --------------------- | --- | --------------------------- |
|     |     | DocumentOrderInvoiceE |     | CostCenter   [PK2]          |
|     |     | OrderType             |     | QuantityType   [PK3]        |
|     |     | CompanyKeyRelated     |     | DateStart   [PK4]           |
RelatedPoSoNumber
Non-Key Data
|     |     | RelatedOrderType |     | QuantityTransaction |
| --- | --- | ---------------- | --- | ------------------- |
RelatedPoSoLineNo
PeggingRecordLinkInterna

| AddressBookMaster |     |     | ItemMaster   |     |     | ItemBranchFile |     |     |     |     |     |
| ----------------- | --- | --- | ------------ | --- | --- | -------------- | --- | --- | --- | --- | --- |
| Key Data          |     |     | Non-Key Data |     |     | Non-Key Data   |     |     |     |     |     |
Identifier2ndItem
| AddressNumber   [PK1] |                           |       | Identifier2ndItem |                             |           |                   |                     |         |     |     |     |
| --------------------- | ------------------------- | ----- | ----------------- | --------------------------- | --------- | ----------------- | ------------------- | ------- | --- | --- | --- |
| Non-Key Data          |                           |       | Identifier3rdItem |                             |           | Identifier3rdItem |                     |         |     |     |     |
|                       |                           |       | D e               | s c r i p t i o n L i n e 1 |           | S a l e s         | R e p o r t i n g C | o d e 1 |     |     |     |
| A l t                 | e r n a t e A d d r e s s | K e y | D e               | s c r i p t i o n L i n e 2 |           | S a l e s         | R e p o r t i n g C | o d e 2 |     |     |     |
| T a                   | x I d                     |       |                   |                             |           | S a l e s         | R e p o r t i n g C | o d e 3 |     |     |     |
| N a                   | m e A l p h a             |       | S e               | a r c h T e x t             |           | .                 |                     |         |     |     |     |
| D e                   | s c r i p C o m p r e s   | s e d | S e               | a r c h T e x t C o m p     | re s s ed | S a l e s         | R e p o r t i n g C | o d e 4 |     |     |     |
|                       |                           |       | S a               | l e s R e p o r t i n g C o | d e 1     | S a l e s         | R e p o r t i n g C | o d e 5 |     | .   |     |
C o s t C e n t e r S a l e s R e p o r t i n g C o d e 2 S a l e s R e p o r t i n g C o d e 6 I t e m B a s e P r i c e F il e
| S t a | n d a r d I n d u s t r y | C o d e |     |                             |       | S a l e s | R e p o r t i n g C | o d e 7 |     | K e y   D a t a |     |
| ----- | ------------------------- | ------- | --- | --------------------------- | ----- | --------- | ------------------- | ------- | --- | --------------- | --- |
| L a n | g u a g e P r e f e r e   | n c e   | S a | l e s R e p o r t i n g C o | d e 3 |           |                     |         |     |                 |     |
A d d r e s s T y p e 1 S a l e s R e p o r t i n g C o d e 4 S a l e s R e p o r t i n g C o d e 8 I d e n t i f i e r S h o r t I te m    [PK1]
|     |     |     | S a | l e s R e p o r t i n g C o | d e 5 | S a l e s | R e p o r t i n g C | o d e 9 |     | C o s t C e n t e r       [ | P K 2 ] |
| --- | --- | --- | --- | --------------------------- | ----- | --------- | ------------------- | ------- | --- | --------------------------- | ------- |
C r e d i t M e s s a g e S a l e s R e p o r t i n g C o d e 6 S a l e s R e p o r t i n g C o d e 10 L o c a t i o n       [ P K 3 ]
| P e          | r s o n C o r p o r a t i o | n C o de |     |     |     |     |     |     |     |                       |     |
| ------------ | --------------------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- |
| AddressType2 |                             |          |     |     |     |     |     |     |     | Lot   [PK4]           |     |
| AddressType3 |                             |          |     |     |     |     |     |     |     | AddressNumber   [PK5] |     |
ItemCustomerKeyID   [PK6]
| AddressType4 |     |     |     |                  |     |     |     | ItemCostFile |     | LotGrade   [PK7] |     |
| ------------ | --- | --- | --- | ---------------- | --- | --- | --- | ------------ | --- | ---------------- | --- |
| AddressType5 |     |     |     | ItemLocationFile |     |     |     |              |     |                  |     |
AddressTypePayables N o n - K e y   D a t a K e y   D a t a F r o m P o t e n c y       [ P K 8 ]
|     |     | .   |     |         |                      |     |     | I d e n t i f i e r S h o r t I te m    [PK1] |     | C u r r e n c y C o d e | F r o m       [ P K 9 ]       |
| --- | --- | --- | --- | ------- | -------------------- | --- | --- | --------------------------------------------- | --- | ----------------------- | ----------------------------- |
|     |     |     |     | P r i m | a r y B i n P S      |     |     |                                               |     | U n i t O f M e a s u r | e A s I n p u t     [ P K 10] |
|     |     |     |     | G l C a | t e g o r y          |     |     | C o s t C e n t e r       [ P K 2]            |     | D a t e E x p i r e d J | u l ia n 1       [ P K 1 1 ]  |
|     |     |     |     | L o t S | t a t u s C o d e    |     |     | L o c a t i o n       [ P K 3 ]               |     |                         |                               |
|     |     |     |     |         |                      |     | ..  | L o t       [ P K 4 ]                         |     | N o n - K e y   D a t   | a                             |
|     |     |     |     | D a t e | L a s t R e c e ipt1 |     |     | LedgType   [PK5]                              |     | Identifier2ndItem       |                               |
QtyOnHandPrimaryUn
|     | SalesOrderHeaderFile          |         |     | QtyBackorderedInPri  |     |     |     | Non-Key Data             |     | Identifier3rdItem    |     |
| --- | ----------------------------- | ------- | --- | -------------------- | --- | --- | --- | ------------------------ | --- | -------------------- | --- |
|     | Key Data                      |         |     | QtyOnPurchaseOrderPr |     |     |     | Identifier2ndItem        |     | DateEffectiveJulian1 |     |
|     |                               |         |     |                      |     |     |     | Identifier3rdItem        |     | AmtPricePerUnit2     |     |
|     | CompanyKeyOrderNo   [PK1]     |         |     | QuantityOnWoReceipt  |     |     |     |                          |     | AmountCreditPrice    |     |
|     | DocumentOrderInvoiceE   [PK2] |         |     | Qty1OtherPrimaryUn   |     |     |     | LotGrade                 |     |                      |     |
|     | OrderType   [PK3]             |         |     | Qty2OtherPrimaryUn   |     |     |     | AmountUnitCost           |     | BasisCode            |     |
|     | AddressNumber   [PK4]  [FK]   |         |     | QtyOtherPurchasing1  |     |     |     | CostingSelectionPurchasi |     | LedgType             |     |
|     |                               |         |     |                      |     |     |     | CostingSelectionInventor |     | FactorValue          |     |
|     | Non-Key Data                  |         |     | QtyHardCommitted     |     |     |     |                          |     |                      |     |
|     | OrderSuffix                   |         |     |                      |     |     |     | UserReservedCode         |     |                      |     |
|     | C o s tC                      | e n ter |     |                      |     |     | .   |                          |     |                      |     |
|     | C o m pa                      | n y     |     |                      |     |     |     | .                        |     |                      |     |
CompanyKeyOriginal
|     | OriginalPoSoNumber |     |     |     |     |     |     |     |     | SalesOrderHis.toryFileFlexibleVe |     |
| --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- |
.
|     |     |     |     |     | .   |     |     |     |     | Key Data |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
SalesOrder/PurchasingTextDetail
|     |     |     |     |     |     | Key Data |     |     |     | CompanyKeyOrderNo   [PK1] |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | ------------------------- | --- |
. C o m p a n y K e y O r d e r N o     [P K 1 ]   [F K ] D o c u m e n tO r d e rI n vo iceE   [PK2]
|     | C u s to m e rMaster |     |     |     |     |       |                       |                                       |     | O r d e r T y p e    |   [ P K 3 ]     |
| --- | -------------------- | --- | --- | --- | --- | ----- | --------------------- | ------------------------------------- | --- | -------------------- | --------------- |
|     | K e y  D a ta        |     |     |     |     | D o c | u m e n tO r d e      | r I n v o ic e E     [P K 2 ]   [F K] |     |                      |                 |
|     |                      |     |     |     |     | O rd  | e r T y p e       [ P | K 3 ]     [F K ]                      |     | Li n e N u m b e r   |       [ P K 4 ] |
A d d re ss N u m b er   [PK1] S a le s O rd erHeaderHistoryFileFlex L i n e N u m b e r     [ P K 4]    [ F K ] N o n - K e y   D ata
|     | N o n -K e y  D a ta |     | K e y |  D a ta |     | L i n e | N u m b e r W | o r kO r d e r     [PK5] | .   | O r d e r S u ff i x |     |
| --- | -------------------- | --- | ----- | ------- | --- | ------- | ------------- | ------------------------ | --- | -------------------- | --- |
ARClass
|     |                     |     | CompanyKeyOrderNo   [PK1]     |     |     | UniqueKeyIDInternal   [PK6]  [FK] |     |     |     | CostCenter |     |
| --- | ------------------- | --- | ----------------------------- | --- | --- | --------------------------------- | --- | --- | --- | ---------- | --- |
|     | CostCenterArDefault |     | DocumentOrderInvoiceE   [PK2] |     |     | IdentifierShortItem   [PK7]  [FK] |     |     |     | Company    |     |
O b je c tA c c t sR e ce i v a b l e O r d e r T y p e      [ P K 3 ] C o s tC e n t e r     [P K .8 ]   [F K] C o m p a n y K e y O ri gi n a l
|     | Su b s id ia r y A cc | ts R e c e i v |     |     |     | Lo c | a tio n      [ P K 9] |    [F K ] |     |     |     |
| --- | --------------------- | -------------- | --- | --- | --- | ---- | --------------------- | --------- | --- | --- | --- |
CompanyKeyARModel O r d e r S u ff ix       [P K 4 ] O ri gi n a lP o S o N u m b e r
|     |                       |        | Non-Key Data       |     |     | Lot   [PK10]  [FK] |     |     |               | OriginalOrderType  |     |
| --- | --------------------- | ------ | ------------------ | --- | --- | ------------------ | --- | --- | ------------- | ------------------ | --- |
|     | D o c A rD e fa u ltJ | e      | CostCenter         |     |     |                    |     |     |               | OriginalLineNumber |     |
|     | D o c Ty A rD e fa    | u ltJe |                    |     |     |                    |     |     |               |                    |     |
|     | CurrencyCodeFrom      |        | Company            |     |     |                    |     |     |               |                    |     |
|     |                       |        | CompanyKeyOriginal |     |     |                    |     |     | AccountLedger |                    |     |
|     | TaxArea1              |        | OriginalPoSoNumber |     |     |                    |     |     | Key Data      |                    |     |
TaxExplanationCode1
|     | AmountCreditLimit |     | OriginalOrderType |     |     |     |     |     | CompanyKey   [PK1]               |     |     |
| --- | ----------------- | --- | ----------------- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- |
|     | ArHoldInvoices    |     | CompanyKeyRelated |     |     |     |     |     | DocumentType   [PK2]             |     |     |
|     |                   |     | RelatedPoSoNumber |     |     |     |     |     | DocVoucherInvoiceE   [PK3]       |     |     |
|     | PaymentTermsAR    |     | RelatedOrderType  |     |     |     |     |     |                                  |     |     |
|     | AltPayor          |     |                   |     |     |     |     |     | DateForGLandVoucherJULIA   [PK4] |     |     |
|     |                   |     | AddressNumber     |     | .   |     |     |     | JournalEntryLineNo   [PK5]       |     |     |
LineExtensionCode   [PK6]
OrderType   [PK28]  [FK]
LineNumber   [PK29]  [FK]
|     |                                 |     |     |                            | .   |     |     |     | CompanyKeyOrderNo   [PK15]  [FK]     |     |     |
| --- | ------------------------------- | --- | --- | -------------------------- | --- | --- | --- | --- | ------------------------------------ | --- | --- |
|     |                                 |     |     |                            |     |     |     | .   | DocumentOrderInvoiceE   [PK16]  [FK] |     |     |
|     | ItemLedgerFile                  |     |     |                            |     |     |     |     | OrderSuffix   [PK33]  [FK]           |     |     |
|     | Key Data                        |     |     |                            |     |     |     |     | Non-Key Data                         |     |     |
|     | OrderType   [PK5]  [FK]         |     |     | AccountsReceivableLedger   |     |     |     |     | GLPostedCode                         |     |     |
|     | DocumentOrderInvoiceE   [PK4]   |     |     | Key Data                   |     |     |     |     |                                      |     |     |
|     |                                 |     |     |                            |     |     |     | .   | BatchNumber                          |     |     |
|     | [FK]                            |     |     | CompanyKey   [PK1]         |     |     |     |     | BatchType                            |     |     |
|     | CompanyKeyOrderNo   [PK3]  [FK] |     |     | DocumentType   [PK2]       |     |     |     |     |                                      |     |     |
|     | LineNumber   [PK6]  [FK]        |     |     | DocVoucherInvoiceE   [PK3] |     |     |     |     |                                      |     |     |
UniqueKeyIDInternal   [PK1]
DocumentPayItem   [PK4]
OrderSuffix   [PK2]  [FK] DocTypeMatching   [PK5] PriceAdjustmentDetail
|     | Non-Key Data |     |     | DocMatchingCheckOr   [PK6] |     |     |     |     |     | Key Data                    |     |
| --- | ------------ | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --------------------------- | --- |
|     |              |     |     | Non-Key Data               |     |     |     |     |     | PriceAdjustmentType   [PK1] |     |
NoOfLinesOnOrder
IdentifierShortItem AddressNumber IdentifierShortItem   [PK2]  [FK]
|     | Identifier2ndItem |     |     | DateInvoiceJ |     |     |     |     |     | AddressNumber   [PK20]  [FK] |     |
| --- | ----------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | ---------------------------- | --- |
Identifier3rdItem DocPayItemMatchCI ItemCustomerKeyID   [PK3]  [FK]
CostCenter DateMatchingCheckOr CurrencyCodeFrom   [PK4]  [FK]
Location DateForGLandVoucherJULIA UnitOfMeasureAsInput   [PK5]  [FK]
Lot FiscalYear1 S.O.DetailLedgerFileFlexibleVer QuantityMinimum   [PK6]
|     | ParentLot |     |     | Century |     |     | Key Data |     |     | DateExpiredJulian1   [PK7]  [FK] |     |
| --- | --------- | --- | --- | ------- | --- | --- | -------- | --- | --- | -------------------------------- | --- |
StorageUnitNumber PeriodNoGeneralLedge CompanyKeyOrderNo   [PK1]  [FK] LedgType   [PK19]  [FK]
SequenceNumberLocati Company DocumentOrderInvoiceE   [PK2]  [FK] CompanyKeyOrderNo   [PK8]  [FK]
TransactionLineNr BatchType OrderType   [PK3]  [FK] DocumentOrderInvoiceE   [PK9]  [FK]
|     | FromTo |     |     | BatchNumber |     |     |     |     |     | OrderType   [PK10]  [FK] |     |
| --- | ------ | --- | --- | ----------- | --- | --- | --- | --- | --- | ------------------------ | --- |
LineNumber   [PK4]  [FK]
LotMasterCardexYN DateBatchJulian CostCenter   [PK17]  [FK] LineNumber   [PK11]  [FK]
LotStatusCode AddressNumberParent AddressNumber   [PK20]  [FK] LineNumberWorkOrder   [PK12]  [FK]
LotPotency AddNoAlternatePayee IdentifierShortItem   [PK16]  [FK] UniqueKeyIDInternal   [PK13]  [FK]
|     | LotGrade |     |     |              |     |     |                         |     |     | CostCenter   [PK14]  [FK] |     |
| --- | -------- | --- | --- | ------------ | --- | --- | ----------------------- | --- | --- | ------------------------- | --- |
|     |          |     |     | GLPostedCode |     |     | Location   [PK18]  [FK] |     |     |                           |     |
ItemNumberShortKit BalancedJournalEntries Lot   [PK19]  [FK] Location   [PK15]  [FK]
CostCenterAlt PayStatusCode FromPotency   [PK21]  [FK] Lot   [PK16]  [FK]
|     |     |     |     | AmountGross |     |     | UnitOfMeasureAsInput   [PK23]  [FK] |     |     | LotGrade   [PK17]  [FK] |     |
| --- | --- | --- | --- | ----------- | --- | --- | ----------------------------------- | --- | --- | ----------------------- | --- |
CompanyKey   [PK24]  [FK]

|     |     | W o r k O r d e r I n s t r u c t io n s F il e |     | W o r k O r d e r M a s t e rF il e |     |     |
| --- | --- | ----------------------------------------------- | --- | ----------------------------------- | --- | --- |
I t e m B r a n c h F i l e K e y   D a t a K e y   D a t a S h o p F l o o r C o n t r o lR o u t in g I n st ru c t
| K e y  D a | t a | D o c u m e n t O r d e r I n v o ic e E     [PK1]  [FK] |     |     | K e y   D a t a |     |
| ---------- | --- | -------------------------------------------------------- | --- | --- | --------------- | --- |
C o s t C e n t e r     [ P K 2 ]    [ F K ] O r d e r T y p e       [ P K 2 ] D C o a c t e u g m o e r i n e t s O W rd o e r k r I O n r v d o e ic r 0 e 0 E 1          [   P [ P K K 1 2 ] ]     [ F K ] D o c u m e n t O r d e r I n vo i c e E      [P K 1 ]   [FK]
S y s t e m C o d e      [ P K 3 ]    [ F K] O r d e r S u f f i x       [P K 3 ] C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 3 ]     [ F K ] It e m N u m b e r S h o r t K it      [ P K 7 ]
Non-Key Data WODetailedRecordType   [PK4] CategoriesWorkOrder003   [PK4]  [FK] SequenceNoOperations   [PK3]
I d e n t i f i e r 2 n d I t e m L i n e N u m b e r W o r k O r d e r       [ P K 5 ] T y p e O p e r a t i o n C o d e       [ P K 4 ]
I d e n t i f i e r 3 r d I t e m C a t e g o r i e s W o r k O r d e r 0 0 1       [ P K 6 ]     [ F K ] N o n - K e y   D a t a A t o L i n e T y p e       [ P K 5 ]
S a l e s R e p o r t i n g C o d e 1 C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 7 ]     [ F K ] O r d e r T y p e P a r e n t S e g m e n t N u m b e r       [ P K 6 ]
S a l e s R e p o r t i n g C o d e 2 C a t e g o r i e s W o r k O r d e r 0 0 3       [ P K 8 ]     [ F K ] O r d e r S u . f f i x C a t e g o r i e s W o r k O r d e r 0 0 1       [ P K 8 ]     [ F K ]
S a l e s R e p o r t i n g C o d e 3 N o n - K e y   D a t a R R e e l l a a t t e e d d O P o r d S e o r N T y u p m e b e r C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 9 ]     [ F K ]
S a l e s R e p o r t i n g C o d e 4 D a t e A s s o c i a t e d S a r L i n e N u m b e r C a t e g o r i e s W o r k O r d e r 0 0 3       [ P K 1 0 ]    [F K ]
S a l e s R e p o r t i n g C o d e 5 D e s c r i p t i o n W o r k O r d e r P e g T o W o r k O r d e r N o n - K e y   D a t a
S a l e s R e p o r t i n g C o d e 6 A s s o c i a t e d I t e m N o 1 P a r e n t W o N u m b e r O r d e r T y p e .
| S a l e s R e | p o r t i n g C o d e 7 |     |     | T y p e W o | O r d e r S u f f i x |     |
| ------------- | ----------------------- | --- | --- | ----------- | --------------------- | --- |
S a l e s R e p o r t i n g C o d e 8 P r i o r i t y W o . T y p e R o u t i n g
S a l e s R e p o r t i n g C o d e 9 D e s c r i p t i o n 0 0 1 I t e m N u m b e r 2 n d K i t
S a l e s R e p o r t i n g C o d e 1 0 S t a t u s C o m m e n t W o I t e m N u m b e r 3 r d K i t
P u r c h a s i n g R e p o r t C o d e 1 . C o m p a n y C o s t C e n t e r A l t
P u r c h a s i n g R e p o r t C o d e 2 S h o p F l o o r C o n t r o l P a r t s L i s t C o s t C e n t e r L i n e I d e n t i f i e r
P u r c h a s i n g R e p o r t C o d e 3 K e y   D a t a C o s t C e n t e r A l t A u t o L o a d D e s c r i p t i o n
P u r c h a s i n g R e p o r t C o d e 4 D o c u m e n t O r d e r I n v o i c e E       [ P K 5 ]     [ F K ] L o c a t i o n D e s c r i p t i o n L i n e 1
P u r c h a s i n g R e p o r t C o d e 5 U n i q u e K e y I D I n t e r n a l       [ P K 1 ] . A i s l e L o c a t i o n O p e r a t i o n S t a t u s C o d e W o
P u r c h R e p o r t i n g C o d e 6 C a t e g o r i e s W o r k O r d e r 0 0 1       [ P K 2 ]     [ F K ] B i n L o c a t i o n I n s p e c t i o n C o d e
P u r c h R e p o r t i n g C o d e 7 . C a t e g o r i e s W o r k O r d e r 0 0 2       [ P K 3 ]     [ F K ] S t a t u s C o d e W o T i m e B a s i s C o d e
P P u u r r c c h h R R e e p p o o r r t t i i n n g g C C o o d d e e 8 9 C a t e g o r i e s W o r k O r d e r 0 0 3       [ P K 4 ]     [ F K ] D a t e S t a t u s C h a n g e d L a b o r O r M a c h i n e
P u r c h R e p o r t i n g C o d e 1 0 N o n - K e y   D a t a S u b s i d i a r y P a y P o i n t C o d e
| C o m m o     | d i t y C o d e         | O r d e r T y p e                   |     | A d d r e s s N u m b e r               |     |     |
| ------------- | ----------------------- | ----------------------------------- | --- | --------------------------------------- | --- | --- |
| P r o d u c t | G r o u p F r o m       | O r d e r S u f f i x               |     | A d d N o O r i g i n a t o r           |     |     |
| D i s p a t c | h G r p                 | T y p e B i l l                     |     | A d d r e s s N u m b e r M a n a g e r |     |     |
| P r i m a r y | L a s t V e n d o r N o | F i x e d O r V a r i a b l e Q t y |     | S u p e r v i s o r                     |     |     |
A d d r e s s N u m b e r P l a n n e r I s s u e T y p e C o d e A d d N o A s s i g n e d T o W o r k O r d e r T i m e T r a n s a c t i o n s
| B u y e r |     | C o p r o d u c t s B y p r o d u c t s |     | A d d r e s s N u m b e r I n s p e c t o r | K e y   D a t a |     |
| --------- | --- | --------------------------------------- | --- | ------------------------------------------- | --------------- | --- |
G l C a t e g o r y C o m p o n e n t T y p e N e x t A d d r e s s N u m b e r U n i q u e K e y I D I n t e r n a l     .   [ P K 1 ]
| C o u n t r y | O f O r i g i n | C o m p o n e n t N u m b e r |     | D a t e T r a n s a c t i o n J u l i a n |     |     |
| ------------- | --------------- | ----------------------------- | --- | ----------------------------------------- | --- | --- |
R e o r d e r P o i n t I n p u t F r o m P o t e n c y D a t e S t a r t N o n - K e y   D a t a
R e o r d e r Q u a n t i t y I n p u t T h r u P o t e n c y D a t e R e q u e s t e d J u l i a n P r o c e s s e d C o d e
R e o r d e r Q u a n t i t y M a x i m u m F r o m G r a d e D a t e W o P l a n C o m p l e t e d D o c u m e n t O r d e r I n v o i c e E
| R e o r d e | r Q u a n t i t y M i n im u m | T h r u G r a d e |     | D a t e C o m p l e t i o n | O r d e r T y p | e   |
| ----------- | ------------------------------ | ----------------- | --- | --------------------------- | --------------- | --- |
O r d e r M u l t i p l e s C o m p a n y K e y R e l a t e d D D a a t t e e A A s s s s i i g g n n e T d o T I n o s p e c t o r A P d a d y r r o e l s l T s r N a u n m s a b c e t r i o n N o
S e r v i c e L e v e l R e l a t e d P o S o N u m b e r P a p e r P r i n t e d D a t e I t e m N u m b e r S h o r t K i t
S a f e t y S t o c k D a y s S u p p l y R e l a t e d O r d e r T y p e C a t e g o r i e s W o r k O r d e r 0 0 4 I t e m N u m b e r 2 n d K i t
S h e l f L i f e D a y s R e l a t e d P o S o L i n e N o C a t e g o r i e s W o r k O r d e r 0 0 5 I t e m N u m b e r 3 r d K i t
C h e c k A v a i l a b i l i t y Y N S e q u e n c e N o O p e r a t i o n s C a t e g o r i e s W o r k O r d e r 0 0 6 C o s t C e n t e r A l t
L a y e r C o d e S o u r c e B u b b l e S e q u e n c e C a t e g o r i e s W o r k O r d e r 0 0 7 C o s t C e n t e r
L o t S t a t u s C o d e R e s o u r c e P e r c e n t C a t e g o r i e s W o r k O r d e r 0 0 8 S e q u e n c e N o O p e r a t i o n s
C o n s t a n t F u t u r . e U s e 1 P R e e r w c o e r n k t P O e f S r c c e r n a t p C a t e g o r i e s W o r k O r d e r 0 0 9 O p e r a t i o n S t a t u s C o d e W o
|     | .   | AsIsPercent          |     | CategoriesWorkOrder010 | ReasonCde             |     |
| --- | --- | -------------------- | --- | ---------------------- | --------------------- | --- |
|     |     | PercentCumulativePla |     | Reference1             | TypeOfHours           |     |
|     |     | StepScrapPercent     |     | Reference2Vendor       | NameRemarkExplanation |     |
|     |     | LeadtimeOffsetDays   |     | AmountOriginalDollars  | BatchNumber           |     |
|     |     | ComponentItemNoShort |     | CrewSize               | DocumentType          |     |
|     |     | ComponentItemNo2nd   |     | RateDistribuOrBill     | DtForGLAndVouch1      |     |
ComponentThirdNumber
|     |     | BranchComponent |     |     | .   |     |
| --- | --- | --------------- | --- | --- | --- | --- |
DescriptionLine1
DescriptionLine2
| C o P r o d u ctsPlanning/CostingTable |     | L o c ation   |     |     |               |     |
| -------------------------------------- | --- | ------------- | --- | --- | ------------- | --- |
| K e y   D a ta                         |     | L o t         |     |     | AccountLedger |     |
| CostCenterAlt   [PK1]                  |     | AddressNumber |     |     | Key Data      |     |
IdentifierShortItem   [PK2]  [FK] LineType CompanyKey   [PK1]
B r a n c h C om p o n e n t       [P K 3 ] S e r i a lN u m b e r L o t It e m M a s te r . . D o c u m e n tT y p e      [ P K 2 ]
E ff e c ti v eT hr u D a te       [ P K 4 ] D a t e T ra n s a ct i o n Julian N o n -K e y  D ata D o c V ou c h e rI n v o i c e E     [PK3]
ItemNumberShortKit   [PK5] DateRequestedJulian Identifier2ndItem DateForGLandVoucherJULIA   [PK4]
CostCenter   [PK6]  [FK] BeginningHhMmSs Identifier3rdItem JournalEntryLineNo   [PK5]
Non-Key Data UnitsTransactionQty DescriptionLine1 LineExtensionCode   [PK6]
F e a t u r e C o s t P e r c e n t Q u a n tit y T ra n s a c t io n D e s c r i p ti o n L i n e 2 A c c o u n t I d       [ P K 9 ]     [ F K ]
E f f e c t i v e F r o m D a t e U n i t s Q u a n t i t y C a n c e le d S e a r c h T e x t S u b l e d g e r       [ P K 1 3 ]     [ F K ]
F e a t u r e P l a n n e d P e r cent U n i t s Q u a n B a c k o r H e ld S e a r c h T e x t C o m p re s s ed S L e u d b g l e e d r g T e y p r T e y     p   [ e P     K   [ 7 P ] K     [ 1 F 4 K ]   ]   [ F K ]
U s e r I d . S a l e s R e p o r t i n g C o d e 1 C e n t u r y       [ P K 1 0 ]     [ F K ]
P r o g r a m I d S a l e s R e p o r t i n g C o d e 2 F i s c a l Y e a r 1       [ P K 1 1 ]     [ F K ]
W o r k S t a t i o n I d S S a a l l e e s s R R e e p p o o r r t t i i n n g g C C o o d d e e 3 4 F i s c a l Q t r F u t u r e U s e       [ P K 1 2 ]   [FK]
|     |                                                             | .          | SalesReportingCode5   |                                   | AssetItemNumber   [PK8]  [FK]                                     |                           |
| --- | ----------------------------------------------------------- | ---------- | --------------------- | --------------------------------- | ----------------------------------------------------------------- | ------------------------- |
|     |                                                             |            | SalesReportingCode6   |                                   | Non-Key Data                                                      |                           |
|     |                                                             |            | SalesReportingCode7   |                                   | GLPostedCode                                                      |                           |
|     |                                                             |            | SalesReportingCode8   |                                   | BatchNumber                                                       |                           |
|     |                                                             |            | SalesReportingCode9   |                                   | BatchType                                                         |                           |
|     |                                                             |            | SalesReportingCode10  |                                   | DateBatchJulian                                                   |                           |
|     |                                                             |            | PurchasingReportCode1 |                                   | DateBatchSystemDateJuliA                                          |                           |
|     | CostCenterMaster                                            |            | PurchasingReportCode2 |                                   | BatchTime                                                         |                           |
|     | Key Data                                                    |            | PurchasingReportCode3 |                                   | Company                                                           |                           |
|     | CostCenter   [PK1]                                          |            | PurchasingReportCode4 |                                   |                                                                   |                           |
|     |                                                             |            | P u r c               | h a s i n g R e p o r t C o d e 5 |                                                                   |                           |
|     | N o n - K e y   D a t a                                     |            | P u r c               | h R e p o r t i n g C o d e 6     |                                                                   |                           |
|     | C o s t C e n t e r T y p e                                 |            | P u r c               | h R e p o r t i n g C o d e 7     |                                                                   |                           |
|     | D e s c r i p C o m p r e s s e d                           |            | P u r c               | h R e p o r t i n g C o d e 8     |                                                                   |                           |
|     | L e v e l O f D e t a i l C c C o d                         | e          | P u r c               | h R e p o r t i n g C o d e 9     | W o r k O r d e r V a r. i a n                                    | c e                       |
|     | C o m p a n y                                               |            | P u r c               | h R e p o r t i n g C o d e 1 0   |                                                                   |                           |
|     | A A d d d d r r e e s s s s N N u u m m b b e e r r J o b A | r          | C o m                 | m o d i t y C o d e               | K e y   D a t a                                                   |                           |
|     | C o u n t y                                                 |            | P r o d               | u c t G r o u p F r o m           | D o c u m e n t O r d e r I n                                     | v o i c e E      [ P K 1] |
|     | S t a t e                                                   |            | D i s p               | a t c h G r p                     | I d e n t i f i e r S h o r t I t e m                             |       [ P K 2 ]           |
|     | M o d e l A c c o u n t s a n d C                           | o n s olid | P r i c i             | n g C a t e g o r y               | C P a o r s e t T n y t C p h e i   l   d   [ R P e K l a 3 t ] i | o n s h i       [ P K 4 ] |
|     | D e s c r i p t i o n 0 0 1                                 |            | R e p r               | i c e B a s k e t P r i c e C a t |                                                                   |                           |
|     | D e s c r i p t i o n 0 1 0 0 2                             |            | O r d e               | r R e p r ic e C a t e g o r y    | N o n - K e y   D a t a                                           |                           |
|     | D e s c r i p t i o n 0 1 0 0 3                             |            | B u y e               | r                                 | O r d e r T y p e                                                 |                           |
|     | D e s c r i p t i o n 0 1 0 0 4                             |            | D r a w               | i n g N u m b e r                 | S e q u e n c e N o O p e                                         | r a t i o n s             |
|     | C a t e g o r y C o d e C o s t C                           | t 0 0 1    | R e v i               | s i o n N u m b e r               | I d e n t i f i e r 2 n d I t e m                                 |                           |
|     | C a t e g o r y C o d e C o s t C                           | t 0 0 2    | D r a w               | i n g S i z e                     | I d e n t i f i e r 3 r d I t e m                                 |                           |
|     | CategoryCodeCostCt003                                       |            |                       |                                   | V StandardUnits a r i a n c e C o d e                             |                           |
|     | CategoryCodeCostCt004                                       |            |                       |                                   | StandardAmount                                                    |                           |
|     | CategoryCodeCostCt005                                       |            |                       |                                   | ActualUnits                                                       |                           |
|     | CategoryCodeCostCt006                                       |            | .                     |                                   | ActualAmount                                                      |                           |
|     | CategoryCodeCostCt007                                       |            |                       |                                   | CurrentUnits                                                      |                           |
|     | CategoryCodeCostCt008                                       |            |                       |                                   | CurrentAmount                                                     |                           |
|     | CategoryCodeCostCt009                                       |            |                       |                                   | PlannedUnits                                                      |                           |
|     | CategoryCodeCostCt010                                       |            |                       |                                   | PlannedAmount                                                     |                           |
|     | CategoryCodeCostCt011                                       |            |                       |                                   | CompletedUnits                                                    |                           |
|     | CategoryCodeCostCt012                                       |            |                       |                                   | CompletedAmount                                                   |                           |
|     | CategoryCodeCostCt013                                       |            |                       |                                   | ScrappedUnits                                                     |                           |
|     | CategoryCodeCostCt014                                       |            |                       |                                   | ScrappedAmount                                                    |                           |
|     | CategoryCodeCostCt015                                       |            |                       |                                   | CurrentUnaccountedUnits                                           |                           |
|     | CategoryCodeCostCt016                                       |            |                       |                                   | CurrentUnaccountedAmount                                          |                           |
|     | CategoryCodeCostCt017                                       |            |                       | .                                 | UnpostableUnits                                                   |                           |
|     | CategoryCodeCostCt018                                       |            |                       |                                   | UnpostableAmount                                                  |                           |
|     | CategoryCodeCostCt019                                       |            |                       |                                   | UnitOfMeasureAsInput                                              |                           |
|     | CategoryCodeCostCt020                                       |            |                       |                                   | UserId                                                            |                           |
|     | CategoryCodeCostCt021 CategoryCodeCostCt022                 |            |                       |                                   | ProgramId                                                         |                           |
|     | CategoryCodeCostCt023                                       |            |                       |                                   | DateUpdated                                                       |                           |
|     | sdfsd                                                       |            |                       |                                   | TimeOfDay                                                         |                           |
|     | CategoryCodeCostCenter25                                    |            |                       |                                   | WorkStationId                                                     |                           |
CategoryCodeCostCenter26
CategoryCodeCostCenter27
CategoryCodeCostCenter28
CategoryCodeCostCenter29

WorkflowProcessRouteMaster
Key Data
ProcessName   [PK1]
ProcessVersion   [PK2]
Non-Key Data
ProcessDescription
ProcessVersionStatus
SystemCodeReporting
ProcessDataStructure
ProcessKeyDataStructure
NextProcessInstance
WorkflowIconPath
GenericLong
|     | ProcessCategoryCode1 | WorkflowActivityRelationships |
| --- | -------------------- | ----------------------------- |
|     | ProcessCategoryCode2 | Key Data                      |
WorkflowOrganizationalStructure ProcessCategoryCode3 ProcessName   [PK1]  [FK]
|     | UserId | ProcessVersion   [PK2]  [FK] |
| --- | ------ | ---------------------------- |
Key Data
|                        | ProgramId     | ActivityName   [PK3]  [FK] |
| ---------------------- | ------------- | -------------------------- |
| ProcessName   [PK1]    | WorkStationId |                            |
| ProcessVersion   [PK2] |               | NextActivity   [PK4]       |
|                        | DateUpdated   | TransitionValue   [PK5]    |
ActivityName   [PK3]
| RulesValue   [PK4] | TimeOfDay | Non-Key Data |
| ------------------ | --------- | ------------ |
| Non-Key Data       |           | UserId       |
ProgramId
OrganizationalModel
WorkStationId
| OrganizationTypeStructur |     | DateUpdated |
| ------------------------ | --- | ----------- |
UserId
TimeOfDay
ProgramId
| WorkStationId | WorkflowActivityRouteMaster |     |
| ------------- | --------------------------- | --- |
| DateUpdated   | Key Data                    |     |
TimeOfDay
ProcessName   [PK1]  [FK]
ProcessVersion   [PK2]  [FK]
ActivityName   [PK3]
WorkflowActivitySpecifications
|     | Non-Key Data        | Key Data          |
| --- | ------------------- | ----------------- |
|     | ActivityDescription | EVERESTPT   [PK1] |
ActivityType
ApplicationIDOW   [PK2]
|     | NextActivityInstance | FRMIDEVEREST   [PK3] |
| --- | -------------------- | -------------------- |
WorkflowIconPath
ControlID   [PK4]
|     | GenericLong         | EVERESTWEVENT   [PK5] |
| --- | ------------------- | --------------------- |
|     | TransitionAttribute | EVERESTERID3   [PK6]  |
TransitionFunction
Non-Key Data
TransitionAndJoin
|     | StructureAttribute | EVERESTEVSPEC |
| --- | ------------------ | ------------- |
EventSpecKey
| WorflowOrganizationalModelMaste | StructureFunction     |                |
| ------------------------------- | --------------------- | -------------- |
| Key Data                        |                       | EventRulesBlob |
|                                 | ActivityCategoryCode1 | ProcessName    |
| OrganizationalModel   [PK1]     | ActivityCategoryCode2 |                |
ActivityName
| OrganizationTypeStructur   [PK2] | ActivityCategoryCode3 | ProcessVersion |
| -------------------------------- | --------------------- | -------------- |
| ProcessName   [PK3]  [FK]        | UserId                |                |
| ProcessVersion   [PK4]  [FK]     | ProgramId             |                |
| ActivityName   [PK5]  [FK]       | WorkStationId         |                |
| RulesValue   [PK6]  [FK]         | DateUpdated           |                |
| Non-Key Data                     | TimeOfDay             |                |
ThresholdBusinessFunction
| Threshold          |     | WorkflowActivityInstance  |
| ------------------ | --- | ------------------------- |
| AssociatedDataItem |     | Key Data                  |
| GroupType          |     | ProcessName   [PK1]  [FK] |
WorkflowProcessInstance
| AuthorizationRequired |     | ProcessVersion   [PK2]  [FK] |
| --------------------- | --- | ---------------------------- |
Key Data
| HigherLevelOverride |                     | ProcessInstance   [PK3]  [FK] |
| ------------------- | ------------------- | ----------------------------- |
| UserId              | ProcessName   [PK1] | ActivityName   [PK4]          |
ProcessVersion   [PK2]
| ProgramId |     | Activitystance   [PK5] |
| --------- | --- | ---------------------- |
WorkStationId ProcessInstance   [PK3] OrganizationalGroupNumber   [PK6]
| DateUpdated | Non-Key Data | SequenceNumber9   [PK7] |
| ----------- | ------------ | ----------------------- |
ProcessStatus
| TimeOfDay |                | Non-Key Data |
| --------- | -------------- | ------------ |
|           | AttributesData | Resource     |
KeyData
RequiredYN9
InstanceOriginator
ActivityStatus
|     | StartDate9 | ActivityAction |
| --- | ---------- | -------------- |
StartTime
HigherLevelOverride
|     | EndDate9 | EmailSerialNumber |
| --- | -------- | ----------------- |
EndTime
StartDate9
StartTime
EndDate9
EndTime
SubProcessDescription
SubProcessInstance
SubProcessVersion

WorkOrderDefaultCodingFile
WorkOrderRecordTypesFile
Key Data
Key Data
CategoriesWorkOrder001   [PK1]
| CategoriesWorkOrder002   [PK2] |     | WODetailedRecordType   [PK1] |
| ------------------------------ | --- | ---------------------------- |
CategoriesWorkOrder003   [PK3] DocumentOrderInvoiceE   [PK2]  [FK]
CategoriesWorkOrder001   [PK3]  [FK]
Non-Key Data
CategoriesWorkOrder002   [PK4]  [FK]
| AddressNumberManager |     | CategoriesWorkOrder003   [PK5]  [FK] |
| -------------------- | --- | ------------------------------------ |
Supervisor
Non-Key Data
Description001
SubTitleDescription01
SubTitleDescription02
SubTitleDescription03
SubTitleDescription04
. SubTitleDescription05
SubTitleDescription06
Item1EditSystem
Item1EditCodes
Item2EditSystem
| WorkOrderMasterFile           |     | Item2EditCodes  |
| ----------------------------- | --- | --------------- |
| Key Data                      |     | Item3EditSystem |
| DocumentOrderInvoiceE   [PK1] |     | Item3EditCodes  |
CategoriesWorkOrder001   [PK2]  [FK]
CategoriesWorkOrder002   [PK3]  [FK]
CategoriesWorkOrder003   [PK4]  [FK]
| Non-Key Data | .   |     |
| ------------ | --- | --- |
OrderType
OrderSuffix
RelatedOrderType
RelatedPoSoNumber
LineNumber
PegToWorkOrder
| ParentWoNumber  |     | WorkOrderInstructionsFile            |
| --------------- | --- | ------------------------------------ |
| TypeWo          |     | Key Data                             |
| PriorityWo      |     | DocumentOrderInvoiceE   [PK1]  [FK]  |
| Description001  |     | OrderType   [PK2]                    |
| StatusCommentWo |     | OrderSuffix   [PK3]                  |
| Company         |     | WODetailedRecordType   [PK4]         |
| CostCenter      |     | LineNumberWorkOrder   [PK5]          |
| CostCenterAlt   |     | CategoriesWorkOrder001   [PK6]  [FK] |
| Location        | .   | CategoriesWorkOrder002   [PK7]  [FK] |
| AisleLocation   |     | CategoriesWorkOrder003   [PK8]  [FK] |
BinLocation
Non-Key Data
| StatusCodeWo      |     | DateAssociatedSar    |
| ----------------- | --- | -------------------- |
| DateStatusChanged |     | DescriptionWorkOrder |
Subsidiary
AssociatedItemNo1
| AddressNumber |     | AssociatedItemNo2 |
| ------------- | --- | ----------------- |
AddNoOriginator
AssociatedItemNo3
AddressNumberManager
Supervisor
AddNoAssignedTo
AddressNumberInspector
NextAddressNumber
DateTransactionJulian
DateStart
DateRequestedJulian
DateWoPlanCompleted
DateCompletion
DateAssignedTo
DateAssignToInspector
PaperPrintedDate
CategoriesWorkOrder004
CategoriesWorkOrder005
CategoriesWorkOrder006
CategoriesWorkOrder007
CategoriesWorkOrder008
CategoriesWorkOrder009
CategoriesWorkOrder010
Reference1
Reference2Vendor
AmountOriginalDollars
CrewSize
RateDistribuOrBill
PayDeductBenefitType
AmtChngToOriginalD

DataItemMaster
| DataFieldDisplayText | Key Data         |     |
| -------------------- | ---------------- | --- |
| Key Data             | DataItem   [PK1] |     |
DataItem   [PK1]  [FK]
Non-Key Data
| LanguagePreference   [PK2]    | SystemCode          |                           |
| ----------------------------- | ------------------- | ------------------------- |
| SystemCodeReporting   [PK3] . |                     |                           |
|                               | SystemCodeReporting | DataItemAlphaDescriptions |
| Non-Key Data                  | GlossaryGroup       |                           |
| ColTitle1XrefBuild            |                     | Key Data                  |
UserId
C o l T i t l e 2 X r e f B u i l d . P r o g r a m I d D a ta I te m     [ P K 1 ]    [F K ]
C o l T i t l e 3 X r e f B u i l d . La n g u a ge P r e fe r e n c e    [PK2]
D a t e U p d a ted
| DescriptionRow | WorkStationId | SystemCodeReporting   [PK3] |
| -------------- | ------------- | --------------------------- |
ScreenName   [PK4]
TimeLastUpdated
Non-Key Data
DescriptionAlpha
DescCompressed
.
.
DataDictionaryGenericTextKeyInd
Non-Key Data
|                 | DataFieldSpecifications | CompositeKey |
| --------------- | ----------------------- | ------------ |
|                 | .                       | ModelRecord  |
| DataItemAliases | Key Data                |              |
UserId
| Key Data               | DataItem   [PK1]  [FK] | DateQuestionEntered |
| ---------------------- | ---------------------- | ------------------- |
| DataItem   [PK1]  [FK] | Non-Key Data           |                     |
TimeEnteredProg
FieldNameAliasXrefIt   [PK2] DataItemClass RecordUpdateByUserNa
| AliasType   [PK3] | DataItemType | DateUpdated     |
| ----------------- | ------------ | --------------- |
|                   | DataItemSize | TimeLastUpdated |
DataFileDecimals
DataFieldParent
NumberOfArrayElements .
ValueForEntryDefault
| DataDictionaryErrorMessageProgr | JustifyLeftOrRghtCde |     |
| ------------------------------- | -------------------- | --- |
Data Dictionary Generic Text
| Key Data         | DataDisplayDecimals   |              |
| ---------------- | --------------------- | ------------ |
| DataItem   [PK1] | DataDisplayRules      | Non-Key Data |
|                  | DataDisplayParameters | Line-Number  |
Non-Key Data
|             | DataEditRules | Generic-Text |
| ----------- | ------------- | ------------ |
| ProgramName | DataEditOp1   |              |
DataEditOp2
HelpTextProgram
HelpListProgram
NextNumberingIndexNo
SystemCodeNextNumbe
ReleaseNumber
UserId
DateUpdated
ProgramId
WorkStationId
TimeLastUpdated