from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products')
    category=models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    # Returns average rating (rounded to 2 decimals) for this product
    @property
    def average_rating(self):
        from django.db.models import Avg
        agg = self.reviews.aggregate(avg=Avg('rating'))
        return round(agg['avg'] or 0, 2)
    
    # Returns total number of reviews for this product
    @property
    def review_count(self):
        return self.reviews.count()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image=models.ImageField(upload_to='category')
    
    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"
    
    def get_total_price(self):
        return self.quantity * self.product.price
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} (@{self.price})"

    def get_subtotal(self):
        return self.quantity * self.price