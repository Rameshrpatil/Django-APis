from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ManagerLoginView
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import EmployeeListCreateView, EmployeeDetailView, CreateManager


schema_view = get_schema_view(
    openapi.Info(
        title="Manager-Employee API",
        default_version='v1',
        description="API documentation for managing employees under managers using JWT authentication.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    # create manager 
    path('manager/create', CreateManager.as_view(), name='create-manager'),
    # manager logins 
    path('manager/login/', ManagerLoginView.as_view(), name='manager-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Your API endpoints
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Swagger and ReDoc documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

