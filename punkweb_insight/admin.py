from django.contrib import admin
from punkweb_insight.models import PageView, Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        "session_key",
        "user",
        "start_time",
        "time_on_site",
        "session_expired",
        "ip_address",
    ]
    search_fields = ["user__username"]

    def session_expired(self, obj):
        return obj.session_expired()

    session_expired.boolean = True


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ["url", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
