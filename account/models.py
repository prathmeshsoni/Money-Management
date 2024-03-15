from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class AccountModel(models.Model):
    account_name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s" % self.account_name
