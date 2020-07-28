from django.shortcuts import render, HttpResponse

# Create your views here.
def simpleResponse(request):
    return HttpResponse('Game App')
