from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# null = True => because we alreday have some values in models
# blank = True => create a customer without a user attached to it
# onetoonefield => user can have one customer and customer can have one user
class Customer(models.Model):   

    user = models.OneToOneField(User,null=True,blank=True ,on_delete=models.CASCADE)
    
    profile_pic = models.ImageField(null=True,blank=True,default="default.png")

    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    mobile = models.CharField(max_length=10)


    def __str__(self):

        return str(self.name)  # convert into str because of signals

# This Model is used for many to many relationship
class Tag(models.Model):
    name = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    
    category = ( 
                ("Electronic","electronics"),
                ("Sport","sports"),
                ("Kitchen","kitchens"),
                ("Men","mens"),
                )

    product_name = models.CharField(max_length=20)
    product_category = models.CharField( max_length=20,choices=category)
    price = models.FloatField(max_length=10)
    product_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100,blank=True,null=True)

    # many to many relationship
    tags = models.ManyToManyField(Tag)

    def __str__(self):

        return self.product_name


class Order(models.Model):

    status = (
        ("Pending","pending"),
        ("Placed","placed"),
        ("Out For Delivery","out for delivery"),
        ("Delivered","delivered")
    )

    placed_by = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order_name = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True)
    placed_on = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20,choices=status)


    def __str__(self):

        return str(self.placed_by) + " => "+ str(self.order_name) + ":"+ str(self.order_status)