from rest_framework import generics, status
from rest_framework.response import Response
from transfer.models import Accounts, Transaction
from transfer.api.serializers import AccountsSerializer, TransactionSerializer
from decimal import Decimal
from transfer.utilities import can_do_transaction, process_csv_and_import_accounts
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class PaginationClass(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AccountsList(generics.ListAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    pagination_class = PaginationClass


class AccountDetailView(generics.RetrieveAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    lookup_field = "uuid"


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = PaginationClass


@api_view(["POST"])
def import_accounts_api(request):
    csv_file = request.FILES.get("csv_file")
    success, message = process_csv_and_import_accounts(csv_file)
    if success:
        return Response({"detail": message}, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)


class TransferMoneyView(APIView):
  
    def post(self, request):
        from_account_id = request.data.get("from_account")
        to_account_id = request.data.get("to_account")
        amount = request.data.get("amount")

        stat, message, from_account, to_account = can_do_transaction(
            from_account_id, to_account_id, amount
        )
        if stat:
            from_account.balance -= Decimal(amount)
            to_account.balance += Decimal(amount)
            Transaction.objects.create(
                sender=from_account, receiver=to_account, amount=amount
            )
            from_account.save()
            to_account.save()
            return Response(
                {"detail": "Transaction successful."}, status=status.HTTP_201_CREATED
            )

        return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)
