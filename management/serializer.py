from rest_framework import serializers
from .models import ManageModel
from category.serializer import CategorySerialize


class ManageSerialize(serializers.ModelSerializer):
    category = CategorySerialize()

    class Meta:
        model = ManageModel
        fields = '__all__'
