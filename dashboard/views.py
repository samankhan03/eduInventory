from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def dashboard_user(request):
    return render(request, 'dashboard_user.html')
def admin(request):
    return HttpResponse('<p>hello </p>')
