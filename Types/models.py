from django.db import models


class TypeModel(models.Model):
    type_name = models.CharField(max_length=30,null =True )

    def __str__(self):
        return "%s" % self.type_name
