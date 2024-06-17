# Punkweb Insight

Punkweb Insight is a Django application that provides visitor and page view tracking and an analytics dashboard for your Django website.

## Built with

- [Django](https://www.djangoproject.com/)

## Requirements

- Python 3.9+
- Django 4.0+

It may work with older versions of Python and Django, but it has not been tested.

## Installation

```bash
pip install punkweb-insight
```

Add `punkweb_insight` to your `INSTALLED_APPS` in your Django settings module:

```python
INSTALLED_APPS = [
    ...
    "punkweb_insight",
]
```

Add the following middleware to your `MIDDLEWARE` in your Django settings module, before `SessionMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "punkweb_insight.middleware.InsightMiddleware", # Here, before SessionMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
]
```

Add the following URL pattern to your `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path("insight/", include("punkweb_insight.urls")), # or any other path you want
]
```

And finally, install the models:

```bash
python manage.py migrate
```

## Configuration

These are the default settings for Punkweb Insight, which can be overridden in your Django settings module:

```python
PUNKWEB_INSIGHT = {}
```

## Testing

Report:

```bash
coverage run && coverage report
```

HTML:

```bash
coverage run && coverage html
```
