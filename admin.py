from django.contrib import admin
from buy.models import *
from workout.models import *
from utils import adminify

class ProductAdmin(admin.ModelAdmin):
    list_display='name domain'.split()

class PurchaseAdmin(admin.ModelAdmin):
    list_display='id myproduct quantity cost mycost_per currency source mywho_with'.split()
    
    list_filter='source currency'.split()
    
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
    extra=10

class ExerciseAdmin(admin.ModelAdmin):
    list_display='id name mymuscles barbell'.split()
    inlines=[
        PMuscleInline,
        SMuscleInline,
    ]
    exclude=['pmuscles','smuscles',]
    
    def mymuscles(self, obj):
        return 'primary:%s\n<br>synergists:%s'%(','.join([m.adm() for m in obj.pmuscles.all()]),','.join([m.adm() for m in obj.smuscles.all()]))

    def get_changelist_form(self, request, **kwargs):
            kwargs.setdefault('form', ApplicantForm)
            return super(ApplicantAdmin, self).get_changelist_form(request, **kwargs)    

    adminify(mymuscles)

class SetAdmin(admin.ModelAdmin):
    list_display='exweight count workout note'.split()
    create_date=models.DateTimeField(auto_now_add=True)
    
class ExWeightAdmin(admin.ModelAdmin):
    list_display='exercise weight side'.split()
    
class MuscleAdmin(admin.ModelAdmin):
    list_display='id name myexercises'.split()
    list_editable=['name',]

    def myexercises(self, obj):
        return '%s<br>\n%s'%(','.join([ex.adm() for ex in obj.primary_exercises.all()]), ','.join([ex.adm() for ex in obj.synergists_exercises.all()]))

    adminify(myexercises)
    
class WorkoutAdmin(admin.ModelAdmin):
    list_display='id mysets date'.split()
    inlines=[SetInline,]
    def mysets(self, obj):
        return ','.join([s.adm() for s in obj.sets.all()])
    adminify(mysets)

   
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(ExWeight, ExWeightAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Workout, WorkoutAdmin)