from django.db import models
import uuid
# Create your models here.
class Accounts (models.Model):
    name = models.CharField("Name",max_length= 255 )
    balance= models.DecimalField("Balance",max_digits=10,decimal_places=2)
    uuid= models.UUIDField("Id",primary_key=True,default=uuid.uuid4,editable=True)

    def __str__(self) -> str:
        return f"{self.name}"
    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    sender=models.ForeignKey(Accounts,on_delete=models.PROTECT,related_name="sent_transactions")
    receiver=models.ForeignKey(Accounts,on_delete=models.PROTECT,related_name ="received_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Transaction from {self.sender} to {self.receiver} for {self.amount}'
    class Meta:
        ordering = ['-at']



