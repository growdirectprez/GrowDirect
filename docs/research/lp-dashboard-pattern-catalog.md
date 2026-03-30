---
type: research
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# LP Dashboard Pattern Catalog

## Pattern Categories

| Category | Count | Chapters |
|----------|-------|----------|
| Time-series / trend lines | 10 | 2, 5, 13 |
| Store/location comparison | 8 | 5, 7, 8 |
| Distribution analysis | 7 | 4, 5 |
| LP initiative measurement | 8 | 7, 8 |
| Risk scoring / driver analysis | 6 | 10 |
| Classification / segmentation | 5 | 11, 12 |
| Correlation / scatter | 4 | 5 |
| Taxonomy / reference tables | 4 | 1, 8 |

---

## 1. Time-Series & Trend Patterns

### 1.1 Incident density by hour of day
**Fig:** ch002_006 | **Type:** Line chart
**Shows:** Shoplifting incidents bucketed by hour (9am-8pm), peak at noon-1pm.
**Canary:** Owl time-window search results; Chirp alert density heatmap by hour.

### 1.2 Normalized risk rate by hour
**Fig:** ch002_007 | **Type:** Line chart
**Shows:** Shoplifter-to-shopper ratio by hour — reveals closing-time spike hidden in raw counts.
**Canary:** Owl number response (normalized risk score by hour); shrink trend chart.

### 1.3 Dual time-series: theft events + sales
**Fig:** ch005_024 | **Type:** Dual line chart
**Shows:** Stolen product count by month alongside monthly sales trend on aligned axes.
**Canary:** Trend dashboard — dual time-series panel showing theft events and sales.

### 1.4 Shrink rate % over time (primary KPI)
**Fig:** ch005_025 | **Type:** Line chart
**Shows:** Stolen products as % of sales across 12 months, peaking at 0.13% in month 6.
**Canary:** KPI sparkline — shrink rate % as primary rolling metric on location and merchant cards.

### 1.5 Manager comparison trend lines
**Fig:** ch005_026 | **Type:** Dual-line chart
**Shows:** Monthly shrink rate % for two LP managers overlaid, one consistently higher.
**Canary:** Manager comparison view — overlaid shrink rate trend lines per manager.

### 1.6 Individual manager anomaly spike
**Fig:** ch005_030 | **Type:** Line chart
**Shows:** Single manager's monthly shrink rate with sharp spike in month 6.
**Canary:** Manager drill-down — individual shrink rate trend with anomaly flagging.

### 1.7 Control chart / run chart
**Fig:** ch005_032 | **Type:** Control chart
**Shows:** Daily incident counts over 19 days with upward trend signaling emerging pattern.
**Canary:** Alert engine — control chart view for daily incident counts with trend-break detection.

### 1.8 LP program pilot: moving average comparison
**Fig:** ch013_003 | **Type:** Line chart (52-week MA)
**Shows:** Return rate % comparing pilot group vs. control before/after LP intervention.
**Canary:** LP program measurement — before/after moving-average trend comparison.

---

## 2. Store / Location Comparison

### 2.1 Revenue baseline by store
**Fig:** ch005_003 | **Type:** Bar chart
**Shows:** Total sales across four stores ($385K-$613K) — establishes baseline for loss context.
**Canary:** Location comparison view — revenue baseline panel alongside shrink rate.

### 2.2 Shrink ranking by store
**Fig:** ch005_006 | **Type:** Bar chart
**Shows:** Total stolen products per store, stores 3 and 4 significantly higher.
**Canary:** Location leaderboard — stolen units by location, sortable descending.

### 2.3 Sales share % by store
**Fig:** ch005_007 | **Type:** Bar chart
**Shows:** Each store's share of total sales (~20-33%) as denominator context for normalization.
**Canary:** Location comparison — sales share % alongside shrink rate for disproportionate loss.

