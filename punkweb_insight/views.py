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
    )

    total_sessions = visitors.count()
    total_page_views = page_views.count()
    total_new_users = new_users.count()
    total_time_on_site = sum([visitor.time_on_site for visitor in visitors])
    average_time_on_site = total_time_on_site / total_sessions if total_sessions else 0

    context = {
        "form": form,
        "visitors": visitors,
        "page_views": page_views,
        "new_users": new_users,
        "total_sessions": total_sessions,
        "total_page_views": total_page_views,
        "total_new_users": total_new_users,
        "total_time_on_site": total_time_on_site,
        "average_time_on_site": average_time_on_site,
    }

    return render(request, "punkweb_insight/index.html", context=context)
