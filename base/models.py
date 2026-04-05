from django.db import models

from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        ANALYST = 'ANALYST', 'Analyst'
        VIEWER = 'VIEWER', 'Viewer'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
# choices: This tells Django to use a dropdown in forms and the admin site.

# Create your models here.

class FinancialRecord(models.Model):
    
    amount = models.IntegerField()
    
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default='EXPENSE'
    )
    
    category = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(AppUser,on_delete=models.CASCADE)