from django.contrib import admin
from insight.models import PageView, Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        "session_key",
        "user",
        "start_time",
        "session_expired",
    )
    search_fields = ("user__username",)

    def session_expired(self, obj):
        return obj.session_expired

    session_expired.boolean = True


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("url", "visitor__user", "created_at")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
