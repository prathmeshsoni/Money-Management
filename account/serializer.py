from rest_framework import serializers

from .models import AccountModel


class AccountSerialize(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__'
