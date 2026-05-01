---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/How to Load New Products.doc.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# How to Load New Products.doc

## Source
File: `Brain/raw/.extract/SWINDON/How to Load New Products.doc.md`
Size: 2,270 bytes

## Raw content
How to Load New Products

To bulk load new products into the command center, complete the following steps:

Collect product information for Client products.  Look for product names, numbers, prices, descriptions, and pictures.

If client is already on-line, product images (.gif and .jpeg) can be collected from the Client web site and stored in a T&K “products” folder (/tk/images/products/)  Developers should collect both preview and full-size images.  Preview images should be re-sized to fit in a 50x50-pixel area, and full images should be sized to fit a 190x 140-pixel area.

Enter product information into an excel spreadsheet- columns should include:
Product ID
Product Name
Department (in the T&K Online store)
Price
Long Description
Preview Image File  *** should include path name to image file: /tk/images/products/imagename,  including extension
Full Image File  *** should include path name to image file:  /tk/images/products/ imagename, including extension
On-line Status *** should be “On-line” for all products you want online

Log on to the BroadVision Command Center, and open up the product category you wish to load client products into.  If you are creating a new category, do so by selecting Category-New from the top menu, and opening that category.  Make sure you choose a category or choose the “Unclassified” folder.  Otherwise, your products will be loaded into whatever category you happen to be in.

Go to the top menu and choose Products-Import to begin the data import.  You will follow a Wizard to complete the following steps.

Choose the Import Format (Excel 5.0)

Browse for the file to import (The Excel spreadsheet you created above.)  Choose to update duplicates.

Choose the table to import (If you have more than one page in your spreadsheet, this determines which page you want to import.)

Choose to “Map Attributes”- then map your spreadsheet columns to the appropriate attributes in the Command Center

Review the Import Summary, and Finish the import

Return to the Command Center and choose Tools-Notify Servers-Notify All from the top menu

If Step 10 doesn’t update the Command Center, refresh the cache by entering
cd retail
. bvvars
cache_utl –r cat –r cnt –r comm
 at the Unix prompt.



## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
