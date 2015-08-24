import datetime

from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django import forms
from day.models import *

from trackerutils import *
from utils import *
from choices import *

import logging
log=logging.getLogger(__name__)

from forms import DayForm

@login_required
def jumping_product(request, product_id):
    pass

@login_required
def jumping_source(request, source_id):
    pass

@login_required
def jumping_person(request, person_id):
    #show the related sources
    vals = {}
    people = Person.objects.all()
    if exclude_disabled:
        people = people.exclude(disabled=True)

    edges = []
    nodes = {}
    linked_ids = set()
    for person in people:
        if person.met_through.exists():
            for operson in person.met_through.all():
                edges.append({'target': operson.id, 'source': person.id, 'value': 1,})
            for operson in person.introduced_to.all():
                if recent_only and not operson.purchases.exists():
                    continue
                linked_ids.add(operson.id)
                linked_ids.add(person.id)
            if recent_only and not person.purchases.exists():
                continue
            linked_ids.add(person.id)
    for person in people:
        if recent_only and (not person.purchases.exists()) and person.id not in linked_ids:
            print 'skipping', person
            continue
        nodes[person.id] = person2obj(person)
    vals['nodes'] = nodes
    vals['edges'] = edges
    vals['recent_only'] = recent_only
    return r2r('jinja2/people_connections.html', request, vals)

#def person2obj(person):
    #return {'id': person.id,
                               #'gender':person.gender,
                               #'reflexive':False,
                               #'left': True,
                               #'right': False,
                               #'name': person.d3_name(),
                               #'created': person.created.strftime(DATE_DASH_REV),
                               #'last_purchase': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).order_by('-created')[0].created.strftime(DATE_DASH_REV) or '2011-01-01',
                               #'purchases_together': Purchase.objects.filter(who_with=person).count(),
                               #'weight': 1,
                               #'spent_together': Purchase.objects.filter(who_with=person).exists() and Purchase.objects.filter(who_with=person).aggregate(Sum('cost'))['cost__sum'] or 0,}

#@login_required
#def days(request):
    #sixmonthago=datetime.datetime.now()-datetime.timedelta(days=180)
    #total=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(created__gte=sixmonthago).aggregate(Sum('cost'))['cost__sum']
    #ear=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).order_by('created')
    #earliest=None
    #if ear:
        #earliest=datetime.datetime.combine(ear[0].created, datetime.time())
    #else:
        #return ''
    #now=datetime.datetime.now()
    #dayrange=(abs((now-earliest).days))+1
    #return '%s%s<br>%s%s/day<br>(%d days)'%(rstripz(total), Currency.objects.get(id=1).symbol, rstripz(total/dayrange), Currency.objects.get(id=1).symbol, dayrange)



#def redir(request):
    #import ipdb;ipdb.set_trace()
    #return HttpResponseRedirect('/today/')