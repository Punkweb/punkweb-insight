from django.urls import path

from punkweb_insight.views import index_view

app_name = "punkweb_insight"
urlpatterns = [
    path("", index_view, name="index"),
]
