import urllib, urlparse, re, os, ConfigParser, logging, uuid, logging.config, types, datetime, json, calendar,random
from django.conf import settings
log=logging.getLogger(__name__)

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
        return False,'no password provided'
    if len(pw)<4:
        return False, 'password too short'
    forbidden=set()
    for c in pw:
        if c not in OK_PASSWORD_CHARS:
            forbidden.add(c)
    if forbidden:
        return False,'password contains forbidden characters'+ '%s'%''.join(forbidden)+'. '+'Passwords may only contain the following characters: '%OK_PASSWORD_CHARS
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
    from jinja2.environment import re
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
        from util import ipdb;ipdb()
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

def make_safe_tag_name(ss):
    res = []
    OKS = ['-', '_', ' ']
    ss=ss.replace('_','-')
    for c in ss:
        if (c.isalnum() and ord(c)<=122) or c in OKS:
            res.append(c)
    combo=''.join(res)
    combo=combo.lower()
    return combo

def make_safe_filename(fn):
    res = []
    rawfn,ext=os.path.splitext(fn)
    OKS = ['-', '_', ]
    rawfn=rawfn.replace('_','-').replace('\'','-')
    for c in rawfn:
        if (c.isalnum() and ord(c)<=122) or c in OKS:res.append(c)
    newfn=''.join(res)
    res=newfn+ext
    return res

def staff_test(user):
    return user and user.is_authenticated() and (user.is_superuser or user.is_staff)

def is_secure_path(path):
    import posixpath
    path = posixpath.normpath(path)
    return not path.startswith(('/', '../'))

def icon(val,yes_word=None, no_word=None):
    from choices import YES_ICON, NO_ICON
    if yes_word and val:
        return YES_ICON+' '+yes_word
    if no_word and not val:
        return NO_ICON+' '+no_word
    return val and YES_ICON or NO_ICON

def humanize_size(sz):
    sz=int(sz)
    if not sz:
        return ''
    if sz<1000:
        return str(sz)
    elif sz<1000000:
        return '%0.1fk'%(sz*1.0/1000)
    elif sz<1000000000:
        return '%0.1fm'%(sz*1.0/1000000)

def user_passes_test(test_func, login_url=None):
    from functools import wraps
    from django.utils.decorators import available_attrs
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            from django.shortcuts import HttpResponseRedirect
            from django.conf import settings
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                        settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            if request.path:
                extra = '?next=%s'% request.path
            else:extra = ''
            return HttpResponseRedirect('/')
        return _wrapped_view
    return decorator

    
def staff_test(user):
    return user and user.is_authenticated() and user.is_staff

def group_day_dat(data, by=None,mindate=None):
    from choices import DATE,MONTH_YEAR,YEAR_MONTH
    if type(mindate)==datetime.date:
        mindate=datetime.datetime.strftime(mindate,DATE)
    adder_day=0
    adder_month=0
    adder_year=0
    first=datetime.datetime.strptime(mindate, DATE)
    now=datetime.datetime.now()
    start=mindate
    res2=[]
    
    if not by:
        by='day'
    if by=='day':
        adder_day=1
        #move start back to the monday
        first=first.date()
    elif by=='week':
        adder_day=7
        #move start back to the monday
        while first.weekday()!=6:
            first=first-datetime.timedelta(days=1)
        first=first.date()
    elif by=='month':
        adder_month=1
        #move start back to the 1st of the month
        first=datetime.date(year=first.year,month=first.month,day=1)
    elif by=='year':
        adder_month=12
        #move start back to jan 1
        first=datetime.date(year=first.year,month=1,day=1)
    
    #start correctly defined, and the interval defined.    
    trying=first
    while 1:
        #for every interval
        thisinterval_start=trying
        thisinterval_total=0
        next_interval_start=add_months(trying,adder_month)
        next_interval_start=next_interval_start+datetime.timedelta(days=adder_day)
        while 1:
            #for every day within it.
            thisinterval_total+=data.get(trying.strftime(DATE),0)
            trying=trying+datetime.timedelta(days=1)
            if trying>=next_interval_start:
                break
        label=thisinterval_start.strftime(DATE)
        if by=='month':
            label=thisinterval_start.strftime(YEAR_MONTH)
        res2.append((thisinterval_total,label))
        if trying>now.date():
            break
    return res2
    
    
