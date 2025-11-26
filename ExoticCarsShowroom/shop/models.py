from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="მოდელი")
    description = models.TextField(verbose_name="აღწერა")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ფასი")
    image = models.ImageField(upload_to='product_images/', verbose_name="ფოტო", blank=True, null=True)
    horsepower = models.IntegerField(verbose_name="ცხენის ძალა")
    max_speed = models.IntegerField(verbose_name="მაქს. სიჩქარე (კმ/სთ)")
    year = models.IntegerField(verbose_name="წელი")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "მანქანა"
        verbose_name_plural = "მანქანები"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_item_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.user.username})"
    
    class Meta:
        verbose_name = "კალათის ნივთი"
        verbose_name_plural = "კალათის ნივთები"