from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from transfer.models import Accounts, Transaction
import uuid
from django.utils import timezone
from decimal import Decimal
from transfer.utilities import can_do_transaction

from io import StringIO


class TransferViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.from_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 1", balance=1000.00
        )
        self.to_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 2", balance=1000.00
        )
        self.url = reverse("import_accounts")
        self.csv_content = b"ID,Name,Balance\ncc26b56c-36f6-41f1-b689-d1d5065b95af,Test Account,100.00\n"
        self.csv_file = SimpleUploadedFile(
            "test.csv", self.csv_content, content_type="text/csv"
        )

    def test_import_accounts_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "import_accounts.html")

    def test_import_accounts_view_post(self):

        response = self.client.post(self.url, {"csv_file": self.csv_file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "import_accounts.html")

        self.assertTrue(Accounts.objects.filter(name="Test Account").exists())
        self.assertEqual(response.context["message"], "Accounts imported successfully.")


    def test_failure_import_accounts_view(self):

        response = self.client.post(self.url, {"csv_file": "self.csv_file"})
        self.assertEqual(response.context["message"], None)
        csv_data = """ID,Name,Balance
                      invalid_data"""
        csv_file = StringIO(csv_data)
        response = self.client.post(self.url, {"csv_file": csv_file})
        self.assertEqual(response.context["message"], "Please upload a CSV file.")

    def test_send_money_view_get(self):
        response = self.client.get(reverse("send_money"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "send_money.html")

    def test_send_money_view_post(self):
        response = self.client.post(
            reverse("send_money"),
            {
                "from_account": str(self.from_account.uuid),
                "to_account": str(self.to_account.uuid),
                "amount": 100,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.from_account.refresh_from_db()
        self.to_account.refresh_from_db()
        self.assertEqual(self.from_account.balance, 900.00)
        self.assertEqual(self.to_account.balance, 1100.00)

    def test_send_money_unvalid_uuid(self):
        response = self.client.post(
            reverse("send_money"),
            {
                "from_account": str(self.from_account.uuid),
                "to_account": str(self.to_account.uuid),
                "amount": 100,
            },
        )

    def test_list_accounts_view(self):
        response = self.client.get(reverse("list_accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_accounts.html")
        self.assertContains(response, self.from_account.name)
        self.assertContains(response, self.to_account.name)

    def test_account_info_view_exists(self):
        response = self.client.get(
            reverse("account_info", kwargs={"pk": self.from_account.uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_info.html")
        self.assertContains(response, self.from_account.name)

    def test_account_info_view_404(self):
        non_existent_uuid = uuid.uuid4()
        response = self.client.get(
            reverse("account_info", kwargs={"pk": non_existent_uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "404.html")


class ListTransactionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("list_transaction")

        self.from_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 1", balance=1000.00
        )
        self.to_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 2", balance=1000.00
        )
        self.transaction1 = Transaction.objects.create(
            sender=self.from_account,
            receiver=self.to_account,
            amount=100.00,
            at=timezone.now(),
        )
        self.transaction2 = Transaction.objects.create(
            sender=self.to_account,
            receiver=self.from_account,
            amount=200.00,
            at=timezone.now(),
        )

    def test_list_transaction(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_transaction.html")
        self.assertIn("transactions", response.context)
        self.assertEqual(len(response.context["transactions"]), 2)
        self.assertQuerysetEqual(
            response.context["transactions"], Transaction.objects.all()
        )


class TransactionUtilsTestCase(TestCase):
    def setUp(self):
        self.from_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Sender Account", balance=Decimal("500.00")
        )
        self.to_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Receiver Account", balance=Decimal("100.00")
        )

    def test_valid_transaction(self):
        status, message, from_account, to_account = can_do_transaction(
            str(self.from_account.uuid), str(self.to_account.uuid), "100.00"
        )
        self.assertTrue(status)
        self.assertEqual(message, "successfully")

    def test_balance_less_than_amount(self):
        status, message, from_account, to_account = can_do_transaction(
            str(self.from_account.uuid), str(self.to_account.uuid), "600.00"
        )
        self.assertFalse(status)
        self.assertEqual(message, "The Balance in less than amount ")

    def test_invalid_uuid(self):
        status, message, from_account, to_account = can_do_transaction(
            "invalid-uuid", "another-invalid-uuid", "100.00"
        )
        self.assertFalse(status)
        self.assertEqual(message, "This is not UUID ")

    def test_same_account(self):
        status, message, from_account, to_account = can_do_transaction(
            str(self.from_account.uuid), str(self.from_account.uuid), "100.00"
        )
        self.assertFalse(status)
        self.assertEqual(message, "You Can not send to the same Account ")

    def test_Acounnt_not_exists(self):
        status, message, from_account, to_account = can_do_transaction(
            str(uuid.uuid4()), str(self.from_account.uuid), "100.00"
        )
        self.assertFalse(status)
        self.assertEqual(message, "This is not an Account in System")
