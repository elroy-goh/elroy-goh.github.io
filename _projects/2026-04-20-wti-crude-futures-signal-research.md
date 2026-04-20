---
layout: page
title: "WTI Crude Futures Signal Research"
date: 2026-04-20
description: >
  Research memo covering exploratory analysis, signal diagnostics, regime tests, and backtest results for WTI crude futures.
project_tags: "Commodity futures · WTI crude · Signal research · Backtesting"
summary: "A notebook-driven commodity futures memo focused on WTI signal research, including EDA, predictive diagnostics, regime conditioning, and simplified backtest analysis."
notebook_source: "/WTI Crude Futures Signal Research.ipynb"
asset_dir: "/assets/img/projects/wti-crude-futures-signal-research"
---

<div class="qr-memo-meta">
  <p class="qr-memo-meta__eyebrow">Research Memo</p>
  <p>A notebook-driven commodity futures memo focused on WTI signal research, including EDA, predictive diagnostics, regime conditioning, and simplified backtest analysis.</p>
  <div class="qr-memo-meta__actions">
    <a class="qr-btn qr-btn--primary" href="/notebooks/WTI%20Crude%20Futures%20Signal%20Research.zip">Download Notebook</a>
  </div>
</div>

# Background

This notebook presents my approach to quantitative signal research, with an emphasis on commodity futures. The focus here is on a basic but practical framework for futures signal research. My background is primarily in energy markets, including Brent crude, WTI crude, Dubai crude, RBOB gasoline, and Singapore 92 motor gasoline. My experience across these markets has covered strategy research, execution, and discretionary trading.

Although my practical experience has been concentrated in energy futures, my research interests are broader and include systematic work across multiple asset classes.

Further details on my background and experiences can be found in [my CV](/cv).

**Disclaimer**
-

The use of AI tools have been involved in writing up this notebook. Though to be clear, all core ideas and methodologies were from me, with knowledge synthesised from reading various books related to quantitative investing and from my college studies. ChatGPT / Claude were involved in coding and understanding some topics in more depth. Where AI tools were used, the generated outputs were checked through thoroughly.

In other words, all analytical frameworks and conclusions are my own. Notwithstanding the above, I am proficient in Python programming, with more than 8 years of working experience using Python.

---

# Introduction

---

This notebook develops a time-series signal research framework for commodity futures. This is unlike the Barra or Axioma-styled factor models where we perform a cross-sectional regression on each date (Similar styled workings as you would have read in Grinold and Kahn's (1999) foundational book on Active Portfolio Management, Qian et al (2007)  Quantitative Portfolio Management and many other equity research focused books).

Some pre-amble just so we are aligned on this: The reason we deviate from that is because cross sectionally, there isn't as many "assets" within the commodity space available to cleanly tease out factor returns. To make matters worse, the behavior and contract availability across commodities differ, i.e. energy futures behaves differently from agriculture futures and fixed income futures. It's (relatively) easy to trade along the curve of crude oil futures, as the front tenors (up to about 6mths out) are relatively well traded. In contrast, cocoa, coffee, soybean, etc, are generally liquid only at the front active contract. Anything beyond gets active only when the front month contract is approaching expiration and positions get rolled to the deferred month.

In this notebook, we shall only work on time-series models for each of the following "signals":

1) Carry

2) Long-term trend

3) Short-term mean reversion


We'll perform this analysis in the following order:
- Exploratory data analysis
- Signal definition and analysis
    - Signal validation: Calculate IC and it's statistics
    - Signal decay v horizon: Plot IC across multiple holding horizons
    - Study signal robustness: Study signal stability across regimes
- Backtest signals
- Orthogonalise signals to understand P&L contribution of a signal to existing pool of signals

Before we proceed, a quick note on the research direction.

## Research Statement

We model the outright returns of the 2nd WTI futures contract (NB2) as the target variable. Carry, trend, and mean reversion are used as the candidate signals. The objective is to evaluate whether these signals contain predictive information for subsequent returns, how that predictive strength evolves across horizons, and whether each signal contributes distinct value within a broader research framework.

We perform our analysis and backtests on settlement prices. Any signals generated at time $T$, will be executed at time $T+1$

Prices, returns, etc are all calculated on raw absolute returns basis. The reason for this choice is that in energy markets, strategies are often built around spreads, e.g. Crack Spreads, Calendar Spreads, etc. Using percentage returns on prices that could be near or below 0 does not make economic sense. The interpretation and handling of returns at that point would then be a little problematic. To simplify things, using raw absolute returns would be more than sufficient.

