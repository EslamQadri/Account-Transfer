from django.urls import path
from transfer.views import (
    import_accounts,
    send_money,
    list_accounts,
    account_info,
    list_transaction,
)
from transfer.api.views import (
    AccountsList,
    TransactionListView,
    import_accounts_api,
    TransferMoneyView,
    AccountDetailView,
)

urlpatterns = [
    path("import", import_accounts, name="import_accounts"),
    path("send_money", send_money, name="send_money"),
    path("list_accounts", list_accounts, name="list_accounts"),
    path("list_transaction", list_transaction, name="list_transaction"),
    path("account_info/<uuid:pk>", account_info, name="account_info"),
    # api ...
    path("api/import_accounts_api", import_accounts_api, name="import_accounts_api"),
    path("api/send_money_api",  TransferMoneyView.as_view(), name="send_money_api"),
    path("api/list_accounts_api", AccountsList.as_view(), name="list_accounts_api"),
    path(
        "api/transaction_list_api",
        TransactionListView.as_view(),
        name="transaction_list_api",
    ),
    path(
        "api/account_info_api/<uuid:uuid>/",
        AccountDetailView.as_view(),
        name="account_info_api",
    ),
]
