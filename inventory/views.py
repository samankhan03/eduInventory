from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def inventory_user(request):
    return render(request, 'inventory_user.html')

def inventory_admin(request):
    return render(request, 'inventory_admin.html')
def admin(request):
    return HttpResponse('<p>hello </p>')
