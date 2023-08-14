from rest_framework import serializers

from Types.serializer import TypeSerialize
from account.serializer import AccountSerialize
from category.serializer import CategorySerialize
from .models import ManageModel


class ManageSerialize(serializers.ModelSerializer):
    category = CategorySerialize()

    class Meta:
        model = ManageModel
        fields = '__all__'


class ManageSerialize_1(serializers.ModelSerializer):
    category = CategorySerialize()
    account = AccountSerialize()
    to_account = AccountSerialize()
    from_account = AccountSerialize()
    type = TypeSerialize()

    class Meta:
        model = ManageModel
        fields = '__all__'
