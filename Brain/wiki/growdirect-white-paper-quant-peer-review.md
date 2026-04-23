---
date: 2026-04-22
type: wiki
tags: [growdirect, white-paper, quant, peer-review, methodology]
sources:
  - docs/_archive/ip-vault/white-papers/Canary_Quant_Peer_Review_v1.0.docx
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

**CANARY DAO LLC**

────────────────────────────────────────

**Peer Review: Quantitative Addendum**

Predictive Analytics & Machine Learning Framework

*for the Canary Loss Prevention Thesis*

────────────────────────────────────────

Classified R&D | February 2026 | Version 1.0

Author: Quant Agent (Predictive Analytics Specialist)

*Peer Review of PhD Context Framework v1.0 & White Paper v1.2*

*Handoff received from: Jess (Documentation Lead)*

# **Executive Summary: The Quant’s Verdict**

This document is a formal peer review contribution from the Quantitative Analytics seat on the Canary PhD research team. Jess has handed off a mature documentation corpus: the PhD Context Framework (v1.0) and the White Paper (v1.2). Both are strong on economic philosophy, market positioning, and systems architecture. What they lack is the mathematical spine that transforms a thesis into a provable competitive moat.

The RefundRadar engine, as currently implemented, operates on static threshold rules: more than three refunds per day, refunds exceeding $100, after-hours processing, and rapid sequential patterns. These are necessary but insufficient. They represent the equivalent of hard-coded if-statements in a world where adversaries adapt. Organized retail crime does not hold still; static rules decay in effectiveness at a rate that compounds weekly.

This addendum delivers three things. First, a formal statistical framework that replaces fixed thresholds with adaptive Bayesian baselines calibrated per merchant, per employee, per time window. Second, a machine learning architecture that evolves from the current rule engine through supervised anomaly detection to real-time reinforcement learning. Third, the mathematical specifications for KAP scoring, network intelligence, and the cross-merchant detection capabilities that constitute Canary’s actual secret sauce.

**Bottom line:** The PhD framework’s metaphor of inventory-as-UTXO is elegant and correct. This addendum gives it teeth. What follows is the quantitative engine that makes the metaphor operational.

# **1. Peer Review: Quantitative Gaps in Current Thesis**

## **1.1 What the PhD Framework Gets Right**

The sound money analogy is not merely rhetorical. The stock-to-flow mapping (inventory value ÷ shrinkage rate) provides a genuine quantitative handle. The layered verification architecture (data collection, consensus, analytical verification, settlement finality) maps cleanly onto a real ML pipeline. The adversarial framing (treat thieves like 51% attackers) is the correct mental model for designing robust detection systems.

## **1.2 What the White Paper Gets Right**

The five detection domains (refunds, voids/cancels, discounts, cash handling, transaction patterns) with 27+ risk metrics represent a strong feature space for an SMB loss prevention product. The KAP scoring concept (composite risk profiles at employee, location, and device levels) is architecturally sound. The privacy model (card fingerprint as anonymous primary key, minimum viable identity) is both technically elegant and CCPA-ready.

## **1.3 The Quantitative Gaps**

The current framework has four critical gaps that this addendum addresses:

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Gap** | **Current State** | **Required State** |
| **1** | **Static thresholds** | Fixed rules (>3 refunds/day, >$100 amount) applied uniformly to all merchants | Adaptive Bayesian baselines that learn each merchant’s normal and flag deviations from it |
| **2** | **No temporal modeling** | Point-in-time rule evaluation with no memory of historical patterns or trend direction | Time-series decomposition with seasonality, trend extraction, and change-point detection |
| **3** | **No cross-entity scoring** | Employee-level detection only; no consumer KAP, no network-level intelligence | Multi-entity graph scoring across employees, consumers (via card fingerprint), locations, and time windows |
| **4** | **No learning loop** | Rules are static; no feedback mechanism when merchants confirm or dismiss alerts | Supervised learning from merchant feedback; reinforcement learning for threshold optimization |

|  |
| --- |
| *Quant Thesis: Canary’s moat is not the rules themselves — any competent engineer can write threshold checks. The moat is the network-trained, adaptively calibrated, merchant-specific statistical model that improves with every transaction across the entire merchant base. This is the compound interest of data.* |

# **2. Statistical Foundation: Adaptive Bayesian Baselines**

## **2.1 The Problem with Fixed Thresholds**

