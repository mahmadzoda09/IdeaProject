from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "админ", "Администратор"
        MANAGER = "менеджер", "Менеджер"
        WAREHOUSE = "склад", "Работник склада"
        ACCOUNTANT = "бухгалтер", "бухгалтер"
        CLIENT = "клиент", "Клиент"
    role = models.CharField( max_length=20, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField(max_length=20,blank=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username