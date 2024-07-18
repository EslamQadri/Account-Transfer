from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from transfer.models import Accounts, Transaction
from django.urls import reverse
from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase



# 15
class AccountsListViewTests(TestCase):
    def setUp(self):
        self.account1 = Accounts.objects.create(name="Account1", balance=100.0)
        self.account2 = Accounts.objects.create(name="Account2", balance=200.0)

    # 16
    def test_accounts_list_view(self):
        client = APIClient()
        url = reverse("list_accounts_api")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class AccountDetailViewTests(TestCase):
    def setUp(self):
        self.account = Accounts.objects.create(name="Test Account", balance=500.0)

    # 17
    def test_account_detail_view(self):
        client = APIClient()
        url = reverse("account_info_api", kwargs={"uuid": self.account.uuid})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Account")


class TransactionListViewTests(TestCase):
    def setUp(self):

        self.account1 = Accounts.objects.create(name="Account1", balance=1000.0)
        self.account2 = Accounts.objects.create(name="Account2", balance=2000.0)
        self.transaction1 = Transaction.objects.create(
            sender=self.account1, receiver=self.account2, amount=50.0
        )
        self.transaction2 = Transaction.objects.create(
            sender=self.account2, receiver=self.account1, amount=25.0
        )

    # 18
    def test_transaction_list_view(self):
        client = APIClient()
        url = reverse("transaction_list_api")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class ImportAccountsApiTest(APITestCase):

    def setUp(self):
        self.url = reverse("import_accounts_api")

    # 19
    def test_import_accounts_success(self):
        # Create a sample CSV file
        csv_content = StringIO("ID,Name,Balance\n1,John Doe,1000\n2,Jane Smith,2000\n")
        csv_file = SimpleUploadedFile(
            "accounts.csv",
            csv_content.getvalue().encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            self.url, {"csv_file": csv_file}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Accounts imported successfully.")

    # 20
    def test_import_accounts_missing_file(self):
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Please upload a CSV file.")


class TransferMoneyViewTests(TestCase):
    def setUp(self):

        self.account1 = Accounts.objects.create(name="Account1", balance=1000.0)
        self.account2 = Accounts.objects.create(name="Account2", balance=2000.0)

    # 21
    def test_transfer_money_view(self):
        client = APIClient()
        data = {
            "from_account": (self.account1.uuid),
            "to_account": (self.account2.uuid),
            "amount": 100.0,
        }
        url = reverse("send_money_api")
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data["to_account"] = self.account1.uuid
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