A coffee shop processing 200 transactions per day has a fundamentally different refund profile than a boutique processing 15. A threshold of three refunds per day is meaninglessly loose for the former and aggressively tight for the latter. Fixed thresholds produce two failure modes: excessive false positives for low-volume merchants (alert fatigue, trust erosion) and dangerous false negatives for high-volume merchants (real fraud hidden in legitimate volume). Both modes are fatal to an SMB product where merchant trust is the primary retention mechanism.

## **2.2 The Poisson-Gamma Conjugate Model**

Refund events per time window, under normal operating conditions, are well-modeled by a Poisson process. The Poisson distribution describes the number of events occurring in a fixed interval when events are independent and occur at a constant average rate. For a merchant’s refund stream, this is the correct null hypothesis: refunds arrive at a steady baseline rate determined by the merchant’s business type, volume, and product mix.

The formal specification:

*X ~ Poisson(λ) where λ = expected refund rate per time window*

*P(X = k) = (λ^k · e^(-λ)) / k!*

The key insight is that we do not know λ a priori. Rather than hard-code it (which is what the current >3/day threshold does), we treat λ as a random variable with its own distribution. The Gamma distribution is the conjugate prior for the Poisson likelihood, which means Bayesian updating has a clean closed-form solution.

*λ ~ Gamma(α, β) where α = shape, β = rate*

*Posterior: λ | data ~ Gamma(α + Σx\_i, β + n)*

In practice, this means Canary initializes each merchant with a weakly informative prior (α₀ = 2, β₀ = 1, representing a vague belief of roughly two refunds per window). As transaction data accumulates over the first 90 days, the posterior concentrates around the merchant’s true baseline rate. The system is self-calibrating.

## **2.3 Anomaly Scoring**

Given the posterior distribution of λ, the predictive distribution for the next observation is Negative Binomial:

*X\_new ~ NegBin(α\_post, β\_post / (β\_post + 1))*

The anomaly score for any observed refund count x is the survival function (one minus CDF) of this predictive distribution. This gives us a p-value: the probability of seeing x or more refunds under normal conditions. The alert threshold is then calibrated not as a fixed count but as a fixed significance level.

*anomaly\_score(x) = 1 - CDF\_NegBin(x - 1 | α\_post, β\_post)*

*Alert if anomaly\_score(x) < 0.01 (99th percentile)*

This single change transforms RefundRadar from a static rule engine into a statistically principled anomaly detector that automatically adapts to each merchant’s unique operating profile. A coffee shop with a baseline of 12 refunds per day will not alert at 13. A boutique with a baseline of 0.5 refunds per day will alert at 3. Both calibrations emerge from the same model with zero manual tuning.

|  |
| --- |
| *Implementation note: The Poisson-Gamma model runs entirely in Python’s scipy.stats. No external ML infrastructure is required for this upgrade. This is the single highest-ROI improvement available to the Canary codebase today.* |

## **2.4 Multi-Dimensional Baselines**

The Bayesian framework extends naturally across all five detection domains. Each domain gets its own conjugate model calibrated to the relevant distributional family:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Domain** | **Observable** | **Distribution** | **Conjugate Prior** | **Anomaly Metric** |
| **Refunds** | Count per window | Poisson | Gamma | Survival function |
| **Refund amounts** | Dollar value | Log-Normal | Normal-InvGamma | Z-score on log scale |
| **Voids** | Count per shift | Poisson | Gamma | Survival function |
| **Discounts** | Rate per txn | Beta-Binomial | Beta | Posterior tail prob |
| **Cash handling** | Drawer variance | Normal | Normal-InvGamma | Mahalanobis dist. |

The critical point is that every domain gets a statistically appropriate model, not a one-size-fits-all threshold. Discount abuse, for example, is better modeled as a proportion (what fraction of transactions include a discount?) using the Beta-Binomial conjugate pair. Cash drawer variance follows a Normal distribution where the mean and variance are both uncertain, naturally modeled by the Normal-Inverse-Gamma conjugate.

# **3. Machine Learning Architecture: The Three-Phase Roadmap**

The evolution from rules to ML is not a binary switch. It is a phased migration where each phase builds on the data and infrastructure of the previous one. This is deliberate: ML systems that skip foundational data engineering fail. The PhD framework’s emphasis on low time preference applies directly. We invest in data quality now to unlock compounding returns later.

