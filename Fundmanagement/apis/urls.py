from django.urls import path
from . import views

urlpatterns = [
    #Admin urls
    path('admin_log/',views.Admin_Log_api.as_view()),
    path('admin_cre_fm/',views.Admin_cre_FM.as_view()),
    path('Admin_List_FM/',views.Admin_List_FM.as_view()),
    path('Admin_List_cust/',views.Admin_List_Cust.as_view()),
    path("Admin_get_FMid/<int:pk>",views.Admin_retrive_FM.as_view()),
    path("Admin_get_custid/<int:pk>",views.Admin_retrive_Cust.as_view()),
    
    
    #FM urls
    path('Fm_login/',views.FM_Login_api.as_view()),
    path('FM_list/',views.FM_Userview.as_view()),
    path('FM_cre_cust/',views.FM_create_Customer.as_view()),
    path('FM_list_cust/',views.FM_list_cust.as_view()),
    path('FM_list_cust/<int:pk>',views.FM_list_custid.as_view()),
    path('Fm_cre_hold/',views.create_holdings.as_view()),

    #Cust urls
    path('Cust_login/',views.Login_Customer.as_view()),
    path('holdings_list/',views.Cust_list_Holdings.as_view()),
    path('cust_cre_hold/',views.cust_create_holding.as_view()),
    path('cust_sell/<int:pk>',views.Cust_sell.as_view())
]
