---
layout: page
title: "Crack Spread Signal Research"
date: 2026-04-29
description: >
  A crack-spread signal study covering signal design, IC checks, regime splits, backtests, and out-of-sample results.
project_tags: "Energy futures · Crack spreads · Signal research · Backtesting"
summary: "A research notebook on crack-spread signals across RBOB, heating oil, and 3-2-1 refinery-margin proxies, with separate tests for normal and stressed market regimes."
notebook_source: "/Crack Spread Signal Research.ipynb"
asset_dir: "/assets/img/projects/crack-spread-signal-research"
---

<div class="qr-memo-meta">
  <p class="qr-memo-meta__eyebrow">Research Memo</p>
  <p>This notebook tests crack-spread trend and mean-reversion signals across RBOB, heating oil, and 3-2-1 spreads, with separate checks for normal and stressed market regimes.</p>
  <div class="qr-memo-meta__actions">
    <a class="qr-btn qr-btn--primary" href="/notebooks/Crack%20Spread%20Signal%20Research.zip">Download Notebook</a>
  </div>
</div>

# Background

This notebook presents my approach to quantitative signal research, with an emphasis on commodity futures. The focus here is a practical research workflow rather than a finished trading strategy. My background is primarily in energy markets, including Brent crude, WTI crude, Dubai crude, RBOB gasoline, and Singapore 92 motor gasoline. My experience across these markets has covered strategy research, execution, and discretionary trading.

Although my practical experience has been concentrated in energy futures, my research interests are broader and include systematic work across multiple asset classes.

