from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from PyPDF2 import PdfReader
from . functions import *
import json

# Create your views here.
def upload(request):
    if request.method == "POST":
        file = request.FILES['file']
        pdf_read(file)
        print("SUSSSSSSSSSSSS")
        return JsonResponse({"message": "Succesful"})
    else:
        return HttpResponse("Hello world!")
    
def getQuery(request):
    if request.method == "POST":
        question = request.POST.get('query_data', '')
        embeded_question = text_embedding(question)
        search_response = semantic_search(embeded_question)
        print(search_response)

        return JsonResponse({"message" : "successful!!!!!!!"})
    else:
        return HttpResponse("Get File")