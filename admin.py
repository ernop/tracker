import datetime, tempfile, shutil, os

from django import forms
from django.contrib import admin, messages
from django.conf import settings
from django.db.models import Sum
from django.forms.models import BaseModelFormSet, BaseInlineFormSet

#import djangoplus.widgets
#from spark import *
LG=[700, 427]
MED=[340,200]
SM=[200,100]
from choices import *
from trackerutils import *
from utils import *
from day.models import *
#from tracker.utils import adminify, mk_default_field, nowdate, rstripz, mk_default_fkfield, rstripzb
from admin_helpers import *

RMBSYMBOL=Currency.objects.get(id=1).symbol
class PurchaseForm(forms.ModelForm):
    who_with=forms.ModelMultipleChoiceField(queryset=Person.objects.all(), widget=FilteredSelectMultiple("name", is_stacked=False), required=False)
    class Meta:
        model = Purchase

def chart_url(dat, size=None, text=None):
    if text is None:
        text = 'Sources'
    dat=[d for d in dat if d[0] > 0]
    dat.sort(key=lambda x:x[0])
    values = ','.join([str(s[0]) for s in dat])
    offsets= ','.join(['%s (%s)'%(s[1], str(s[0])) for s in dat])
    res = '<h3>%s</h3><div class="piespark" values="%s" labels="%s"></div>' % (text, values, offsets)
    return res

class BetterDateWidget(admin.widgets.AdminDateWidget):
    def render(self, name, value, attrs=None):
        return super(BetterDateWidget, self).render(name, value)

class OverriddenModelAdmin(admin.ModelAdmin):
    """normal, except overrides some widgets."""
    formfield_overrides = {
        #models.DateTimeField: {'widget': admin.widgets.AdminDateWidget,},
        #models.DateField: { 'widget': admin.widgets.AdminDateWidget,},
        #models.DateTimeField: {'widget': BetterDateWidget,},
        #models.DateField: { 'widget': BetterDateWidget,},
    }

    def _media(self):
        from django.forms import Media
        js = ("/static/admin/js/core.js","/static/admin/js/admin/RelatedObjectLookups.js",
              '/static/admin/js/jquery.js',"/static/admin/js/jquery.init.js",
              "/static/admin/js/actions.js",
              '/static/admin/js/calendar.js',
              '/static/admin/js/admin/DateTimeShortcuts.js',
              '/static/js/jquery-1.7.2.min.js',
              '/static/js/DjangoAjax.js',
              '/static/js/jquery.sparkline.min.js',
              '/static/js/admin_init.js',
              )
        med=Media(js=js)
        return med

    media=property(_media)

    def changelist_view(self, request, extra_context=None):
        #the way searches work in django is fucking stupid.
        #when you view by ID and then apply a filter/search it doesn't cancel the previous ID.  so you get no results
        #and confuse yourself.
        if request.GET.has_key('id'):
            #delete id parameter if there are other filters! yes!
            real_keys = [k for k in request.GET.keys() if k not in getattr(self, 'not_count_filters', [])]
            if len(real_keys) != 1:
                q = request.GET.copy()
                del q['id']
                request.GET = q
                request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(OverriddenModelAdmin,self).changelist_view(request, extra_context=extra_context)

def new_sparkline(results, width, height):
    res = '<div class="sparkline-data">%s</div>'%(','.join([str(s) for s in results]))
    return res

