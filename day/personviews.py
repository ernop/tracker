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
def person(request, person_id):
    try:
        person = Person.objects.get(id = person_id)
    except:
        person = None
    vals = {}
    vals['person'] = person
    return r2r('jinja2/person.html', request, vals)
    