Further details on my background and experiences can be found in my CV at [https://elroy-goh.github.io/cv](https://elroy-goh.github.io/cv).

All analytical frameworks, interpretations, and conclusions in this notebook are my own.

# Introduction

The notebook studies four standard crack-spread structures:

1. RBOB crack
2. Heating oil crack
3. 3-2-1 crack spread
4. 5-3-2 crack spread

Crack spreads are useful proxies for refinery economics. They are not literal refinery margins because each refinery has its own yield profile, operating constraints, location, feedstock slate, etc. Still, they are economically meaningful relative prices inside the crude and products complex. They can move sharply when the physical market is hit by refinery outages, freight issues, sanctions, inventory stress, and/or product-specific shortages.

In stressed markets, crack moves can persist because the physical constraint does not clear immediately. In quieter markets, I would expect crack levels to mean-revert more often. That leads to a four-signal setup:

1. Normal trend
2. Normal mean reversion
3. Stress trend
4. Stress mean reversion

The split is intentional. Under stressed conditions, I want the trend signal to react faster and the mean-reversion signal to be slower. Under normal conditions, I want the opposite: a slower trend signal and a faster mean-reversion signal.

The analysis is carried out in this order:

1. Exploratory data analysis
2. Signal definition
3. Information coefficients and robustness checks
4. Regime analysis
5. Standalone and portfolio backtests
6. Out-of-sample validation

---

# Research Design and IS/OOS Split

Before we proceed on with the data exploration, let's define the validation framework. The signals and portfolio rules are studied first on the in-sample period then checked separately out of sample.

We'll use the following periods:

1. In-sample: 2017-05-19 to 2021-12-31
2. Out-of-sample: 2022-01-01 to 2026-02-17

We'll use the entire data history for EDA as it is generally descriptive. The signals diagnostics, sensitivity checks, regime tests, and portfolio constructions are carried out purely on IS data. The OOS section then checks on whether the same choices survive outside the period where the research decisions were made.

---

# Load Data

A short note on data construction before moving on to the analysis:

The crack spreads are rolled on the 15th of the month before contract expiry. This is to accommodate the expiration of the WTI leg, which generally expires around 21th of every month while the RBOB/HO legs expires at the end of the month. This makes it so that when we are constructing our portfolio, a J26 RBOB contract follows a J26 HO and WTI leg.

Under production research, we should test the results across several roll conventions instead of relying on a single construction.

One other detail for the blended cracks. I normalise the 3-2-1 and 5-3-2 spreads to one crude-barrel equivalent, so they are easier to compare against the single-product RBOB and HO cracks. That means the P&L shown in this notebook should be read as a normalised P&L instead of an exchange-quoted multi-leg crack.

---

# Exploratory Data Analysis

We'll work through a little bit of exploratory data analysis before working on the signals.

A few things I would expect going in:

1. RBOB crack should show visible seasonality because gasoline specs rotate between winter and summer blends. This can make the level series look mean-reverting over longer windows, however that is purely an artifact of the spec switch.
2. Heating oil used to have a stronger seasonal identity when it was closer to a heating-fuel contract. Since the post-2013 ultra-low-sulfur diesel specification became the main standard, I recall that the seasonal bounce no longer show up.
3. The 3-2-1 and 5-3-2 blended cracks should be very similar. The weights are different, but both are still mainly combinations of RBOB, HO, and CL at very similar percentages.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-01.png" | relative_url }}" alt="Crack Spread Signal Research figure 1">
  <figcaption>Figure 1. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-02.png" | relative_url }}" alt="Crack Spread Signal Research figure 2">
  <figcaption>Figure 2. Exported directly from the notebook output.</figcaption>
</figure>

The unrolled RBOB crack seasonality comes through clearly in the level chart. That is consistent with the grade-rotation story. HO crack is less seasonal, which is also broadly in line with the product-spec change discussed above.

The 5-3-2 and 3-2-1 structures are almost indistinguishable  with correlation of 0.99. The 5-3-2 blend is 60/40 RBOB/HO, while the 3-2-1 is roughly 67/33. That difference is too small to justify carrying both through the rest of the notebook and we shall drop 5-3-2 from this point.

The 3-2-1 is still correlated with the single-product cracks, but is different enough to be worth testing separately.

## ACF/PACF Plots on Monthly Returns

The monthly ACF and PACF are a quick way to check whether any obvious seasonal or autoregressive structure shows up in crack changes. I use monthly changes here because the seasonal question is naturally annual, not daily.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-03.png" | relative_url }}" alt="Crack Spread Signal Research figure 3">
  <figcaption>Figure 3. Exported directly from the notebook output.</figcaption>
</figure>

HO crack does not show a clean pattern. There are a few spikes around lag 15/17, but there doesn't seem to be any strong economic reason to attach meaning to those specific lags.

RBOB crack has some lag 13/14 movement, but the chart does not give a clean enough return-process story.

The 3-2-1 chart looks more interesting at first glance. The spikes around lag 11 and 22 could be read as a rough annual pattern. Let's follow up with some checks in the next section.

## Seasonality in 3-2-1 Crack Spread

We use two cleaner checks to study the potential annual or near-annual pattern here:
1. Calendar-month average changes -- to see if there is a month-of-year effect.
2. A direct lag-12 relationship, to test whether the current month's change is related to the same month last year.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-04.png" | relative_url }}" alt="Crack Spread Signal Research figure 4">
  <figcaption>Figure 4. Exported directly from the notebook output.</figcaption>
</figure>

The calendar-month summary does not show a clean deterministic seasonal pattern. Every month-of-year average has a 95% confidence interval that overlaps zero, including the larger positive April estimate. That makes it hard to argue that the monthly 3-2-1 change has a stable calendar-month return effect in this sample.

The direct lag-12 relationship is also weak. The same-month-last-year correlation is -0.120 across 94 observations, with a HAC t-statistic of -1.385 and a regression beta of -0.118. That is not strong enough to treat the earlier lag-11/22 ACF movement as evidence of a tradable annual-return pattern.

---

# Signal Definition

We define four signals: trend and mean reversion, each split into stress and normal variants.

The hypothesis is that crack spreads behave differently across physical market states. When a supply shock hits, the move can persist for days or weeks. In that case, a faster trend signal may make sense. Under normal conditions, I would expect extreme crack levels to revert more often, while any broader trend should be measured over a slower window.

To keep the setup simple, I use two anchor horizons:

1. Short term: 40 trading days
2. Long term: 120 trading days

The trend signals are scaled by a lagged 40-day EWMA volatility estimate. For both signal families, the stress variants use the faster trend window and slower mean-reversion window. The normal variants reverse that choice.

These parameters are not optimised. They are based on market intuition and we'll later check these through sensitivity analysis.

## Trend Signals

Both trend variants use the same form on the rolled crack series:

$$
S^{trend}_t = \frac{P^{roll}_{t-s} - P^{roll}_{t-l}}{\sigma_{rolling}}
$$

where:

1. $P^{roll}$ is the rolled crack-spread price
2. $l$ is the lookback window
3. $s$ is the skip window
4. $\sigma\_{rolling}$ is the lagged 40-day EWMA standard deviation of crack changes

The sign convention is straightforward. If the recent rolled price is above the older rolled price, the trend signal is positive. A positive signal maps to a long crack position in the backtest.

I include a skip window because very short-term reversals can contaminate the trend signal. Under stressed conditions, I use a 40-day lookback with a 2-day skip. Under normal conditions, I use a 120-day lookback with a 5-day skip.

## Mean-Reversion (or Roll) Signals

Both mean-reversion variants use a percentile-rank form on the unrolled crack series:

$$
S^{mr}_t = -2 \times (Rank_t(L) - 0.5)
$$

where $Rank\_t(L)$ is the percentile rank of the current crack level within the trailing $L$ observations.

The negative sign means high crack levels produce short signals and low crack levels produce long signals. The signal here is not scaled as percentile ranking is already bounded and  is already unitless. An alternative interpretation to this signal is `roll`, where futures roll up/down depending on the term structure.

I use percentile ranking rather than moving-average crossover because crack spreads are more naturally read relative to their own \`nearby\` history. Under stressed conditions, the rank is computed over 120 days so the signal only reacts to broader extremes. Whereas under normal conditions, the rank window is 40 days so the signal reacts to local range extension.

## Parameter Summary

| Signal         | Regime | Source series | Primary window           | Skip   | Volatility lookback |
| -------------- | ------ | ------------- | ------------------------ | ------ | ------------------- |
| Trend          | Stress | Rolled        | Lookback = 40 days       | 2 days | EWMA span = 40 days |
| Trend          | Normal | Rolled        | Lookback = 120 days      | 5 days | EWMA span = 40 days |
| Mean reversion | Stress | Unrolled      | Rank lookback = 120 days | N/A    | N/A                 |
| Mean reversion | Normal | Unrolled      | Rank lookback = 40 days  | N/A    | N/A                 |

---

# Information Coefficients (In-Sample)

Before backtesting, let us first check if the signals have any directional relationship with subsequent crack moves.

The alignment here is important. We cannot produce and consume the signal exactly at the same time. If we had more granular data, we could assume that we enter our positions after a short delay from the time the settlement data gets released by hitting/lifting at BBO. As our signals here are assumed to be produced at time $T$ and our data here happened to be daily settlement, the earliest timestamp we could enter a position is at time $T+1$. The main target here is therefore `terminal_change_2d`, which refers to the realised return from $T+1$ to $T+2$.

Alternatively, with daily settlement data only, we could assume that we trade at settlement price (that produced the signal) and add in some slippage cost assumption, which would work as well, provided it is reasonable.

We'll study both the terminal IC and cumulative IC, which answers if the signal predicts price move on a specific future day and if the signal predicts the total move over a forward window. We use Newey-West corrected t-statistics due to the serially dependent signals and residuals. For cumulative IC, the overlap is an additional reason to prefer HAC inference.

As a rough heuristic, we should treat an IC as having potential if it is positive (>= 0.03) with t-statistics consistently around 1.5-2.0 or higher.

We print an averaged IC/t-stat table. The values in the table are descriptive summaries and the averaged t-stat should not be interpreted as a formal pooled test statistic.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-05.png" | relative_url }}" alt="Crack Spread Signal Research figure 5">
  <figcaption>Figure 5. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-06.png" | relative_url }}" alt="Crack Spread Signal Research figure 6">
  <figcaption>Figure 6. Exported directly from the notebook output.</figcaption>
</figure>

The in-sample IC picture is weak. Most values are small, and the t-statistics are not strong enough to make a confident directional claim. (I left the printing of tables out, but results are generally weak. Feel free to re-run this notebook locally.)

Across the three product cracks, the broad pattern is that the mean-reversion signals are mostly positive, while the trend variants are generally negative. The magnitudes are still small, so I would not treat this as  evidence of a tradable mean-reversion effect. However, it does suggest that the simple trend-following story is not well supported unconditionally.

The mean-reversion result looks more constructive for RBOB and 3-2-1, especially beyond the single-day horizon. That makes some sense because 3-2-1 still contains a large gasoline-crack component, so it should not be surprising if it shares some behaviour with RBOB.  The ICs are not strong enough by themselves, but they do tell us where the signal family is more aligned with the original hypothesis.

On the other hand, HO crack looks partly flipped relative to RBOB and 3-2-1.

As the point of this notebook is to showcase my research methodologies, despite the weak IC, we shall continue on and perform robustness checks and portfolio diagnostics.

## Bootstrap IC Confidence Intervals

Point estimates do not tell the full story, especially when the estimated ICs are this small. It does not tell us how stable that estimate is and how confident we are that the estimated values are no different from the null -- i.e. In this case, 0.

Here, we build a confidence interval around the estimates by running a block bootstrap on the 2-day terminal IC (our target variable). I resample 1,000 times using 21-trading-day blocks, so the resample still keeps some of the short-run dependence in daily crack changes. The table reports the IC and its 95% bootstrapped confidence interval.

If the interval spans zero, we should not treat the IC as meaningfully different from not having any predictive relationship. Unsurprisingly, most intervals crosses zero, consistent with the earlier results.

## Rolling Information Coefficients

A full (in-) sample IC can hide where the signals may/may not have actually worked. We plot rolling ICs to see whether the relationship is broad-based or concentrated in one market.

Using a 126-day rolling window, roughly six months, makes this easier to see. Mean reversion appears to work better in some windows, but it is not consistently positive across the full sample. The trend variants also spend a fair amount of time below zero, which are all consistent with the earlier full-sample IC results. This suggests that any signal effect could be regime-dependent or event-dependent, not a smooth relationship that holds throughout the sample.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-07.png" | relative_url }}" alt="Crack Spread Signal Research figure 7">
  <figcaption>Figure 7. Exported directly from the notebook output.</figcaption>
</figure>

## Sensitivity Analysis

We perform a narrow parameter sweep around the chosen parameters (lookback windows and skip days) to identify if the results depends too much on one specific window.

An IC that flips signs with a small tweak in parameter is probably not robust in the first place. However, if the magnitude and sign holds across a small neighborhood around the chosen parameters, we can treat the chosen parameters as stable and that it is not just a lucky set of parameters to test well.

Each signal has been tested over a small grid, then aggregated to produce the heatmap below:

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-08.png" | relative_url }}" alt="Crack Spread Signal Research figure 8">
  <figcaption>Figure 8. Exported directly from the notebook output.</figcaption>
</figure>

The sensitivity results looks "stable" across the parameters tested. There are parameter choices that do flip signs, but the values are generally very small. That is another evidence that shows that these signal families do not have much predictive power **in this setup**.

## Multiple Testing Correction

A common pitfall in signal research is to test a wide range of parameters, find one specification that looks good, and then treat that result as if it were the original hypothesis. That is not a fair read and that was indeed one of the first mistakes I made when I started my career (I did not know better).

When testing multiple parameters, the likelihood of identifying a set that perform well increases with the number of parameter set used. For a signal that is pure random noise, there is a 5% chance of rejecting the null hypothesis that there is no predictive power. For 2 independent signals that is pure random noise, there is about 9.5% chance of rejecting the null hypothesis ($1 - 0.95^2$).

Therefore, it is always good practice to keep track of the full set of parameters tested. For this notebook, the sensitivity grid is the local hypothesis family. It tests 4 signals across 3 spreads with 3-9 parameter variations each. That gives 72 spread-level specification tests.

I therefore apply two multiple-testing corrections:

1. Benjamini-Hochberg (BH), which controls the false discovery rate. This is the more relevant correction here because the tests are related and the signals are generally correlated.
2. Bonferroni, which controls the family-wise error rate. This is stricter and we include it in as a reference bar.

The p-values come from the Newey-West HAC t-statistics in the sensitivity grid, treated as approximately normal.

Even before applying multiple-testing correction, only a small number of 3-2-1 crack mean-reversion specifications were significant. So it is unsurprising that after applying BH and Bonferroni correction, there are still no rejections (rejection = significant results).

---

# Regime Analysis (In-Sample)

I test three regime families:

1. The crack spread's own realised-volatility regime. This is the main one and the only regime used for switching later.
2. The CL NB1/NB2 curve regime. This is a broader crude-market state variable (Contango vs Backwardation)
3. A trading-date seasonal split. This checks whether summer versus winter market conditions matter.

The rolling ICs showed that signal behaviour fluctuates  across time. That naturally raises the next question: is the performance being split by market regime? In this section, we'll check whether the signals behave differently across volatility regimes, crude term-structure regimes, and seasonal conditions.

I treat the volatility split as the main candidate because it maps most directly to the stress versus normal signal design. The crude-curve and seasonal splits are descriptive diagnostics.

## Crack Volatility Regimes

This is the most important regime split in the notebook. My expectations is that stress signals should look better when the crack's own realised volatility is high, while normal signals should look better outside high-volatility periods.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-09.png" | relative_url }}" alt="Crack Spread Signal Research figure 9">
  <figcaption>Figure 9. Exported directly from the notebook output.</figcaption>
</figure>

The volatility-regime result is mixed. I expected stress-trend signals to look better in high-volatility periods, but the results point more toward mean reversion. That weakens the original stress-trend hypothesis.

## CL Curve Regimes

Backwardation, flat structure, and contango can all say something about crude inventory pressure and the wider oil complex. It would also be useful to understand if the crude term structure also helps explain product crack behavior.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-10.png" | relative_url }}" alt="Crack Spread Signal Research figure 10">
  <figcaption>Figure 10. Exported directly from the notebook output.</figcaption>
</figure>

The crude-curve result is mixed. This just suggests the front crude curve is not the main conditioning variable for these daily crack returns.

## Seasonal Condition Regimes

The seasonal split is motivated by product-market structure, especially gasoline's summer and winter grade switch.

For this regime study, the bucket is based on trading month, not the contract specification. If seasonality matters for the predictive relationship, I would expect at least some difference between summer and winter-season results.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-11.png" | relative_url }}" alt="Crack Spread Signal Research figure 11">
  <figcaption>Figure 11. Exported directly from the notebook output.</figcaption>
</figure>

The seasonal result is also not clean.

## Regime IC Delta Summary

The summary below reports regime IC, Newey-West t-statistic, and IC delta versus the full-sample baseline, averaged across the three spreads.

---

# In-Sample Backtest Results

I start with standalone sign-based backtests, then move to portfolio-level constructions.

Positions are long one unit when the signal is positive and short one unit when the signal is negative.

Costs have two parts. Normal trading cost is charged when the target position changes, using a \\$0.03 per-contract one-way assumption whereas Roll cost is charged when the contract rolls, which based on our configuration, happens around the 15th or 16th of the month. I treat the roll as closing the old contract and opening the new one, so the roll-date cost is \\$0.06 per active unit.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-12.png" | relative_url }}" alt="Crack Spread Signal Research figure 12">
  <figcaption>Figure 12. Exported directly from the notebook output.</figcaption>
</figure>

The clearest positive standalone result is RBOB stress mean reversion, with a Sharpe of 1.075. 3-2-1 mean reversion remains positive but modest, while most trend variants stay negative. HO does not contribute a clean positive result.

## Equal-Weighted Portfolios

At the portfolio level, I first build two simple benchmarks:

1. An equal-weighted portfolio of the normal-condition signals.
2. An equal-weighted portfolio of the stress-condition signals.

Each active spread-signal leg receives the same weight. Positions are updated when the underlying signal changes and roll costs are charged on the dates where the structured spread contract changes.

This would then act as a baseline for comparison before adding volatility-switching rules. If the switching rule is unable to beat the equal-weighted portfolios, then the added regime layer may not be worth the effort.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-13.png" | relative_url }}" alt="Crack Spread Signal Research figure 13">
  <figcaption>Figure 13. Exported directly from the notebook output.</figcaption>
</figure>

The family baselines are negative after roll costs. Normal-only has a Sharpe of -0.441 and stress-only has a Sharpe of -0.290. Stress-only has a shallower max drawdown, -11.671 versus -17.989 for normal-only, but neither family is attractive on its own.

## Volatility-Switching Portfolio

I now add the switching overlay. The rule is intentionally simple:

1. If the crack is in a high-volatility regime, activate the two stress signals.
2. Otherwise, activate the two normal signals.

The regime is dependent on the crack's own volatility and does not depend on crude spreads or other products.

Positions update as the active regime and signal signs change.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-14.png" | relative_url }}" alt="Crack Spread Signal Research figure 14">
  <figcaption>Figure 14. Exported directly from the notebook output.</figcaption>
</figure>

The switching overlay improves the IS portfolio relative to the two family baselines -- it is marginally better than stress-only signal by the end of the backtest. Similar to the other portfolios, the vol-switching ended with negative pnl post-cost, with a Sharpe of -0.052. Its max drawdown is -10.468, which is shallower than the normal-only portfolio and slightly better than stress-only.

## Signal-Strength and Threshold Sizing

I now test an alternative execution model with two changes:

1. Trend signals use clipped volatility-scaled magnitude:

$$
\text{position}^{trend}_t = \frac{\text{clip}(S^{trend}_t, -3, 3)}{3}
$$

2. Mean-reversion signals use percentile-rank distance from neutral:

$$
\text{position}^{mr}_t = -2 \times (Rank_t(L) - 0.5)
$$

I also add a simple threshold version where positions only updates when the target position changes by at least 0.10. Roll costs are applied to any active residual position (proportionately) on roll dates, so lower turnover does not eliminate the monthly roll drag, but a lower cost is applied when the positions are sized less than 1.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-15.png" | relative_url }}" alt="Crack Spread Signal Research figure 15">
  <figcaption>Figure 15. Exported directly from the notebook output.</figcaption>
</figure>

The sizing rules do not improve the benchmark in this run. The sign-based switching portfolio has a Sharpe of -0.052 after roll costs while the scaled daily version falls to -0.692 and the threshold-scaled version has a negative Sharpe of -0.372.

This is slightly unexpected as I would have expected the daily scaled position to avoid periods where signals are weak, i.e. expected returns are low, or volatility is too high. The poor performance of the daily scaled version may therefore be partly due to higher turnover and cost drag overwhelming whatever benefit the scaling rule provides.

---

# Out-of-Sample Validation

Let's now proceed to perform a short study on the out-of-sample data (from 2022-01-01 to 2026-02-17). The parameters are fixed upfront and not re-estimated.

The OOS period includes several unusual shocks in the market, such as the 2022 Russia-Ukraine war, 2025 Trump inauguration, etc. It is not a quiet period and for signal research that survived up to this point, this could be a useful stress test.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/crack-spread-signal-research/figure-16.png" | relative_url }}" alt="Crack Spread Signal Research figure 16">
  <figcaption>Figure 16. Exported directly from the notebook output.</figcaption>
</figure>

The signal-level OOS table remains mixed, consistent with earlier IS analysis.

At the portfolio level, the vol-switching strategy improves from an IS Sharpe of -0.052 to an OOS Sharpe of 0.313 after roll costs. That is better out of sample than in sample, but the OOS t-stat is only 0.615 and the max drawdown is larger at -14.688. A large part of positive pnl comes from the 2022 Russian-Ukraine war. For the remaining periods beyond that, the pnl has largely been moving sideways.

The evidence here is that these signals are insufficient to be treated as standalone trading strategies.

# Areas of Improvement

- Lack of physical-market information. We could pull in EIA weekly status report data from DOE to better inform our research. Current regimes are price derived and may not properly encapsulate regional fundamentals.

- The OOS result is also event-sensitive. The positive OOS portfolio result is helped by the 2022 energy shock.

- Period of study includes multiple unusual periods, such as COVID, Russia-Ukraine war, etc