class ProductAdmin(OverriddenModelAdmin):
    search_fields = ['name', ]
    list_display='name mydomain mypurchases mysources mywith myspark'.split()
    list_per_page = 10
    list_filter = ['domain', ]

    def mydomain(self, obj):
        return obj.domain.clink()

    def mypurchases(self, obj):
        #return obj.summary()
        links = '<br>'.join([p.clink() for p in Purchase.objects.filter(product=obj)])
        alllink = '<a class="btn" href="../purchase/?product_id=%d">all</a>' % obj.id
        filters = ''

        return links + '<br><br>' + '<br>' + alllink

    def myspark(self, obj):
        purch=Purchase.objects.filter(product=obj)
        if not purch:
            spark= ''
        else:
            mindate=None
            res={}
            costres = {}
            for pu in purch:
                date=pu.created.strftime(DATE)
                res[date]=res.get(date, 0)+pu.quantity
                costres[date] = costres.get(date, 0) + pu.get_cost()
                if not mindate or date<mindate:
                    mindate=date
            first=datetime.datetime.strptime(mindate, DATE)
            now=datetime.datetime.now()
            trying=first
            res2=[]
            costres2 = []
            while trying<now:
                dt = trying.strftime(DATE)
                res2.append((res.get(dt, 0)))
                costres2.append((costres.get(dt, 0)))
                trying=datetime.timedelta(days=1)+trying
            counts = new_sparkline(results=res2, width=5, height=30)
            costs = new_sparkline(results=costres2, width=5, height=30)
            return 'Counts %s<br>Costs%s' % (counts, costs)
            #tmp=savetmp(im)
            #spark='<img style="border:2px solid grey;"  src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])

    def mywith(self, obj):
        res = {}
        ps = Purchase.objects.filter(product=obj)
        for p in ps:
            for person in p.who_with.all():
                cl = person.clink()
                res[cl] = res.get(cl, 0) + 1
        tbl = mktable(sorted(res.items(), key=lambda x:(-1*x[1], x[0])))
        return tbl
        #res = ', '.join(['%s%s'%(th[0], (th[1]!=1 and '(%d)'%th[1]) or '') for th in sorted(res.items(), key=lambda x:(-1*x[1], x[0]))])
        #return res

    @debu
    def mysources(self, obj):
        #return ''
        purch=Purchase.objects.filter(product=obj)

        pie=''
        sources=Source.objects.filter(purchases__product=obj).distinct()
        dat=[(ss.total_spent(product=obj), str(ss)) for ss in sources]


        #ss=Source.objects.filter(purchases__product__domain=obj).distinct()


        dat.sort(key=lambda x:x[0])
        lifevalues = ','.join([str(s[0]) for s in dat])
        lifeoffsets = ','.join(['%s (%s)'%(s[1], str(s[0])) for s in dat])
        liferes = '<h3>Sources</h3><div class="piespark" values="%s" labels="%s"></div>' % (lifevalues, lifeoffsets)

        res = {}
        for p in purch:
            cl = p.source.id
            res[cl] = res.get(cl, 0) + 1

        ss = Source.objects.filter(purchases__product=obj).distinct()
        filters = []
        res = sorted(res.items(), key=lambda x:(-1*x[1], x[0]))
        for n in range(len(res)):
            source = Source.objects.get(id=res[n][0])
            res[n] = res[n] + ('<a class="nb" href="/admin/day/purchase/?product__id=%d&source=%d">filter</a>'%(obj.id, source.id), )
            res[n] = (source.clink(), ) + res[n][1:]



        tbl = mktable(res)
        #sourcefilters = ', '.join(['%s%s'%(th[0], (th[1]!=1 and '(%d)'%th[1]) or '') for th in sorted(res.items(), key=lambda x:(-1*x[1], x[0]))])

        return liferes + '<br>' + tbl

    adminify(mysources, mypurchases, mydomain, myspark, mywith)

