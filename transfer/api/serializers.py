# serializers.py
from rest_framework import serializers
from transfer.models import Accounts, Transaction


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["uuid", "name", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "sender", "receiver", "amount", "at"]
        read_only_fields = ["id", "at"]
