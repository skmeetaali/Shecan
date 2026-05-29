from django.shortcuts import render
from .models import NormalUserProfile
from .models import user
from django.http import HttpResponse
from traceback import print_exc

# Create your views here.
def home(request):
    return HttpResponse("Welcome to She Can Authentication App")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        age = request.POST.get("age")
        
        try:
            User = user.objects.create_user(username=username, password=password)
            User.save()
            user_profile = NormalUserProfile.objects.get(user=User)
            user_profile.name = name
            user_profile.age = age
            user_profile.save()
           
            return render(request, "authentication/register.html", {"message": "User created successfully"})
        
        except Exception as e:
            print(e)
            print_exc()
            return render(request, "authentication/register.html", {"message": "Error creating user"})
    return render(request, "authentication/register.html")