class PurchaseAdmin(OverriddenModelAdmin):
    list_display='id myproduct mydomain mycost mysource size mywho_with mycreated note'.split()
    list_filter=' product__domain currency source who_with'.split()
    date_hierarchy='created'
    list_editable=['note',]
    search_fields= ['product__name']
    form=PurchaseForm
    list_per_page = 20
    def mysource(self, obj):
        return obj.source.clink()

    def mycreated(self, obj):
        return '<a href="/admin/day/purchase/?created__day=%d&created__month=%d&created__year=%d">%s</a>'%(obj.created.day, obj.created.month, obj.created.year, obj.created.strftime(DATE))

    @debu
    def mycost(self, obj):
        costper=''
        if obj.quantity>1:
            costper=' (%s, %s%s each)'%(rstripz(obj.quantity), rstripz(float(obj.cost)/obj.quantity), obj.currency.symbol)
        #if float(int(obj.cost))==obj.cost:
            #return '%d%s%s'%(rstripz(obj.cost), obj.currency.symbol, costper)
        return '%s%s%s'%(rstripzb(float(obj.cost)), obj.currency.symbol, costper)

    def myproduct(self, obj):
        return obj.product.clink()

    def mywho_with(self, obj):
        return ', '.join([per.clink() for per in obj.who_with.all()])

    def mydomain(self, obj):
        return '<a href=/admin/day/domain/?id=%d>%s</a>'%(obj.product.domain.id, obj.product.domain)

    adminify(mycost, myproduct, mywho_with, mydomain, mycreated, mysource)
    mywho_with.display_name='Who With'
    formfield_for_dbfield=mk_default_field({ 'quantity':1,'created':datetime.datetime.now, 'currency':1}) #'hour':get_named_hour
    formfield_form_foreignkey=mk_default_fkfield({'currency':1,'hour':gethour,})
    fields='product cost source size quantity created hour who_with note currency '.split()

class DomainAdmin(OverriddenModelAdmin):
    list_display='id myproducts mypie mysource'.split()
    list_filter=['name',]

    def mypie(self, obj):
        res=''
        if obj.products.count()>1:
            dat=[(p.total_spent(), str(p)) for p in obj.products.all()]
            dat.sort(key=lambda x:x[0])
            monthdat=[(p.total_spent(start=monthago()),str(p)) for p in obj.products.all()]
            monthdat.sort(key=lambda x:x[0])
        else:
            dat = []
            monthdat = []
        lifevalues = ','.join([str(s[0]) for s in dat])
        lifeoffsets = ','.join(['%s (%s)'%(s[1], str(s[0])) for s in dat])
        liferes = '<h3>Lifetime</h3><div class="piespark" values="%s" labels="%s"></div>' % (lifevalues, lifeoffsets)

        monthvalues = ','.join([str(s[0]) for s in monthdat])
        monthoffsets = ','.join(['%s (%s)'%(s[1], str(s[0])) for s in monthdat])
        monthres = '<h3>Last Month</h3><div class="piespark" values="%s" labels="%s"></div>' % (monthvalues, monthoffsets)

        return liferes + '<br>' + monthres

    def myproducts(self, obj):
        total=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(product__domain=obj).aggregate(Sum('cost'))['cost__sum']#.filter(created__gte=sixmonthago)
        ear=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(product__domain=obj).order_by('created')
        earliest=None
        if ear:
            earliest=datetime.datetime.combine(ear[0].created, datetime.time())
        else:
            total= ''
        if total and ear:
            now=datetime.datetime.now()
            dayrange= abs((now-earliest).days)+1
            total='%s%s<br>%s%s/day<br>(%d days)'%(rstripz(total), RMBSYMBOL, rstripz(total/dayrange), RMBSYMBOL, dayrange)
        purch=Purchase.objects.filter(product__domain=obj)
        if not purch:
            costs=''
        else:
            mindate=None
            res={}
            for pu in purch:
                date=pu.created.strftime(DATE)
                res[date]=res.get(date, 0)+pu.get_cost()
                if not mindate or date<mindate:
                    mindate=date
            first=datetime.datetime.strptime(mindate, DATE)
            now=datetime.datetime.now()
            trying=first
            res2=[]
            while trying<now:
                res2.append((res.get(trying.strftime(DATE), 0)))
                trying=datetime.timedelta(days=1)+trying
            costs= new_sparkline(results=res2, width=2, height=100)
            #tmp=savetmp(im)
            #graph='<img style="border:2px solid grey;" src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])
        summary=obj.summary()
        return '<h2>%s</h2>%s<br>%s<br>%s<br>'%(obj.name, total, costs, summary)

    def mysource(self, obj):
        """in the last month"""
        #-------------------------------source pie
        ss=Source.objects.filter(purchases__product__domain=obj).distinct()

        dat=[(s.total_spent(domain=obj), s.name) for s in ss]
        dat.sort(key=lambda x:x[0])
        lifevalues = ','.join([str(s[0]) for s in dat])
        lifeoffsets = ','.join(['%s (%s)'%(s[1], str(s[0])) for s in dat])
        liferes = '<h3>Sources</h3><div class="piespark" values="%s" labels="%s"></div>' % (lifevalues, lifeoffsets)
        return liferes

    def my_month_history(self, obj):
        purchases=Purchage.objects.filter()

    def mycreated(self, obj):
        return obj.created.strftime(DATE)
    adminify(myproducts, mysource, mycreated, mypie)

