from django.utils import timezone

from django.db import models
from django.contrib.auth.models import  User
from shop.models import Product


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity*self.product.price

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.IntegerField()
    payment_method=models.CharField(max_length=20)
    amount=models.IntegerField(null=True)
    order_id=models.CharField(null=True,max_length=50)
    order_date=models.DateTimeField(default=timezone.now())
    is_ordered=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.order_id)

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()