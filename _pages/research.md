---
title: "Research"
permalink: /research/
layout: page
---


Each research memo presents my approach to quantitative signal research, with a particular emphasis on commodity futures. The focus is on practical frameworks and methodologies developed through hands-on experience in energy markets such as Brent crude, WTI crude, Dubai crude, RBOB gasoline, and Singapore 92 motor gasoline. While my background is rooted in energy, my research interests extend to systematic strategies across multiple asset classes. For more on my experience, see [my CV](/cv).

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
</div>

---

All analytical frameworks, interpretations, and conclusions in these notebooks are my own.
