from django.urls import path

from insight.views import (
    index_view,
    page_stats_detail_view,
    page_stats_index_view,
    page_view_detail_view,
    page_view_index_view,
    referrer_stats_detail_view,
    referrer_stats_index_view,
    visitor_detail_view,
    visitor_index_view,
    vistory_history_view,
)

app_name = "insight"
urlpatterns = [
    path("", index_view, name="index"),
    path("page-views/", page_view_index_view, name="page_view_index"),
    path("page-views/<int:pk>/", page_view_detail_view, name="page_view_detail"),
    path("pages/", page_stats_index_view, name="page_stats_index"),
    path("page/", page_stats_detail_view, name="page_stats_detail"),
    path("referrers/", referrer_stats_index_view, name="referrer_stats_index"),
    path("referrer/", referrer_stats_detail_view, name="referrer_stats_detail"),
    path("visitors/", visitor_index_view, name="visitor_index"),
    path("visitors/<str:pk>/", visitor_detail_view, name="visitor_detail"),
    path("visitors/<str:pk>/history/", vistory_history_view, name="visitor_history"),
]