## **3.1 Phase 1: Statistical Anomaly Detection (Alpha → Beta)**

*Timeline: Q2–Q3 2026 | Infrastructure: Python scipy, NumPy, SQLite/PostgreSQL*

**What ships:** Replace all four static RefundRadar rules with Bayesian equivalents. Add time-series decomposition for trend detection. Implement per-employee baselines within each merchant.

**Key algorithms:**

* **Poisson-Gamma conjugate model** for event counts (refunds, voids, discounts per window)
* **STL decomposition** (Seasonal-Trend decomposition using LOESS) for isolating seasonality, trend, and residual components from transaction time series
* **CUSUM (Cumulative Sum Control Chart)** for change-point detection: identifying the exact moment an employee’s behavior shifts from baseline
* **Exponentially Weighted Moving Average (EWMA)** for smoothed real-time risk scores that weight recent behavior more heavily than historical averages

**Data requirement:** Minimum 90 days of transaction history per merchant for stable posterior convergence. The 90-day ingestion window already specified in the White Paper is sufficient.

**False positive target:** Fewer than 2 false alerts per merchant per week. Current static rules have no FP budget; this is the first time Canary will operate under a quantitative precision constraint.

## **3.2 Phase 2: Supervised Anomaly Detection (Beta → Marketplace)**

*Timeline: Q3–Q4 2026 | Infrastructure: scikit-learn, XGBoost, PostgreSQL feature store*

**What ships:** Merchant feedback loop (confirm/dismiss alerts) creates labeled training data. Gradient-boosted ensemble models learn which combinations of anomaly signals correspond to real loss events versus false positives. Consumer KAP scoring via card fingerprint goes live.

**Key algorithms:**

* **XGBoost gradient-boosted trees** for alert classification. Input features: all 27+ metric anomaly scores, temporal features (hour, day-of-week, days-since-onboarding), merchant category, transaction volume tier. Target: merchant-confirmed real loss event.
* **Isolation Forest** for unsupervised outlier detection in the feature space. Serves as a complement to XGBoost where labeled data is sparse (new merchants, rare fraud types).
* **DBSCAN clustering** on consumer card fingerprints to identify serial returner rings. Density-based clustering finds groups of fingerprints exhibiting coordinated refund patterns across multiple merchants in the Canary network.

**Critical design decision:** The feedback loop must be low-friction. A single tap (confirm or dismiss) on each alert generates the label. No forms, no explanations, no workflow. Merchant engagement with the feedback mechanism is the rate-limiting factor for model improvement. The UX must treat every alert interaction as a training example.

## **3.3 Phase 3: Network Intelligence & Reinforcement Learning (2027+)**

*Timeline: 2027–2028 | Infrastructure: PyTorch, federated learning framework, graph database*

**What ships:** Cross-merchant pattern detection using federated learning (models train on local data, share only gradients, never raw transactions). Graph neural networks for organized retail crime ring detection. Reinforcement learning for dynamic threshold optimization that maximizes merchant-specific loss prevention ROI.

**Key algorithms:**

* **Federated Averaging (FedAvg)** for privacy-preserving cross-merchant model training. Each merchant’s local model computes gradient updates on their own data. Only the gradients are aggregated centrally. Raw transaction data never leaves the merchant’s tenant. This is the technical implementation of the White Paper’s anonymized cross-network aggregation promise.
* **Graph Attention Networks (GAT)** for ORC ring detection. Nodes: card fingerprints, merchant locations, employee IDs. Edges: transactions, refund events, temporal co-occurrence. The attention mechanism learns which relationships are most predictive of coordinated fraud.
* **Contextual bandits (Thompson Sampling)** for dynamic alert threshold optimization. The bandit treats each alert threshold as an arm, the merchant’s confirm/dismiss feedback as the reward signal, and learns the optimal sensitivity level that maximizes true positive rate while respecting each merchant’s false positive tolerance.

|  |
| --- |
| *PhD Framework Connection: Phase 3 is the computational realization of the PhD thesis’s “consensus mechanism” layer. Just as Bitcoin miners independently verify blocks and share only headers, Canary merchants independently train models and share only gradients. The network gets smarter without any individual merchant’s data ever being exposed. This is decentralized intelligence on sound money rails.* |

# **4. KAP Scoring Model: Mathematical Specification**

