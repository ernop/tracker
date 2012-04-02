from django.contrib import admin
from buy.models import *
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