import datetime, tempfile, shutil, os

from django.contrib import admin
from django.conf import settings
from django.db.models import Sum

from tracker.buy.models import *
from tracker.workout.models import *
from tracker.utils import adminify, DATE, mk_default_field, nowdate

from spark import sparkline_discrete
from tracker.buy.models import HOUR_CHOICES, hour2name, name2hour
def gethour():
    hour=datetime.datetime.now().hour
    if hour<2:
        return 'midnight'
    if hour<6:
        return 'early morning'
    if hour<11:
        return 'morning'
    elif hour<14:
        return 'noon'
    elif hour<20:
        return 'evening'
    elif hour<23:
        return 'night'
    return 'midnight'

def savetmp(self):
    out=tempfile.NamedTemporaryFile(dir=settings.SPARKLINES_DIR, delete=False)
    self.save(out,'png')
    print 'created',out.name
    os.chmod(out.name, 0644)
    return out

class ProductAdmin(admin.ModelAdmin):
    list_display='name domain mypurchases mylastmonth'.split()
    
    def mypurchases(self, obj):
        return ','.join([p.adm() for p in Purchase.objects.filter(product=obj)])
    
    def mylastmonth(self, obj):
        purch=Purchase.objects.filter(product=obj)
        if not purch:
            return
        
        mindate=None
        res={}
        for pu in purch:
            date=pu.created.strftime(DATE)
            res[date]=res.get(date, 0)+1
            if not mindate or date<mindate:
                mindate=date
        first=datetime.datetime.strptime(mindate, DATE)
        now=datetime.datetime.now()
        trying=first
        res2=[]
        while trying<now:
            res2.append((res.get(trying.strftime(DATE), 0)))
            trying=datetime.timedelta(days=1)+trying
        im=sparkline_discrete(results=res2, width=5, height=30)
        tmp=savetmp(im)
        return '<img style="border:2px solid grey;"  src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])

    
    adminify(mylastmonth, mypurchases)

