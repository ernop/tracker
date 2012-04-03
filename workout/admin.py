from django.contrib import admin
from workout.models import *
from utils import adminify

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