# Generated by Django 4.2 on 2024-06-03 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Visitor",
            fields=[
                (
                    "session_key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("expiry_age", models.IntegerField(blank=True, null=True)),
                ("expiry_time", models.DateTimeField(blank=True, null=True)),
                ("time_on_site", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="visit_history",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-start_time",),
            },
        ),
        migrations.CreateModel(
            name="PageView",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("url", models.CharField(blank=True, max_length=2048)),
                ("query_string", models.TextField(blank=True)),
                ("referrer", models.CharField(blank=True, max_length=2048)),
                ("method", models.CharField(blank=True, max_length=8)),
                (
                    "visitor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_views",
                        to="punkweb_insight.visitor",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]