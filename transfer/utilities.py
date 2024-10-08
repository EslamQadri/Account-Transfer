import uuid
from transfer.models import Accounts
from decimal import Decimal


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False


def get_account_if_exists(account_id):
    try:
        account = Accounts.objects.get(uuid=account_id)
        return account
    except Accounts.DoesNotExist:
        return None


import pandas as pd
from transfer.models import Accounts


def process_csv_and_import_accounts(csv_file):

    try:
        df = pd.read_csv(csv_file)
        accounts = [
            Accounts(uuid=row["ID"], name=row["Name"], balance=row["Balance"])
            for index, row in df.iterrows()
        ]
        Accounts.objects.bulk_create(
            accounts,
            update_conflicts=True,
            unique_fields=["uuid"],
            update_fields=["name", "balance"],
        )
        return True, "Accounts imported successfully."
    except:
        return False, "Please upload a CSV file."


def can_do_transaction(from_account_id, to_account_id, amount):
    message = None
    from_account = None
    to_account = None
    if is_valid_uuid(from_account_id) and is_valid_uuid(to_account_id):
        if from_account_id != to_account_id:
            from_account = get_account_if_exists(from_account_id)
            to_account = get_account_if_exists(to_account_id)
            if from_account and to_account:
                if from_account.balance < Decimal(amount) or Decimal(amount) <= 0:
                    message = "The Balance in less than amount "
                    return (False, message, from_account, to_account)
                else:
                    message = "successfully"
                    return (True, message, from_account, to_account)
            else:
                message = "This is not an Account in System"
                return (False, message, from_account, to_account)

        else:
            message = "You Can not send to the same Account "
        return (False, message, from_account, to_account)
    else:
        message = "This is not UUID "
        return (False, message, from_account, to_account)
