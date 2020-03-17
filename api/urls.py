
from django.urls import path  ,include
from api import views

urlpatterns = [

    path("",views.index,name="index"),
    path("json",views.json_data,name="json"),
    path("json_rest",views.json_rest_response,name="json_rest"),
    path("json_serialize",views.json_serializer,name="json_serialize"),
    path("json_detail/<int:pk>",views.json_serializer_detail,name="json_detail"),
    path("json_create",views.json_serializer_create,name="json_create"),
    path("json_update/<int:pk>",views.json_serializer_update,name="json_update"),
    path("json_delete/<int:pk>",views.json_serializer_delete,name="json_delete"),

    # In order to use authentication for api
    path('rest-auth/', include('rest_auth.urls')),

              ]  


