---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/Pages from rdf-100-ug.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# Pages from rdf-100-ug.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/Pages from rdf-100-ug.pdf.md`
Size: 32,243 bytes

## Raw content
Retek® Demand Forecasting
10.0

User Guide

    Retek Demand Forecasting

The software described in this documentation is furnished under a license
agreement, is the confidential information of Retek Inc., and may be used
only in accordance with the terms of the agreement.

No part of this documentation may be reproduced or transmitted in any form
or by any means without the express written permission of Retek Inc., Retek
on the Mall, 950 Nicollet Mall, Minneapolis, MN 55403, and the copyright
notice may not be removed without the consent of Retek Inc.

Information in this documentation is subject to change without notice.

Retek provides product documentation in a read-only-format to ensure
content integrity.  Retek Customer Support cannot support documentation
that has been changed without Retek authorization.

Retek® Demand Forecasting™ is a trademark of Retek Inc.

Retek and the Retek logo are registered trademarks of Retek Inc.

This unpublished work is protected by confidentiality agreement, and by
trade secret, copyright, and other laws. In the event of publication, the
following notice shall apply:

©2002 Retek Inc. All rights reserved.

All other product names mentioned are trademarks or registered trademarks
of their respective owners and should be treated as such.

Printed in the United States of America.

Corporate Headquarters:

Retek Inc.

Retek on the Mall

950 Nicollet Mall

Minneapolis, MN 55403

888.61.RETEK (toll free US)
+1 612 587 5000

European Headquarters:

Retek

110 Wigmore Street

London

W1U 3RW

United Kingdom

Switchboard:

+44 (0)20 7563 4600

Sales Enquiries:

+44 (0)20 7563 46 46
Fax:  +44 (0)20 7563 46 10

Retek® Confidential

Customer Support

Customer Support hours:

Customer Support is available 7x24x365 via e-mail, phone, and Web access.

Depending on the Support option chosen by a particular client (Standard,
Plus, or Premium), the times that certain services are delivered may be
restricted.  Severity 1 (Critical) issues are addressed on a 7x24 basis and
receive continuous attention until resolved, for all clients on active
maintenance.

Contact Method  Contact Information

Internet (ROCS)   www.retek.com/support

E-mail

Phone

Mail

Retek’s secure client Web site to update and view issues

support@retek.com

US & Canada: 1-800-61-RETEK (1-800-617-3835)
World: +1 612-587-5800
EMEA: 011 44 1223 703 444
Asia Pacific: 61 425 792 927

Retek Customer Support
Retek on the Mall
950 Nicollet Mall
Minneapolis, MN 55403

When contacting Customer Support, please provide:

•  Product version and program/module name.

•  Functional and technical description of the problem (include business

impact).

•  Detailed step by step instructions to recreate.

•  Exact error message received.

•  Page shots of each step you take.

Contents   i

Contents

Chapter 1 – Overview.............................................................. 1

What is Retek Demand Forecasting? .................................................................. 1

Forecasting challenges and solutions .................................................................. 2

Selecting the best forecasting method ........................................................................ 2
Handling items with limited demand histories ........................................................... 2
Handling lost sales and unusually high demand......................................................... 3
Forecasting demand for new products and locations.................................................. 3
Incorporating the effects of promotions and other event-based challenges on demand
.................................................................................................................................... 4
Providing detailed sales predictions based on an assortment plan ............................. 4

Retek Demand Forecasting Features................................................................... 5

Retek Demand Forecasting Modules .................................................................. 7

Predict......................................................................................................................... 7
Promote....................................................................................................................... 7
Curve .......................................................................................................................... 7
Preprocessing.............................................................................................................. 8

Chapter 2 – Predict (Statistical Forecasting)........................ 9

Overview ............................................................................................................. 9

Workbooks and Wizards ............................................................................................ 9

Forecast Administration Workbook .................................................................. 10

Forecast Administration Wizard............................................................................... 12
Basic Settings workflow tab ..................................................................................... 12
Advanced Settings workflow tab.............................................................................. 19

