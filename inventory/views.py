from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Inventory Page:)")

def htmlCall(request):
    return render(request, 'inventory_user.html')