class PersonAdmin(OverriddenModelAdmin):
    list_display='id myinfo disabled birthday created mymet_through myintroduced_to mywith mysources mydomains mypurchases'.split()
    list_filter=[GenderFilter, AnyPurchaseFilter,KnownSinceLongAgo, 'met_through']
    date_hierarchy = 'created'
    list_editable=['birthday',  'disabled']
    list_per_page = 10
    search_fields = 'first_name last_name'.split()
    actions = ['disable','male','female','organization', 'set_longago', 'set_today', ]

    def set_longago(self, request, queryset):
        for person in queryset:
            person.created = settings.LONG_AGO
            person.save()

    def set_today(self, request, queryset):
        for person in queryset:
            person.created = datetime.datetime.today()
            person.save()

    def organization(self,request,queryset):
        for pp in queryset:
            pp.gender=3
            pp.save()

    def male(self,request,queryset):
        for pp in queryset:
            pp.gender=1
            pp.save()

    def female(self,request,queryset):
        for pp in queryset:
            pp.gender=2
            pp.save()

    def myinfo(self,obj):
        if obj.created == settings.LONG_AGO:
            known_for = 'long ago'
        else:
            known_for = humanize_date(obj.created)
        return '%s %s %s<br>known since %s'%(obj.first_name, obj.last_name, obj.get_gender(), known_for)

    def disable(self, request, queryset):
        for pp in queryset:
            pp.disabled = True
            pp.save()
            messages.info(request, 'disabled %s'%pp)

    def mymet_through(self, obj):
        return ', '.join([p.clink() for p in obj.met_through.all()])
        #return '%s'%''.join([str(per) for per in obj.met_through.all()])

    def myintroduced_to(self, obj):
        #import ipdb;ipdb.set_trace()
        return mktable([(p.clink(), ) for p in obj.introduced_to.order_by('first_name', 'last_name')])

    @debu
    def mywith(self, obj):
        counts = {}
        costs = {}
        ps = obj.purchases.all()
        for p in ps:
            togethercount = p.who_with.count()
            for person in p.who_with.exclude(id=obj.id):
                counts[person.id] = counts.get(person.id, 0) + 1
                costs[person.id] = costs.get(person.id, 0) + (p.get_cost() / togethercount)
        bits = [(Person.objects.get(id=p).clink(), counts[p], '%0.1f' % costs[p]) for p in counts.keys()]
        tbl = mktable(sorted(bits, key=lambda x:-1*x[1]))
        return tbl

    def mysources(self, obj):
        #import ipdb;ipdb.set_trace()
        res = {}
        ps = Purchase.objects.filter(who_with=obj)
        for p in ps:
            cl = p.source.clink()
            res[cl] = res.get(cl, 0) + 1
        #res = ', '.join(['%s%s'%(th[0], (th[1]!=1 and '(%d)'%th[1]) or '') for th in sorted(res.items(), key=lambda x:(-1*x[1], x[0]))])
        tbl = mktable(sorted(res.items(), key=lambda x:(-1*x[1], x[0])))
        return tbl
        #return res

    def mypurchases(self, obj):
        alllink = '<a href=/admin/day/purchase/?who_with=%d>all</a>' % obj.id
        purch = Purchase.objects.filter(who_with=obj)
        res = {}
        counts = {}
        costs = {}
        for p in purch:
            counts[p.product.id] = counts.get(p.product.id, 0) + 1
            costs[p.product.id] = costs.get(p.product.id, 0) + p.cost
        bits = []
        doneprod = set()
        for p in purch:
            if p.product.id in doneprod:
                continue
            doneprod.add(p.product.id)
            bits.append([counts[p.product.id], p.product.clink(), '<a href="../purchase/?product_id=%d&who_with=%d">%d (%0.1f)</a>' % (p.product.id, obj.id, counts[p.product.id], costs[p.product.id])])
        bits.sort(key=lambda x:-1*x[0])
        bits = [b[1:] for b in bits]
        tbl = mktable(bits)
        return tbl + '<br>' + alllink
        #prods = ', '.join(['%s%s'%(th[0], (th[1]!=1 and '(%d)'%th[1]) or '') for th in sorted(res.items(), key=lambda x:(-1*x[1], x[0]))])
        #return prods + '<br>' + alllink

    def mydomains(self, obj):
        res = obj.domain_summary_data()
        #count, costs
        counts, costs = res['counts'], res['costs']
        html = '<table class="table thintable">'
        #import ipdb;ipdb.set_trace()
        rows = []
        for domain_id in counts.keys():
            row = '<tr><td>%s<td><a href="../purchase/?product__domain__id=%d&who_with=%d">%s times</a><td>cost: %s' % (Domain.objects.get(id=domain_id).name, domain_id, obj.id, counts[domain_id], costs[domain_id])
            rows.append([counts[domain_id], row])
        rows.sort(key=lambda x:-1*x[0])
        rows = [r[1] for r in rows]
        html += '\n'.join(rows)
        html += '</table>'
        return html


    adminify(mymet_through, myintroduced_to, mysources, mypurchases, myinfo, mydomains, mywith)

