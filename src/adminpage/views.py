from django.shortcuts import render

# Create your views here.

def adminpage(request):
    return render(request, 'admins/dashboard.html')
    
