from django.shortcuts import render
from django.http import JsonResponse
from nlp import utilities

# Create your views here.
def homePage(request):
    return render(request,"index.html")

def nlpRequest(request):
    intput = request.GET.get("nlp_request")

    return JsonResponse({"nlpResponse": str(utilities.process(intput))})