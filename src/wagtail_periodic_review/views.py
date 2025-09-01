from django.core.exceptions import FieldError
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

    def _get_editable_pages(self):
        return PagePermissionPolicy().instances_user_has_permission_for(
            self.request.user, "change"
        )

    def get_queryset(self):
        queryset = filter_across_subtypes(
            self._get_editable_pages(),
            last_review_date__isnull=False,
        )
        try:
            return add_review_date_annotations(queryset).order_by("next_review_date")
        except FieldError:
            return queryset
