---
title: "Research Engineering"
permalink: /engineering/
layout: page
---


Quantitative research is more than models and statistics — it requires solid engineering. This page outlines the modular tooling I use to build reproducible pipelines, from raw data through to deployable strategies.

## Pipeline Architecture

The diagram below shows the high-level data flow. Each stage is a standalone module with a clean interface, making it straightforward to swap data sources, model classes, or portfolio solvers without touching downstream code.

<div class="qr-pipeline">
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Raw Data</span>
    <span class="qr-pipeline__desc">Public + vendor feeds</span>
  </div>
  <div class="qr-pipeline__arrow">→</div>
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Validation</span>
    <span class="qr-pipeline__desc">Missingness · outliers · alignment</span>
  </div>
  <div class="qr-pipeline__arrow">→</div>
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Features</span>
    <span class="qr-pipeline__desc">Time-series · cross-section · microstructure</span>
  </div>
  <div class="qr-pipeline__arrow">→</div>
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Models</span>
    <span class="qr-pipeline__desc">Regression · ML · factor models</span>
  </div>
  <div class="qr-pipeline__arrow">→</div>
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Backtest</span>
    <span class="qr-pipeline__desc">Walk-forward · purged CV · cost model</span>
  </div>
  <div class="qr-pipeline__arrow">→</div>
  <div class="qr-pipeline__stage">
    <span class="qr-pipeline__label">Portfolio</span>
    <span class="qr-pipeline__desc">Weights · constraints · risk budget</span>
  </div>
</div>

## Pipeline Components

**Data ingestion** — Adapters for public and vendor sources, handling API rate limits, retries, and audit logs. Public datasets work out of the box; vendor adapters are stubbed with clean interfaces ready for credentials.

**Data validation** — Automatic checks for missingness, outlier ticks, timestamp misalignment, and unit consistency. Validation runs before any feature computation, so bad data never silently corrupts downstream results.

**Feature engineering** — Modular functions computing time-series, cross-sectional, and microstructure features. All feature code lives in a feature store that can be imported by any model or experiment script without duplication.

**Model & backtesting** — Walk-forward and purged k-fold runners with configurable embargo periods. Supports parametric models, ML algorithms, and custom cost models. In-sample and out-of-sample results are logged separately.

**Portfolio construction** — Signal-to-weight routines with turnover limits, leverage caps, and risk-budget constraints. Includes mean-variance and risk-parity variants plus sensitivity analyses over key parameters.

## Reproducibility & Testing

All components are written in Python, packaged with versioned dependencies, and tested using `pytest`. A `Makefile` in each project repository provides a three-command interface:

```bash
make setup   # create virtualenv and install pinned dependencies
make test    # run unit tests and integration tests
make run     # execute the default experiment or backtest
```

Every experiment uses a fixed random seed and a versioned environment file. Long-running jobs log metrics and artefacts to disk so results are auditable after the fact.

## Repository

A companion open-source repository will be linked here once published. It will contain the actual code for data ingestion, feature computation, backtesting, and portfolio optimisation — fully runnable on a fresh machine.

*Repository link coming soon.*