class CurrencyAdmin(OverriddenModelAdmin):
    list_display='name rmb_value symbol mytotal my3months'.split()
    list_editable = ['rmb_value', ]
    def mytotal(self, obj):
        total=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(source=obj).aggregate(Sum('cost'))['cost__sum']
        cre=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(source=obj).order_by('created')
        earliest=None
        if cre:
            earliest=datetime.datetime.combine(cre[0].created, datetime.time())
        if total and cre:
            now=datetime.datetime.now()
            dayrange=(abs((now-earliest).days)+1)
            return '%0.0f<br>%0.2f/day<br>(%d days)'%(total, total/dayrange, dayrange)

    def my3months(self, obj):
        monthago=datetime.datetime.now()-datetime.timedelta(days=30)
        total=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(source=obj).filter(created__gte=monthago).aggregate(Sum('cost'))['cost__sum']
        cre=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(source=obj).order_by('created')
        earliest=None
        if cre:
            earliest=datetime.datetime.combine(cre[0].created, datetime.time())
        if total and earliest:
            now=datetime.datetime.now()
            dayrange=min(90.0,(abs((now-earliest).days))+1)
            return '%0.0f<br>%0.2f /day<br>(%d days)'%(total, total/dayrange, dayrange)

    adminify(mytotal, my3months)

class RegionAdmin(OverriddenModelAdmin):
    list_display = 'name currency mysources'.split()
    list_per_page = 10
    search_fields = ['name', ]
    actions = []

    def mysources(self, obj):
        myobjs = Source.objects.filter(region=obj)
        links = ', '.join([source.clink() for source in myobjs[:10]])
        return '%s (%d total)' % (links, myobjs.count())

    adminify(mysources)

