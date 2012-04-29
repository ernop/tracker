import datetime

# Create your views here.

from coffin.shortcuts import *
from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet)
from django.shortcuts import HttpResponseRedirect
from workout.models import *
from django.template import RequestContext
from admin import *
from django.forms.formsets import formset_factory

def do_measurementset(request, measurementset_id=None):
    vals={}
    if request.method=='POST':
        formset=modelformset_factory(Measurement)
        import ipdb;ipdb.set_trace()
        ff=formset(request.POST)
        ff.save()
        #that's it!
        return HttpResponseRedirect('/admin/workout/')
    else:
        ms=MeasurementSet.objects.get(id=measurementset_id)
        msids=[]
        for spot in ms.measurement_spots.all():
            m=Measurement(place=spot, created=datetime.datetime.now(), amount=0)
            m.save()
            msids.append(m.id)
        qs=Measurement.objects.filter(id__in=msids)
    formset=modelformset_factory(Measurement, extra=0)
    vals['formset']=formset(queryset=qs)
    return render_to_response('many.html',vals,RequestContext(request))
