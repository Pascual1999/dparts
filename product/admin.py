from django.contrib import admin

from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from .models import Category, Product, Tag, ProductTag


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1


class ProductResource(resources.ModelResource):
    category = fields.Field(
            column_name='category',
            attribute='category',
            widget=ForeignKeyWidget(Category, field='name')
        )

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku', 'brand', 'description',
                  'stock', 'price')
        excluded = ('date_added', 'tags')


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['id', 'name', 'category', 'stock', 'stock_on_hold',
                    'units_sold', 'date_added', 'price', 'is_active']
    inlines = [ProductTagInline]
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'category', 'tags']
    list_per_page = 20
    readonly_fields = ['thumbnail', 'slug', 'units_sold']
    view_on_site = False


class TagAdmin(admin.ModelAdmin):
    inlines = [ProductTagInline]
    list_per_page = 20
    list_display = ['name']
    readonly_fields = ['slug']
    view_on_site = False




class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    view_on_site = False
    list_display = ['name', 'productos']

    def productos(self, obj):
        return obj.products.count()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