---

# Exploratory Data Analysis - Raw Data

---

Reason we're taking NB2 is because carry/roll yield is one of our "signals", so the expected move is on the deferred month contract. Here we'll perform some analysis on the data just to get a sense of how the return structure has been like.

## Price and Histogram of Returns

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-01.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 1">
  <figcaption>Figure 1. Exported directly from the notebook output.</figcaption>
</figure>

## Returns by Pre & Post-Covid

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-02.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 2">
  <figcaption>Figure 2. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-03.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 3">
  <figcaption>Figure 3. Exported directly from the notebook output.</figcaption>
</figure>

## ACF and PACF Plots
We'll try to identify if there are traits of AR/MA characteristics. If there are, we can also build an ARIMA model out of it.

### ACF and PACF Plots of Daily Returns

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-04.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 4">
  <figcaption>Figure 4. Exported directly from the notebook output.</figcaption>
</figure>

Returns on NB2 contract does not seem to display any distinct AR/MA traits. At least that does not seem to be the case. We shall group them by contract, just to have an understanding if contract month displays seasonal effects.

### ACF and PACF Plots of Returns by Contract

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-05.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 5">
  <figcaption>Figure 5. Exported directly from the notebook output.</figcaption>
</figure>

Expected to see spike in PACF at 12th lag, but does not seem to be significant either. Maybe, just maybe, this isn't the right way to represent or reflect such a characteristic.

## Commentary on EDA

Full range:
Returns of 2nd-month WTI contract is slightly left-skewed (skew: -0.72). However, it has significantly fatter tails with kurtosis of 5.99.

However, as market regimes might have changed pre and post-covid, we shall take a look at the return distributions separately.

