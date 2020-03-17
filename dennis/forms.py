from django.forms import ModelForm
from dennis.models import Order,Customer

class Create_Order_Form(ModelForm):

    class Meta:
        model = Order
        fields = "__all__"


# Create Register Form

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django import forms

class Create_User_Form(UserCreationForm):

    class Meta : 
        model = User
        fields = ['username','email','password1','password2']


# Customer Form using in account_setting view
# used for update the values
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user"]
