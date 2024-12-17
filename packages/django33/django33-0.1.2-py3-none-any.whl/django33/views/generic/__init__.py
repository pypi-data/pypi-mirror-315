from django33.views.generic.base import RedirectView, TemplateView, View
from django33.views.generic.dates import (
    ArchiveIndexView,
    DateDetailView,
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    WeekArchiveView,
    YearArchiveView,
)
from django33.views.generic.detail import DetailView
from django33.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django33.views.generic.list import ListView

__all__ = [
    "View",
    "TemplateView",
    "RedirectView",
    "ArchiveIndexView",
    "YearArchiveView",
    "MonthArchiveView",
    "WeekArchiveView",
    "DayArchiveView",
    "TodayArchiveView",
    "DateDetailView",
    "DetailView",
    "FormView",
    "CreateView",
    "UpdateView",
    "DeleteView",
    "ListView",
    "GenericViewError",
]


class GenericViewError(Exception):
    """A problem in a generic view."""

    pass
