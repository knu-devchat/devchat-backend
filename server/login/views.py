from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
@csrf_exempt
def login_with_github(req):
    if req.method == 'GET':
        return JsonResponse({'test': "test임"})

@csrf_exempt
def logout(req):
    pass