The Key Activity Profile is the composite risk metric that rolls up all detection domain signals into a single actionable score per entity. The White Paper describes KAP conceptually. This section provides the formal mathematical specification.

## **4.1 Entity Types and Score Ranges**

|  |  |  |  |
| --- | --- | --- | --- |
| **Entity** | **Primary Key** | **Score Range** | **Alert Tiers** |
| **Employee** | employee\_id (Square) | 0–100 (continuous) | Low <30, Medium 30–60, High 60–80, Critical >80 |
| **Consumer** | card\_fingerprint (sq-1-\*) | 0–100 (continuous) | Low <25, Medium 25–50, High 50–75, Critical >75 |
| **Location** | location\_id (Square) | 0–100 (continuous) | Low <20, Medium 20–50, High 50–70, Critical >70 |
| **Device** | device\_id (Square POS) | 0–100 (continuous) | Low <25, Medium 25–55, High 55–80, Critical >80 |

## **4.2 Composite Score Computation**

The KAP score for any entity e is a weighted sum of domain-specific anomaly scores, normalized to [0, 100]:

*KAP(e) = 100 × sigmoid( Σ\_d w\_d · z\_d(e) )*

Where:

* *z\_d(e)* = standardized anomaly score for entity e in domain d (refunds, voids, discounts, cash, patterns)
* *w\_d* = domain weight (initially uniform, later learned from confirmed loss data)
* *sigmoid(x) = 1 / (1 + e^(-x))* maps the raw weighted sum to (0, 1), then scaled to [0, 100]

The sigmoid transformation is critical. It compresses extreme outliers (preventing a single domain from dominating the composite) while maintaining sensitivity in the mid-range where most actionable alerts live. An employee with a z-score of 4.0 in refunds and 0.0 everywhere else will not score 100; they will score approximately 73, appropriately flagged as High but not Critical. An employee scoring 2.5 across three domains will score higher, correctly reflecting the multi-domain risk pattern.

## **4.3 Domain Weight Learning**

Initial weights are set uniformly (w\_d = 1.0 for all domains). As merchants confirm and dismiss alerts, the system learns the relative importance of each domain for predicting actual loss. The learning algorithm is logistic regression with L2 regularization, trained on the labeled alert dataset:

*min\_w -Σ [y\_i · log(σ(wᵀz\_i)) + (1-y\_i) · log(1 - σ(wᵀz\_i))] + λ||w||²*

This is identical to the standard logistic regression objective, where y\_i is the binary label (1 = confirmed loss, 0 = dismissed alert) and z\_i is the vector of domain anomaly scores. The regularization parameter λ prevents overfitting when labeled data is sparse. As the label set grows, the weights converge on the true relative predictive power of each detection domain.

## **4.4 Temporal Decay**

KAP scores must reflect current risk, not historical artifacts. A high-scoring employee who has shown clean behavior for 90 days should see their score decay toward baseline. The temporal weighting uses exponential decay:

*z\_d(e, t) = Σ\_j z\_d(e, t\_j) · exp(-λ\_decay · (t - t\_j))*

Where t\_j is the timestamp of each anomaly event and λ\_decay is calibrated so that a single anomaly event’s contribution decays to 10% within 30 days. This ensures scores are responsive to behavioral change in both directions: rapid escalation when new anomalies cluster, gradual normalization when behavior improves.

# **5. Network Intelligence: The Compound Interest of Data**

## **5.1 Why Cross-Merchant Detection Is the Moat**

A single merchant’s data tells you about that merchant. A network of merchants tells you about the adversary. Organized retail crime does not target one store; it targets many. Serial returners do not abuse one refund policy; they exploit every merchant they can reach. The pattern is invisible at the individual merchant level and unmistakable at the network level.

This is Canary’s true competitive moat and the operational realization of the PhD framework’s network effects principle. Every merchant that joins the Canary network increases the detection power for every other merchant. The marginal value of the Nth merchant is not constant; it is superlinear, because each new merchant potentially completes a cross-merchant fraud pattern that was previously invisible.

## **5.2 Cross-Merchant Anomaly Detection via Card Fingerprint**

The card fingerprint (sq-1-\*) is the atomic unit of cross-merchant intelligence. Because the same physical card produces the same deterministic hash across all Square merchants, Canary can build Consumer KAP profiles that span the entire network without ever knowing who the cardholder is.