class SourceAdmin(OverriddenModelAdmin):
    list_display='name mytotal myproducts mywith mysummary mydomains myregion'.split()
    list_per_page = 10
    list_filter = ['region', ]
    search_fields = ['name', ]
    actions = []

    actions = ['set_beijing', 'set_tokyo', 'set_slo']

    def make_assign_function(region_name):
        def func(self, request, queryset):
            for obj in queryset:
                obj.region = Region.objects.get(name=region_name)
                obj.save()
        return func

    set_beijing = make_assign_function('beijing')
    set_tokyo= make_assign_function('tokyo')
    set_slo = make_assign_function('slo')

    def myregion(self, obj):
        if obj.region:
            return obj.region.clink()
        return ''

    #_g = globals()
    #import ipdb;ipdb.set_trace()


    #for region in Region.objects.all():
        #funcname = 'assign_to_%s'%region.name.lower()
        #actions.append(funcname)
        #func = make_assign_function(region.name.lower())
        #func.__name__ = str(funcname)
        #_g[funcname] = func

    def myproducts(self, obj):
        products=Product.objects.filter(purchases__source=obj).distinct()
        dat=[(oo.total_spent(source=obj),str(oo)) for oo in products]
        return chart_url(dat, text='')

    def mydomains(self, obj):
        res = obj.domain_summary_data()
        #count, costs
        counts, costs = res['counts'], res['costs']
        html = '<table class="table thintable">'
        #import ipdb;ipdb.set_trace()
        rows = []
        for domain_id in counts.keys():
            row = '<tr><td>%s<td>%s times<td>cost: %s' % (Domain.objects.get(id=domain_id).name, counts[domain_id], costs[domain_id])
            rows.append([counts[domain_id], row])
        rows.sort(key=lambda x:-1*x[0])
        rows = [r[1] for r in rows]
        html += '\n'.join(rows)
        html += '</table>'
        return html

    def mysummary(self, obj):
        return obj.summary()

    @debu
    def mywith(self, obj):
        res = {}
        ps = Purchase.objects.filter(source=obj)
        for p in ps:
            for person in p.who_with.all():
                cl = person.clink()
                res[cl] = res.get(cl, 0) + 1
        tbl = mktable(sorted(res.items(), key=lambda x:(-1*x[1], x[0])))
        return tbl
    @debu
    def mytotal(self, obj):
        #monthago=datetime.datetime.now()-datetime.timedelta(days=30)
        purchases=Purchase.objects.filter(currency_id__in=RMB_CURRENCY_IDS).filter(source=obj).order_by('created')
        total=purchases.aggregate(Sum('cost'))['cost__sum']
        if purchases:
            earliest=datetime.datetime.combine(purchases[0].created, datetime.time())

        if total and earliest:
            dayrange=abs((datetime.datetime.now()-earliest).days)+1
            return '<div class="nb">%0.0f%s<br>%s%s /day<br>(%d days)</div>'%(total, RMBSYMBOL, rstripz(total/dayrange), RMBSYMBOL, dayrange)

    adminify(mytotal, mysummary, myproducts, mywith, myregion, mydomains)

class PMuscleInline(admin.StackedInline):
    model = Exercise.pmuscles.through

class SMuscleInline(admin.StackedInline):
    model = Exercise.smuscles.through

class SetInline(admin.StackedInline):
    model=Workout.exweights.through
    extra=12

class ExerciseAdmin(OverriddenModelAdmin):
    list_display='id name myhistory barbell'.split()
    inlines=[
        PMuscleInline,
        SMuscleInline,
    ]
    exclude=['pmuscles','smuscles',]

    def mymuscles(self, obj):
        return 'primary:%s\n<br>synergists:%s'%(', '.join([m.clink() for m in obj.pmuscles.all()]),', '.join([m.adm() for m in obj.smuscles.all()]))

    def get_changelist_form(self, request, **kwargs):
        kwargs.setdefault('form', ApplicantForm)
        return super(ApplicantAdmin, self).get_changelist_form(request, **kwargs)

    #def myspark(self, obj):
        #past=[]
        #res={}
        #mindate=None
        #zets=Set.objects.filter(exweight__exercise=obj).order_by('-workout__created')
        #if not zets:
            #return ''
        #for zet in zets:
            ##past.append((zet.workout.date, zet.count, zet.exweight.weight))
            #date=zet.workout.created.strftime(DATE)
            #res[date]=max(res.get(date, 0), zet.exweight.weight)
            #if not mindate or date<mindate:
                #mindate=date
        #first=datetime.datetime.strptime(mindate, DATE)
        #now=datetime.datetime.now()
        #trying=first
        #res2=[]
        #while trying<now:
            #res2.append((res.get(trying.strftime(DATE), 0)))
            #trying=datetime.timedelta(days=1)+trying
        #im=sparkline_discrete(results=res2, width=5, height=200)
        ##tmp=savetmp(im)
        #return '<img style="border:2px solid grey;" src="/static/sparklines/%s">'%(tmp.name.split('/')[-1])


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

    adminify(mymuscles, myhistory)

