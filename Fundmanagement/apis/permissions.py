from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from .models import AdminUser,Holdings
import jwt

class Is_Admin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.Role =='Admin':
            return False
        return True
    
class IS_FM(BasePermission):
    def has_permission(self, request,view):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user =AdminUser.objects.filter(id=payload['id']).first()
        
        if user.Role=='FM' and user.Is_FM==True:
            print("inside Permission custom")
            return True
        else:
            return False
        
class IS_CUST(BasePermission):
    def has_permission(self, request,view):
        token =request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthentication')
        
        try:
            payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user =AdminUser.objects.filter(id=payload['id']).first()
        
        if user.Role=='CUST' and user.Is_Customer==True:
            print("inside Permission custom")
            return True
        else:
            return False
        