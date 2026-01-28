from django.db import models
from django.core.validators import MinValueValidator

from UserProfile.models import User
# Create your models here.


class Books(models.Model):
    title=models.CharField(max_length=30,blank=False,null=False)
    author=models.CharField(max_length=30,blank=False,null=False)
    genre=models.CharField(max_length=30,blank=False,null=False)
    description=models.TextField()
    price=models.DecimalField(blank=False,null=False,max_digits=10,decimal_places=2,validators=[MinValueValidator(1.0)])
    stock=models.IntegerField(blank=False,null=False,
                              validators=[MinValueValidator(0)])
    coverPage=models.ImageField(upload_to='coverpage/',blank=False,null=False)


class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    book=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField(default=(1))


    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    def get_total_price(self):
        return self.book.price * self.quantity


# models.py

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.book.price * self.quantity
