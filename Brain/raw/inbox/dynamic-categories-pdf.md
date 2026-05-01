---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Reading/Dynamic Categories.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Dynamic Categories.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Reading/Dynamic Categories.pdf.md`
Size: 16,011 bytes

## Raw content
Using dynamic categories

1

Dynamic categories are an example of capturing and using visitor session information, such as the
visitor’s category selection, to determine the consequential display of content to that visitor. By
recording the category in the session proﬁle, you can use it in a matching rule to display content
that’s much more speciﬁc to the visitor’s preferences. When dynamic categories are used in
matching rules, the source category for the matching content is determined directly by visitor
interaction at run time rather than by business managers when they create matching rules.

Dynamic categories reduce the number of rules required in certain scenarios, such as context-based
matching scenarios. Imagine a home page with buttons or images linking to a sports area and a
travel area. The sports area links to information on baseball, tennis, soccer, and other sporting
events. Travel leads to information on island, skiing, adventure, and family vacations. Your goal is
to display the appropriate coupon according to the sports or travel subcategory that the visitor
selects. You can accomplish it by creating two dynamic categories named Sports and Travel, setting
the Sports and Travel subcategory values to the corresponding coupons, and then creating a rule set
with these two rules:

if (selected = Sports) then return coupons from Sports dynamic category
if (selected = Travel) then return coupons from Travel dynamic category

Implementing and using dynamic categories involves procedures performed by various members
of the site development team using different parts of BroadVision One-To-One Enterprise. Team
members need to be familiar with the following:

l Creating rules and rule sets using the One-To-One Command Center

l Implementing page scripts using JavaScript

This document describes the end-to-end dynamic category solution that’s delivered with
BroadVision® One-To-One™ Enterprise. This solution is both a comprehensive feature that can be
used as it is, and a powerful tool that provides an example of how to create a custom dynamic
category solution for your business. This document describes the following topics:

l “Creating dynamic categories” on page 2.

l “Creating matching rules with dynamic categories” on page 3.

l “Using dynamic categories in page scripts” on page 8.

Using dynamic categories

295-41A-HAP

BroadVision, Inc.

2

Using dynamic categories
Creating dynamic categories

Creating dynamic categories

To create dynamic categories, you:

1. Edit the dynamic category speciﬁcation ﬁle, $BV1TO1/samples/dbschema/

matching_type.src, to change the DYNAMIC_CATEGORY type.

2. Update the One-To-One database by running make.

Editing the dynamic category speciﬁcation ﬁle

The following matching_type.src ﬁle speciﬁcation is the default dynamic category setup that’s
delivered with the BroadVision One-To-One Enterprise. The friendly names in the
matching_type.src ﬁle speciﬁcation, such as “Dynamic category 1,”compose the drop-down list
that’s displayed in the Command Center Matching Rules interface. The mapping numbers
determine the order in which the friendly names are displayed in the drop-down list.

The Database Administrator’s Guide provides complete information on setting up and modifying
the BroadVisionOne-To-One database.

NAME: DYNAMIC_CATEGORY
PRIMITIVE: DICT
SEMANTICS: Dynamic category terms used by matching engine
MAPPING:

1 "CATEGORY1" "Dynamic category 1",
2 "CATEGORY2" "Dynamic category 2",
3 "CATEGORY3" "Dynamic category 3",
4 "CATEGORY4" "Dynamic category 4"

Adding dynamic categories to the database

The new dynamic categories speciﬁed in the matching_type.src ﬁle must be added to the
One-To-One database. The following command, using the sample makeﬁle in $BV1TO1/samples/
dbschema/, generates the matching_type.sql ﬁle and executes the SQL statements:

make -f schema.mk matching_type.sql

Before running this make command, be sure the BV_DB_VENDOR environment variable is set
correctly (to oracle for an Oracle database system, sybase for a Sybase system, and
informix for an Informix system) in bv1to1.conf.

BroadVision, Inc.

295-41A-HAP

Using dynamic categories

Viewing dynamic categories in the Command Center

The following screen capture of the Rule Action - Category Matching dialog in the Command
Center shows how dynamic categories are displayed in the Command Center.

Using dynamic categories
Creating matching rules with dynamic categories

3

The dynamic
category
specification file
determines the
dynamic category
names and list
order in the
One-To-One
Command Center
rule wizard

Creating matching rules with dynamic categories

To match content to Web site visitors using dynamic categories, you must deﬁne the appropriate
matching rules using the Command Center rules wizard. The rules wizard provides a series of
dialogs in which you enter information about a rule set and its rules. To open the rules wizard, select
the Rule Set|New menu command.

Dynamic categories can be used to determine the default action in a matching rule set. The default
action determines what will be displayed to the visitor when rule set evaluation fails to display the
appropriate content. Dynamic categories can be used in the default action in a matching rule set to
determine:

l The category from which content items are displayed when the matching rule set evaluation

doesn’t display a sufﬁcient number of items.

l The category name and, if speciﬁed, attributes displayed when the matching rule set evaluation

doesn’t display a category name.

Dynamic categories can be used in matching rules to determine:

l At run time, the category from which content items are displayed, or

l At run time, the category name that’s displayed. If attributes are deﬁned for the category, the

category attributes are also displayed to the visitor.

Using dynamic categories

295-41A-HAP

BroadVision, Inc.

4

Using dynamic categories
Creating matching rules with dynamic categories

The following examples illustrate the use of dynamic categories in the four scenarios mentioned
above. For a detailed explanation of creating matching rules and rule sets, refer to the Command
Center User’s Guide.

Picking default content from a dynamic category

When rule evaluation displays insufﬁcient content, the rule set default action can retrieve content
items from a category that’s dynamically determined at run time for display on a Web page. You can
use the Rule Set Action dialog in the rules wizard to let visitor interaction determine which category
is retrieved at run time.

Displaying default content from a dynamically determined category

For a matching rule set, you can use the Rule Set Action dialog, for the selected default action, to
specify a quantity of items to be retrieved by the default action dynamic category or branch.

If the Include Subcategories checkbox is enabled and marked, and you specify a dynamic
category that maps to a parent category at run time, the rule retrieves the specified quantity of
items from the entire branch rather than the dynamic category only.

In the Rule Set Action dialog:

1. Select Items in the Retrieve group box. If the Include Subcategories checkbox is enabled, do one

of the following:

• Mark the checkbox to retrieve items from a selected category and any branch of

subcategories under it.

• Leave the checkbox clear to retrieve items from the selected category only.

2. Enter the maximum Quantity of items you want the default action to retrieve.

BroadVision, Inc.

295-41A-HAP

Using dynamic categories

Using dynamic categories
Creating matching rules with dynamic categories

5

3. To specify the category from which the items are retrieved, do one of the following:

• Select a category. Choose Selected category in the From group box. Click the button to the

right of the ﬁeld to open the Content Categories dialog. Select the category in the tree. Click
OK in the dialog to copy the category path to the Selected Category ﬁeld in the Rule Set
Action dialog.

• Use a dynamic category. Select Dynamic Category in the From group box, and choose one

from the list.

Dynamically retrieving a category name as default content

When rule evaluation displays insufﬁcient content, the rule set default action can also retrieve a
category name that’s dynamically determined at run time for display on a Web page. Matching rule
sets that retrieve categories can use only the Pick Default Content default action.

In the Rule Set Action dialog:

1. Select Category in the Retrieve group box.

2. In the From group box, do one of the following:

• Select a category. Choose Selected category in the group box. Click the button to the right of
the ﬁeld to open the Content Categories dialog. Select the category in the tree, and click OK
in the dialog to copy the category path to the Selected Category ﬁeld in the Rule Set Action
dialog.

• Select Dynamic Category in the From group box, and choose one from the list.

Using dynamic categories

295-41A-HAP

BroadVision, Inc.

6

Using dynamic categories
Creating matching rules with dynamic categories

Using dynamic categories for matching rules

A dynamic category can be used to determine at run time which content is displayed to a visitor
when a matching rule is true. You can choose to display either a set of content items or the category
name itself when a rule is true.

Displaying content items from a dynamically determined category

When you choose to display a set of content items from a dynamic category, the system retrieves
and displays the number of content items pre-determined in the matching rule. The system retrieves
this content from the category corresponding to the dynamic category selected by the visitor at run
time.

In the Rule Action dialog:

1. Select Items in the Retrieve group box. If the Include Subcategories checkbox is enabled, do one

of the following:

• Mark the checkbox to retrieve items from a selected category and any branch of

subcategories under it.

• Leave the checkbox clear to retrieve items from the selected category only.

2. Enter the maximum Quantity of items you want the rule action to retrieve.

3. To specify the category from which the items are retrieved, do one of the following:

• Select a category. Choose Selected category in the From group box. Click the button to the

right of the ﬁeld to open the Content Categories dialog. Select the category in the tree. Click
OK in the dialog to copy the category path to the Selected Category ﬁeld in the Rule Set
Action dialog.

BroadVision, Inc.

295-41A-HAP

Using dynamic categories

Using dynamic categories
Creating matching rules with dynamic categories

7

• Use a dynamic category. Select Dynamic Category in the From group box, and choose one

from the list.

Dynamically displaying a category name as default content

When you choose to display a a category name from a dynamic category, the system retrieves and
displays the dynamic category determined by the visitor at run time.

In the Category Matching dialog:

1. Select Category in the Retrieve group box.

2. In the From group box, do one of the following:

• Select a category. Choose Selected category in the group box. Click the button to the right of
the ﬁeld to open the Content Categories dialog. Select the category in the tree, and click OK
in the dialog to copy the category path to the Selected Category ﬁeld in the Rule Set Action
dialog.

• Select the Dynamic Category in the From group box, and choose one from the list.

Using dynamic categories

295-41A-HAP

BroadVision, Inc.

8

Using dynamic categories
Using dynamic categories in page scripts

Rule set view for Personalized news

The following screen capture shows the Rule Set View dialog, which summarizes the Personalized
news rule set.

Using dynamic categories in page scripts

Business managers set up dynamic categories as placeholders or “virtual” categories so that they
can create rules based on transient session information. The value assigned to the dynamic category
at run time is determined by the script writer and by visitor behavior during the session.

For example, the bw_news.jsp script in the Broadway sample application ($BV1TO1/broadway/
scripts) allows visitors to personalize their news pages by selecting the news categories they
want to view. The following section describes how a simpliﬁed version of this script might work.

This section assumes familiarity with JavaScript development. For more information about the
JavaScript APIs mentioned, refer to the Script API Reference in the Developer’s Guide to
Components and Scripts.

Displaying personalized news

This section describes one way to use a script to display information from a category chosen at run
time by a visitor. The following are the basic steps you must follow in a page script to display
content from a dynamic category.

BroadVision, Inc.

295-41A-HAP

Using dynamic categories

Display selection
list

The script displays an HTML SELECT list with the news child categories:

Using dynamic categories
Using dynamic categories in page scripts

9

The following code segment sets up an HTML SELECT list. (The actual bw_news.jsp script
generates this list dynamically, making it unnecessary to update the page script when categories are
added or deleted.)

<select name="NEWS_PREFERENCE1">

<option value="Business"</option>
<option value="Entertainment"</option>
<option value="Health"</option>
...
</select>

Get current
selection

The visitor selects a category and clicks the Submit button, causing the application to revisit the
script.The visitor’s ﬁrst preference is stored in NEWS_PREFERENCE1 variable and stored in the
visitor object (an instance of BVI_Visitor) as visitor.NEWS_PREFERENCE1.

Display news items When the visitor submits a preference, the script is revisited and does the following:

1. Initializes and assigns a series of variables, including:

• cntmgr, the value of the BVI_ContentManager for the current session. In this script the

content manager is used to retrieve category information.

• newsCategory, which stores category information about the News category. The script
displays content from the News child categories, such as Business, Sports, and Headline
News.

2. Retrieves content for the selected category using the categoryInfo() method of the
BVI_ContentManager object and puts it in Session.sessionProﬁle.CATEGORY1.

This is the step in which the contents of the dynamic category are set for the session.

var catInfo = cntmgr.categoryInfo("News/" + visitor.NEWSPREFERENCE1,

"MyBank", "EDITORIAL");

Session.sessionProfile.CATEGORY1 = catInfo.OID;

Using dynamic categories

295-41A-HAP

BroadVision, Inc.

10

Using dynamic categories
Using dynamic categories in page scripts

3. Creates a new BVI_MatchingAgent, matchObject, and calls its matchContent() method to
retrieve content for display. Note that the ﬁrst parameter is the rule set name (also called
“collection” in the Developer’s Guide to Components and Scripts). “Personalized news” is a rule set
deﬁned in the Command Center. Its default action is to select items from a dynamic category,
CATEGORY1.

// have the matching agent evaluate the rule

var matchObject = new BVI_MatchingAgent();
var news = matchObject.matchContent("Personalized news", "MyBank",

"EDITORIAL", visitor, Session.sessionProfile, 4);

The “dynamic news” rule indicates that 5 content items are to be retrieved when the rule is
executed. The page script calls for 4 content items to be displayed. The application displays the
smaller number of items indicated in the rule or the page script.

4. Displays the content.

for(news.cursor=0; news.cursor<news.length; news.cursor++) {
%>

<ul><li><%=news.ED_NAME%></ul>

<%
        }
%>

BroadVision, Inc.

295-41A-HAP

Using dynamic categories


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
