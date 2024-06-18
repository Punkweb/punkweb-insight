from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils import timezone

from punkweb_insight.models import PageView, Visitor


class InsightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def has_session_middlware(self, request):
        return hasattr(request, "session")

    def is_bot(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()

        if not user_agent:
            return True

        bot_agents = ["bot", "crawl", "spider", "slurp"]
        suspicious_paths = [
            "/admin.php",
            "/admin-post.php",
            "/admin-ajax.php",
        ]

        if any(agent in user_agent for agent in bot_agents):
            return True

        if any(request.path.lower().startswith(path) for path in suspicious_paths):
            return True

        return False

    def check_path(self, request):
        path = request.path

        admin_url = reverse("admin:index")
        insight_url = reverse("punkweb_insight:index")
        static_url = settings.STATIC_URL
        media_url = settings.MEDIA_URL

        return not any(
            [
                path.startswith(admin_url),
                path.startswith(insight_url),
                path.startswith(static_url),
                path.startswith(media_url),
                path.startswith("/favicon"),
            ]
        )

    def should_track(self, request):
        if not self.has_session_middlware(request):
            return False

        if self.is_bot(request):
            return False

        if not self.check_path(request):
            return False

        return True

    def get_client_ip(self, request):
        headers = (
            "HTTP_X_FORWARDED_FOR",
            "HTTP_X_REAL_IP",
            "HTTP_CLIENT_IP",
            "HTTP_X_CLIENT_IP",
            "HTTP_X_CLUSTER_CLIENT_IP",
            "HTTP_FORWARDED_FOR",
            "HTTP_FORWARDED",
            "REMOTE_ADDR",
        )

        for header in headers:
            ip = request.META.get(header, None)
            if ip:
                try:
                    validate_ipv46_address(ip)
                    return ip
                except ValidationError:
                    pass

        return ""

    def refresh_visitor(self, request):
        session_key = request.session.session_key

        try:
            visitor = Visitor.objects.get(session_key=session_key)
        except Visitor.DoesNotExist:
            ip_address = self.get_client_ip(request)
            visitor = Visitor(pk=session_key, ip_address=ip_address)

        user = request.user if request.user.is_authenticated else None

        if user and not visitor.user:
            visitor.user = user

        visitor.expiry_age = request.session.get_expiry_age()
        visitor.expiry_time = request.session.get_expiry_date()

        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if user_agent:
            visitor.user_agent = user_agent

        time_on_site = 0
        if visitor.start_time:
            delta = timezone.now() - visitor.start_time
            seconds = (delta.days * 24 * 3600) + delta.seconds
            time_on_site = (delta.microseconds + seconds * 10**6) / 10**6

        visitor.time_on_site = time_on_site

        try:
            with transaction.atomic():
                visitor.save()
        except IntegrityError:
            visitor = Visitor.objects.get(pk=session_key)

        return visitor

    def create_page_view(self, request, visitor):
        referrer = request.META.get("HTTP_REFERER", "")
        query_string = request.META.get("QUERY_STRING", "")

        PageView.objects.create(
            visitor=visitor,
            url=request.path,
            query_string=query_string,
            referrer=referrer,
            method=request.method,
        )

    def __call__(self, request):
        response = self.get_response(request)

        if not self.should_track(request):
            return response

        if not request.session.session_key:
            request.session.save()

        visitor = self.refresh_visitor(request)
        self.create_page_view(request, visitor)

        return response
