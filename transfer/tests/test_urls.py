from django.test import SimpleTestCase
from django.urls import reverse, resolve
from transfer.views import import_accounts, send_money, list_accounts, account_info
import uuid



class TestTransferURLs(SimpleTestCase):
    def test_import_accounts_url_resolves(self):
        url = reverse("import_accounts")
        self.assertEqual(resolve(url).func, import_accounts)

    def test_send_money_url_resolves(self):
        url = reverse("send_money")
        self.assertEqual(resolve(url).func, send_money)

    def test_list_accounts_url_resolves(self):
        url = reverse("list_accounts")
        self.assertEqual(resolve(url).func, list_accounts)

    def test_account_info_url_resolves(self):
        uuid_value = uuid.uuid4()
        url = reverse("account_info", kwargs={"pk": uuid_value})
        self.assertEqual(resolve(url).func, account_info)
