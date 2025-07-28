from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transactions(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('food and drinks', 'Food and drinks'),
        ('transport', 'Transport'),
        ('rent', 'Rent'),
        ('purchases', 'Purchases'),
        ('life and entertainment', 'Life and entertainment'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"
