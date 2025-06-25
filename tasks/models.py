from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.TextField(blank=True, null=True) 
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)])   
    email = models.EmailField(unique=True)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Active Task', 'Active Task'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
            ordering = ['-created_at'] 
    