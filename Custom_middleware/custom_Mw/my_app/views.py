from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def myView(request):
    print("inside My view")
    return HttpResponse({"message":"inside view"})