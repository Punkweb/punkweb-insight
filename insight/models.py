from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from insight.managers import PageViewManager

User = get_user_model()


class Visitor(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(
        User,
        related_name="visit_history",
        null=True,
        on_delete=models.SET_NULL,
    )
    start_time = models.DateTimeField(auto_now_add=True)
    expiry_age = models.IntegerField(blank=True, null=True)
    expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-start_time",)

    @property
    def session_expired(self):
        if self.expiry_time:
            return self.expiry_time <= timezone.now()
        return False

    def __str__(self):
        return f"{self.user or 'Anonymous'}"


class PageView(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    visitor = models.ForeignKey(
        Visitor, related_name="page_views", on_delete=models.CASCADE
    )
    url = models.CharField(max_length=2048, blank=True)
    query_string = models.TextField(blank=True)
    referrer = models.CharField(max_length=2048, blank=True)
    method = models.CharField(max_length=8, blank=True)

    objects = PageViewManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.visitor} - {self.url} - {self.created_at} "
