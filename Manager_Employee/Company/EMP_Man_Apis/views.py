from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployeeSerializer, ManagerSerializer
from rest_framework.generics import get_object_or_404
from .models import Manager, Employee
from .serializers import ManagerLoginSerializer, EmployeeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import BasicAuthentication

class CreateManager(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=ManagerSerializer, responses={201: ManagerSerializer})
    def post(self, request):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return Response({'detail': 'Unauthorized. Only superusers can create managers.'}, status=status.HTTP_403_FORBIDDEN)
        
        # If the user is a superuser, proceed with the creation of a manager
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerLoginView(APIView):
    @swagger_auto_schema(request_body=ManagerLoginSerializer)
    def post(self, request):
        serializer = ManagerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        manager = Manager.objects.filter(username=username).first()
        if manager and manager.check_password(password):
            refresh = RefreshToken.for_user(manager)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "role": manager.id,
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class EmployeeListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes= [MultiPartParser]

    # List employees of the current manager
    @swagger_auto_schema(responses={200: EmployeeSerializer(many=True)})
    def get(self, request):
        employees = Employee.objects.filter(manager=request.user)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    # Create a new employee for the current manager
    @swagger_auto_schema(request_body=EmployeeSerializer, responses={201: EmployeeSerializer})
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(manager=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    # Retrieve an employee's details
    @swagger_auto_schema(responses={200: EmployeeSerializer})
    def get(self, request, pk):
        employee = get_object_or_404(Employee.objects.filter(manager=request.user), pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    # Update an employee's information
    @swagger_auto_schema(request_body=EmployeeSerializer, responses={200: EmployeeSerializer})
    def put(self, request, pk):
        employee = get_object_or_404(Employee.objects.filter(manager=request.user), pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete an employee
    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        employee = get_object_or_404(Employee.objects.filter(manager=request.user), pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