### 2.4 Store benchmark significance test
**Fig:** ch007_001 | **Type:** Table
**Shows:** t-test of 25 stores' shrink against 1.38% benchmark with p-value.
**Canary:** Store benchmarking view — flag stores where shrink exceeds industry benchmark.

### 2.5 Shrink distribution with CI overlay
**Fig:** ch007_002 | **Type:** Annotated output (histogram + boxplot + CI)
**Shows:** One-sample t-test with shrink histogram, boxplot, and 99% confidence interval.
**Canary:** Shrink distribution panel — histogram + boxplot across locations with CI.

### 2.6 Regional shrink comparison (A vs B)
**Fig:** ch007_003, ch007_006 | **Type:** Table
**Shows:** West (2.41%) vs. East (1.75%) with t-stat and p-value confirming significance.
**Canary:** Multi-location comparison — side-by-side shrink rates with significance test.

### 2.7 Cohort distribution comparison
**Fig:** ch007_007 | **Type:** Side-by-side histograms + boxplots
**Shows:** Two store groups' shrink distributions with visual comparison.
**Canary:** Cohort comparison view — distribution visual for test vs. control stores.

### 2.8 Year-over-year paired comparison
**Fig:** ch007_009, ch007_011 | **Type:** Table
**Shows:** Last year vs. this year shrink for 25 stores with paired t-test (p=1.35E-06).
**Canary:** Health Check report — statistical proof of shrink improvement over time.

---

## 3. Distribution Analysis

### 3.1 Shrink value percentile table
**Fig:** ch004_010, ch004_012 | **Type:** Annotated output / table
**Shows:** 5-number summary (min, Q1, median, Q3, max) of stolen product values.
**Canary:** Shrinkage distribution panel — percentile table or box-plot of loss amounts.

### 3.2 Skewness reference (left/symmetric/right)
**Fig:** ch004_016 | **Type:** Conceptual diagram
**Shows:** Three distribution shapes with mean/median/mode positions annotated.
**Canary:** Data quality calibration — understanding skew informs which metric to display.

### 3.3 Empirical rule (68/95/99.7)
**Fig:** ch004_018 | **Type:** Annotated normal curve
**Shows:** 68% within +/-1 sigma, 95% within +/-2 sigma, 99.7% within +/-3 sigma.
**Canary:** Anomaly detection thresholds — the sigma bands define WARN and ALERT levels.

### 3.4 Right-skewed transaction amounts
**Fig:** ch004_019 | **Type:** Histogram
**Shows:** Right-skewed amount distribution concentrated in low range with long tail.
**Canary:** Transaction size distribution — right tail identifies candidates for LP review.

### 3.5 Log-scale transformation
**Fig:** ch004_020 | **Type:** Histogram (log scale)
**Shows:** Same skewed data on log scale reveals symmetric shape and meaningful outlier bands.
**Canary:** Log-scale view for shrinkage histograms — normalizes heavily skewed LP data.

### 3.6 Shrink rate confidence interval
**Fig:** ch006_009 | **Type:** Annotated output
**Shows:** Mean LP shrink = $8,000 with 95% CI [$7,657-$8,343].
**Canary:** Owl search / shrink KPI card — point estimate + confidence interval bounds.

### 3.7 Sales distribution with normal overlay
**Fig:** ch005_015 | **Type:** Histogram + normal curve
**Shows:** Sales data histogram with normal curve overlaid, identifying outlier periods.
**Canary:** Sales distribution panel — flag periods deviating from expected revenue pattern.

---

## 4. LP Initiative Measurement

### 4.1 Before/after shrink by store (paired)
**Fig:** ch007_008 | **Type:** Table
**Shows:** 20 stores' shrink before vs. after intervention with per-store difference.
**Canary:** LP initiative impact view — before/after at store level.

### 4.2 A/B test: test vs. control summary
**Fig:** ch008_008 | **Type:** Table
**Shows:** 100 test vs. 100 control stores' shrink rates with -0.09% net program impact.
**Canary:** LP initiative results — canonical test/control comparison table.

