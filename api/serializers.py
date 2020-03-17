

from api.models import Task
from rest_framework import serializers


class Task_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = "__all__"