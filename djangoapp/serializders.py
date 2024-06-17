from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city', 'marks']
        
        
        
class ProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ['title', 'description']