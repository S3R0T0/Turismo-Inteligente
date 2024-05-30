from django.shortcuts import render
from django.http import JsonResponse
from nlp import utilities

# Create your views here.
def homePage(request):
    return render(request,"index.html")

def nlpRequest(request):
    return JsonResponse({"nlpResponse": "hola mundo"})