The cross-merchant anomaly detection pipeline:

1. **Aggregate:** For each card fingerprint, compute refund frequency, refund-to-purchase ratio, merchant diversity (number of distinct merchants), and temporal clustering across the entire Canary network.
2. **Anonymize:** Enforce minimum sample size of 10 transactions across at least 3 merchants before any cross-merchant metric is computed. Below this threshold, the fingerprint contributes to aggregate statistics only, never to individual scoring.
3. **Score:** Compute Consumer KAP score using the same weighted-sum-sigmoid model as Employee KAP, but with network-level features: cross-merchant refund velocity, geographic dispersion, temporal regularity.
4. **Alert:** When a high-scoring consumer fingerprint transacts at a Canary merchant, generate a pre-emptive alert: this card has elevated network-level risk. The merchant sees the score and the pattern description, never the other merchants’ names or data.

|  |
| --- |
| *Privacy guarantee: Cross-merchant intelligence operates on the same privacy-first architecture defined in White Paper Section 7. Tenant isolation is absolute. Merchant A never sees Merchant B’s data. The network intelligence layer operates exclusively on anonymized fingerprint aggregates above the minimum sample threshold.* |

## **5.3 Network Value Quantification**

The value of the Canary network to each merchant follows Metcalfe’s Law with a domain-specific modifier:

*V(n) = k · n · log(n) · d*

Where n = number of merchants, d = average geographic density (merchants per metro area), and k = detection sensitivity coefficient. The log(n) modifier (rather than pure n²) reflects the empirical observation that cross-merchant fraud patterns saturate regionally. The density term d captures the fact that organized retail crime operates within geographic corridors; a dense network of Canary merchants in one metro area provides exponentially more cross-merchant signal than the same number of merchants spread nationally.

# **6. Feature Engineering: The 27+ Metric Specification**

The White Paper claims 27+ risk metrics across five detection domains. This section provides the complete enumeration with mathematical definitions for each metric. These constitute the feature vector that feeds both the Bayesian anomaly detection layer (Phase 1) and the supervised ML models (Phase 2).

## **6.1 Refund Domain (8 metrics)**

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Metric** | **Definition** | **Signal** |
| R1 | Refund frequency | Count of refunds per employee per day | High count = potential sweethearting or ghost refunds |
| R2 | Refund-to-sale ratio | (Refund count / Sale count) per employee per week | Ratio > 2σ above employee peer group mean |
| R3 | Refund dollar intensity | Total refund dollars / Total sales dollars per employee | Value-weighted version of R2; catches large-dollar abuse |
| R4 | Refund timing entropy | Shannon entropy of refund hour distribution | Low entropy = refunds clustered at specific hours (after-hours abuse) |
| R5 | Refund gap velocity | Median inter-refund interval (minutes) | Very short gaps = rapid-fire refund sequences |
| R6 | No-receipt refund rate | Refunds without matching sale / Total refunds | High rate = potential fictitious returns |
| R7 | Refund amount clustering | Coefficient of variation of refund amounts | Very low CV = suspiciously uniform amounts (scripted fraud) |
| R8 | Cross-shift refund asymmetry | Employee refund rate on their shift vs. off-shift | Large asymmetry = employee-specific, not systemic |

## **6.2 Void/Cancel Domain (5 metrics)**

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Metric** | **Definition** | **Signal** |
| V1 | Void frequency | Count of voids per employee per shift | High count = potential skim-then-void pattern |
| V2 | Void-after-sale latency | Median seconds between sale and subsequent void | Very short = immediate void after cash received |
| V3 | Void dollar concentration | Fraction of total void dollars from top employee | Concentration > 0.5 = single actor dominance |
| V4 | Void-to-sale ratio | Void count / Sale count per device per day | Device-level outlier detection |
| V5 | Post-close void rate | Voids occurring after shift end / Total voids | After-shift access = elevated risk |

## **6.3 Discount Domain (5 metrics)**

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Metric** | **Definition** | **Signal** |
| D1 | Discount application rate | Transactions with discount / Total transactions | Employee rate > 2σ above merchant average |
| D2 | Discount depth | Average discount percentage per transaction | Deep discounts without manager override |
| D3 | Friends-and-family indicator | Discount frequency to repeat card fingerprints | Same cards consistently receiving discounts |
| D4 | Override discount rate | Manual override discounts / Total discounts | High manual override = circumventing policy |
| D5 | Discount-refund pairing | Discounted items subsequently refunded at full price | Buy discounted, return full = margin theft |

