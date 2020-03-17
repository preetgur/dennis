from django.shortcuts import render,HttpResponse
from dennis.models import *
from dennis.decorators import unauthencticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required

# Create your views here.


# @allowed_users(allowed_roles=['admin'])  # only admin can access this page
@admin_only
def home(request):

    orders = Order.objects.all()
    total_orders = orders.count()
    pending_orders = orders.filter(order_status='Pending').count()
    placed_orders = orders.filter(order_status="Placed").count()
    delivered_orders = orders.filter(order_status='Delivered').count()
    out_for_delivery = orders.filter(order_status='Out For Delivery').count()

    customers = Customer.objects.all()
    products = Products.objects.all()

    context = {
        "order":orders,
        "total_orders":total_orders ,
         "pending":pending_orders,
         "placed":placed_orders,
         "delivered":delivered_orders,
         "out_delivery":out_for_delivery,

         "customers":customers,
         "products":products,
         }

    return render(request,'dennis/index.html',context)


from dennis.filters import Order_filter
def customer(request,pk):
    
    customer = Customer.objects.get(id=pk)

    # fetch the detail from 'Order' table as orders placed by specific user
    order_detail = customer.order_set.all()

    #Filter
    my_filter= Order_filter(request.GET,queryset=order_detail)
    order_detail = my_filter.qs

    context = {
        "order_detail" :order_detail,
        "customer":customer,
        "my_filter":my_filter,
            }

    return render(request,"dennis/customer.html",context)


###################  Create New order Using forms ##################

from dennis.forms import Create_Order_Form
from django.shortcuts import redirect

@login_required(login_url="login")
def createOrder(request):
    form = Create_Order_Form()

    if request.method == "POST":
        form = Create_Order_Form(request.POST)

        if form.is_valid() :
            form.save()
            return redirect("/dennis")

    context ={"form":form}
    return render(request,"dennis/create_order.html",context)


###############################

##################  Update Order status #####################

def update_order(request,pk):

    order = Order.objects.get(id=pk)
    instance_form = Create_Order_Form(instance=order)  # get the prefilled values in form

    if request.method =="POST":
        # get the updated values 
        # instance = order => update the form of particluar user whose id = pk
        instance_form = Create_Order_Form(request.POST,instance=order)

        if instance_form.is_valid():
            instance_form.save()
            return redirect("/dennis")

    context ={"form":instance_form}    
    return render(request,"dennis/update_order.html",context)
###############################


################# Delete order #############;

def delete_order(request,pk):
    order = Order.objects.get(id=pk)

    if request.method =="POST" :
        order.delete()
        return redirect("/dennis")
    
    context ={"item":order}

    return render(request,"dennis/delete_order.html",context)

    

####################################

################## Create Mulitple Order ###############
# helps to create multiple forms inside single form

from django.forms import inlineformset_factory   
# Customer => Parent model
# Order => child model 
# fields=('order_name','order_status') => Fields we want in the form
# extra =4 => create 4 forms 
def multiple_order(request,pk):
    Multiple_Forms = inlineformset_factory(Customer,Order,fields=('order_name','order_status'),extra=4)
    customer = Customer.objects.get(id = pk)

    # get the initial products of customer
    # multi_form = Multiple_Forms(instance=customer)

    # Hides the initial products of customer
    multi_form = Multiple_Forms(queryset=Order.objects.none(),instance=customer)

    """ set the value of "placed_by" in "Create_Order_Form" which uses the 'order' table fields and set  "customer" name automatic

    form = Create_Order_Form(initial={'placed_by':customer})
 """
    if request.method == "POST":
        # form = Create_Order_Form(request.POST)
        multi_form = Multiple_Forms(request.POST,instance=customer)

        if multi_form.is_valid():
            multi_form.save()
            return redirect("/dennis")

    context ={"customer":customer ,"form":multi_form}
    return render(request,"dennis/multiple_order.html",context)

#####################################


#################### Register  #################

