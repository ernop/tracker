import urllib, urlparse, re, os, ConfigParser, logging, uuid, logging.config, types, datetime, json, calendar

from django.template import RequestContext

def adminify(*args):
    for func in args:
        name=None
        if not name:
            if func.__name__.startswith('my'):
                name=func.__name__[2:]
            else:
                name=func.__name__
            name = name.replace('_', ' ')
        func.allow_tags=True
        func.short_description=name

def chunkify(l,n):
    """chunkify(range(10), 2) ==> [[0,1],[2,3],...[8,9]]"""
    res=[]
    while l:
        sub=l[:n]
        res.append(sub)
        l=l[n:]
    return res

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

def save_image_locally(url):
    """randomize name, and return name of image found at end of the url
    save it to static/aimg/name[0]/name"""

    parts=urlparse.urlparse(url)
    f,ext=os.path.splitext(parts.path)
    rnd=str(uuid.uuid4())
    if not ext:
        ext='.jpg'
        #stick a .jpg on there.
    fn=rnd+ext
    outdir='/home/ernie/RD3/rd3/static/aimg/%s/'%rnd[0]
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    outpath=outdir+fn
    try:
        urllib.urlretrieve(url, outpath)
    except Exception, e:
        log.error('error saving url %s %s',url, e)
        return None
    return fn

def get_local_image_path(obj):
    if obj.image_url:
        if obj.local_image_name:
            return '/static/aimg/%s/%s'%(obj.local_image_name[0], obj.local_image_name)
        else:
            log.error('obj has image url but no local image name.  weird. %s, id=%s',obj.image_url, obj.id)
        return ''
        #in the error case at least don't kill the template.  None is ok if not obj.image_url.


def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

import sys
import traceback
def format_exception(maxTBlevel=10):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    res='%s\n%s\n%s\n%s'%(excName, str(exc)[:100]+'...', excArgs, ''.join(excTb))
    return res

#class ConnectionRefresher(sqlalchemy.interfaces.PoolListener):
    #def __init__(self):
        #self.retried = False
    #def checkout(self, dbapi_con, con_record, con_proxy):
        #import sqlalchemy
        #import sqlalchemy.interfaces
        #import _mysql_exceptions
        #try:
            #dbapi_con.cursor().execute('select now()')
        #except mysql_exceptions.OperationalError:
            #if self.retried:
                #self.retried = False
                #raise
            #self.retried = True
            #raise sqlalchemy.exc.DisconnectionError


def is_valid_password(pw):
    OK_PASSWORD_CHARS='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[{]}|;:,<.>/?`~'
    if not pw:
        return False,_('no password provided')
    if len(pw)<4:
        return False, _('password too short')
    forbidden=set()
    for c in pw:
        if c not in OK_PASSWORD_CHARS:
            forbidden.add(c)
    if forbidden:
        return False,_('password contains forbidden characters')+ '%s'%''.join(forbidden)+'. '+_('Passwords may only contain the following characters: ')+'%s'%OK_PASSWORD_CHARS
    return True,''

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    if 'star' in group_names:
        login_url='/star/login/'
    elif 'nc' in group_names:
        login_url='/'
    elif 'staradmin' in group_names:
        login_url='/star/login/'
    elif 'ncadmin' in group_names:
        login_url='/admin/'
    elif 'sales' in group_names:
        login_url='/admin/'
    else:
        #logger.error('there was an error in group_required. for groups %s'%str(group_names))
        #import traceback
        #logger.error(traceback.format_exc())
        login_url='/'
    #also redirects them to the proper group login.... assuming
    #we even want to keep multiple login pages for the separate groups.
    return user_passes_test(in_groups, login_url)

def mk_default_field(vals):
    """within a given klass (which is a subset of admin.ModelAdmin),
    return a function which, if assigned the name 'formfield_for_dbfield',
    will make the fields listed in vals default to their value there - either the raw val
    or function call"""
    def inner(self, db_field, **kwargs):
        if db_field.name in vals:
            th=vals[db_field.name]
            if hasattr(th, '__call__'):
                kwargs['initial']=th()
            else:
                kwargs['initial']=th
            kwargs.pop('request')
            ff=db_field.formfield(**kwargs)
            if db_field.name=='created':
                ff.widget.attrs={'class':'vDateField'}
                #omg, can't believe this works.
            return ff
        return super(self.__class__, self).formfield_for_dbfield(db_field, **kwargs)
    return inner

