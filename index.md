---
title: "Thư viện truyện của tôi"
layout: "base.njk"
---
# Danh sách truyện

<ul>
{% for story in collections.storyList %}
    <li>
        <a href="{{ collections[story] | first | url }}">{{ story }}</a>
    </li>
{% endfor %}
</ul>
