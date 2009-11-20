from django import template

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

from django_histograms.utils import Histogram

register = template.Library()

def get_date_filter(context, attname):
    request = context['request']
    filters = [("%s__%s" % (str(attname), a), a) for a in ["year", "month", "day"]]
    r = {}
    for filter in filters:
        if filter[0] in request.GET:
            r[filter[1]] = request.GET[filter[0]]
    return r

@tag(register, [Model(), Variable(), Optional([Variable(), Variable()])])
def histogram_for(context, model, attname, months=2, day_labels=True):
    dates = get_date_filter(context, attname)
    return Histogram(model, attname, months=months, **dates).render(css=True, day_labels=day_labels)


@tag(register, [Model(), Variable(), Optional([Variable(), Variable()])])
def histogram_for_days(context, model, attname, days=31, day_labels=True):
    dates = get_date_filter(context, attname)
    return Histogram(model, attname, days=days, **dates).render(css=True, day_labels=day_labels)
