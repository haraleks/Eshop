from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count

from shop.admin import export_to_csv
from users.models.profile_models import Customer

User = get_user_model()

admin.site.register(User)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "sex",
                    "date_of_birth", "created_at", "count_product_wish")
    search_fields = ['id', 'name', 'sku']
    list_filter = ("id", "first_name", "last_name")

    actions = [export_to_csv]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _count_product_wish=Count('wish_lists', distinct=True))
        return queryset

    def count_product_wish(self, obj):
        return obj._count_product_wish

    count_product_wish.admin_order_field = '_count_product_wish'