Forecast Maintenance Workbook...................................................................... 24

Basic Settings workflow tab ..................................................................................... 26
Advanced Settings workflow tab.............................................................................. 27

Run Batch Forecast ........................................................................................... 32

Batch Forecast Wizard.............................................................................................. 33

Delete Forecasts ................................................................................................ 35

Delete Forecasts Wizard........................................................................................... 35

ii    Retek Demand Forecasting

Forecast Approval Workbook ........................................................................... 36

Forecast Approval Wizard........................................................................................ 37
Final Forecast Worksheet ......................................................................................... 38
Source Level Worksheet........................................................................................... 40
Approval Worksheet................................................................................................. 41
Final Parameters Worksheet..................................................................................... 42
Confidence Worksheet ............................................................................................. 44

Interactive Forecasting Workbook .................................................................... 45

Final Forecasting Parameter Worksheet................................................................... 46
Final Interactive Forecasting Worksheet .................................................................. 47

Forecast Scorecard Workbook .......................................................................... 48

Forecast Scorecard Wizard ....................................................................................... 48
Final Error Measure Worksheet ............................................................................... 50
Final Actuals vs. Forecasts Worksheet..................................................................... 53

Export Forecasts................................................................................................ 53

Export Forecasts Wizard .......................................................................................... 54

Forecast Export Administration Workbook ...................................................... 55

Export Parameters Worksheet .................................................................................. 56

Chapter 3 – Promote (Promotional Forecasting) ............... 61

Overview ........................................................................................................... 61

Promotional Forecasting and Expect Profitability.................................................... 62
Examples of Promotion Events ................................................................................ 62
Promote workbooks and wizards.............................................................................. 63

Promotion Planner Workbook........................................................................... 64

Promotion Planner wizard ........................................................................................ 65
Promotion Planner workbook and worksheet........................................................... 65

Promotion Selector Wizard ............................................................................... 66

Causal Maintenance Workbook ........................................................................ 68

Final PromoEffects Worksheet................................................................................. 68

Promotional “What-If” Analysis Workbook..................................................... 70

Promotion What-If Analysis Wizard ........................................................................ 70
Promotion Planning Worksheet................................................................................ 71
Final Promotion Effects Worksheet ......................................................................... 72
Final Promotion Effectiveness Analysis Worksheet ................................................ 73
Optional Fact Based Advertising Measures ............................................................. 73

Procedures in Promotional Forecasting............................................................. 76

Retek® Confidential

Contents   iii

Chapter 4 – Curve (Profile-based Forecasting) .................. 77

Overview ........................................................................................................... 77

Profile Management Terminology and Workflow ............................................ 78

Profiles (spreading ratios)......................................................................................... 78

Profile generation techniques ............................................................................ 79

Profile generation techniques ................................................................................... 80
Defining the training window for historical data...................................................... 81
Aggregating historical data....................................................................................... 81
Unreliable data, thresholds, and threshold exceptions.............................................. 83
Loading default ratios............................................................................................... 83
Approving the generated profiles ............................................................................. 84

Profile Administration Workbook..................................................................... 86

Profile Administration Wizard ................................................................................. 86
Profile Administration Workbook ............................................................................ 86
Core Profile Worksheet ............................................................................................ 87

Profile Maintenance Workbook ........................................................................ 89

Profile Maintenance Workbook................................................................................ 89

Run Batch Profile .............................................................................................. 90

Profile Approval Workbook.............................................................................. 91

Profile Approval Wizard .......................................................................................... 91
Profile Approval Worksheet..................................................................................... 92
Source Level Worksheet........................................................................................... 92
Final Profile Worksheet............................................................................................ 94

Chapter 5 – Preprocessing................................................... 95

Overview ........................................................................................................... 95

Preprocessing workbook templates and wizards............................................... 95

Administration Workbook................................................................................. 96

Administration Wizard ............................................................................................. 96
Administration Worksheet........................................................................................ 96

Run Batch Workbook........................................................................................ 98

Run Selection Update........................................................................................ 99

