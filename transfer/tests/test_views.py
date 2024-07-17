from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from transfer.models import Accounts, Transaction
import uuid


# 4
class TransferViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.from_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 1", balance=1000.00
        )
        self.to_account = Accounts.objects.create(
            uuid=uuid.uuid4(), name="Account 2", balance=1000.00
        )

    # 5
    def test_import_accounts_view_get(self):
        response = self.client.get(reverse("import_accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "import_accounts.html")

    # 6
    def test_import_accounts_view_post(self):
        csv_content = b"ID,Name,Balance\ncc26b56c-36f6-41f1-b689-d1d5065b95af,Test Account,100.00\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")

        response = self.client.post(reverse("import_accounts"), {"csv_file": csv_file})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "import_accounts.html")
      
        self.assertTrue(Accounts.objects.filter(name="Test Account").exists())

    # 7
    def test_send_money_view_get(self):
        response = self.client.get(reverse("send_money"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "send_money.html")

    # 8
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

    # 9
    def test_list_accounts_view(self):
        response = self.client.get(reverse("list_accounts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_accounts.html")
        self.assertContains(response, self.from_account.name)
        self.assertContains(response, self.to_account.name)

    # 10
    def test_account_info_view_exists(self):
        response = self.client.get(
            reverse("account_info", kwargs={"pk": self.from_account.uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account_info.html")
        self.assertContains(response, self.from_account.name)

    # 11
    def test_account_info_view_404(self):
        non_existent_uuid = uuid.uuid4()
        response = self.client.get(
            reverse("account_info", kwargs={"pk": non_existent_uuid})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "404.html")
