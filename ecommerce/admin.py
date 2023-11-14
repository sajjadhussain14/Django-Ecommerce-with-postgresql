from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from ecommerce.models import Categories,Brands,   Products, Attribute, AttributeValue, ProductAttribute, Variation, VariationAttribute,Images,MainBanner,MiniBanner,Logo 

from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from django import forms  # Import forms module
from django.contrib.admin import AdminSite


admin.site.site_header = "Admin panel"
admin.site.site_title = "  Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Shop"

# Register your models here.

class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
     # Add the prepopulated_fields dictionary
    prepopulated_fields = {
        'slug': ('name',),   
    }


admin.site.register(Brands, BrandsAdmin)

class CategoriesAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)
    
    # Add the prepopulated_fields dictionary
    prepopulated_fields = {
        'slug': ('name',),  # For categories, populate 'slug' from 'name'
    }

    def save_model(self, request, obj, form, change):
        # Customize the save_model method to set 'slug' for subcategories
        if not obj.pk and obj.parent:
            parent_slug = obj.parent.slug
            obj.slug = f"{parent_slug}-{obj.name}"
        
        # Convert the slug to lowercase
        obj.slug = obj.slug.lower()
    
        super().save_model(request, obj, form, change)

    def indented_title(self, obj):
        return mark_safe(
            f'{"&nbsp;&nbsp;&nbsp;&nbsp;" * obj.level}{obj.name}'
        )

    indented_title.short_description = 'Category'

admin.site.register(Categories, CategoriesAdmin)

class InlineImage(admin.TabularInline):
    model = Images


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute

class VariationAttributeInline(admin.TabularInline):
    model = VariationAttribute

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    order = 3
class ProductsAdmin(admin.ModelAdmin):
    list_display=['id','title','slug', 'price','created','updated','in_stock','is_active','featured']

    list_filter=['in_stock','is_active']
    list_editable=['in_stock','price','is_active','featured']
    prepopulated_fields={'slug':('title',)}
    inlines = [ProductAttributeInline]
    inlines = [InlineImage]

class VariationAdmin(admin.ModelAdmin):
    list_display = ( 'product', 'Sku', 'price', 'stock')
    inlines = [VariationAttributeInline]

admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Variation, VariationAdmin)
# Register the ProductAttribute model
admin.site.register(ProductAttribute)

# Register the VariationAttribute model
admin.site.register(VariationAttribute)



@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ['content_id', 'name', 'display_image', 'text1', 'text2', 'text3', 'slug', 'is_active']
    list_editable = ['is_active']  # Add "is_active" to list_editable
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="30" height="30" />')

    display_image.short_description = 'Image'
    
    def save_model(self, request, obj, form, change):
        print(f"Saving {obj.name}, is_active={obj.is_active}")
        super().save_model(request, obj, form, change)
        
        
        
        
@admin.register(MiniBanner)
class MiniBannerAdmin(admin.ModelAdmin):
    list_display = ['content_id', 'name', 'display_image', 'text1', 'text2', 'text3', 'slug', 'is_active']
    list_editable = ['is_active']  # Add "is_active" to list_editable
    prepopulated_fields = {'slug': ('name',)}

    label = "CMS"

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="30" height="30" />')

    display_image.short_description = 'Image'
    
    def save_model(self, request, obj, form, change):
        print(f"Saving {obj.name}, is_active={obj.is_active}")
        super().save_model(request, obj, form, change) 
        
class LogoAdmin(admin.ModelAdmin):
    list_display = ('id','alt_text', 'display_image' )  # Customize the fields you want to display in the admin list
    
    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="40" height="40" />')
    
    search_fields = ('alt_text',)  # Add fields you want to be searchable in the admin panel

# Register the Logo model with its admin class
admin.site.register(Logo, LogoAdmin)        