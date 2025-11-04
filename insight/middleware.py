import re
from django.conf import settings
from django.db import IntegrityError, transaction
from django.urls import resolve

from insight.models import PageView, Visitor


class InsightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_paths = getattr(
            settings,
            "INSIGHT_EXCLUDE_PATHS",
            [
                r"^/static/",
                r"^/media/",
                r"^/.well-known/",
                r"^/favicon(\..+)?$",
                r"^/apple-touch-icon(\..+)?$",
                r"^/android-chrome(\..+)?$",
                r"^/robots\.txt$",
                r"^/humans\.txt$",
                r"^/sitemap\.xml$",
                r"^/manifest\.json$",
                r"^/site.webmanifest$",
                r"^/service-worker\.js$",
            ],
        )
        self.exclude_apps = getattr(
            settings,
            "INSIGHT_EXCLUDE_APPS",
            ["admin", "insight"],
        )
        self.exclude_url_names = getattr(
            settings,
            "INSIGHT_EXCLUDE_URL_NAMES",
            [
                "static",
                "media",
                "favicon",
                "robots_txt",
                "sitemap",
                "health_check",
            ],
        )

    def has_session_middlware(self, request):
        return hasattr(request, "session")

    def check_path(self, request):
        for pattern in self.exclude_paths:
            if re.match(pattern, request.path):
                return False

        try:
            match = resolve(request.path)
            if (
                match.app_name in self.exclude_apps
                or match.url_name in self.exclude_url_names
            ):
                return False
        except Exception:
            pass
        return True

    def should_track(self, request):
        if not self.has_session_middlware(request):
            return False

        if not self.check_path(request):
            return False

        # Other rules to ignore certain requests can be added here

        return True

    def refresh_visitor(self, request):
        session_key = request.session.session_key

        try:
            visitor = Visitor.objects.get(session_key=session_key)
        except Visitor.DoesNotExist:
            with transaction.atomic():
                visitor = Visitor.objects.create(pk=session_key)

        user = request.user if request.user.is_authenticated else None

        if user and not visitor.user:
            visitor.user = user

        visitor.expiry_age = request.session.get_expiry_age()
        visitor.expiry_time = request.session.get_expiry_date()

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
