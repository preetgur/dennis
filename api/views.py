from django.shortcuts import render,HttpResponse
from django.http import JsonResponse


def index(request):
    return render(request,"api/index.html")


def json_data(request):

    data ={
        "Name": "Gurpreet Singh",
        "Mobile":9914204589,
        "Email": "preetgur0137@gmail.com",
        "Qualification":"B.Tech [CSE]",
        "Address": "Village Khandoli,Tehsil Rajpura"
                }

    return JsonResponse(data,safe=False)



from rest_framework.decorators import api_view
from rest_framework.response import Response    

@api_view(['GET'])
def json_rest_response(request):

    data ={
        "Name": "Gurpreet Singh",
        "Mobile":9914204589,
        "Email": "preetgur0137@gmail.com",
        "Qualification":"B.Tech [CSE]",
        "Address": "Village Khandoli,Tehsil Rajpura"
                }
    return Response(data)


from api.serializers import Task_Serializer
from api.models import Task

@api_view(['GET'])
def json_serializer(request):
    tasks = Task.objects.all()
    serializer = Task_Serializer(tasks,many=True)
    return Response(serializer.data)


# Detail view : fetch the data of singel oject
# hit url : => http://127.0.0.1:8000/json_detail/6
@api_view(['GET'])
def json_serializer_detail(request,pk):
    tasks = Task.objects.get(id =pk)
    serializer = Task_Serializer(tasks,many=False)
    return Response(serializer.data)    


# Create view : Create the element in database
# hit url : => http://127.0.0.1:8000/json_create
from django.contrib.auth.decorators import login_required

@login_required(login_url='/rest-auth/login/')
@api_view(['POST'])
def json_serializer_create(request):

    serializer = Task_Serializer(data=request.data)  # for forms it is : request.Post

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)    


# update view : Update the database using api
# hit url : => http://127.0.0.1:8000/json_update/8
@api_view(['POST'])
def json_serializer_update(request,pk):
    tasks = Task.objects.get(id = pk)
    serializer = Task_Serializer(instance=tasks, data=request.data) 

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)    

# Delete api 
@api_view(['DELETE'])
def json_serializer_delete(request,pk):
    tasks = Task.objects.get(id = pk)
    tasks.delete()

    return Response("Items is Deleted .. !")    

 
    
