from django.shortcuts import render
from .serializer import userserializer
from rest_framework import viewsets,status
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
# from rest_framework.decorators import lo
from django.contrib.auth import authenticate
from rest_framework.decorators import  api_view
from django.contrib.auth.models import User

# Create your views here.

class Userviewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=userserializer
 
    @action(detail=False,methods=['Post']) 
    def newuser(self,request):
     serializer=self.get_serializer(data=request.data)
     if serializer.is_valid():
         serializer.save()
         return Response ({'message':'Your registration is completed'},status=status.HTTP_201_CREATED)
     return Response ({'error':'Registration is not get well,Try again'},status=status.HTTP_400_BAD_REQUEST)
     

    @action(detail=False,methods=['Post']) 
    def login(self,request):
       if request.method == 'POST':  
        username=request.data.get('username')
        password=request.data.get('password')
        print(username,password)

        user=None

        if '@' in username:
            try:
                user=User.objects.get(email=username)
                print(user)
                if not user.check_password(password):
                  user = None  
            except User.ObjectDoesNotExist:
                pass
        
        if not user:
            user=authenticate(username=username,password=password)
        
        

        if user:
            token, _ = Token.objects.get_or_create(user=user)
           
            return Response({'token': token.key,'user_id':user.id}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False,methods=['Post']) 
    def logout(self,request):
          if request.method == 'POST':
               try:
                      request.user.auth_token.delete()
                      return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
               except:
                      return Response({'error': 'Logout process donot go well.'}, status=status.HTTP_200_OK)
                   

















    

