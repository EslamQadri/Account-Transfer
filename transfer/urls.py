from django.urls import path
from transfer.views import import_accounts, send_money,list_accounts,account_info

urlpatterns = [
    path("import", import_accounts, name="import_accounts"),
    path("send_money", send_money, name="send_money"),
    path ("list_accounts",list_accounts,name = "list_accounts"),
    path("account_info/<uuid:pk>",account_info,name="account_info")
]
