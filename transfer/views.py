from django.shortcuts import render
import csv
from transfer.models import Accounts, Transaction

from django.contrib import messages
import pandas as pd
from django.db import transaction
from decimal import Decimal
from transfer.utilities import can_do_transaction


# Create your views here.

# to do make prograsse bar
@transaction.atomic
def import_accounts(request):
    message = None
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        if not csv_file:
            message = " Plaese Import CSV File "
            return render(request, "import_accounts.html", {"message": message})
        else:
            df = pd.read_csv(csv_file)
            list_of_accounts = [
                Accounts(uuid=row["ID"], name=row["Name"], balance=row["Balance"])
                for index, row in df.iterrows()
            ]
            Accounts.objects.bulk_create(
                list_of_accounts,
                update_conflicts=True,
                unique_fields=["uuid"],
                update_fields=["name", "balance"],
            )

            message = " successfully Insert in DataBase "
            print("\n\n", message, "\n\n")
            return render(request, "import_accounts.html", {"message": message})
    return render(request, "import_accounts.html", {"message": message})


@transaction.atomic
def send_money(request):
    names = Accounts.objects.order_by("name")
    message = None
    if request.method == "POST":
        from_account_id = request.POST["from_account"]
        to_account_id = request.POST["to_account"]
        amount = request.POST["amount"]

        status, message, from_account, to_account = can_do_transaction(
            from_account_id, to_account_id, amount
        )
        if status:
            from_account.balance -= Decimal(amount)
            to_account.balance += Decimal(amount)
            Transaction.objects.create(
                sender=from_account, receiver=to_account, amount=amount
            )
            from_account.save()
            to_account.save()
            return render(
                request, "send_money.html", {"names": names, "message": message}
            )

    return render(request, "send_money.html", {"names": names, "message": message})


def list_accounts(request):
    accounts = Accounts.objects.all()
    return render(request, "list_accounts.html", {"accounts": accounts})


def account_info(request, pk):
    if Accounts.objects.filter(uuid=pk).exists():
        account = Accounts.objects.get(uuid=pk)
        return render(request, "account_info.html", {"account": account})
    else:
        return render(request, "404.html")