### 4.3 A/B test: store-level drill-down
**Fig:** ch008_009 | **Type:** Table
**Shows:** Store-by-store pre/post shrink with improvement flag.
**Canary:** Store drill-down — per-location experiment results, sortable.

### 4.4 Binary outcome headline
**Fig:** ch008_010 | **Type:** Table
**Shows:** "68% of test stores improved vs. 52% of controls."
**Canary:** Experiment summary card — "X% of your stores improved" headline.

### 4.5 Significance badge
**Fig:** ch008_011 | **Type:** Table (paired t-test)
**Shows:** t-stat -7.78, p=7.05E-12 confirming device effectiveness.
**Canary:** Initiative significance indicator on result cards.

### 4.6 Sales lift alongside shrink impact
**Fig:** ch008_013 | **Type:** Table
**Shows:** Test stores +0.02% program impact on revenue alongside shrink reduction.
**Canary:** Initiative results — sales lift panel alongside shrink impact.

### 4.7 ROI calculation
**Fig:** ch008_014 | **Type:** Table
**Shows:** Program cost ($87,500) vs. shrink reduction ($324,000) = 3.7:1 ROI.
**Canary:** Health Check ROI summary — merchant-facing return on LP investment.

### 4.8 ANOVA: LP tool effectiveness ranking
**Fig:** ch007_014, ch007_015 | **Type:** Annotated output + Tukey table
**Shows:** F-test comparing 6 LP tools' effectiveness with significance groupings.
**Canary:** LP tool leaderboard — ranked effectiveness with differentiation bands.

---

## 5. Risk Scoring & Driver Analysis

### 5.1 Multi-predictor shrink regression
**Fig:** ch010_016, ch010_017, ch010_019, ch010_023 | **Type:** Regression output
**Shows:** Shrink = f(Internal_Theft, ORC_Theft, Manager_Tenure), R^2=0.99.
**Canary:** Health Check driver analysis — "what drives your shrink" explainability panel.

### 5.2 Predicted vs. actual shrink
**Fig:** ch010_018, ch010_020 | **Type:** Scatter plot
**Shows:** Predicted vs. observed shrink per store along 45-degree line.
**Canary:** Model accuracy view — "how accurate is the shrink forecast" chart.

---

## 6. Classification & Segmentation

### 6.1 Confusion matrix
**Fig:** ch011_006 | **Type:** Matrix
**Shows:** 2x2 TP/FP/FN/TN with sensitivity/specificity formulas.
**Canary:** Model evaluation widget for any binary risk classifier.

### 6.2 ROC curve with AUC
**Fig:** ch011_007 | **Type:** Line chart
**Shows:** Sensitivity vs. 1-specificity, AUC=0.6585.
**Canary:** Model quality view — detection power vs. false alarm rate.

### 6.3 KS lift chart
**Fig:** ch011_008 | **Type:** Line chart
**Shows:** Cumulative separation between predicted classes across score percentiles.
**Canary:** Model ranking view — how well risk score separates high from low risk.

### 6.4 Decision tree segmentation
**Fig:** ch012_009, ch012_013, ch012_019 | **Type:** Decision tree
**Shows:** Color-coded CHAID tree with leaf-node probabilities (tenure + age + crime index).
**Canary:** Risk segmentation view — which employee/location segments are highest risk.

---

## 7. Correlation & Scatter Analysis

### 7.1 Employee theft vs. total shrink
**Fig:** ch005_016 | **Type:** Scatter plot
**Shows:** Shrink % vs. employee theft $, wide dispersal — theft doesn't predict all shrink.
**Canary:** Correlation explorer — isolate non-theft shrink contributors.

### 7.2 Sales vs. stolen products
**Fig:** ch005_018, ch005_021 | **Type:** Scatter plot
**Shows:** Monthly sales vs. theft count, weak correlation — high revenue doesn't mask theft.
**Canary:** Correlation view — test whether high-revenue periods drive or mask theft.

