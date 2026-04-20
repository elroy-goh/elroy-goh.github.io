---
title: "Methods & Standards"
permalink: /methods/
layout: page
---


Good quantitative research depends on rigor more than cleverness. The principles below guide my work and help prevent false discoveries. They reflect well-documented failure modes in quantitative finance: backtest overfitting, look-ahead bias, Sharpe inflation, and underestimated transaction costs. Stating and adhering to these standards is a key differentiator between professional research and hobby backtesting.

## Data Leakage Controls

All experiments are designed to prevent label leakage and look-ahead bias:

- **Purged and embargoed cross-validation** — cross-validation folds are purged to remove samples whose labels overlap the test period, and an embargo period is applied after each split to prevent information bleed.
- **Chronological timestamp alignment** — when merging data from multiple feeds, timestamps are aligned strictly to avoid inadvertent forward-filling of future values.
- **Strict out-of-sample separation** — walk-forward testing is preferred over random splits; the out-of-sample window is defined before any modelling begins and never revisited.

## Multiple Testing Discipline

Exploring many ideas without correction inflates the apparent hit rate. I mitigate this by:

- **Pre-registering hypotheses** — success criteria and evaluation metrics are defined before running any experiment.
- **Family-wise error control** — when testing multiple signals simultaneously, I apply Bonferroni or Benjamini–Hochberg corrections to control the false discovery rate.
- **Reporting distributions, not cherries** — results are reported across the full parameter grid or signal universe, not only for the best-performing configuration.

## Cost & Risk Modelling

Gross returns are meaningless without costs. Every backtest includes:

- **Transaction cost models** accounting for commissions, bid-ask spreads, and slippage proportional to trade size and market impact.
- **Turnover constraints** to keep capacity and market impact realistic.
- **Risk metrics** — volatility, maximum drawdown, and factor exposure — to understand the source of returns and identify when they might fail.

## Conservative Evaluation

- **Sharpe ratio estimation** adjusts for serial dependence and return non-normality. The standard iid assumption overstates statistical significance; I apply autocorrelation corrections before drawing inference.
- **Robustness analysis** examines parameter sensitivity, sub-period stability, and performance across market regimes.
- **Failure case documentation** is a required section of every research memo. Acknowledging when and why a signal breaks is a credibility signal, not a weakness.

## Summary

These standards collectively guard against the four most common failure modes in quantitative research: leakage, overfitting, cost neglect, and Sharpe inflation. Every flagship memo on this site applies them explicitly and documents where they bind.