Segregated view:
Skewness pre-covid seems to be near 0, whereas post-covid skewness was at -0.76. This however, does not constitute a very significant left skew. It is apparent, though, that the tails has gotten fatter post-covid as shown by the Q-Q Plot. This, however, does not corroborate with the kurtosis calculated in the chart titles. (See explanation below, it's mainly due to normalisation method)

Both ACF and PACF for daily and contract returns does not seem to be significant. That does not preclude the fact that seasonality effects may be present in structured spreads though.

### Kurtosis Paradox Explained (Credits to Claude)

Kurtosis is a standardised moment: μ₄/σ⁴. Post-COVID realised volatility is materially higher, so even if absolute tail moves are larger, normalising by a larger σ⁴ can reduce or flatten the kurtosis metric. The Q-Q plots visualise absolute deviations from normality; kurtosis measures normalised ones. The table below compares absolute vs z-scored tail behaviour to make this explicit.

Additionally, the pre-COVID sample (2017–2019, ~2.5 years) includes the end-2018 crude selloff (WTI fell ~$40 in ~3 months) in a relatively low-vol environment, which produces a high normalised kurtosis. The post-COVID sample (2020–present) is longer and absorbs multiple stress events, so the tail events are large in absolute terms but not as extreme relative to the elevated σ.

---

# Signal

---

## Signal Definition

**Carry**
- Carry or Roll Yield. Idea: during backwardation (positive spread), when the front-month contract expires, the deferred leg would roll up. Reason being that the contracts are intrinsically linked to the same underlying product.
$$F_0 = S_0 e^{(r+s-c)T}$$
- As expiration draws closer, T -> 0, prices would converge towards spot prices.
- That's the high level reasoning, however, in energy markets there are more nuances to it. There could be dislocation between spot and futures prices due to issues such as market stress, storage constraints, etc.
- We formulate the signal as: $$\frac{(F_{1,t} - F_{2,t})}{\sigma_{rolling}}$$

**Long-term trend**
- As with the paper by Jegadeesh and Titman (1993) on momentum, we posit that assets that have been trending up tend to keep outperforming.
- Though, to be clear, their paper was on cross-sectional basis.
- We ignore the recent returns in case of short-term reversals and formulate signals as: $$\frac{F_{2,t-skip} - F_{2,t-long lookback}}{\sigma_{rolling}}$$

**Short-term mean reversion**
- As with the saying, long-term trend, short term reversal. Short-term reversals are likely an artifact of overreaction in the market which then corrects itself shortly after --> Mean reversion
- We'll go with the 2MA crossover method.
- We formulate signals as: $$-\frac{SMA(5)_{F2} - SMA(20)_{F2}}{\sigma_{rolling}}$$
- The choice of 5 and 20 is entirely arbitrary. ML practitioners may treat this as a tunable parameter, discretionary traders swear by a fixed 14/21 rule, etc. I chose 5/20 just so I can keep the required data period under a month, with no particular reason.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-06.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 6">
  <figcaption>Figure 6. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-07.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 7">
  <figcaption>Figure 7. Exported directly from the notebook output.</figcaption>
</figure>

The purpose of this plot is to understand if there are any signal drifts pre to post covid. Carry seems to have turned more positive post-covid. Which is not unexpected. At least for the earlier years, it makes sense for the energy market to be in backwardation (+ve carry/spread). The rest seems more or less align

## Signal Statistics

For a single-instrument study, we would want to know whether the signal is persistent, whether it overlaps materially with the other signals, and whether stronger signal buckets are followed by larger subsequent dollar moves over the same horizon used in the backtest. We study these in the following sections.

Signal persistence gives a clue towards turnover and cost drag, or even an insight into whether it is just a long single stale exposure instead of multiple repeatable opportunities.

Being able to identify how much a signal overlaps with other signals will allow us to understand the contribution of this signal. If we treat highly correlated signals as independent ones, we would end up being overweight on the same exposure.

Bucket monotonicity asks whether stronger signal realizations line up with stronger subsequent moves in the expected direction.

From the autocorrelation numbers, we can see that carry and trend are both very persistent. Both retained substantial 21-day correlation, though it is not unexpected, since the term structure (carry) is intricately linked to fundamentals and the S&D situations could often persist for long periods of time. Trend is calculated with a rather long lookback period, and therefore the signal is also expected to move more slowly, and has higher autocorrelation. Mean reversion is much less persistent by the 21-day horizon and has the highest sign-change rate and average position change, so it is in a sense the most expensive of the three to trade.

The correlation matrix is also useful. Carry and trend have a moderate positive correlation of 0.42, which suggests some shared directional structure, but neither is close enough to be treated as a duplicate signal. Mean reversion is weakly related to the other two, especially to trend, which is encouraging from a diversification perspective.

## Preparation of Backtest DataFrame

Predictive tests are kept in raw absolute (dollar) changes so that IC, bucket monotonicity, and directional checks stay aligned to the same unit of analysis. The predictive horizon is set to `2D`, consistent with a signal observed at $T$, executed at $T+1$. In other words, the above are evaluated against the price change in WTI from T+1 to T+2.

This makes sense in the context of this notebook because we lag our trade by a day. However, when working on this as a live trading strategy, we would seek to use intraday data and assume we could trade after a short delay after the settlement price prints.

In our backtest, we assume if the signal does not change signs, the position persists and carries over to the next period. Alternatives to this could be vol scaling, where we scale in and out of a position depending on realised/expected volatility or we could also increase/decrease holdings at discrete points of the signal, e.g. 1/2/3 z-score from 0.

We additionally assume that the one-way cost per futures traded is $0.02. This is a fair cost, seeing that we could enter and exit positions via TAS (Trade at Settlement -- 0 slippage). The 2c should be sufficient to cover exchange cost and other fees.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-08.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 8">
  <figcaption>Figure 8. Exported directly from the notebook output.</figcaption>
</figure>

For bucket monotonicity to be strong, the expectations would be for Q1 returns to be negative (assuming most signals in Q1 is negative) and progressively increase to positive by Q5.

Bucket monotonicity is weak overall. Carry and trend are not monotonic and both have negative top-minus-bottom spreads (-0.022 and -0.05 respectively), which means stronger signal magnitude is not translating cleanly into stronger subsequent returns. Mean reversion has the best top-minus-bottom spread (0.046), but the bucket profile is still noisy rather than smoothly ordered.

## Information Coefficient and Decay Profile

The point of this section is two-fold. I want:

1) Decay profile for the signal across holding horizons. 
2) Separate cumulative IC from the marginal daily move, because cumulative forward windows overlap by construction and can therefore look artificially smooth.

Spearman is the headline measure here because the bucket test is fundamentally monotonic in spirit, while Pearson is retained as a sensitivity check.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-09.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 9">
  <figcaption>Figure 9. Exported directly from the notebook output.</figcaption>