def mk_default_fkfield(vals):
    def inner(self, db_field, **kwargs):
        if db_field.name in vals:
            th=vals[db_field.name]
            if hasattr(th, '__call__'):
                kwargs['initial']=th()
            else:
                kwargs['initial']=th
            return db_field.formfield(**kwargs)
    return inner

def nowdate():
    from choices import DATE
    return datetime.datetime.now().strftime(DATE)

def rstripz(x, bold=False):
    if bold:
        return ('<b>%0.1f'%x).rstrip('0').rstrip('.')+'</b>'
    return ('%0.1f'%x).rstrip('0').rstrip('.')

def rstripzb(x):
    return rstripz(x, bold=True)

def staff_test(user):
    return user and user.is_authenticated() and user.is_staff

def r2r(template, request, context=None, lang=None):
    if not context:
        context={}
    from coffin.shortcuts import render_to_response
    return render_to_response(template, context, RequestContext(request))

def r2s(template, context=None):
    from coffin.shortcuts import render_to_string
    return render_to_string(template, dictionary=context)

def r2j(res):
    from django.shortcuts import HttpResponse, HttpResponseRedirect
    return HttpResponse(json.dumps(res), mimetype='application/json')

def humanize_date(dt, nopast=False):
    '''if nopast, then for past days just always give the date.
    this also shows the year if it's in not the current app year.'''
    from choices import HUMANIZE_DATE, HUMANIZE_DATE_YEAR, HOUR_MIN_M
    if type(dt) == datetime.date:
        dt = datetime.datetime(year=dt.year, day=dt.day, month=dt.month)
    if dt:
        age=datetime.datetime.now()-dt
        if age.days<1 and (nopast and age.days>0):
            hours=age.seconds/3600
            if hours>0:
                if hours==1:
                    return '%d hour ago'%hours
                else:
                    return '%d hours ago'%hours
            minutes=age.seconds/60
            if minutes>0:
                if minutes==1:
                    return '%d minute ago'%minutes
                else:
                    return '%d minutes ago'%minutes
            else:
                return 'Just Now'
            return dt.strftime(HOUR_MIN_M)
        else:
            res=dt.strftime(HUMANIZE_DATE_YEAR)
            if res[-2]=='0':
                res=res[:-2]+res[-1]
            return res
    else:
        return ''

def get_nested_objects(obj):
    from django.contrib.admin.util import NestedObjects
    collector = NestedObjects(using='default')
    collector.collect([obj])
    return collector.nested()

def ipdb():
    import inspect
    try:
        par = inspect.stack()[1]
        desc = '%s line:%s' % (par[1], [par[2]])
    except:
        log.error('failed to inspect stack.')
        import ipdb;ipdb.set_trace()
        desc='failed to inspect stack.'
    if settings.LOCAL:
        log.error('missed ipdb call. %s', desc)
        import ipdb;ipdb.set_trace()
    else:
        log.error('missed ipdb call. %s', desc)


def get_contenttype(model):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(model)

def make_le(request, obj, change_message, action_flag=2):
    from django.contrib.admin.models import LogEntry
    from day.models import User
    '''make logentry.'''
    try:
        if request is None:
            user = User.objects.filter(username='ernie')[0]
            ip=''
            if not obj:
                class Bag():
                    pass
                obj=Bag()
                obj.id=None
            if obj.__class__ == user.__class__:
                user = obj
            #just user ernie
            content_type=None
        else:
            user = request.user
            ip = request.META['REMOTE_ADDR']
            content_type = get_contenttype(obj.__class__)
        if user.is_anonymous():
            log.info('anon user did an action, saving as ernie.')
            user = User.objects.get(username='ernie')
        object_id = obj.id
        object_repr = str(obj)
        le = LogEntry(user=user, content_type=content_type, object_id=object_id, object_repr=object_repr, action_flag=action_flag, change_message=change_message)
        le.save()
    except Exception, e:
        log.error(e)
        ipdb()

def sqlp(statement):
    import sqlparse
    res = sqlparse.format(statement, reindent=True)
    print res


def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)