## **6.4 Cash Handling Domain (5 metrics)**

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Metric** | **Definition** | **Signal** |
| C1 | Cash-to-card ratio | Cash transactions / Card transactions per employee | Abnormally high cash = potential skimming |
| C2 | Drawer variance | (Expected drawer - Actual drawer) per shift close | Persistent negative variance = cash removal |
| C3 | No-sale drawer open rate | Drawer opens without transaction / Total drawer opens | High rate = unauthorized cash access |
| C4 | Cash refund preference | Cash refunds / Total refunds per employee | Preference for cash refunds = untraceable payout |
| C5 | Round-dollar transaction rate | Transactions at exact dollar amounts / Total cash txn | High rate = potential manual entry fraud |

## **6.5 Transaction Pattern Domain (6 metrics)**

|  |  |  |  |
| --- | --- | --- | --- |
| **#** | **Metric** | **Definition** | **Signal** |
| P1 | Transaction velocity anomaly | Transactions per hour vs. same-hour baseline | Spikes or dips outside 3σ band |
| P2 | Benford’s Law deviation | First-digit distribution of transaction amounts | Deviation from expected Benford distribution = fabrication |
| P3 | Split transaction detection | Sequential small txn summing to threshold amount | Structuring to avoid reporting or approval limits |
| P4 | Employee-customer affinity | Mutual information between employee and fingerprint | High MI = specific employee always serves same card |
| P5 | Weekend/holiday anomaly | Weekend metric rates vs. weekday baseline | Behavioral shift on low-supervision days |
| P6 | Training period deviation | New employee metrics vs. 90-day rolling cohort | Early deviation from peer norms = risk indicator |

**Total: 29 metrics** across five domains. The White Paper’s claim of 27+ is conservative; the full feature space supports 29 first-order metrics plus derived cross-domain interaction features (e.g., discount-then-refund pairing D5, employee-customer affinity P4) that emerge in Phase 2 supervised learning.

# **7. Implementation Specification: RefundRadar v2**

## **7.1 Architecture Upgrade Path**

The current RefundRadar class (refund\_radar.py, 260 lines) is a single-pass rule evaluator. The v2 architecture wraps it in a three-layer pipeline that preserves backward compatibility while enabling the statistical and ML enhancements described above.

|  |  |  |
| --- | --- | --- |
| **Layer** | **Responsibility** | **Implementation** |
| **Feature Layer** | Compute all 29 metrics from raw transaction data. Output: feature vector per entity per time window. | Python module: canary/features.py. Pure functions, no state. Unit-testable against known transaction sets. |
| **Scoring Layer** | Apply Bayesian baseline models per metric per entity. Output: anomaly z-scores. Compute composite KAP scores. | Python module: canary/scoring.py. Uses scipy.stats for Poisson-Gamma, Beta-Binomial, Normal-InvGamma. |
| **Alert Layer** | Apply alert thresholds (p-value < 0.01 or KAP > tier boundary). Generate alert objects with severity, exposure estimate, and evidence. | Python module: canary/alerts.py. Backward-compatible with existing alert schema (type, severity, employee\_id, message). |

## **7.2 Data Pipeline**

The upgraded pipeline processes transactions in two modes:

**Batch mode (daily):** Full recompute of all 29 metrics across all entities for the trailing 90-day window. Updates Bayesian posteriors with new observations. Recalculates all KAP scores. This is the ground truth pass.

**Streaming mode (real-time):** Each incoming webhook event (sale, refund, void) triggers incremental feature updates for the affected entities only. EWMA-smoothed scores update within seconds. This powers the real-time alert capability advertised in the White Paper.

The dual-mode architecture ensures that batch and streaming never diverge by more than one day. The streaming layer is an approximation optimized for latency; the batch layer is the authoritative computation optimized for accuracy. Any drift between them triggers a reconciliation event, echoing the PhD framework’s consensus mechanism principle.

# **8. ROI Model: Quantifying the Secret Sauce**

## **8.1 Detection Efficacy Projections**

