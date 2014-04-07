python manage.py shell_plus

for pp in Purchase.objects.all():
    try:
        day=Day.objects.get(date=pp.created.date())
    except Day.DoesNotExist:
        day=Day(date=pp.created.date())
        day.save()
    pp.day=day
