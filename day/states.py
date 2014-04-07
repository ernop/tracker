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

def states(request):
    vals={}
    note_problems=[]
    vals['note_problems']=note_problems
    day_problems=[]
    vals['day_problems']=day_problems
    
    
    bads=Note.objects.filter(kinds=None).filter(text='')
    note_problems.append(('empty notes',bads,bads.count()))
    
    bads=Note.objects.exclude(kinds=None).filter(text='')
    note_problems.append(('notes missing tags',bads,bads.count()))
    
    bads=Day.objects.filter(purchases=None,notes=None)
    day_problems.append(('day obj with nothing',bads,bads.count()))
    
    template='jinja2/states.html'
    
    return r2r(template, request, context=vals)