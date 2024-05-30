from django.urls import path
from nlp import views

urlpatterns = [
    path("",views.homePage,name="homePage"),
    path("nlpRequest/",views.nlpRequest,name="nlpRequest")
]