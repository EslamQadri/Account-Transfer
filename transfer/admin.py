from django.contrib import admin
from transfer.models import Accounts ,Transaction
# Register your models here.
admin.site.register((Accounts ,Transaction))