---
title: "Research"
permalink: /research/
layout: page
---


Each memo follows a full research lifecycle: hypothesis, data selection, methodology, validation design, results, robustness checks, failure analysis, and implementation notes. Click through for the full writeup.

---

<div class="qr-card-grid">
  {% assign projects_sorted = site.projects | sort: "date" | reverse %}
  {% for project in projects_sorted %}
    <a class="qr-card qr-card--link" href="{{ project.url | relative_url }}">
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

  <div class="qr-card">
    <h3>Crack Spread Signal Research (WIP)</h3>
    <p class="qr-card__tags">Energy futures · Crack spreads · Work in progress</p>
    <p>An upcoming research notebook studying crack spread signals, their construction, and whether they carry useful predictive information once costs and implementation constraints are accounted for.</p>
  </div>

  <div class="qr-card">
    <h3>Cross-Asset Futures Microstructure &amp; Roll Characteristics (WIP)</h3>
    <p class="qr-card__tags">Agri · Metals · Fixed income · Energy · Work in progress</p>
    <p>An upcoming notebook on bid/ask spreads across products and times of day, with an additional section on liquidity across tenors and what that reveals about roll behaviour in each asset class.</p>
  </div>
</div>

---