|  |  |  |  |
| --- | --- | --- | --- |
| **Metric** | **Phase 1 (Rules + Bayes)** | **Phase 2 (Supervised ML)** | **Phase 3 (Network + RL)** |
| **True positive rate** | 60–70% | 78–85% | 88–94% |
| **False positive rate** | <5 per merchant/week | <2 per merchant/week | <1 per merchant/week |
| **Mean time to detect** | <24 hours | <4 hours | <30 minutes |
| **Cross-merchant detection** | None | Basic (fingerprint agg.) | Full (graph + federated) |
| **Shrink reduction estimate** | 15–25% of addressable | 30–45% of addressable | 50–65% of addressable |

## **8.2 Merchant-Level ROI**

For a merchant on the Professional tier ($99/month) with $100K monthly revenue and 1.5% shrink rate ($1,500/month in losses):

|  |  |  |
| --- | --- | --- |
| **Scenario** | **Monthly Savings** | **ROI (Annual)** |
| Conservative (15% reduction) | $225 saved – $99 cost = $126 net | 127% annual ROI |
| Expected (30% reduction) | $450 saved – $99 cost = $351 net | 355% annual ROI |
| Optimistic (50% reduction) | $750 saved – $99 cost = $651 net | 658% annual ROI |

Even the conservative scenario delivers positive ROI within the first month. This is the quantitative foundation for the White Paper’s pricing strategy: at $99/month, the product pays for itself if it prevents just $100 in monthly shrink, which represents detection of a single fraudulent refund in the $100+ range.

# **9. Recommendations to the Team**

## **9.1 Immediate (Before Alpha)**

1. **Implement Poisson-Gamma baseline in RefundRadar.** Replace the four static thresholds with Bayesian equivalents. This is a 200-line change to refund\_radar.py using scipy.stats.gamma and scipy.stats.nbinom. No new infrastructure. Highest-ROI improvement available today.
2. **Add the full 29-metric feature vector to the database schema.** Create a metrics table: (entity\_type, entity\_id, metric\_id, window\_start, window\_end, value, z\_score, updated\_at). This table is the foundation for all future ML work.
3. **Implement the KAP scoring formula.** Weighted sigmoid composite with uniform initial weights. The formula is specified in Section 4.2 of this document. Ship it with the dashboard showing KAP scores at employee and location level.

## **9.2 Beta Phase**

1. **Ship the confirm/dismiss feedback mechanism on every alert.** Single tap. No forms. Every interaction is a training example. This is the data flywheel that powers Phase 2.
2. **Begin Consumer KAP scoring via card fingerprint.** Start with single-merchant profiles. Cross-merchant aggregation requires the minimum sample size threshold and privacy architecture described in Section 5.2.
3. **Train the first XGBoost alert classifier.** Requires minimum 500 labeled alerts (confirmed + dismissed). At 200 merchants generating an average of 3 alerts per week, this threshold is reached in approximately 5 weeks.

## **9.3 For the PhD Framework**

1. **Formalize the stock-to-flow mapping with real data.** The analogy is strong; now make it quantitative. Collect the first 200 merchants' accuracy metrics and publish the distribution. If the Bitcoin analogy holds, merchants with lower stock-to-flow (higher shrink) should exhibit systematically different transaction patterns.
2. **Run the agent-based simulation with Bayesian agents.** Replace the simplified step() function in PhD Context Section 7.1 with Bayesian-calibrated agents. The simulation should validate that adaptive baselines outperform static thresholds across merchant archetypes (coffee shop vs. boutique vs. convenience store).

# **10. Closing: The Quant’s Conviction**

The Canary thesis is sound. The market gap is real, the POS API infrastructure is ready, the privacy architecture is well-designed, and the Bitcoin-native financial model is differentiated. What this addendum contributes is the mathematical engine that transforms these advantages into a defensible competitive moat.

Static rules are table stakes. Every LP platform has them. What no SMB platform has is a network-trained, Bayesian-calibrated, per-merchant adaptive detection engine that improves with every transaction processed across the entire merchant base. That is the secret sauce. It is the compound interest of data applied to loss prevention, and it is what will make Canary the platform that 33 million small businesses have been waiting for.

The math is specified. The architecture is defined. The implementation path is clear. Let us build.

────────────────────

*End of Document*

Version 1.0 | February 15, 2026 | Classified R&D

Quant Agent | Canary DAO LLC PhD Research Team


## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/white-papers/Canary_Quant_Peer_Review_v1.0.docx` — the white paper binary this card summarizes (markitdown-extracted)