def insert_defaults():
    from day.models import *
    for name,symbol,val in settings.DEFAULT_CURRENCIES:
        cc=Currency(name=name,symbol=symbol,rmb_value=val)
        cc.save()
    for name in settings.DEFAULT_DOMAINS:
        dd=Domain(name=name)
        dd.save()
    for name,curname in settings.DEFAULT_REGIONS:
        rr=Region(name=name,currency=Currency.objects.get(name=curname))
        rr.save()
    name2id={}    
    for fn,ln,mt,gender in settings.DEFAULT_PEOPLE:
        pp=Person(first_name=fn,last_name=ln,gender=gender)
        pp.save()
        name2id[pp.first_name]=pp.id
        if mt:
            for personname in mt:
                otherperson=Person.objects.get(id=name2id[personname])
                pp.met_through.add(otherperson)
    for name,dname in settings.DEFAULT_PRODUCTS:
        #print name,dname
        pp=Product(name=name, domain=Domain.objects.get(name=dname))
        pp.save()
    for name in settings.DEFAULT_PHOTOTAGS:
        pt=PhotoTag(name=name)
        pt.save()
        
def nice_sparkline(results,width,height):
    '''a better one, results now consists of value & label'''
    '''stick the labels for x into labels[rnd]
    
    to produce: make {'2014-05-24': 15.0, '2014-05-21': 155.0}
    then produce results with costres2=group_day_dat(costres, by='month',mindate=mindate)
    
    '''
    ii=0
    num_results=[]
    labels={}
    for total,label in results:
        label+=' %d'%two_sig(total)
        labels[ii]=label
        ii+=1
        num_results.append(total)
    data=','.join([str(s) for s in num_results])
    rnd=str(int(random.random()*100000))
    res = '<div sparkid="%s" class="sparkline-data">%s</div>'%(rnd,data)    
    res+='<script>$(document).ready(function(){labels[%s]=%s});</script>'%(rnd,json.dumps(labels))
    return res
    
    
def simple_sparkline(results, width, height):
    #itd be nice if this was way better for labelling and stuff.
    res = '<div class="simple-sparkline-data">%s</div>'%(','.join([str(s) for s in results]))
    return res

def two_sig(n):
    #round to the left two significant digits.
    ct=0
    orign=n
    while n>1:
        n=n/10
        ct+=1
    return round(orign,-1*(ct-2))

        
def get_span_created_photos(start, end, user=None):
    res=[]
    from day.photomodels import Photo
    photos=Photo.objects.filter(deleted=False, incoming=False, photo_created__gte=start, photo_created__lt=end)
    photos=photos.order_by('photo_created')
    for ph in photos:
        if user:
            if ph.can_be_seen_by(user):
                res.append(ph)
        else:
            if ph.can_be_seen_by(user=None):
                res.append(ph)
    return res
    
def get_span_tags(start, end, user=None):
    photos=get_span_created_photos(start, end,user=user)
    tag_counts={}
    for photo in photos:
        tags=photo.tags.all()
        for tag in tags:
            if tag.tag.name in settings.EXCLUDE_FROM_PHOTOSET_TAGS:
                continue
            name=tag.tag.name
            if tag.tag not in tag_counts:
                tag_counts[tag.tag]=0
            tag_counts[tag.tag]+=1
            #tag_counts[tag]=tag_counts.get(tag,0)+1
    res=sorted(tag_counts.items(),key=lambda x:(-1*x[1]))
    res=[s for s in res if s[1]>2]
    return res

def prespan(contents):
    return '<span class="pre">%s</span>'%contents


def gender2id(txt):
    txt=txt.lower()
    if txt=='male':return 1
    if txt=='female':return 2
    if txt=='organization':return 3
    return 0