from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products')
    category=models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image=models.ImageField(upload_to='category')
    
    def __str__(self):
        return self.name