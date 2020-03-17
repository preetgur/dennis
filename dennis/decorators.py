from django.http import HttpResponse
from django.shortcuts import redirect

"""
If user is authencticated then it is redirect to the "home" page 
Else execute the current function
"""

def unauthencticated_user(view_func):

    def wrapper_func(request,*args,**kwargs):
        #   we can be used request only 
        if request.user.is_authenticated:
            return redirect('home')

        else:
            return view_func(request,*args,**kwargs)    

    return wrapper_func    


""" 
First create the groups in the admin pannel : ['admin','customer']
Below decoarator can be called as : @allowed_users(allowed_roles=['admin'])
Now Go to the "User" model in admin pannel and add the group to them .
Either : admin, customer
"""

def allowed_users(allowed_roles=[]):
    def decorator(view_func):

        def wrapper_func(request,*args,**kwargs):
            # @allowed_users(allowed_roles=['admin'])  
            print("###### Allowed users described in views function : ",allowed_roles)

            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  # fetch the [login] user's group 
                print("##### Actual Type of user : ",group)

             # if customer in list which is allowed_roles['admin']   
            if group in allowed_roles:
                    
                return view_func(request,*args,**kwargs)

            else :
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator        





def admin_only(view_func):

    def wrapper_func(request,*args,**kwargs):

        group = None 

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect('user_page')

        if group == "admin":
            return view_func(request,*args,**kwargs)    

    return wrapper_func    

        

