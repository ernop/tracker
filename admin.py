import datetime
from django.contrib import admin
from tracker.buy.models import *
from tracker.workout.models import *
from tracker.utils import adminify, DATE

class ProductAdmin(admin.ModelAdmin):
    list_display='name domain'.split()

class PurchaseAdmin(admin.ModelAdmin):
    list_display='id myproduct quantity cost mycost_per currency source mywho_with created'.split()
    
    list_filter='source currency'.split()
    date_hierarchy=['created',]
    
    def mycost_per(self, obj):
        return '%0.2f'%(float(obj.cost)/obj.quantity)
    
    def myproduct(self, obj):
        return '<a href="/admin/buy/product/%d">%s</a>'%(obj.id, obj.product.name)
    
    def mywho_with(self, obj):
        return '%s'%''.join([str(per) for per in obj.who_with.all()])    
    
    adminify(mycost_per, myproduct, mywho_with)

class DomainAdmin(admin.ModelAdmin):
    list_display='id name myproducts'.split()
    list_filter=['name',]
    def myproducts(self, obj):
        return '%d products'%obj.products.count()
    
    adminify(myproducts)
    
class PersonAdmin(admin.ModelAdmin):
    list_display='id first_name last_name birthday mymet_through'.split()
    list_filter=['met_through',]
    
    def mymet_through(self, obj):
        return '%s'%''.join([str(per) for per in obj.met_through.all()])
    
    adminify(mymet_through)

class SourceAdmin(admin.ModelAdmin):
    list_display='id name mypurch'.split()
    def mypurch(self, obj):
        return '%d purchases'%obj.purchases.count()
    adminify(mypurch)

admin.site.register(Product, ProductAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Source)
admin.site.register(Currency)
admin.site.register(Person, PersonAdmin)

class PMuscleInline(admin.StackedInline):
    model = Exercise.pmuscles.through
    
class SMuscleInline(admin.StackedInline):
    model = Exercise.smuscles.through

class SetInline(admin.StackedInline):
    model=Workout.exweights.through
    extra=12

class ExerciseAdmin(admin.ModelAdmin):
    list_display='id name mymuscles myhistory barbell '.split()
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
    
    def myhistory(self, obj):
        #import ipdb;ipdb.set_trace()
        past=[]
        for zet in Set.objects.filter(exweight__exercise=obj).order_by('-workout__date'):
            past.append((zet.workout.date, zet.count, zet.exweight.weight))
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
            
    adminify(mymuscles, myhistory)

class SetAdmin(admin.ModelAdmin):
    list_display='exweight count workout note'.split()
    create_date=models.DateTimeField(auto_now_add=True)
    
class ExWeightAdmin(admin.ModelAdmin):
    list_display='exercise weight side mysets'.split()
    def mysets(self, obj):
        preres=[(s.workout.date.strftime(DATE), s.workout.id)  for s in obj.sets.all()]
        date2workoutid={}
        for k,v in preres:
            date2workoutid[k]=v
        res={}
        for k in preres:res[k[0]]=res.get(k[0],0)+1
        res2=', '.join(sorted(['%s:<b>%d</b>'%(Workout.objects.get(id=date2workoutid[kv[0]]).adm(),kv[1]) for kv in res.items()]))
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
        #import ipdb;ipdb.set_trace() 
        super(WorkoutForm, self).__init__(*args, **kwgs)
    
    def clean_date(self):
        import ipdb;ipdb.set_trace()
    
    def clean(self):
        if self.is_bound:
            if self.instance.date is None:
                self.instance.date=datetime.datetime.now()
                self.cleaned_data['date']=datetime.datetime.now()
        import ipdb;ipdb.set_trace()
        super(WorkoutForm, self).clean()
        return self.cleaned_data
    
    #def save(self):
        #if not self.date:
            #self.date=datetime.datetime.now()
        #super(WorkoutForm, self).save()
    
class WorkoutAdmin(admin.ModelAdmin):
    list_display='mydate mysets'.split()
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
            #import ipdb;ipdb.set_trace()
            if exercise.barbell:
                for zet in zets:weights[(zet.exweight.weight, zet.exweight.side,)]=[]
                for zet in zets:weights[(zet.exweight.weight, zet.exweight.side,)].append(zet.count)
            else:
                for zet in zets:weights[zet.exweight.weight]=[]
                for zet in zets:weights[zet.exweight.weight].append(zet.count)
            weights['sets']=zets
            res2[exercise]=weights
            
        res3=''
        #import ipdb;ipdb.set_trace()
        for exercise, summary in sorted(res2.items(), key=lambda x:x[1]['sets'][0].id):
            #order by set id, so the order you do them in the workout is right.
            res3+='%s '%exercise
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
    
    def mydate(self, obj):
        return obj.date.strftime(DATE)
    
    adminify(mydate)
    adminify(mysets)

   
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(ExWeight, ExWeightAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Workout, WorkoutAdmin)