class SetAdmin(OverriddenModelAdmin):
    list_display='exweight count workout note'.split()
    create_date=models.DateTimeField(auto_now_add=True)

class ExWeightAdmin(OverriddenModelAdmin):
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

class MuscleAdmin(OverriddenModelAdmin):
    list_display='id name myexercises'.split()
    list_editable=['name',]

    def myexercises(self, obj):
        return '%s<br>\n%s'%(','.join([ex.clink() for ex in obj.primary_exercises.all()]), ','.join([ex.adm() for ex in obj.synergists_exercises.all()]))

    adminify(myexercises)

class WorkoutForm(forms.ModelForm):
    class Meta:
        model=Workout

    def __init__(self, *args, **kwgs):
        super(WorkoutForm, self).__init__(*args, **kwgs)

    def clean_date(self):
        pass

    def clean(self):
        if self.is_bound:
            if self.instance.created is None:
                self.instance.created=datetime.datetime.now()
                self.cleaned_data['created']=datetime.datetime.now()
        super(WorkoutForm, self).clean()
        return self.cleaned_data

class WorkoutAdmin(OverriddenModelAdmin):
    list_display='mycreated mysets'.split()
    inlines=[SetInline,]
    #form=WorkoutForm#unnecessary
    def mysets(self, obj):
        return obj.mysets()


    def mycreated(self, obj):
        return obj.created.strftime(DATE)
    formfield_for_dbfield=mk_default_field({'created':nowdate,})
    adminify(mycreated, mysets)

