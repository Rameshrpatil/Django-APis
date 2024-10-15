from rest_framework import serializers
from .models import Manager, Employee
import re

# manager login serializer 
class ManagerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

#manager create srializer
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['first_name', 'last_name', 'email', 'date_joined','username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Make password write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.date_joined = validated_data.get('date_joined', instance.date_joined)
        instance.username = validated_data.get('username', instance.username)
        new_password = validated_data.get('password')
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance

    def validate_password(self, value):
        if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', value):
            raise serializers.ValidationError('Invalid Password')
        return value

#Emloyee Crud serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'designation', 'date_of_joining', 'is_active','profile_img' , 'manager']
        read_only_fields = ['manager']