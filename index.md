---
layout: home
title: 親子景點地圖
---

歡迎來到親子景點小站！這裡集結多個適合帶孩子出遊的地點，提供交通方式、開放時間與貼心提醒。

<section class="attraction-grid">
  {% for attraction in site.attractions %}
  <article class="card">
    <h2><a href="{{ attraction.url | relative_url }}">{{ attraction.title }}</a></h2>
    <p class="meta">{{ attraction.city }} · {{ attraction.age_range }}</p>
    <p>{{ attraction.excerpt | strip_html | truncate: 100 }}</p>
    <div class="tags">
      {% for tag in attraction.tags %}
      <span class="tag">{{ tag }}</span>
      {% endfor %}
    </div>
  </article>
  {% endfor %}
</section>
