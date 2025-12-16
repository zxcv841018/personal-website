---
layout: default
title: 親子景點列表
permalink: /attractions/
---

<div class="attractions-intro">
  <h1 class="h1 mb-2">親子景點列表</h1>
  <p class="text-gray">點選卡片即可瀏覽每個景點的獨立介紹與照片。</p>
</div>

{% assign attractions = site.data.attractions | sort: 'name' %}
<div class="attraction-grid">
  {% for attraction in attractions %}
    <a class="attraction-card" href="{{ site.baseurl }}/attractions/{{ attraction.slug }}/">
      <div class="attraction-card-image">
        {% if attraction.image_url %}
          <img src="{{ attraction.image_url }}" alt="{{ attraction.name }} 圖片" loading="lazy">
        {% else %}
          <div class="attraction-card-placeholder">暫無圖片</div>
        {% endif %}
      </div>
      <div class="attraction-card-body">
        <div class="d-flex flex-items-center mb-1">
          <h2 class="h4 flex-auto mb-0">{{ attraction.name }}</h2>
          {% if attraction.rating %}<span class="label label-green ml-2">⭐ {{ attraction.rating }}</span>{% endif %}
        </div>
        <p class="text-gray mb-1">{{ attraction.category }} · {{ attraction.address }}</p>
        <p class="text-gray f6">{{ attraction.status }} {% if attraction.hours %}<span class="text-gray">{{ attraction.hours }}</span>{% endif %}</p>
      </div>
    </a>
  {% endfor %}
</div>
