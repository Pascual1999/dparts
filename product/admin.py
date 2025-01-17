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
                  'price')
        excluded = ('date_added', 'tags')


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['id', 'name', 'date_added', 'price', 'is_active']
    inlines = [ProductTagInline]
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'category', 'tags']
    list_per_page = 20
    readonly_fields = ['thumbnail', 'slug']


class TagAdmin(admin.ModelAdmin):
    inlines = [ProductTagInline]
    list_per_page = 20
    readonly_fields = ['slug']


admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
