from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
class Bottle(models.Model):
    text = models.CharField(max_length=100)
    range = models.IntegerField()
    
class CustomerUserManager(BaseUserManager):
    def create_user(self, password , **extrafields) :
        user = self.model (extrafields)
        user.set_password(password)
        user.save(using = self._db)
        return user 
class CustomerUser(AbstractBaseUser , PermissionsMixin) : 
    username = models.CharField(max_length= 10 , unique=True)
    coin = models.IntegerField(default=50)
    x = models.IntegerField()
    y = models.IntegerField()
    objects = CustomerUserManager   
    def __str__(self) -> str:
        return self.name   

 
    
# Create your models here.
