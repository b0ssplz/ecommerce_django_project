from django.db.models import Count
from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse


from . import models

# Register your models here.

#admin.site.register(models.Collection)
#admin.site.register(models.Product)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    
    @admin.display(ordering='products_count')
    def product_count(self, collection):
        
        url = (reverse('admin:store_product_changelist') 
        + '?' 
        + urlencode({'collection__id': str(collection.id) }))
        
        return format_html('<a href="{}">{}</a>',url, collection.products_count)
        #return collection.products_count

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count('product'))



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','inventory_status', 'collection_title']
    list_editable = ['price']
    list_select_related = ['collection']
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 3:
            return 'Low'
        else:
            return "High"
        
    def collection_title(self,product):
        return product.collection.title
    
@admin.register(models.Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    