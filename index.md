---
layout: page
title: ""
permalink: "/"
---

<section class="qr-hero">
  <div class="qr-hero__layout">
    <div class="qr-hero__body">
      <h1 class="qr-hero__headline">Quantitative Research</h1>
      <p class="qr-hero__sub">Systematic cross-asset · commodities microstructure · research engineering</p>
      <p class="qr-hero__pitch">
        Reproducible signal research and portfolio construction pipelines, validated with
        leakage controls, cost modeling, and regime analysis.
      </p>
      <ul class="qr-hero__bullets">
        <li>Commodities trading, execution, and intraday data</li>
        <li>Python research tools and robust pipelines</li>
        <li>Expanding portfolio of systematic research</li>
      </ul>
      <p class="qr-hero__cta">
        <a class="qr-btn qr-btn--primary" href="/cv/">View CV</a>
        <a class="qr-btn qr-btn--secondary" href="/assets/pdf/cv.pdf">Download CV</a>
      </p>
      <p class="qr-hero__links">
        <!-- <a href="https://github.com/elroy-goh" target="_blank" rel="noopener">GitHub</a> · -->
        <a href="https://www.linkedin.com/in/gjgoh/" target="_blank" rel="noopener">LinkedIn</a> ·
        <a href="mailto:elroy.ggj@gmail.com">Email</a>
      </p>
    </div>
    <div class="qr-hero__media">
      <div class="qr-hero__headshot-wrap">
        <img class="qr-hero__headshot" src="/assets/img/headshot.png" alt="Elroy Goh headshot">
      </div>
    </div>
  </div>
</section>

## Experience Snapshot

- **Commodity trading &amp; risk analysis** — hands-on exposure to oil and agricultural markets, execution workflows, and hedging mechanics
- **Quantitative research engineering** — data pipelines, feature stores, and backtest harnesses in Python
- **Risk management &amp; microstructure** — intraday execution and slippage modelling

---

## Current Focus

This site is in the midst of expanding. Additional portfolio materials are being prepared for publication.

---

## Research Memos

<div class="qr-card-rail" aria-label="Research memos and upcoming topics">
  {% assign projects_preview = site.projects | sort: "date" | reverse %}
  {% for project in projects_preview limit:3 %}
    <a class="qr-card qr-card--link qr-card--rail" href="{{ project.url | relative_url }}">
      <h3>{{ project.title }}</h3>
      {% if project.project_tags %}
      <p class="qr-card__tags">{{ project.project_tags }}</p>
      {% endif %}
      {% if project.summary %}
      <p>{{ project.summary }}</p>
      {% elsif project.description %}
      <p>{{ project.description }}</p>
      {% endif %}
    </a>
  {% endfor %}
</div>

<p><a class="qr-btn qr-btn--secondary" href="/research/">Browse all research →</a></p>

---

## From the Notes Section

<div class="qr-card-grid">
  {% assign notes_preview = site.notes | sort: "date" | reverse %}
  {% for note in notes_preview limit:3 %}
    <a class="qr-card qr-card--link" href="{{ note.url | relative_url }}">
      <h3>{{ note.title }}</h3>
      <p class="qr-card__tags">{{ note.note_category }}</p>
      <p>{{ note.summary }}</p>
    </a>
  {% endfor %}
</div>

<p><a class="qr-btn qr-btn--secondary" href="/notes/">Browse all notes →</a></p>
