from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.core.validators import MaxLengthValidator

stocks ={('AAPL','Apple'),('MSFT','Microsoft'),('GOOGL','Google'),('TES','TESLA'),('TATH','TATA_Tech'),('AMZ','AMAZON')}
locations ={('PUN','Pune'),('MUM','Mumbai'),('BAN','Bangalore'),('DEL','Delhi'),('HYD','Hyderabad'),('NYC','NEW_YORK')}
Associated_companies={('grow','grow'),('upstocks','upstocks'),('zerodha','zerodha')}


# Create your models here.

class AdminUser(AbstractUser):
    Role=models.CharField(choices={('Admin','Admin'),('FM','FundManager'),('CUST','Customer')})
    contact_info =models.BigIntegerField(null=True)
    Location =models.CharField(choices=locations)
    Associated_company =models.CharField(choices=Associated_companies)
    Is_FM =models.BooleanField(default=False)
    Is_Customer =models.BooleanField(default=False)
    Is_Admin =models.BooleanField(default=False)
    Foriegn_id =models.PositiveIntegerField()
    
    

class Holdings(models.Model):
    stock_name=models.CharField(choices=stocks, max_length=50)
    quantity =models.IntegerField()
    holder=models.ForeignKey(AdminUser,on_delete=models.CASCADE)
