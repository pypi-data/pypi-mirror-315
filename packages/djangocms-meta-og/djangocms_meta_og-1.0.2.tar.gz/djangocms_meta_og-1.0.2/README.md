# DjangoCMS Meta OG


HTML Meta tags [OpenGraph](https://ogp.me/) for [DjangoCMS](https://www.django-cms.org/).
The project is based on the [Django Meta OG](https://gitlab.nic.cz/django-apps/django-meta-og) project.

### Install

`pip install djangocms-meta-og`


Add into settings.py:

```python
INSTALLED_APPS = [
    "django_meta_og",
    "djangocms_meta_og",
    ...
]

TEMPLATES  = [
    {"OPTIONS": {
            "context_processors": [
                "djangocms_meta_og.context_processors.meta",
                ...
            ]
        }
    }
]
```

Add into the templates:

```django
{% load djangocms_meta_og %}
{% djangocms_meta_og_prefix as og_prefix %}
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

### Prefix for Meta tags in template

Some Meta tags may already be defined in the template. Their prefix is ​​included in the prefix list via the definition in settings:

```python
META_OG_PREFIX_IN_TEMLATES = (
    ("og", "https://ogp.me/ns#"),
    ("article", "https://ogp.me/ns/article#"),
)
```

### License

BSD License
