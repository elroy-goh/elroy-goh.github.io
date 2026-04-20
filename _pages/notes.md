---
title: "Notes"
permalink: /notes/
layout: page
---

Short-form commentary on market structure, trading practice, research engineering, and tooling.

---

<div class="qr-card-grid">
  {% assign notes_sorted = site.notes | sort: "date" | reverse %}
  {% for note in notes_sorted %}
    <a class="qr-card qr-card--link" href="{{ note.url | relative_url }}">
      <h3>{{ note.title }}</h3>
      <p class="qr-card__tags">{{ note.note_category }}{% if note.tags %} · {{ note.tags | join: " · " }}{% endif %}</p>
      <p>{{ note.summary }}</p>
    </a>
  {% endfor %}
</div>

---
