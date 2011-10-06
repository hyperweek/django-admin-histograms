from django.conf.urls.defaults import url, patterns
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_histograms.utils import Histogram


class HistogramAdmin(admin.ModelAdmin):
    histogram_months = 2
    histogram_days = None

    def get_urls(self):
        urlpatterns = patterns("",
            url(r"^report/$", self.admin_site.admin_view(self.report_view),
                name="%s_report" % self.model._meta.object_name)
        )
        return urlpatterns + super(HistogramAdmin, self).get_urls()

    def report_view(self, request):
        assert self.date_hierarchy is not None, "Set date_hierarchy you idiot"

        histogram = Histogram(self.model, self.date_hierarchy,
            self.queryset(request), months=self.histogram_months,
            days=self.histogram_days)

        context = {
            'title': "Histogram for %s" % self.model._meta.object_name,
            'histogram': histogram,
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
        }

        return render_to_response("admin/report.html", context,
            context_instance=RequestContext(request, current_app=self.admin_site.name))
