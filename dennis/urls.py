from django.urls import path
from dennis import views

from django.contrib.auth import views as auth_views  # for reset the password

urlpatterns = [
    path("",views.home,name="home"),
    path("register",views.register_page,name="register"),
    path("login",views.login_page,name="login"),
    path("logout",views.logout_page,name="logout"),
    path("user_page",views.user_page,name="user_page"),
    path("accounts",views.account_settings,name="accounts"),



    path("customer/<str:pk>",views.customer,name="customer"),
    path("create_order",views.createOrder,name="create_order"),
    path("update_order/<int:pk>",views.update_order,name="update_order"),
    path("delete_order/<int:pk>",views.delete_order,name="delete_order"),
    path("multiple_order/<int:pk>",views.multiple_order,name="multiple_order"),

    # using bulit in class based views to reset password and their name is also predefined
    # submit email form
    path("reset_password/",auth_views.PasswordResetView.as_view(template_name="dennis/password_reset.html"),name="reset_password"),
    # Email sent message success
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="dennis/password_reset_sent.html"),name="password_reset_done"),
    # Link to password reset form in email
    path("reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(template_name="dennis/password_reset_form.html"),
    name="password_reset_confirm"),

    # password succesfully changed message
    path("reset_password_complete/",
    auth_views.PasswordResetCompleteView.as_view(template_name="dennis/password_reset_done.html"),
    name="password_reset_complete"),




    
]