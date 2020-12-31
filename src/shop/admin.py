import csv
import datetime

from django.contrib import admin
from django.db.models import Count, F
from django.http import HttpResponse

from shop.models import (Category, Subcategory, Product,
                         Attribute, Value, ProductItems,
                         PromoCode, Basket, PositionProduct,
                         ProductsCompare, DesiredProducts,
                         Feedback)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename{}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    queryset_values = queryset.values()
    fields = queryset_values[0].keys()
    writer.writerow([field for field in fields])

    for obj in queryset.values():
        data_row = []
        for field, value in obj.items():
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "count_subcategory", "count_product")
    search_fields = ['id', 'name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _count_subcategory=Count('subcategory', distinct=True),
            _count_product=Count('subcategory__product', distinct=True)
        )

        return queryset

    def count_subcategory(self, obj):
        return obj._count_subcategory

    count_subcategory.admin_order_field = '_count_subcategory'

    def count_product(self, obj):
        return obj._count_product

    count_product.admin_order_field = '_count_product'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "main_character", "price", "subcategory", "category")
    search_fields = ['id', 'name', 'sku']
    list_filter = ("price", "subcategory", "subcategory__category")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _category=F('subcategory__category__name'),
            _main_character=F('main_character__value_model__value_char')
        )

        return queryset

    def category(self, obj):
        return obj._category

    category.admin_order_field = '_category'

    def main_character(self, obj):
        return obj._main_character

    main_character.admin_order_field = '_main_character'


admin.site.register(Subcategory)
admin.site.register(Attribute)
admin.site.register(Value)
admin.site.register(ProductItems)
# admin.site.register(PromoCode)


def is_active_change(modeladmin, request, queryset):
    for query in queryset:
        if query.is_active:
            query.is_active = False
        else:
            query.is_active = True
        query.save()


is_active_change.short_description = 'Activate and Deactivate promo code'


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "quantity", "discount", "remainder", "is_active")
    search_fields = ["code"]
    list_filter = ("created_at", "is_active")
    actions = [is_active_change, export_to_csv]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _count_used=Count('basket', distinct=True),
            _remainder=F('quantity') - F('_count_used')
        )
        return queryset

    def remainder(self, obj):
        return obj._remainder

    remainder.admin_order_field = '_remainder'


admin.site.register(Basket)
admin.site.register(PositionProduct)
admin.site.register(ProductsCompare)
admin.site.register(DesiredProducts)
admin.site.register(Feedback)
