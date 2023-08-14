from rest_framework import serializers

from .models import TypeModel


class TypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = TypeModel
        fields = '__all__'
