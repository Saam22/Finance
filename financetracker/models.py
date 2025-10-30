from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Transaction(models.Model):
    transaction_type = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10, choices=transaction_type)
    date = models.DateField()
    category = models.CharField(max_length=255)  
    def __str__(self):
        return f"{self.title} - {self.transaction_type} - {self.amount}"
