from django.test import TestCase
from transfer.models import Accounts, Transaction
import uuid


class AccountsModelTest(TestCase):

    def setUp(self):
        self.account1 = Accounts.objects.create(name="Account 1", balance=100.00)
        self.account2 = Accounts.objects.create(name="Account 2", balance=200.00)

    # 1
    def test_account_creation(self):
        account = Accounts.objects.get(name="Account 1")
        self.assertEqual(account.balance, 100.00)
        self.assertIsInstance(account.uuid, uuid.UUID)

    # 2
    def test_string_representation(self):
        account = Accounts.objects.get(name="Account 1")
        self.assertEqual(str(account), "Account 1")


class TransactionModelTest(TestCase):

    def setUp(self):
        self.account1 = Accounts.objects.create(name="Account 1", balance=100.00)
        self.account2 = Accounts.objects.create(name="Account 2", balance=200.00)
        self.transaction = Transaction.objects.create(
            sender=self.account1, receiver=self.account2, amount=50.00
        )

    # 3
    def test_transaction_creation(self):
        transaction = Transaction.objects.get(sender=self.account1)
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(transaction.receiver, self.account2)

    # 4
    def test_string_representation(self):
        transaction = Transaction.objects.get(sender=self.account1)
        self.assertEqual(
            str(transaction),
            f"Transaction from {self.account1} to {self.account2} for 50.00",
        )
