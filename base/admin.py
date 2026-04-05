from django.contrib import admin
from .models import AppUser, FinancialRecord
# Register your models here.
admin.site.register([AppUser,FinancialRecord])
