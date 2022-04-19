from django.db.models import Count
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse

from tags.models import TaggedItem


from . import models

# Register your models here.

#admin.site.register(models.Collection)
#admin.site.register(models.Product)



#------ Collection-----------
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        
        url = (reverse('admin:store_product_changelist') 
        + '?' 
        + urlencode({'collection__id': str(collection.id) }))
        
        return format_html('<a href="{}">{}</a>',url, collection.products_count)
        #return collection.products_count

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count('product'))


#------ Product -----------

class TagInline(GenericTabularInline):
    model = TaggedItem  
    min_num = 1
    max_num = 5
    extra = 0

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    
    inlines = [TagInline]
    prepopulated_fields= {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'price','inventory_status', 'collection_title']
    list_editable = ['price']
    list_select_related = ['collection']
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return "High"
        
    def collection_title(self,product):
        return product.collection.title
    
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,f'{updated_count} updated', messages.SUCCESS )
  
    
    
    
#------ Customer -----------

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    
    @admin.display(ordering='orders_count')
    def orders(self, customer):
        return customer.orders_count
 
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        
        url = (reverse('admin:store_order_changelist') 
        + '?' 
        + urlencode({'order__id': str(customer.id) }))
        
        return format_html('<a href="{}">{} orders</a>',url, customer.orders_count)
 
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(orders_count=Count('order'))
    

    
#------ Order -----------

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    max_num = 5
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
    #autocomplete_fields =['customer']