### 7.3 Store-level box plots
**Fig:** ch005_010, ch005_012 | **Type:** Box-and-whisker
**Shows:** Sales/shrink distributions across stores — variability as an LP signal.
**Canary:** Location risk panel — box plots to flag erratic revenue or chronic loss stores.

---

## 8. Taxonomy & Reference

### 8.1 LP analytics activities (current + future)
**Fig:** ch001_001, ch001_002 | **Type:** Table
**Shows:** Current (exception reporting, shrink modeling) and future (predictive fraud, ORC) LP analytics.
**Canary:** Feature roadmap alignment — which capabilities we cover and what's next.

### 8.2 LP initiative taxonomy (17 controls)
**Fig:** ch008_001 | **Type:** Table
**Shows:** Enumerated LP initiatives (cameras, EAS, training, audits, etc.).
**Canary:** Initiative setup — dropdown of supported LP controls.

### 8.3 LP metrics taxonomy (12 KPIs + 8 operational)
**Fig:** ch008_002, ch008_003 | **Type:** Table
**Shows:** Loss metrics (shrink, void rate, return rate) + operational metrics (sales, conversion).
**Canary:** KPI library — the exact metric set for the merchant dashboard.

### 8.4 Initiative-to-metric mapping matrix
**Fig:** ch008_006, ch008_007 | **Type:** Matrix
**Shows:** Which metrics to track per LP initiative, and at what granularity.
**Canary:** Initiative configuration — auto-select correct metrics when merchant picks an LP program.

### 8.5 ORC network / link analysis
**Fig:** ch003_001, ch003_005 | **Type:** Network graph
**Shows:** Customer identities linked by shared cards, addresses, returns.
**Canary:** Owl ORC detection; customer identity graph; fraud cluster alert.

### 8.6 Shrink source breakdown
**Fig:** ch003_002 | **Type:** Pie chart
**Shows:** Shoplifting 39.3%, employee theft 35.8%, admin error 16.8%, unknown 7.2%.
**Canary:** Shrink summary dashboard — loss category breakdown widget.

### 8.7 Return rate vs. shrink correlation
**Fig:** ch003_004 | **Type:** Line chart
**Shows:** High-shrink stores have elevated return rates across percentiles.
**Canary:** Owl search (shrink + return rate correlation); store risk scoring.

### 8.8 N-squared fraud pattern detection
**Fig:** ch013_004 | **Type:** Table
**Shows:** Repeated co-visits, shared baskets, cross-txn card patterns, multi-step return fraud.
**Canary:** Owl transaction linkage and sequence detection.

---

## Gap Analysis: What Canary Has vs. Needs

| Pattern | Have Today | Gap |
|---------|-----------|-----|
| Alert list (alert_set) | Yes — Owl search | - |
| Single KPI (number) | Yes — Owl number response | - |
| Grouped results with drill | Yes — GRO-207 just shipped | - |
| Time-series trend lines | Partial — hourly_metrics exists, no UI | **Need trend chart component** |
| Store comparison bar charts | No | **Need location comparison view** |
| Distribution histograms/box plots | No | **Need distribution visualization** |
| Scatter/correlation plots | No | **Need correlation explorer** |
| A/B test / initiative measurement | No | **Need experiment framework** |
| Decision tree segmentation | No | **Need risk segmentation view** |
| ROC/KS model quality | No | **Need model evaluation display** |
| Control chart with trend detection | No | **Need run chart component** |
| Manager/employee scorecard | Partial — Chirp alerts by employee | **Need dedicated scorecard view** |
| Pareto chart (top N categories) | No | **Need Pareto component** |
| Shrink rate sparkline KPI | No | **Need sparkline widget** |
| ROI calculation | No | **Need ROI summary for Health Check** |

