from datetime import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Expense(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(0))])
    date = models.DateTimeField(default=datetime.now)
    category = models.CharField(
        max_length=100,
        choices=(
            ("Food", "Food"),
            ("Travel", "Travel"),
            ("Utilities", "Utilities"),
        ),
    )
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
