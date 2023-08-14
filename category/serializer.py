from rest_framework import serializers

from .models import CategoryModel


class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