from django.contrib.auth.forms import UserCreationForm
from dennis.forms import Create_User_Form 
from django.contrib import messages
from django.contrib.auth.models import Group 

@unauthencticated_user
def register_page(request):
    # form = UserCreationForm()
    form = Create_User_Form()

    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = Create_User_Form(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            """
            This code is handle in signal.py file

                        # Adding the new user to "customer" group automatically
                        group = Group.objects.get(name="customer")
                        user.groups.add(group)

                        # when the new user is created assigned the customer profile
                        # Link the customer table  with user table

                        Customer.objects.create( 
                                            user= user,
                                            name = user.username,
                                            email = user.email,  
                                                    )  
            """
            messages.success(request,"Account is created succesfuly for "+username)
            return redirect('login')

    context ={"form":form}
    return render(request,"dennis/register.html",context)

#####################

#################### Login  #################

from django.contrib.auth import authenticate, login


@unauthencticated_user
def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None : 
            login(request,user)
            return redirect('home')
        else:

            messages.info(request,"Invalid username or password !!!")
    context ={}
    return render(request,"dennis/login.html",context)

#####################

##################### Logout ######################
from django.contrib.auth import logout


def logout_page(request):
    
    logout(request)
    return redirect("login")


#####################


####################### User page #############

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])  # only customer access this page
def user_page(request):

    # get the id of user
    # pk  = request.user.id
    # customer Table
    # customer = Customer.objects.get(id=pk)

    # order Table
    # order_detail = customer.order_set.all()

    # One liner :  grab all the order of the customer
    order_detail = request.user.customer.order_set.all()

    # queries on order Table
    total_orders = order_detail.count()
    pending_orders = order_detail.filter(order_status='Pending').count()
    placed_orders = order_detail.filter(order_status="Placed").count()
    delivered_orders = order_detail.filter(order_status='Delivered').count()
    out_for_delivery = order_detail.filter(order_status='Out For Delivery').count()

    context = {
        "customer":customer,
        "order":order_detail,
        "total_orders":total_orders,
        "pending_orders":pending_orders,
        "placed_orders":placed_orders,
        "delivered_orders":delivered_orders,
        "out_for_delivery":out_for_delivery
        }

    return render(request,"dennis/user.html",context)

###############


####################### Accounts Settings
from dennis.forms import CustomerForm

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def account_settings(request):

    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()
            return redirect("user_page")

    context ={"form":form}
    return render(request,'dennis/accounts.html',context)


################

def queries(request):

    # Get all  the products by tag of "Kitchen stuff" :( query Many to Many fields)  : {tags is many to many field}
    #  tags = models.ManyToManyField(Tag)

    products = Products.objects.filter(tags__name="kitchen stuff")

    category = Producst.objects.filter(product_category ="Men")

    #Returns the First customer in table
    firstcustomer= Customer.objects.first()
    
    #Returns the last customer in table
    lastcustomer= Customer.objects.last()

    # Returns the total no of order in order
    total_orders = Order.objects.all().count()

    # Returns the no of order "planced" 
    placed_orders = orders.filter(order_status="Placed").count()

    #Returns single customer by name
    customerByName = Customer.objects.get(name="Gurpreet")

    #Returns single customer by name
    customerById = Customer.objects.get(id=1)

    #Returns all the orders[table 'Order'] related to customer (firstcustomer)
    # relationship bw Customer and order table

    all_orders = firstcustomer.order_set.all()

    # Returns the total count for number of time a "Realme 2" was ordered by the gurpreet

    """ # Get the gurpreet : Now Make a query on gurpreet
        # Now we have to make the queries on the 'Order' table
        # Get the order_name from order table : order_set.filter(order_name)
        # Where 'order_name' is the foreign key which is linked with the 'Product' table and the name of the product is store under the name of "product_name"
        # Now we have to make the reference to the product_name
        # filter(order_name__product_name="Realme 2"
    """
    #reference to the foreign key value
    gurpreet = Customer.objects.get(name="Gurpreet")
    realme_order = gurpreet.order_set.filter(order_name__product_name="Realme 2").count()