Preprocessing Methods ................................................................................... 100

Mathematical formulation of preprocessing methods ............................................ 102
Chart-form examples of preprocessing effects ....................................................... 105

iv    Retek Demand Forecasting

Chapter 6 – Retek Demand Forecasting methods ........... 109
Why use statistical forecasting? ............................................................................. 109

Forecasting techniques used in RDF ............................................................... 110

Exponential Smoothing .......................................................................................... 110
Regression Analysis ............................................................................................... 110
Bayesian Analysis .................................................................................................. 110
Prediction Intervals................................................................................................. 111
Automatic Method Selection .................................................................................. 111
Source level forecasting.......................................................................................... 111

Equation Notation Definitions ........................................................................ 112

Time Series Forecasting Techniques............................................................... 113

Confidence limits.................................................................................................... 114
AutoES Forecasting................................................................................................ 114
SeasonalES Forecasting.......................................................................................... 115
Components of Exponential Smoothing................................................................. 115
Simple Moving Average......................................................................................... 116
Simple Exponential Smoothing .............................................................................. 116
Croston’s Method ................................................................................................... 116
Holt Exponential Smoothing .................................................................................. 117
Multiplicative Winters Exponential Smoothing ..................................................... 117
Additive Winters Exponential Smoothing.............................................................. 118
Seasonal Regression ............................................................................................... 118
Bayesian Information Criterion .............................................................................. 122

Profile-based forecasting................................................................................. 123

Forecast method...................................................................................................... 123
Confidence intervals ............................................................................................... 123
Profile based method and new SKUs ..................................................................... 123
Example.................................................................................................................. 123

Bayesian Forecasting....................................................................................... 124

Overview ................................................................................................................ 124
Sales Plans vs. Historic Data .................................................................................. 125
Forecasting Algorithm............................................................................................ 126
Guidelines............................................................................................................... 127

Daily Forecasting (and other non-weekly forecasts)....................................... 128

Promotional Forecasting ................................................................................. 129

Promotional Forecasting - Expert Involvement...................................................... 130
Promotional Forecasting - Technical Algorithm Details........................................ 131
Algorithm Process .................................................................................................. 131
Promotional Forecasting – Daily Forecasting ........................................................ 133
Selecting the best forecasting method .................................................................... 134
Automatic forecast level selection.......................................................................... 136

Retek® Confidential

Contents   v

Profile-based forecasting................................................................................. 139

Forecast method...................................................................................................... 139
Confidence intervals ............................................................................................... 139
Profile based method and new SKUs ..................................................................... 139
Example.................................................................................................................. 140

Bayesian forecasting ....................................................................................... 141

Sales plans vs. historic data .................................................................................... 142
Forecasting algorithm ............................................................................................. 142
Guidelines............................................................................................................... 144

Causal (promotional) forecasting methods ..................................................... 144

The causal forecasting algorithm............................................................................ 145
Causal forecasting algorithm process ..................................................................... 148
Causal forecasting array interface description........................................................ 149
Causal forecasting at the daily level ....................................................................... 150
Final considerations about causal forecasting ........................................................ 152

Glossary............................................................................... 153

Index..................................................................................... 161

Chapter 1 – Overview   1

Chapter 1 – Overview

What is Retek Demand Forecasting?

Retek Demand Forecasting is a Windows-based statistical and causal forecasting
solution. It uses state-of-the-art modeling techniques to produce high quality
forecasts – with minimal human intervention. Forecasts produced by the Demand
Forecasting system enhance the retailer’s supply-chain planning, allocation, and
replenishment processes, enabling a profitable and customer-oriented approach to
predicting and meeting product demand.

Today’s progressive retail organizations know that store-level demand drives the
supply chain.  The ability to forecast consumer demand productively and
accurately is vital to a retailer’s success.  The business requirements for
consumer responsiveness mandate a forecasting system that more accurately
forecasts at the point of sale, handles difficult demand patterns, forecasts
promotions and other causal events, processes large numbers of forecasts, and
minimizes the cost of human and computer resources.

