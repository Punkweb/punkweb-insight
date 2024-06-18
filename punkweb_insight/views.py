from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.utils import timezone

from punkweb_insight.forms import IndexFiltersForm
from punkweb_insight.models import PageView, Visitor

User = get_user_model()


@login_required
@permission_required("punkweb_insight.view_page_view", raise_exception=True)
def index_view(request):
    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = IndexFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    visitors = Visitor.objects.filter(
        start_time__date__gte=start,
        start_time__date__lte=end,
    )

    page_views = PageView.objects.filter(
        created_at__date__gte=start,
        created_at__date__lte=end,
    )

    new_users = User.objects.filter(
        date_joined__date__gte=start,
        date_joined__date__lte=end,
    ).order_by("-date_joined")

    total_visitors = visitors.count()
    total_page_views = page_views.count()
    total_new_users = new_users.count()
    total_time_on_site = sum([visitor.time_on_site for visitor in visitors])
    average_time_on_site = total_time_on_site / total_visitors if total_visitors else 0

    popular_pages = PageView.objects.popular(start=start, end=end)

    base_url = request.build_absolute_uri("/")[:-1]

    popular_referrers = PageView.objects.popular_referrers(
        start=start, end=end, base_url=base_url
    )

    context = {
        "form": form,
        "total_visitors": total_visitors,
        "total_page_views": total_page_views,
        "total_new_users": total_new_users,
        "total_time_on_site": total_time_on_site,
        "average_time_on_site": average_time_on_site,
        "recent_visitors": visitors[:10],
        "new_users": new_users[:10],
        "popular_pages": popular_pages,
        "popular_referrers": popular_referrers,
    }

    return render(request, "punkweb_insight/index.html", context=context)
