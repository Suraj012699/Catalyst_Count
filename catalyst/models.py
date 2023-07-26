from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email,first_name,last_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()





class Data(models.Model):
    Emp_id = models.IntegerField(blank=True, null=True)
    Name = models.CharField(max_length=100,blank=True, null=True)
    Domain = models.CharField(max_length=100,blank=True, null=True)
    Year = models.IntegerField(blank=True, null=True)
    Industry = models.CharField(max_length=100, blank=True, null=True)
    Size = models.CharField(max_length=100, blank=True, null=True)
    Locality = models.CharField(max_length=50,blank=True, null=True)
    Country = models.CharField(max_length=100,blank=True, null=True)
    Url = models.CharField(max_length=100,blank=True, null=True)
    Current_Emp = models.IntegerField(blank=True, null=True)
    Total_Emp = models.IntegerField(blank=True, null=True)

    










