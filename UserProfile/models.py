from django.db import models
from django.core.validators import RegexValidator


from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    choice=[("customer","Customer"),
             ('admin',"Admin")]
    
    role=models.CharField(max_length=10,choices=choice,default='customer')
    contact_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid number")],
        null=True,blank=True
    )

    @property
    def is_admin_group_member(self):
        return self.role == 'admin'
