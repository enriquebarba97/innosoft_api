#from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import Ponente

def getPonentes(request):
  users = Ponente.objects.all()
  data = list(users.values("id","name","age"))
  return JsonResponse(data, safe=False)

def getPonenteById(request, param):
  data = Ponente.objects.filter(id=param)
  return JsonResponse(list(data.values("id","name","age")),safe=False)