from django.db import models
from django.contrib.auth.models import Group, Permission

class Product(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Products'
class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name =  models.CharField(max_length=50)
    email =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=15)
    Id_no  =  models.CharField(max_length=100, unique=True)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")
    
    class Meta:
        verbose_name_plural = 'Customer' 

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)  # ForeignKey to Customer model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    Serial_no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - {self.product}"

    class Meta:
        verbose_name_plural = 'Records'

     

            

      


