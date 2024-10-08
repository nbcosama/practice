from django.shortcuts import render, redirect
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
from .otp import *
import smtplib

from django.utils import timezone
from datetime import timedelta
from pptx import Presentation
from django.contrib import messages
import uuid
# Create your views here.




def home(request):
    if not request.session.get('has_visited'):
        request.session['has_visited'] = True
        visit_count, created = VisitCount.objects.get_or_create(id=1)
        visit_count.count += 1
        visit_count.save()
        
    visitors_count = VisitCount.objects.first().count if VisitCount.objects.exists() else 0
    files = StudyMaterials.objects.all().order_by('-id')
    # delete all file in 24 hours
    for file in files:
        if file.date < timezone.now() - timedelta(days=1):
            file.pptx.delete()
            file.delete()
            return redirect(home)
    if request.method == 'POST' :
        if request.GET.get("action") == "add":
            PPTX_file = request.FILES.get('study_material')
            password = request.POST.get('password')
            title = request.POST['title']
            if PPTX_file and title :
                studey_material = StudyMaterials.objects.create(title=title, password = password,  pptx=PPTX_file)
            else:
                return HttpResponse('Please fill all the fields')
            messages.success(request, 'File Successfully Uploaded')
            return redirect('/')
        elif request.GET.get("action") == "get":
            id = request.GET.get('id')
            password = request.POST.get('password')
            file = StudyMaterials.objects.get(id=id)
            if file.password == request.POST.get('password'):
                return render(request, 'index.html',  {'securedfiles': file, 'visitors_count':visitors_count})
            else:
                messages.error(request, 'Password is incorrect')
                return redirect(home)
    context = {'files': files, 'visitors_count':visitors_count}        
    return render(request, 'index.html', context)
    
    
  
  
  
  
def community(request):
    
    datas = ShareProblems.objects.all().order_by('-id')
    if request.method == 'POST' :
        if request.GET.get("action") == "add":
            title = request.POST.get('title')
            description = request.POST.get('description')
            code = request.POST.get('code') 
            tags = request.POST.get('tags')
            try:
                studey_material = ShareProblems.objects.create(title=title, description=description, code=code, tags=tags)
                messages.success(request, 'File Successfully Uploaded')
                return redirect('community')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                return redirect('community')
    context = {'datas':datas}
    return render(request, 'view.html', context)
  
  
def community_detail(request):
    id = request.GET.get('id')
    datas = ShareProblems.objects.get(id=id)
    return render(request, 'render.html', {'datas': datas})
  
  
  
  
  
  
  
  
    
    
    
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
        to_email = datas.get('email')
        otp_code = datas.get('otp')
        try:
            filtered_code = OtpCode.objects.get(otpcode=otp_code, email = to_email)
        except OtpCode.DoesNotExist:
            filtered_code = None  # Or any other appropriate action
        
        
        verify_otp = send_otp(request, to_email)
        if otp_code == "":
            return Response({"message": "Please Verify Your Account"})
        
        elif filtered_code:
            # check otp from OtpCode object
            
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
                # serializesss.save()
                # print(serialize.data)
                return Response({'status':200, 'payload': serialize.data, 'token': str(token_obj[0])}, status=201)
        else:
            return Response({'message':'Please enter a valid code'})
    return Response(serialize.errors)
       
    
    
    
    
@api_view(['POST', 'PUT', 'DELETE'])
def login(request):
    if request.method == 'POST':
        data = request.data
        # username = data.get('username')
        # password = data.get('password')
        if data is None:
            return Response({'message': 'Invalid Request'})
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







@api_view(['POST'])
def sendemail(request):
    email = "smtp.otp@gmail.com"
    app_password = "emir yxvo wpsr ctuv"  # Use the app password here
    
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=email, password=app_password)
    connection.sendmail(from_addr=email, to_addrs="mohammadosama2021@gmail.com", msg="Hi md osama")
    connection.close()
    return Response({"message": "working", "mail": "Sent"})







@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def degree(request):
    if request.method == 'GET':
        degree = Degree.objects.all()
        degree_serializer = DegreeSerializer(degree, many=True)
        return Response(degree_serializer.data)
    else:
        return Response({'message': 'Invalid Request'})















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