class PurchaseAdmin(admin.ModelAdmin):
    list_display='id myproduct mydomain quantity cost mycost_per currency source mywho_with created'.split()
    
    list_filter='source currency product__domain'.split()
    date_hierarchy='created'
    
    def mycost_per(self, obj):
        return '%0.2f'%(float(obj.cost)/obj.quantity)
    
    def myproduct(self, obj):
        return obj.product.adm()
    
    def mywho_with(self, obj):
        return '%s'%''.join([per.adm() for per in obj.who_with.all()])    
    
    def mydomain(self, obj):
        return '<a href=/admin/buy/domain/?id=%d>%s</a>'%(obj.product.domain.id, obj.product.domain)
    
    adminify(mycost_per, myproduct, mywho_with, mydomain)
    formfield_for_dbfield=mk_default_field({'hour':lambda x:hour2name[gethour()], 'quantity':1,'created':datetime.datetime.now})
    #def formfield_for_dbfield(self, db_field, **kwargs):
        #if db_field.name=='hour':
            #kwargs['initial']=hour2name[gethour()]
            #kwargs.pop('request')
            #return db_field.formfield(**kwargs)
        #if db_field.name=='quantity':
            #kwargs['initial']=1
            #kwargs.pop('request')
            #return db_field.formfield(**kwargs)
        #if db_field.name=='created':
            #kwargs['initial']=datetime.datetime.now()
            #kwargs.pop('request')
            #return db_field.formfield(**kwargs)
        #return super(PurchaseAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'currency':
            kwargs['initial'] = 1
            return db_field.formfield(**kwargs)
        return super(PurchaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class DomainAdmin(admin.ModelAdmin):
    list_display='id name myproducts mytotal myspent'.split()
    list_filter=['name',]
    list_editable=['name',]
    def myproducts(self, obj):
        return obj.summary()
        
    def myspent(self, obj):
        purch=Purchase.objects.filter(product__domain=obj)
        if not purch:
            return
        mindate=None
        res={}
        for pu in purch:
            date=pu.created.strftime(DATE)
            res[date]=res.get(date, 0)+pu.cost
            if not mindate or date<mindate:
                mindate=date
        first=datetime.datetime.strptime(mindate, DATE)
        now=datetime.datetime.now()
        trying=first
        res2=[]
        while trying<now:
            res2.append((res.get(trying.strftime(DATE), 0)))
            trying=datetime.timedelta(days=1)+trying
        im=sparkline_discrete(results=res2, width=5, height=100)
        tmp=savetmp(im)
        return '<img style="border:2px solid grey;" src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])    
    
    def mytotal(self, obj):
        """in the last month"""
        monthago=datetime.datetime.now()-datetime.timedelta(days=30)
        total=Purchase.objects.filter(currency__name='rmb').filter(product__domain=obj).filter(created__gte=monthago).aggregate(Sum('cost'))['cost__sum']
        ear=Purchase.objects.filter(currency__name='rmb').filter(product__domain=obj).order_by('created')
        earliest=None
        if ear:
            earliest=datetime.datetime.combine(ear[0].created, datetime.time())
        
        if total and ear:
            now=datetime.datetime.now()
            dayrange=min(30.0,(abs((now-earliest).days))+1)
            return '%0.0f<br>%0.2f /day<br>(%d days)'%(total, total/dayrange, dayrange)
        
    adminify(myproducts, myspent, mytotal)
    
class PersonAdmin(admin.ModelAdmin):
    list_display='id first_name last_name birthday mymet_through'.split()
    list_filter=['met_through',]
    
    def mymet_through(self, obj):
        return '%s'%''.join([str(per) for per in obj.met_through.all()])
    
    adminify(mymet_through)


class CurrencyAdmin(admin.ModelAdmin):
    list_display='name symbol mytotal my3months'.split()
    def mytotal(self, obj):
        total=Purchase.objects.filter(currency__name='rmb').filter(source=obj).aggregate(Sum('cost'))['cost__sum']
        cre=Purchase.objects.filter(currency__name='rmb').filter(source=obj).order_by('created')
        earliest=None
        if cre:
            earliest=datetime.datetime.combine(cre[0].created, datetime.time())
        if total and cre:
            now=datetime.datetime.now()
            dayrange=(abs((now-earliest).days)+1)
            return '%0.0f<br>%0.2f /day<br>(%d days)'%(total, total/dayrange, dayrange)            

    def my3months(self, obj):
        monthago=datetime.datetime.now()-datetime.timedelta(days=30)
        total=Purchase.objects.filter(currency__name='rmb').filter(source=obj).filter(created__gte=monthago).aggregate(Sum('cost'))['cost__sum']
        cre=Purchase.objects.filter(currency__name='rmb').filter(source=obj).order_by('created')
        earliest=None
        if cre:
            earliest=datetime.datetime.combine(cre[0].created, datetime.time())
        if total and earliest:
            now=datetime.datetime.now()
            dayrange=min(90.0,(abs((now-earliest).days))+1)
            return '%0.0f<br>%0.2f /day<br>(%d days)'%(total, total/dayrange, dayrange)                    
        
    adminify(mytotal, my3months)

class SourceAdmin(admin.ModelAdmin):
    list_display='name mytotal mysummary'.split()
    
    def mysummary(self, obj):
        return obj.summary()
    
    #def mypurch(self, obj):
        #return '%s'%obj.all_purchases_link()
    
    def mytotal(self, obj):
        monthago=datetime.datetime.now()-datetime.timedelta(days=30)
        total=Purchase.objects.filter(currency__name='rmb').filter(source=obj).aggregate(Sum('cost'))['cost__sum']
        ear=Purchase.objects.filter(currency__name='rmb').filter(source=obj).order_by('created')
        earliest=None
        if ear:
            earliest=datetime.datetime.combine(ear[0].created, datetime.time())
        
        if total and earliest:
            now=datetime.datetime.now()
            dayrange=min(30.0,(abs((now-earliest).days))+1)
            return '%0.0f<br>%0.2f /day<br>(%d days)'%(total, total/dayrange, dayrange)        
        
    adminify(mytotal, mysummary)

admin.site.register(Product, ProductAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Person, PersonAdmin)

class PMuscleInline(admin.StackedInline):
    model = Exercise.pmuscles.through
    
class SMuscleInline(admin.StackedInline):
    model = Exercise.smuscles.through

class SetInline(admin.StackedInline):
    model=Workout.exweights.through
    extra=12

class ExerciseAdmin(admin.ModelAdmin):
    list_display='id name myhistory myspark barbell'.split()
    inlines=[
        PMuscleInline,
        SMuscleInline,
    ]
    exclude=['pmuscles','smuscles',]
        
    def mymuscles(self, obj):
        return 'primary:%s\n<br>synergists:%s'%(', '.join([m.adm() for m in obj.pmuscles.all()]),', '.join([m.adm() for m in obj.smuscles.all()]))

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', ApplicantForm)
        return super(ApplicantAdmin, self).get_changelist_form(request, **kwargs)    
    
    def myspark(self, obj):
        past=[]
        res={}
        mindate=None
        zets=Set.objects.filter(exweight__exercise=obj).order_by('-workout__created')
        if not zets:
            return ''
        for zet in zets:
            #past.append((zet.workout.date, zet.count, zet.exweight.weight))        
            date=zet.workout.created.strftime(DATE)
            res[date]=max(res.get(date, 0), zet.exweight.weight)
            if not mindate or date<mindate:
                mindate=date
        first=datetime.datetime.strptime(mindate, DATE)
        now=datetime.datetime.now()
        trying=first
        res2=[]
        while trying<now:
            res2.append((res.get(trying.strftime(DATE), 0)))
            trying=datetime.timedelta(days=1)+trying
        im=sparkline_discrete(results=res2, width=5, height=200)
        tmp=savetmp(im)
        return '<img style="border:2px solid grey;" src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])                
        
    
    def myhistory(self, obj):
        past=[]
        for zet in Set.objects.filter(exweight__exercise=obj).order_by('-workout__created'):
            past.append((zet.workout.created , zet.count, zet.exweight.weight))
        past.sort(key=lambda x:x[0], reverse=True)
        res=''
        lasttime=None
        for p in past:
            if p[0]==lasttime:
                pass
            else:
                res+='<br>%s '%p[0].strftime(DATE)
                lasttime=p[0]
            res+='%d@<b>%d</b> '%(p[1], p[2])
        return res
            
    adminify(mymuscles, myhistory, myspark)

class SetAdmin(admin.ModelAdmin):
    list_display='exweight count workout note'.split()
    create_date=models.DateTimeField(auto_now_add=True)
    
class ExWeightAdmin(admin.ModelAdmin):
    list_display='exercise weight side mysets'.split()
    def mysets(self, obj):
        preres=[(s.workout.created.strftime(DATE), s.workout.id)  for s in obj.sets.all()]
        date2workoutid={}
        for k,v in preres:
            date2workoutid[k]=v
        res={}
        for k in preres:res[k[0]]=res.get(k[0],0)+1
        res2=', '.join(sorted(['%s:<b>%d</b>'%(Workout.objects.get(id=date2workoutid[kv[0]]).clink(),kv[1]) for kv in res.items()]))
        return res2
    
    adminify(mysets)
    
class MuscleAdmin(admin.ModelAdmin):
    list_display='id name myexercises'.split()
    list_editable=['name',]

    def myexercises(self, obj):
        return '%s<br>\n%s'%(','.join([ex.adm() for ex in obj.primary_exercises.all()]), ','.join([ex.adm() for ex in obj.synergists_exercises.all()]))

    adminify(myexercises)

from django import forms
class WorkoutForm(forms.ModelForm):
    class Meta:
        model=Workout
    
    def __init__(self, *args, **kwgs):
        super(WorkoutForm, self).__init__(*args, **kwgs)
    
    def clean_date(self):
        #import ipdb;ipdb.set_trace()
        pass
    
    def clean(self):
        if self.is_bound:
            if self.instance.created is None:
                self.instance.created=datetime.datetime.now()
                self.cleaned_data['created']=datetime.datetime.now()
        super(WorkoutForm, self).clean()
        return self.cleaned_data
    
    #def save(self):
        #if not self.date:
            #self.date=datetime.datetime.now()
        #super(WorkoutForm, self).save()
    

class WorkoutAdmin(admin.ModelAdmin):
    list_display='mycreated mysets'.split()
    inlines=[SetInline,]
    #form=WorkoutForm#unnecessary
    def mysets(self, obj):
        res={}
        preres={}
        for s in obj.sets.all():res[s.exweight.exercise]=[]
        for s in obj.sets.all():res[s.exweight.exercise].append(s)
        #res is dict of exercise => [exweights,]
        res2={}
        for exercise,zets in res.items():
            weights={}
            if exercise.barbell:
                for zet in zets:weights[(zet.exweight.weight, zet.exweight.side,)]=[]
                for zet in zets:weights[(zet.exweight.weight, zet.exweight.side,)].append(zet.count)
            else:
                for zet in zets:weights[zet.exweight.weight]=[]
                for zet in zets:weights[zet.exweight.weight].append(zet.count)
            weights['sets']=zets
            res2[exercise]=weights
            
        res3=''
        for exercise, summary in sorted(res2.items(), key=lambda x:x[1]['sets'][0].id):
            #order by set id, so the order you do them in the workout is right.
            res3+='%s '%exercise.clink()
            for weight, counts in summary.items():
                if weight=='sets':continue
                if type(weight) is tuple:
                    res3+=' <b>%d</b>(%d):'%(weight[0], weight[1])
                else:
                    res3+='<b>%d</b>:'%(weight)
                res3+=','.join(['%d'%cc for cc in counts])
            #res3+='%s %s'%(exercise, ' ,'.join(['%d'%s for s in summary]))
            res3+='<br>'
        return res3
    
    def mycreated(self, obj):
        return obj.created.strftime(DATE)
    formfield_for_dbfield=mk_default_field({'created':datetime.datetime.now,})
    adminify(mycreated, mysets)


class MeasuringSpotAdmin(admin.ModelAdmin):
    list_display='name mymeasurements myhistory mydomain'.split()
    list_filter=['domain',]
    def mymeasurements(self, obj):
        return '<br>'.join([m.adm() for m in obj.measurements.all()])
    
    def myhistory(self, obj):
        mes=obj.measurements.all()
        if not mes:
            return
        mindate=None
        res={}
        for m in mes:
            date=m.created.strftime(DATE)
            res[date]=m.amount
            if not mindate or date<mindate:
                mindate=date
        first=datetime.datetime.strptime(mindate, DATE)
        now=datetime.datetime.now()
        trying=first
        res2=[]
        while trying<now:
            res2.append((res.get(trying.strftime(DATE), 0)))
            trying=datetime.timedelta(days=1)+trying
        im=sparkline_discrete(results=res2, width=5, height=100)
        tmp=savetmp(im)
        return '<img style="border:2px solid grey;" src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])
    
    
    def mydomain(self, obj):
        return '<a href=/admin/buy/domain/?id=%d>%s</a>'%(obj.domain.id, obj.domain)
    
    adminify(mymeasurements, myhistory, mydomain)

class MeasurementAdmin(admin.ModelAdmin):
    list_display='place mycreated amount'.split()
    
    def mycreated(self, obj):
        return obj.created.strftime(DATE)
    
    
    formfield_for_dbfield=mk_default_field({'created':nowdate,})
    adminify(mycreated)
    class Meta:
        fields='place amount created'.split()
        
    fieldsets = (
          ('Main', {
               'fields': ('place amount created'.split())
           },),
       )    
        
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(ExWeight, ExWeightAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(MeasuringSpot, MeasuringSpotAdmin)