from rest_framework import serializers
from .models import AdminUser, Holdings

import re


class AdminSerilizer(serializers.Serializer):
    username= serializers.CharField()
    password=serializers.CharField()
    # class Meta:
    #     model= AdminUser
    #     fields =['username','password']

class FundmanagerSerializer(serializers.ModelSerializer):
    class Meta:
        model =AdminUser
        fields= ['id','first_name','last_name','email','contact_info','Location','Associated_company','username','password','Role','Foriegn_id','Is_FM']
        extra_kwargs={
            'username':{'write_only':True},
            'password':{'write_only':True},
        }
        
    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance =self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def update(self,instance,validated_data):
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name =validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.contact_info=validated_data.get("contact_info", instance.contact_info)
        instance.Location=validated_data.get("Location", instance.Location)
        instance.Associated_company=validated_data.get("Associated_company", instance.Associated_company)
        instance.username=validated_data.get("username", instance.username)
        instance.Foriegn_id=validated_data.get("Foriegn_id",instance.Foriegn_id)
        new_password =validated_data.get("password")
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance
    
        
    def password_validate(self,value):
        if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',value):
            raise serializers.ValidationError('Invalid Password')
    
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminUser
        fields=['id','first_name','last_name','email','contact_info','Location','username','password','Role',"Foriegn_id",'Is_Customer']
        extra_kwargs={
            'username':{'write_only':True},
            'password':{'write_only':True}
        }
        
    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance =self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self,instance,validated_data):
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name =validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.contact_info=validated_data.get("contact_info", instance.contact_info)
        instance.Location=validated_data.get("Location", instance.Location)
        instance.username=validated_data.get("username", instance.username)
        new_password =validated_data.get("password")
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance
   
        
    def password_validate(self,value):
        if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',value):
            raise serializers.ValidationError('Invalid Password')
               

class HoldingsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Holdings
        fields ='__all__'