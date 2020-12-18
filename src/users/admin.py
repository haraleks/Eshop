from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models.profile_models import Customer

User = get_user_model()

admin.site.register(User)
admin.site.register(Customer)
