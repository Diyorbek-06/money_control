from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from datetime import date
User = get_user_model()

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_income = models.BooleanField(default=False)  # True kirim, False chiqim uchun

    def __str__(self):
        return f"{self.name} ({'Kirim' if self.is_income else 'Chiqim'})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('cash', 'Naqd'), ('card', 'Karta')])
    date = models.DateTimeField(default=date.today)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.type} ({self.category.name})"