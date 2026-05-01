BroadVision One-To-One

Verity enhancement

This document describes new functionality provided in Version 4.1D of BroadVision® One-To-One™
Enterprise for working with the Verity SEARCH’97 search engine.

Version 4.1D adds two new methods to existing BroadVision interfaces: BVI_Search, described in
the Developer’s Guide to Components and Scripts and BV_Search, described in the API Reference.

The current API does a Verity search, then uses those search results to retrieve contents from the
BroadVision database. The new API adds the ability to perform a Verity search and then return
those results directly without retrieving content from the database. The search results for the new
API are returned in the form of Verity search ﬁelds.

This new API has the following advantages:

l It does not access the database to get content identiﬁed by the Verity search results.

l It allows searches on Verity collections that are not based on content.

l It allows searches across multiple collections that have the same Verity search ﬁelds.

The rest of this document covers the following topics:

l “Deﬁning Verity search ﬁelds” on page 2

l “BVI_Search::getSearchResults” on page 3

l “BV_Search::getContent” on page 4

One-To-One Search

298-41D-XAP

BroadVision, Inc.

2

BroadVision One-To-One Verity enhancement

Deﬁning Verity search ﬁelds

Before you can perform a Verity search on ﬁelds, you must ﬁrst deﬁne the ﬁelds in a style.ufl ﬁle
and then provide an attribute mapping ﬁle that tells Verity SEARCH’97 which One-To-One content
columns can be searched.

The style ﬁles that deﬁne the One-To-One speciﬁc ﬁelds are contained in these directories:

$BV1TO1_VAR/collection/style/EDITORIAL
$BV1TO1_VAR/collection/style/PRODUCT

If you created ﬁeld deﬁnitions for Name, Price, and Description, your style.ufl ﬁle in the
PRODUCT directory might look like this:

data-table: dd1
{
  varwidth: OID dxa
    /indexed = yes
    /minmax = yes
}

data-table: dd4
{
  varwidth: Name ddv
    /indexed = yes
    /minmax = no
}
data-table: dd5
{
  varwidth: Price ddx
    /indexed = yes
    /minmax = yes
}
data-table: dd6
{
  varwidth: Description ddy
    /indexed = no
    /minmax = no
}

The attribute mapping ﬁle for building the indexes would then contain these lines:

OID
NAME
LONGDESC
PRICE

FIELD
FIELD
BOTH
FIELD

OID
Name
Description
Price

 For additional information about style.ufl ﬁles and attribute mapping ﬁles, refer to the
Installation and System Administration Guide, and to the Verity SEARCH’97 documentation
supplied separately by Verity, Inc.

BroadVision, Inc.

298-41D-XAP

One-To-One Search

BroadVision One-To-One Verity enhancement

3

BVI_Search::getSearchResults

Gets Verity search results.

BVI_ContentList getSearchResults(

string
string
BVI_StringList
long

queryString,
sortString,
fieldList,
max_count);

Return value

A BVI_ContentList containing the results of the Verity search, one search result per row.

Parameters

queryString

sortString

fieldList

max_count

A Verity query language string.

A Verity sort string.

A list of strings specifying the ﬁelds that Verity should return.

Maximum count of results returned. Each matching result is a row
in the returned BVI_ContentList.

Remarks

Unlike BVI_Search::getContent(), this method returns the Verity search results as is, and does
not use the Verity search results to get a list of content.

In order to be able to return Verity search results directly, the ﬁelds speciﬁed in fieldList, must be
among the ﬁelds that are speciﬁed when creating the collection, with the exception of “SCORE” and
“VdkVgwKey”, which are generated ﬁelds that are always available from the seach results.

Note that the “VdkVgwKey” ﬁeld created by the BroadVision indexer tool contains a string
representation of three integers that give the OID, store-id, and content-type in that order. For
example, “6001 90 0” indicates the following:

= 6001

oid
store id = 90
cnt_type = 0

The BroadVision indexer tool only creates collections for content based searches. If you want to
perform searches on items that are not based on content, you must write your own indexer so that
you have control over the format of and information in VdkVgwKey. For information about writing
your own indexer tool, refer to the documentation supplied by Verity, Inc.

 For additional information about creating collections and running the BroadVision indexer
tool, refer to the Installation and System Administration Guide.

BVI_Search::getSearchResults is deﬁned in search.jsi and is available in the
BroadVision libbvc.so library. It is intended to be called from a BroadVision style page script.
Refer to the Developer’s Guide to Components and Scripts for information about other BVI_Search
methods.

One-To-One Search

298-41D-XAP

BroadVision, Inc.

4

BroadVision One-To-One Verity enhancement

BV_Search::getContent

Gets Verity search results.

virtual long getContent(

const char
const char
const BVRT_ContentSchema

BVRT_ContentList
long

*queryString,
*sortString,
*fields,
&cnt_list,

max_count);

Return value

Zero on success; anything else indicates an error. Data is returned through the cnt_list
parameter.

Parameters

queryString

sortString

fields

cnt_list

max_count

Points to a Verity query language string.

Points to a Verity sort string.

Points to a list of strings specifying the ﬁelds that Verity should
return.

A reference to an empty BVRT_ContentList. The caller owns the
reference.

Maximum count of results returned. Each matching result is a row
in the returned BVI_ContentList.

Remarks

This method returns the search result ﬁelds. The names in fields become the attributes of the
returned BVRT_ContentList.

This method is called indirectly by BVI_Search::getSearchResults() described earlier.

For information about other methods in the BV_Search class refer to the API Reference.

 This method is defined in search.hh and is available in the BroadVision libbvsearch.so
library. You should call this method only if you are writing your own component as defined in
the Developer’s Guide to Components and Scripts or if you are writing your own server.

BroadVision, Inc.

298-41D-XAP

One-To-One Search