linesample = lambda m, n: [i*n//m + n//(2*m) for i in range(m)]
class MeasuringSpotAdmin(OverriddenModelAdmin):
    list_display='myname myhistory'.split()
    list_filter=['domain',]
    def myname(self, obj):
        ct=obj.measurements.all()
        if obj.exclude_zeros:
            ct=ct.exclude(amount=0)
        ll=len(ct)
        if ll>28:
            indexes=linesample(6,len(ct[2:]))+[len(ct)-1]
            ct=ct[:2]+[ct[th] for th in indexes]
        meas='<br>'.join([m.clink() for m in ct])
        return '<h3>%s</h3><h4>%s</h4>%s'%(obj.name, obj.domain.clink(), meas)

    def myhistory(self, obj):
        mes=obj.measurements.all()
        if obj.exclude_zeros:
            mes=mes.exclude(amount=0)
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
        lastt=None
        while trying<now:
            if trying.strftime(DATE) in res:
                lastt=res.get(trying.strftime(DATE))
            res2.append(lastt)
            trying=datetime.timedelta(days=1)+trying
        thang = new_sparkline(results=res2, width=2, height=100)
        return '<div>%s</div>'% thang


    def mydomain(self, obj):
        return '<a href=/admin/day/domain/?id=%d>%s</a>'%(obj.domain.id, obj.domain)
    def mysets(self, obj):
        return ' | '.join([ms.clink() for ms in obj.measurementset_set.all()])
    adminify( myhistory, mydomain, mysets, myname)

class MeasurementAdmin(OverriddenModelAdmin):
    list_display='id myplace mycreated amount'.split()
    list_filter=['place',]

    def myplace(self, obj):
        return obj.place.clink()

    def mycreated(self, obj):
        return obj.created.strftime(DATE)

    formfield_for_dbfield=mk_default_field({'created':nowdate,})
    adminify(mycreated, myplace)
    #fields='place amount created'.split()
    fields=(('place','amount','created',),)

class TagAdmin(OverriddenModelAdmin):
    list_display='name mydays'.split()
    list_filter=['name',]
    #date_hierarchy='day'
    @debu
    def mydays(self, obj):
        return ', '.join([day.clink() for day in obj.days.all()])
    adminify(mydays)

#class TagDayAdmin(OverriddenModelAdmin):
    #list_display='id tag day'.split()

class DayAdmin(OverriddenModelAdmin):
    list_display='date mytags mynotes myaday'.split()
    search_fields=['text','tag__name']
    date_hierarchy='date'
    @debu
    def mytags(self, obj):
        return ', '.join([t.clink() for t in obj.tags.all()])

    @debu
    def myaday(self, obj):
        return obj.vlink()


    @debu
    def mynotes(self, obj):
        return '<br>'.join(['%s %s'%(n.clink(text=n.day), n.subnotelink()) for n in obj.notes.all()])

    adminify(mytags, myaday, mynotes)

class NoteAdmin(OverriddenModelAdmin):
    list_display='text myaday mynotekinds'.split()
    list_filter=['kinds',]
    list_search=['kinds',]
    date_hierarchy='created'
    @debu
    def myaday(self, obj):
        return obj.day.vlink()
    @debu
    def mynotekinds(self, obj):
        return '<br>'.join([n.clink() for n in obj.kinds.all()])
    adminify(myaday, mynotekinds)

class NoteKindAdmin(OverriddenModelAdmin):
    list_display='name mynotes myvlink'.split()

    @debu
    def mynotes(self, obj):
        #return '<b>'.join(['%s %s'%(n.clink(text=n.day), ','.join([nk.clink() for nk in n.kinds.all()])) for n in obj.notes.all()])
        return '<br>'.join(['%s (%s) %s'%(n.clink(text=n.day), n.day.vlink(text='day'), n.subnotelink()) for n in obj.notes.all()])
    @debu
    def myvlink(self, obj):
        return obj.vlink()

    adminify(mynotes, myvlink)

admin.site.register(Product, ProductAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(ExWeight, ExWeightAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(MeasuringSpot, MeasuringSpotAdmin)

admin.site.register(Tag, TagAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteKind, NoteKindAdmin)
#admin.site.register(TagDay, TagDayAdmin)

class MSetFormSet(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            qs = super(MSetFormSet, self).get_queryset().none()
            self._queryset = qs
        return self._queryset

from django.forms.models import (modelform_factory, modelformset_factory, inlineformset_factory, BaseInlineFormSet)

class MInline(admin.TabularInline):
    model=MeasurementSet.measurement_spots.through
    extra=1
    formset =  MSetFormSet
    def get_formset(self, request, obj, **kwargs):
        formset = inlineformset_factory(MeasurementSet, Measurement)

    def get_formsets(self, request, obj, **kwargs):
            formset = inlineformset_factory(MeasurementSet, Measurement)

    #def queryset(self, request):
        #queryset = super(InlineModelAdmin, self).queryset(request)
        #if not self.has_change_permission(request):
            #queryset = queryset.none()
        #return queryset

class MeasurementSetAdmin(OverriddenModelAdmin):
    list_display='id name mycontains mydo'.split()
    filter_horizontal = ('measurement_spots',)
    #inlines=[MInline,]
    def mydo(self, obj):
        return '<a href="/do_measurementset/%d">%s</a>'%(obj.id, obj.name)

    def mycontains(self, obj):
        return ' | '.join([spot.clink() for spot in obj.measurement_spots.all()])

    adminify(mydo, mycontains)


admin.site.register(MeasurementSet, MeasurementSetAdmin)
