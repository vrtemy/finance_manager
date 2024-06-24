from django.db import models
from users.models import User, Wallet


class TransactionCategory(models.Model):
    ico = models.ImageField(upload_to='categories-icons')
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    type = models.BooleanField(default=False)  # True(+) False(-)
    sum = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=TransactionCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} | {self.user} | {self.category}'
    




