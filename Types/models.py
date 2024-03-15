from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class TypeModel(models.Model):
    type_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return "%s" % self.type_name


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'Types':
        TypeModel.objects.get_or_create(type_name='Income')
        TypeModel.objects.get_or_create(type_name='Expense')
        TypeModel.objects.get_or_create(type_name='Transfer')
