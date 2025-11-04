from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from insight.forms import DateFiltersForm
from insight.models import PageView, Visitor

User = get_user_model()


@login_required
def index_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
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

    total_visitors = visitors.count()
    total_page_views = page_views.count()

    popular_pages = PageView.objects.popular(start=start, end=end)

    base_url = request.build_absolute_uri("/")[:-1]

    popular_referrers = PageView.objects.popular_referrers(
        start=start, end=end, base_url=base_url
    )

    context = {
        "form": form,
        "total_visitors": total_visitors,
        "total_page_views": total_page_views,
        "recent_visitors": visitors[:10],
        "popular_pages": popular_pages,
        "popular_referrers": popular_referrers,
    }

    return render(request, "insight/index.html", context=context)


@login_required
def visitor_index_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = Visitor.objects.filter(
        start_time__date__gte=start,
        start_time__date__lte=end,
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "visitors": page,
    }

    return render(request, "insight/visitor_index.html", context=context)


@login_required
def visitor_detail_view(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    visitor = get_object_or_404(Visitor, pk=pk)
    page_views = (
        PageView.objects.filter(visitor=visitor)
        .values("url")
        .annotate(
            total_views=models.Count("url"),
        )
        .order_by("-total_views")
    )
    context = {
        "visitor": visitor,
        "page_views": page_views,
    }

    return render(request, "insight/visitor_detail.html", context=context)


@login_required
def page_view_index_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = PageView.objects.filter(
        created_at__date__gte=start,
        created_at__date__lte=end,
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "page_views": page,
    }

    return render(request, "insight/page_view_index.html", context=context)


@login_required
def page_view_detail_view(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    page_view = get_object_or_404(PageView, pk=pk)
    context = {
        "page_view": page_view,
    }

    return render(request, "insight/page_view_detail.html", context=context)


@login_required
def vistory_history_view(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    visitor = get_object_or_404(Visitor, pk=pk)

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = PageView.objects.filter(
        visitor=visitor,
        created_at__date__gte=start,
        created_at__date__lte=end,
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "visitor": visitor,
        "page_views": page,
    }

    return render(request, "insight/visitor_history.html", context=context)


@login_required
def page_stats_index_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = (
        PageView.objects.filter(
            created_at__date__gte=start,
            created_at__date__lte=end,
        )
        .values("url")
        .annotate(
            total_views=models.Count("url"),
            total_visitors=models.Count("visitor", distinct=True),
        )
        .order_by("-total_views")
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "popular_pages": page,
    }

    return render(request, "insight/page_stats_index.html", context=context)


@login_required
def page_stats_detail_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    page_url = request.GET.get("url")

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "page_url": page_url,
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(
        {
            "page_url": page_url,
            "start": request.GET.get("start", start),
            "end": request.GET.get("end", end),
        }
        or defaults
    )
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = PageView.objects.filter(
        url=page_url,
        created_at__date__gte=start,
        created_at__date__lte=end,
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "page_url": page_url,
        "total_views": qs.count(),
        "page_views": page,
    }
    return render(request, "insight/page_stats_detail.html", context=context)


@login_required
def referrer_stats_index_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(request.GET or defaults)
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    base_url = request.build_absolute_uri("/")[:-1]

    qs = (
        PageView.objects.filter(
            created_at__date__gte=start,
            created_at__date__lte=end,
        )
        .exclude(referrer__exact="")
        .exclude(referrer__startswith=base_url)
        .values("referrer")
        .annotate(
            total_views=models.Count("referrer"),
            total_visitors=models.Count("visitor", distinct=True),
        )
        .order_by("-total_views")
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "popular_referrers": page,
    }

    return render(request, "insight/referrer_stats_index.html", context=context)


@login_required
def referrer_stats_detail_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    page_url = request.GET.get("referrer")

    end = timezone.now()
    start = end - timezone.timedelta(days=7)

    defaults = {
        "page_url": page_url,
        "start": start,
        "end": end,
    }

    form = DateFiltersForm(
        {
            "page_url": page_url,
            "start": request.GET.get("start", start),
            "end": request.GET.get("end", end),
        }
        or defaults
    )
    if form.is_valid():
        start = form.cleaned_data["start"] or start
        end = form.cleaned_data["end"] or end

    qs = PageView.objects.filter(
        referrer=page_url,
        created_at__date__gte=start,
        created_at__date__lte=end,
    )
    page_size = 50
    paginator = Paginator(qs, page_size)
    page_param = request.GET.get("page", 1)
    page = paginator.get_page(page_param)

    context = {
        "form": form,
        "page_url": page_url,
        "total_views": qs.count(),
        "page_views": page,
    }
    return render(request, "insight/referrer_stats_detail.html", context=context)
