from django.contrib.auth.models import User
from django.db import models

from Types.models import TypeModel
from account.models import AccountModel
from category.models import CategoryModel


class ManageModel(models.Model):
    type = models.ForeignKey(TypeModel, on_delete=models.CASCADE, null=True)
    date_name = models.DateTimeField()
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True, blank=True)
    to_account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='to_account')
    from_account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='from_account')
    amount = models.IntegerField()
    note = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.type.type_name == 'Transfer':
            self.account = None
            self.category = None
        else:
            self.to_account = None
            self.from_account = None
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return "%s" % self.type
