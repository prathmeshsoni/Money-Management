from django.contrib import admin
from management.models import ManageModel
# from .models import Profile, addressModel, buyModel, Sub_bayModel, add_to_cart
from django.contrib.auth.models import User

admin.site.register(ManageModel)
# admin.site.register(User)
# admin.site.register(addressModel)
# admin.site.register(buyModel)
# admin.site.register(Sub_bayModel)
# admin.site.register(add_to_cart)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

# class UserAdmin(BaseUserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
#     list_filter = ('is_staff', 'date_joined')

# # admin.site.unregister(User)
# admin.site.register(User, UserAdmin)