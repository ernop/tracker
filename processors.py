def static_url_processor(request):
    from django.conf import settings
    res={'LOCAL':settings.LOCAL,'ADMIN_EXTERNAL_BASE':settings.ADMIN_EXTERNAL_BASE,'path':request.path}
    return res