from django.shortcuts import render
from django.http import JsonResponse
from nlp import utilities

# Create your views here.
def homePage(request):
    return render(request,"index.html")

def nlpRequest(request):
    print(utilities.process())
    return JsonResponse({"nlpResponse": "hola mundo"})