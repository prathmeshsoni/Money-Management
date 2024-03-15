from Types.models import TypeModel
from User.models import Profile
from account.models import AccountModel
from category.models import CategoryModel
from django.contrib import admin

from .models import ManageModel

admin.site.register(ManageModel)
admin.site.register(AccountModel)
admin.site.register(CategoryModel)
admin.site.register(TypeModel)
admin.site.register(Profile)
