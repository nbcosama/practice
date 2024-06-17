from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import *
from rest_framework.decorators import api_view
from .serializders import *
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.




def home(request):
    
    return render(request, 'index.html')
    
    
    
    
@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([])
@permission_classes([])
def students(request):
    if request.method == 'GET':
        datas = request.data
        # id = datas.get('id')
        students = Student.objects.all()
        student_serializer = StudentSerializer(students, many=True)
        return Response(student_serializer.data)
    elif request.method == 'POST':
        datas = request.data
        # id = datas.get('id')
        serialize = StudentSerializer(data = datas)
        if serialize.is_valid():  
            try: 
                username = datas["name"]
                if username:
                    name = username.lower().replace(" ", "")
                create_user = User.objects.create_user(username=name, password=datas["password"])
            except Exception as e:
                return Response({'message': 'User already exist' , 'error' :str(e)})    
            token_obj = Token.objects.get_or_create(user=create_user)
            serializesss = Student.objects.create(name=datas['name'], roll=datas['roll'], city=datas['city'], marks=datas['marks'], user=create_user)
            serializesss.save()
            # print(serialize.data)
            return Response({'status':200, 'payload': serialize.data, 'token': str(token_obj[0])}, status=201)
        return Response(serialize.errors)
       
    
    
    
    
@api_view(['POST', 'PUT', 'DELETE'])
def login(request):
    if request.method == 'POST':
        data = request.data
        # username = data.get('username')
        # password = data.get('password')
        try:
            user = User.objects.get(username=data['username'])
            if user.check_password(data['password']):
                student_profile = Student.objects.get(user_id=user.id)
                problems = Problems.objects.filter(user=user)
                prob_serialize = ProblemsSerializer(problems, many=True)
                serialize = StudentSerializer(student_profile, many=False)
                token_obj = Token.objects.get_or_create(user=user)
                return Response({'User': serialize.data, 'problems':prob_serialize.data,  'token': str(token_obj[0])})
            else:
                return Response({'message': 'Invalid password'})
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'})
    else:
        return Response({'message': 'Invalid Request'})
      
    
    
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_problems(request):
    if request.method == 'POST':
        user = request.user
        problems = Problems.objects.filter(user=user)
        prob_serialize = ProblemsSerializer(problems, many=True)
        return Response({'problems':prob_serialize.data})
    else:
        return Response({'message': 'Invalid Request'})
    
    
    
    
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_problem(request):
    problem = ProblemsSerializer(data=request.data)
    if problem.is_valid():
        problem = Problems.objects.create(title=request.data['title'], description=request.data['description'], user=request.user)
        problem.save()
        return Response('Problem Register')
    return Response('Problem')















# @api_view(['GET', 'POST'])
# def home(request):
#     if request.method == 'GET':
#         students = {
#                     'Name':'Osama',
#                     'id': 1,
#                     "data" : [ ' 1', '2', '3']
#                     }
#         return Response(students)
#     elif request.method == 'POST':
#         data = request.data
#         print(data)
#         print(data['data'])
#         return Response('POST request')