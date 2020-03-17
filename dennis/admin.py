from django.contrib import admin
from dennis.models import Customer,Products,Order,Tag
# Register your models here.

admin.site.register(Customer)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Tag)

