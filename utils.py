import urllib, urlparse, re, os, ConfigParser, logging, uuid, logging.config

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
        logger.error('there was an error in group_required. for groups %s'%str(group_names))
        import traceback
        logger.error(traceback.format_exc())
        login_url='/'
    #also redirects them to the proper group login.... assuming
    #we even want to keep multiple login pages for the separate groups.
    return user_passes_test(in_groups, login_url)