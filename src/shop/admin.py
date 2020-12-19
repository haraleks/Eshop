from django.contrib import admin

from shop.models import (Category, Subcategory, Product,
                         Attribute, Value, ProductItems,
                         PromoCode, Basket, PositionProduct,
                         ProductsCompare, DesiredProducts,
                         Feedback)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Value)
admin.site.register(ProductItems)
admin.site.register(PromoCode)
admin.site.register(Basket)
admin.site.register(PositionProduct)
admin.site.register(ProductsCompare)
admin.site.register(DesiredProducts)
admin.site.register(Feedback)
