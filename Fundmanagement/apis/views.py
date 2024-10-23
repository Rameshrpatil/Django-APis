from django.shortcuts import render
from .serializers import AdminSerilizer,FundmanagerSerializer,CustomerSerializer,HoldingsSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework import generics
from .models import AdminUser,Holdings
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import Is_Admin,IS_FM,IS_CUST
import jwt, datetime
# Create your views here.

class Admin_Log_api(generics.ListCreateAPIView):
    # serializer_class =AdminSerilizer
    
    def post(self,request):
        serializer=AdminSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['username'])
        print(serializer.validated_data['password'])
        
        user=authenticate(request,username=serializer.validated_data['username'],password=serializer.validated_data['password'])
        print(user.username)
        print(user.password)
        print(user.email)
        print(user.Role)
        
        if user.Role =='Admin':
            return Response('Admin login Success')
        return Response({'msg':"invalid Uername or password"})
    
class Admin_cre_FM(generics.CreateAPIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAdminUser,Is_Admin]
    def post(self,request):
        data=request.data
        user_instance=request.user
        # print(user_instance.id)
        request.data['Foriegn_id']=user_instance.id
        serializer =FundmanagerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class Admin_List_FM(generics.ListAPIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[Is_Admin,IsAdminUser]
    serializer_class=FundmanagerSerializer
    queryset=AdminUser.objects.all()
    def get_queryset(self):
        return AdminUser.objects.filter(Role="FM").all()
    
class Admin_List_Cust(generics.ListAPIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[Is_Admin,IsAdminUser]
    serializer_class=CustomerSerializer
    queryset=AdminUser.objects.all()
    def get_queryset(self):
        return AdminUser.objects.filter(Role="CUST").all()
    

class Admin_retrive_FM(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[Is_Admin,IsAdminUser]
    serializer_class=FundmanagerSerializer
    queryset=AdminUser.objects.all()
    
class Admin_retrive_Cust(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[Is_Admin,IsAdminUser]
    serializer_class=CustomerSerializer
    queryset=AdminUser.objects.all()
    

class FM_Login_api(generics.CreateAPIView):
    def post(self,request):
        username= request.data['username']
        password=request.data['password']
        
        user=AdminUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user doesnt exists')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        # return Response({'msg':'Success'})
        
        if user.Role =='FM':
            payload ={
                'id':user.id,
                'exp':datetime.datetime.utcnow() +datetime.timedelta(minutes=10),
                'iat':datetime.datetime.utcnow()
            }
            
            token =jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
            
            response =Response()
            
            response.set_cookie(key='jwt',value=token,httponly=True)
            response.data ={
                'jwt':token
            }
            
            return response
            
    
class FM_Userview(generics.ListAPIView):
    def get(self,request):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user =AdminUser.objects.filter(id=payload['id']).first()
        serializer =FundmanagerSerializer(user)
        
        return Response(serializer.data)
    
class FM_list_cust(generics.ListAPIView):
    permission_classes=[IS_FM]
    serializer_class=CustomerSerializer
    queryset =AdminUser.objects.all()
    def list(self,request,*args, **kwargs):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        queryset = self.queryset.filter(Foriegn_id=payload['id'])
        serializer = self.get_serializer(queryset, many=True)  # Serialize queryset
        return Response(serializer.data) 
    
class FM_list_custid(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IS_FM]
    serializer_class=CustomerSerializer
    queryset=AdminUser.objects.filter(Role='CUST').all()
    
class create_holdings(generics.CreateAPIView):
    permission_classes=[IS_FM]
    def post(self,request):
        token =request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthentication')
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user = AdminUser.objects.filter(id=request.data['holder']).first()
        if user.Foriegn_id == payload['id']:
            serilizer =HoldingsSerializer(data=request.data)
            serilizer.is_valid(raise_exception=True)
            serilizer.save()
            return Response(serilizer.data)
        return Response({"msg":"something went wrong","user":user})
        
    
class Logoutview(generics.CreateAPIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            "msg":"successfull logout"
        }
        return response
    

class FM_create_Customer(generics.CreateAPIView):
    permission_classes=[IS_FM]
    def post(self,request):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        request.data['Foriegn_id']=payload['id']
        serializer =CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class Login_Customer(generics.CreateAPIView):
    # permission_classes=[IS_CUST]
    def post(self,request):
        username= request.data['username']
        password=request.data['password']
        
        user=AdminUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('user doesnt exists')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        # return Response({'msg':'Success'})
        
        if user.Role =='CUST':
            payload ={
                'id':user.id,
                'exp':datetime.datetime.utcnow() +datetime.timedelta(minutes=10),
                'iat':datetime.datetime.utcnow()
            }
            
            token =jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
            
            response =Response()
            
            response.set_cookie(key='jwt',value=token,httponly=True)
            response.data ={
                'jwt':token
            }
            
            return response
        
class Cust_list_Holdings(generics.ListAPIView):
    permission_classes=[IS_CUST]
    serializer_class=HoldingsSerializer
    queryset =Holdings.objects.all()
    def list(self,request,*args, **kwargs):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        queryset = self.queryset.filter(holder=payload['id'])
        serializer = self.get_serializer(queryset, many=True)  # Serialize queryset
        return Response(serializer.data) 
    
class Cust_sell(generics.RetrieveDestroyAPIView):
    permission_classes=[IS_CUST]
    serializer_class=HoldingsSerializer
    queryset=Holdings.objects.all()
    def list(self,request):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        queryset = self.queryset.filter(holder=payload['id'])
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
    def delete(self,request,pk):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user=Holdings.objects.filter(id=pk).first()
        print(user.holder_id)
        if user.holder_id == payload['id']:
            user.delete()
        return Response({'msg':"deleted"})
        
        
class cust_create_holding(generics.CreateAPIView):
    permission_classes=[IS_CUST]
    def post(self,request):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        request.data['holder']=payload['id']
        serializer =HoldingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    