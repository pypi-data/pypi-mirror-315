# Django Meta OG


HTML Meta tags [OpenGraph](https://ogp.me/) for [Django](https://www.djangoproject.com/).
The project uses the project [DjangoCMS Meta OG](https://gitlab.nic.cz/djangocms-apps/djangocms-meta-og) project.

### Install

`pip install django-meta-og`


Add into settings.py:

```python
INSTALLED_APPS = [
    "django_meta_og",
    ...
]

TEMPLATES  = [
    {"OPTIONS": {
            "context_processors": [
                "django_meta_og.context_processors.meta",
                ...
            ]
        }
    }
]
```

Add into the templates:

```django
{% load django_meta_og %}
{% django_meta_og_prefix as og_prefix %}
<head{% if og_prefix %} prefix="{{ og_prefix }}"{% endif %}>
    {% include "django_meta_og/header_meta.html" %}
```

The result can be:

```html
<head prefix="og: https://ogp.me/ns#">
    <meta property="og:type" content="website" />
    <meta property="og:title" content="The Title" />
    ...
</head>
```

### License

BSD License
