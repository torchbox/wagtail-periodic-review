from collections.abc import Mapping
from typing import Any

from django.urls import path, reverse
from django.utils.translation import gettext as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.ui.components import Component
from wagtail.permission_policies.pages import PagePermissionPolicy

from .utils import for_review_this_month, review_overdue
from .views import PeriodicReviewContentReport


class BaseHomePanel(Component):
    heading = ""
    description = ""
    description_icon = "info-circle"
    description_css_class = "help-info"
    template_name = "wagtailadmin/periodic_review/home_panel.html"

    def __init__(self, request):
        self.request = request

    def get_page_list(self):
        return PagePermissionPolicy().instances_user_has_permission_for(
            self.request.user, "change"
        )

    def get_context_data(self, parent_context: Mapping[str, Any]) -> Mapping[str, Any]:
        context = super().get_context_data(parent_context)
        context.update(
            {
                "request": self.request,
                "heading": self.heading,
                "description": self.description,
                "description_icon": self.description_icon,
                "description_css_class": self.description_css_class,
                "page_list": self.get_page_list(),
            }
        )
        return context


class OverdueReviewsPanel(BaseHomePanel):
    heading = _("Content review overdue")
    description = _("The following pages are overdue a review, but are still live.")
    description_css_class = "help-critical"
    description_icon = "warning"
    order = 200

    def get_page_list(self):
        all_pages = super().get_page_list()
        return review_overdue(all_pages.live())[:10]


class ForReviewThisMonthPanel(BaseHomePanel):
    heading = _("For review this month")
    description = _("The following live pages are due a review this month.")
    description_css_class = "help-warning"
    description_icon = "help"
    order = 201

    def get_page_list(self):
        all_pages = super().get_page_list()
        return for_review_this_month(all_pages.live())[:10]


@hooks.register("construct_homepage_panels")
def add_review_panels(request, panels):
    panels.append(OverdueReviewsPanel(request))
    panels.append(ForReviewThisMonthPanel(request))


@hooks.register("register_reports_menu_item")
def register_report_menu_item():
    return MenuItem(
        _("Periodic review content"),
        reverse("wagtail_periodic_review_report"),
        icon_name=PeriodicReviewContentReport.header_icon,
        order=800,
    )


@hooks.register("register_admin_urls")
def register_report_url():
    urls = [
        path(
            "reports/periodic-review/",
            PeriodicReviewContentReport.as_view(),
            name="wagtail_periodic_review_report",
        )
    ]

    if WAGTAIL_VERSION >= (6, 2):
        # Add a results-only view to add support for AJAX-based filtering
        urls.append(
            path(
                "reports/periodic-review/results/",
                PeriodicReviewContentReport.as_view(results_only=True),
                name="wagtail_periodic_review_report_results",
            ),
        )

    return urls


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        # icon id "icon-wpr-calendar-stats"
        "wagtail_periodic_review/icons/calendar-stats.svg",
    ]
