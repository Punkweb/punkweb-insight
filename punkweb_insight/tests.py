from django.test import TestCase


class InsightMiddlewareTestCase(TestCase):
    def test_bot_agents_are_ignored(self):
        pass

    def test_suspicious_paths_are_ignored(self):
        pass

    def test_excluded_paths_are_ignored(self):
        # admin
        # insight
        # static
        # media
        # favicon
        pass

    def test_response_is_returned_when_tracking_is_ignored(self):
        pass

    def test_visitor_is_created(self):
        pass

    def test_visitor_is_updated(self):
        pass

    def test_page_view_is_created(self):
        pass
