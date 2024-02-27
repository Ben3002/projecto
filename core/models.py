from django.db import models
from django.conf import settings
from PIL import Image
#from django.shortcuts import 
from django.contrib.auth.models import User
from account.models import Account
from django.contrib.auth import get_user_model

# Create your models here.


CATEGORY_CHOICES = (
    ('S', 'Shirts'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
    ('SH', 'Shorts'),
    ('H', 'Hoodies'),
    ('J', 'Jumper'),
    ('SS', 'Shoes'),
    ('SK', 'Socks'),
    ('B', 'Bags'),
    ('T', 'Tank Top'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    colour = models.CharField(max_length=100, default = 'Black')
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField()
    image = models.ImageField()

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices for rating from 1 to 5

    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Show latest reviews first