from functools import cache

from django.core.exceptions import FieldError
from django.db.models import F, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from wagtail.models import Page, get_page_models


@cache
def get_periodic_review_models():
    from .models import PeriodicReviewMixin

    return [m for m in get_page_models() if issubclass(m, PeriodicReviewMixin)]


def add_review_date_annotations(queryset):
    if queryset.model is not Page:
        return queryset

    if not (periodic_review_models := get_periodic_review_models()):
        return queryset

    last_review_date_fields = []
    next_review_date_fields = []
    for model in periodic_review_models:
        last_review_date_fields.append(f"{model.__name__.lower()}__last_review_date")
        next_review_date_fields.append(f"{model.__name__.lower()}__next_review_date")

    if len(last_review_date_fields) > 1:
        return queryset.annotate(
            last_review_date=Coalesce(*last_review_date_fields),
            next_review_date=Coalesce(*next_review_date_fields),
        )

    return queryset.annotate(
        last_review_date=F(last_review_date_fields[0]),
        next_review_date=F(next_review_date_fields[0]),
    )


def filter_across_subtypes(queryset, **filters):
    if queryset.model is not Page:
        return queryset

    if not (periodic_review_models := get_periodic_review_models()):
        return queryset.none()

    q = Q()
    for page_type in periodic_review_models:
        q |= Q(
            **{
                f"{page_type.__name__.lower()}__{key}": value
                for key, value in filters.items()
            }
        )
    return queryset.filter(q)


def review_overdue(queryset):
    month_start = timezone.now().date().replace(day=1)
    queryset = filter_across_subtypes(
        queryset, next_review_date__isnull=False, next_review_date__lt=month_start
    )
    try:
        return add_review_date_annotations(queryset).order_by("-next_review_date")
    except FieldError:
        return queryset


def for_review_this_month(queryset):
    today = timezone.now().date()
    queryset = filter_across_subtypes(
        queryset,
        next_review_date__isnull=False,
        next_review_date__year=today.year,
        next_review_date__month=today.month,
    )
    try:
        return add_review_date_annotations(queryset).order_by("next_review_date")
    except FieldError:
        return queryset
