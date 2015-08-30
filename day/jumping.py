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