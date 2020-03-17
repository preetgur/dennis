from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from dennis.models import Customer
from django.contrib.auth.models import Group 

#sender => models
# instance => instance of that model

def customer_profile(sender,instance,created,**kwargs):
    print(sender)    # < class "django.contrib.auth.models.User">
    print(instance)  #  return username
    print(created)   #  return True/False
    if created:

        # Adding the new user to "customer" group automatically
        group = Group.objects.get(name="customer")

        # user.groups.add(group)
        instance.groups.add(group)

        # Customer.objects.create( user= user, name = user.username, email = user.email,)
        Customer.objects.create( user= instance, name = instance.username, email = instance.email,)  

        print("############ User Created")

post_save.connect(customer_profile,sender=User)

# @receiver(post_save, sender=User)
# def update_profile(sender,instance,created,**kwargs):

#     if created == False:
#         instance.customer.save()
#         print("############ Profile Updated")



"""
################ Configure in apps.py

class DennisConfig(AppConfig):
    name = 'dennis'

    # for signals
    def ready(self):
        import dennis.signals


###############
Make sure that "app" name is listed in installed app in settings.py as :
    "dennis.apps.DennisConfig"  not like "dennis" only


############  Add to __init__.py  : if not configure in apps.py as above and  app name as "dennis" only

default_app_config = 'dennis.apps.DennisConfig'

"""

"""
 Signals are like event-based programming. You can hook up callback functions that get executed when specific events happen.
"""