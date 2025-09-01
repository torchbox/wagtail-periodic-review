from django.conf import settings
from django.core.exceptions import FieldError
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from wagtail.admin.views.reports import PageReportView
from wagtail.permission_policies.pages import PagePermissionPolicy

from .filters import PeriodicReviewFilterSet
from .utils import add_review_date_annotations, filter_across_subtypes


class PeriodicReviewContentReport(PageReportView):
    filterset_class = PeriodicReviewFilterSet
    header_icon = "wpr-calendar-stats"
    page_title = _("Periodic review content")
    index_url_name = "wagtail_periodic_review_report"
    index_results_url_name = "wagtail_periodic_review_report_results"
    results_template_name = "reports/periodic_review_report_results.html"

    @cached_property
    def show_locale_labels(self):
        return getattr(settings, "WAGTAIL_I18N_ENABLED", False)

    def _get_editable_pages(self):
        return PagePermissionPolicy().instances_user_has_permission_for(
            self.request.user, "change"
        )

    def get_queryset(self):
        queryset = filter_across_subtypes(
            self._get_editable_pages(),
            last_review_date__isnull=False,
        )

        if self.show_locale_labels:
            queryset = queryset.prefetch_related("locale")

        try:
            return add_review_date_annotations(queryset).order_by("next_review_date")
        except FieldError:
            return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["show_locale_labels"] = self.show_locale_labels
        return context
