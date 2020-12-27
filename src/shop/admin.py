from django.contrib import admin
from django.db.models import Count, F

from shop.models import (Category, Subcategory, Product,
                         Attribute, Value, ProductItems,
                         PromoCode, Basket, PositionProduct,
                         ProductsCompare, DesiredProducts,
                         Feedback)


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
        # TODO main_character__value_model__value_char ???
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
admin.site.register(PromoCode)
admin.site.register(Basket)
admin.site.register(PositionProduct)
admin.site.register(ProductsCompare)
admin.site.register(DesiredProducts)
admin.site.register(Feedback)