Forecasting drives the business tasks of planning, replenishment, purchasing, and
allocation. As forecasts become more accurate, businesses run more efficiently
by buying the right inventory at the right time. This ultimately lowers inventory
levels, improves safety stock requirements, improves customer service, and
increases the company’s profitability.

The competitive nature of business requires that retailers find ways to cut costs
and improve profit margins. The accurate forecasting methodologies provided
with Retek Demand Forecasting can provide tremendous benefits to businesses.

A connection from Retek Demand Forecasting to Retek Predictive Planning
products is built directly into the business process by way of the automatic
approvals of forecasts, which are then fed directly to Retek Predictive Planning.
This process allows you to accept all or part of a generated sales forecast.  Once
that decision is made, the remaining business measures are planned within Retek
TopPlan.

2    Retek Demand Forecasting

Forecasting challenges and solutions

A number of challenges affect the ability of organizations to forecast product
demand accurately.  These challenges include selecting the best forecasting
method to account for level, trending, seasonal, and spiky demand; generating
forecasts for items with limited demand histories; forecasting demand for new
products and locations; incorporating the effects of promotions and other event-
based challenges on demand; and accommodating the need of operational
systems to have sales predictions at more detailed levels than planning programs
provide.

Selecting the best forecasting method

One challenge to accurate forecasting is the selection of the best model to
account for level, trending, seasonal, and spiky demand.  Retek’s AutoES
(Automatic Exponential Smoothing) forecasting method manages this
complexity.  You simply select the AutoES forecast generation method, and the
system finds the best model.

The AutoES method evaluates multiple forecast models, such as:

•  Simple Exponential Smoothing

•  Holt Exponential Smoothing

•  Additive and Multiplicative Winters Exponential Smoothing

•  Crostons Intermittent Demand Model

•  Seasonal Regression forecasting to determine the optimal forecast method to

use for a given set of data.

The accuracy of each forecast and the complexity of the forecast model are
evaluated to determine the most predictive method.

Handling items with limited demand histories

Another challenge to creating accurate forecasts is predicting demand for items
with a limited sales history.  The accuracy of time series forecasts is diminished
when short or sparse historical data is fed into the forecasting model.  The
Demand Forecasting approach to this challenge is to generate forecasts at
multiple levels of data aggregation.

Forecasts are typically difficult to generate directly at the SKU/Store/Week level
due to the low sales volumes of the items in question.  Although forecast
information is often required at a low level (the final forecast level), data is often
too sparse and inconsistent to identify clear demand patterns.  For this reason, it
is sometimes necessary to aggregate sales data from this base level to a higher
forecasting level, in order to generate a reasonable forecast.  At the higher level,
trends and seasonality in the data can be identified.  Once the forecast is created
at the higher level (the source level), the results can be applied at the low (final
forecast) level based on that level’s relationship to the total.  Demand Forecasting
generates forecasts directly at the lower level to determine demand proportions
across SKUs.

Handling lost sales and unusually high demand

Chapter 1 – Overview   3

Ideally, future forecasts are based on past demand. Retailers record sales as a
means to measure demand. These two figures can differ when inventory drops to
zero and there is demand, but no sales. To manage this situation, RDF has a
module called Preprocessing that recognizes when sales might be lower than
actual demand, and adjusts sales values up to a predicted level of demand.

A retailer may also want to adjust sales before using them as proxies for demand
in forecasting when past sales were unusually high due to an external event that
is not expected to repeat. For example, if bad weather causes a power outage,
causing the sales of batteries and flashlights for the week to soar. These high
sales values, however, are not good predictors of expected sales for the next
week. The same interpolation algorithms used to adjust sales up to correct for lost
sales can be used to adjust sales down to correct for unusually high demand.

For more details on the Preprocessing module, see Chapter 5.

Forecasting demand for new products and locations

Retek Demand Forecasting can also forecast demand for new products and
locations for which no sales history exists.  You can model a new product’s
demand behavior based on that of an existing, similar product.  Forecasts can be

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