</figure>

On aggregate, information coefficients are small across the board. As recommended in Grinold and Kahn (1999), an 
IC of 0.05 is considered good and 0.10 exceptional, so these results remain weak by that standard. The IC at horizon 1 - which is shown mainly as a same-day reference case rather than the tradable implementation in this notebook - also does not show much potential.

Trend Spearman IC is negative across horizons, which suggests that the way it is currently constructed moves against the stated hypothesis. Carry is mixed but remains close to zero, so it is not providing convincing predictive evidence either.

We shall dissect the signals a little, across different regimes to understand if the signal may perform better under different circumstances.

### IC Stability

We study the stability of IC across a narrow range of parameters. The goal here is not to optimise our results, but instead, to check if the signs and magnitude of predictions are stable in the neighborhood of defined settings.

> **Note:** I would often run a check of IC on aggregate and against different regimes first, to study IC using the current parameters before looking into the IC stability. If the results does not produce anything meaningful, I would close the research as there is unlikely any more value to extract and any backtest results would be based off spurious relationship. However, I would not be performing that here as it might end up bloating this entire notebook and deviating from the original purpose.

*The cumulative-horizon IC decay is shown mainly descriptively. If one were to attach t-stats to those cumulative windows, overlap would need to be handled because the forward windows share observations. That concern does not apply in the same way to the single-day realised-change tests used elsewhere in the notebook.*

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-10.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 10">
  <figcaption>Figure 10. Exported directly from the notebook output.</figcaption>
</figure>

## IC By Regimes

### Across Contango / Flat / Backwardation Regimes

Term structure for energy futures is arguably one of the most economically relevant regime split. Something I learned from my past experience is that when the term structure flips from contango to backwardation or vice versa, that flip can be very abrupt. Therefore, being near a spread of 0 could potentially be informative of subsequent move. However, we shall not study this in depth in this notebook as the main purpose of this isn't to be exhaustive in our search for potential signals, but rather, display research competencies and methodologies.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-11.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 11">
  <figcaption>Figure 11. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-12.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 12">
  <figcaption>Figure 12. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-13.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 13">
  <figcaption>Figure 13. Exported directly from the notebook output.</figcaption>
</figure>

Conditioning on term structure, carry's interpretation makes it somewhat different from others, in the sense that a positive carry is essentially backwardation (term structure) and negative reflects contango. So the signal and the regime is essentially one and the same. 

Carry does not behave as originally hypothesised. If the construction were working cleanly, I would expect IC to be positive. Instead, IC is negative in backwardation and near flat in contango, even though P&L is positive in backwardation and strongest when the curve is flat. I would therefore not read this as a clean ordinal relationship, nor as an especially reliable standalone P&L.

Trend is only mildly constructive in backwardation and clearly poor in contango. Mean reversion is weak overall.

So the main takeaway from this section is not that any signal is strong, but that market structure does appear to matter for how weak signals behave.

### Across Volatility Regimes

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-14.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 14">
  <figcaption>Figure 14. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-15.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 15">
  <figcaption>Figure 15. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-16.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 16">
  <figcaption>Figure 16. Exported directly from the notebook output.</figcaption>
</figure>

Conditioning on realised volatility, the split is cleaner, but still signal-specific rather than broadly supportive.

Carry is economically best in normal volatility, while both high- and low-volatility regimes are weaker. Since ICs remain close to zero in all three buckets and t-stats are low, I would not read this as stronger predictive strength, especially with the low t-stats. Though, given the idea behind carry, it does seem perfectly logical to get this results. With the absence of stochasticity, we expect deferred futures to roll up in backwardation and roll down in contango. With added noise, the performance would be less "predictable".

Trend is roughly flat in high and normal volatility, but clearly poor in low volatility. Mean reversion shows the opposite pattern, doing best in low volatility and losing money in normal volatility.

So this section does not support a simple statement that higher volatility is uniformly good or bad. Instead, it suggests that carry prefers calmer but still active markets, trend is unreliable in quiet markets, and mean reversion benefits most when realised volatility is subdued.

### Across Pre/Post Covid Regimes

I treat the Covid split as a stress-period robustness check rather than the main regime framework. It is still useful to know whether the signal only works because of one unusual sub-period.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-17.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 17">
  <figcaption>Figure 17. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-18.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 18">
  <figcaption>Figure 18. Exported directly from the notebook output.</figcaption>
