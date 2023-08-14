from django.contrib.auth.models import User
from django.db import models


class CategoryModel(models.Model):
    cat_name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s" % self.cat_name
