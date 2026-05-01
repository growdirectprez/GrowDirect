The GSLM supports location specific pricing, and will leverage industry standard promotional mechanics which can support Rollback and TAB pricing in addition to functionality for link saves (buy one get one) threshold discounts, and tiered pricing.  
Assumptions:
Item selling price will be held at location level in the GSLM
The GSLM does not model entities for establishing price zones, price zones are considered enterprise functionality, and location prices will be stored as point in time values on the SkuIteminSalesOutlet entity.
All temporary price effective dates and eligibility requirements are defined in the Promotion entities
Price date ranges on the SkutIteminSalesOutlet are an operational requirement for shelf label placement, they do not drive pricing logic in the model
Use Cases:
Send store specific regular price to store
Send store specific price change (permanent markdown) to store
Send promotional prices to store 
Buy / Get: Buy item(s)  and get other item(s) at a discounted price
Price Cut (Rollback): A simple price reduction promotion
Threshold: Buy a particular multiple of an item(s) and get some sort of discount based on a qty or amount spent
The following section describes the GSLM entities and their attributes which have been modeled as part of the Customer scope:
Offer Limit
Multiple promotions on an item at the same time
Promotion
Entity Name
Description
Promotion
The Promotion entity defines a set of activities designed to attract attention to a particular product and to increase its sales using discounts, advertising and publicity.  A promotion usually lasts for a short time, measured in weeks. (E.g. "Fourth of July", "Back to school", etc.)
Attribute
Type
Description
promotion_id 
 Number
The unique identifier of the Promotion
promotion_name 
 Text
The name of the Promotion (E.g. Back to School)
promotion_desc 
 Text
The extended description of the promotion

Promotion Component
Entity Name
Description
PromotionComponent
The promotion component entity defines the types of offers which are associated with a higher level promotions.  (E.g. Promotion: Back to School; Promotion Component: 10% off School Supplies)
Attribute
Type
Description
promo_component_id 
 Number
The unique identifier of the  promotion component
promotion_id 
 Promotions
The Foreign key to the promotions entity, the promotion to which the component is related
promo_component_name 
 Text
The name of the Promotion Component (E.g. Back to School 10% off Supplies)

Promotion Threshold
Entity Name
Description
PromotionThreshold
A condition or set of conditions that must be met for the customer to trigger the promotion and so be eligible for, or to receive the reward.
Attribute
Type
Description
threshold_id 
 Number
The unique identifier of the promotion threshold.  Promotion Thresholds can be assigned to more than on promotion via the promotions component detail entity.  This enables a single threshold structure which defines reward tiers to be used for any promotions that is based on the same mechanics.  (E.g. A Promotion Threshold which contains intervals such as Spend $10 get $1 off, Spend $30 get $3 off ,  can be used for a back to school promotions, or a holiday promotion without recreating the reward structure)
threshold_name 
 Text
The name of the promotion threshold which describes the reward structure of the threshold intervals (Buy on get one, $ off)
threshold_qualification_type 
 Code
The method used determines if a purchase meets the threshold. The qualification type can either be threshold or item level. If the qualification type is Threshold then the qualification criteria described in the related 'Threshold Interval' is related to the entire set of qualifying products in the buy list. If the qualification type is Item level then the qualification criteria described in the related 'Threshold Interval' is related to each different type of item.  For example : If a Promotion was set up to give a discount for any three items bought then the type would be Threshold and in the 'ThresholdInterval' entity the qty would be 3. If the promotion was to give a discount if any three of the same items were bought then the type would be Item and in the 'ThresholdInterval' entity the qty would be 3.

Threshold Interval
Entity Name
Description
ThresholdInterval
Threshold intervals define reward tiers which can be offered to a customer as part of the promotion.  
Attribute
Type
Description
threshold_interval_id 
 Number
The unique identifier of the threshold interval
threshold_id 
 PromotionThresholds
The foreign key to the Promotion Thresholds entity
threshold_type 
Code
A code which works in conjunction with the threshold_amount attribute to define how the requirements of the promotions are tracked.  Valid values would be amount or quantity  
threshold_amount 
 Amount
When the threshold type is amount then this field will hold the amount (value in money) of the qualifying purchases required to trigger the reward.
threshold_currency 
 Code
The currency code of the value contained in the  threshold_amount attribute.
threshold_qty 
 Number
When the threshold type is quantity then this field will hold the count in eaches or possibly volume or weight of the qualifying purchases that trigger the reward.  Qualifying purchase quantity.  E.g. buy two bottles of shampoo to get a bottle of conditioner.

Promotion Component Detail
Entity Name
Description
PromotionComponentDetail
The description of the type of promotion that is being applied.
Attribute
Type
Description
promo_component_dtl_id 
 Number
The promotion component detail ID
promo_component_id 
 PromotionComponents
The reference to the component this entity is part of
threshold_id 
PromotionThresholds
A Reference to the threshold held against this Component Detail
promo_detail_type
Code
This specifies the type of promotion, the main types are either Buy/Get (Buy so many of a particular item(s) and get a discount on another item(s)), Threshold (Exceed some threshold scenario qty/amount etc and get some form of discount) or Price Change (a simple reduced price on an item)
buy_item_type 
 Code
This specifies the purchasing behavior required to trigger the promotion, it can either be ALL (meaning all items listed on the promotion need to be purchased in order for the promotion to be triggered) or ANY (meaning any combinations of items attached to the promotion need to be bought in order to trigger the promotion). This is only applicable for Buy/Get type promotions.
buy_item_qty 
 Number
If buy_item_type is set to ANY then this stipulates how many items must be bought in total to trigger the promotion.
promo_limit_qty 
 Number
This attribute can be used to set a maximum number of this promotion a customer can qualify for.

Sales Outlet SKUItem Promo Comp Detail
Entity Name
Description
SalesOutletSKUItem
PromoCompDetail
The description of an item that is part of a promotion and the amount of discount that needs to be applied to the item if it is discounted in a particular promotion
Attribute
Type
Description
promo_component_dtl_id
 PromotionComponentDetails
The Identifier of the Promotion Component Detail Entity that this set of item attributes is related to
sku_item_in_sales_outlet_id
 SKUItemsInSalesOutlets
The item in location value where the promotional component detail will be applied
promo_change_type
Code
A code to describe the type of discount to be applied to this item. Examples values would be Amount Off, Percent Off, Fixed Price, No Change or Free
promo_change_amount
 Amount?
If the change_type is Amount Off or Fixed Price then this field will hold the amount accordingly
promo_change_percent
Decimal
If the change_type is Percent Off then this will hold the percentage that the item will be discounted
promo_change_selling_uom
 Code?
If the change_type is fixed price, then this will hold the unit of measure of the fixed price (amount)
promo_change_currency
 Code?
The currency code of the promotional amount off
promo_start_date
 Date?
The start date of the item promotion in the store
promo_end_date
 Date?
The end date of the item promotion in the store
promo_sequence_nbr
Number
If and item is part of mutliple active promotions, this specifies the sequence in which the discounts should be applied.









Global Store Logical Model – Price & Promotion