</figure>

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-19.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 19">
  <figcaption>Figure 19. Exported directly from the notebook output.</figcaption>
</figure>

Conditioning on the pre/post-Covid split, I would treat this mostly as a robustness check rather than a primary regime framework. The sample imbalance is large, so I would not place much weight on small pre-Covid differences.

Carry monetises modestly in both periods, but IC is more negative pre-Covid and only slightly negative post-Covid, so this still does not support the original monotonic signal hypothesis. With weak IC and weak t-stats, I would not treat the observed P&L as especially reliable either.

Trend is close to flat post-Covid but materially worse pre-Covid, where the realised P&L is clearly negative. Mean reversion also looks poor pre-Covid and only mildly positive post-Covid. Overall, this split is less informative than term structure or realised volatility.

### Commentary on IC by Regimes

Across all three regime cuts, the main conclusion does not change: ICs remain small and t-stats are weak, so I would not treat these as statistically convincing signals. Regime conditioning is therefore more useful here as a diagnostic than as evidence of predictive strength.

Term structure is the most informative split. Backwardation is the least bad environment for carry and trend, while contango is clearly poor for trend. Mean reversion behaves differently from the other two and holds up somewhat better in contango.

Volatility gives a different kind of separation. Carry works best when volatility is normal, which is economically plausible, but the ICs remain too weak to call this strong evidence. Trend remains weak, especially in low volatility, while mean reversion appears to do best when volatility is subdued.

Overall, regime analysis helps explain signal behaviour, but not enough to claim robust predictive power, at least not in this notebook.

---

# Backtest Results

---

For simplicity, we'll just assume that we go long when the signal is positive and short when it is negative. This is an extreme simplification, but there are too many alternatives to carrying this out to contain in this notebook. These will be covered in potential areas of improvements in section 7 below.

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-20.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 20">
  <figcaption>Figure 20. Exported directly from the notebook output.</figcaption>
</figure>

Standalone backtest results are fairly clear in this run. Carry is the only signal that is positive on its own, but even there the Sharpe is only 0.311. Trend and mean reversion are both negative, with mean reversion showing the largest turnover and by far the deepest drawdown.

## Orthogonalisation of Signals

So far, all signals have been studied on a standalone basis. The next question I would naturally ask is what is the information contribution of each signal and how do I account for P&L attribution.

Here, we perform a sequential orthogonalisation of the signals as covered in Qian et al (2007). I keep the signal order as carry, trend, then mean reversion. Carry therefore acts as the anchor signal.

### P&L Contribution per Signal

<figure class="qr-figure">
  <img src="{{ "/assets/img/projects/wti-crude-futures-signal-research/figure-21.png" | relative_url }}" alt="WTI Crude Futures Signal Research figure 21">
  <figcaption>Figure 21. Exported directly from the notebook output.</figcaption>
</figure>

Under this sequential orthogonalisation, only mean reversion appears to retain a somewhat cleaner residual component. Being the anchor signal, carry is largely unchanged, while trend deteriorates.

Mean reversion improves visibly. Its orthogonal IC increases relative to the raw signal, and orthogonal Sharpe turns positive, while its full-sample $R^2$ is also the lowest of the three. That is at least consistent with mean reversion sharing less common variation with carry and trend than they share with one another.

Even so, I would keep the interpretation restrained. The orthogonal t-stats remain weak, and the overall signal remains far from compelling.

---

# Areas of Improvements

---

1) Single instrument research that may be too narrowly scoped and potentially do not generalise well to other instruments

2) As of yet, roll costs are not taken into consideration. Though, in my opinion, costs could be argued to be secondary as when we construct a portfolio, we could pool multiple weak signals together and tune the optimisation engine to take a position or fulfill the turnover only if the expected returns exceeds the cost amortised.

3) Hold-out set should have been used, where we train and validate on a training and validation set. Thereafter, when we have completed our analysis we could run a simulation on the test set to study out-of-sample / walk-forward performance

4) Multiple testing adjustments. Since these signals have been widely studied and we implemented a parameter sweep, we should adjust our analysis to account for multiple testing.

5) Backtesting could be done on a volatility-scaled basis or entry and exit conditions could be implemented based on some discrete levels, e.g. 1/2/3 z-scores. Currently, what we do is trade based on signal signs.

6) Backtests is not cost-aware, in the sense that it does not prevent trading even when expected returns do not cover cost.
