from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        #Getting the post parameters 
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password1 =request.POST['password1']
        password2=request.POST['password2']

        if len(username)>15:
            messages.error(request,'Username must be under 15 characters')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request,'Username should only contain letters and numbers')
            return redirect('signup')
        
        if len(password1)<8:
            messages.error(request,'Password length must be atleast 8 characters or greater')
            return redirect('signup')
        if password1 == password2:
            if User.objects.filter(username=username).exists() == False:
                if User.objects.filter(email=email).exists() == False:
                    #Create the user
                    myuser= User.objects.create_user(username,email,password1)
                    myuser.first_name=fname
                    myuser.last_name=lname
                    myuser.save()
                    messages.success(request, 'Your Account has been created successfully')
                    return redirect('signup')
                else:
                    messages.error(request,'Email already taken')
                    return redirect('signup')

            else:
                messages.error(request,'Username already taken')
                return redirect('signup')
        else:
            messages.error(request,'Passwords donot match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        #Getting the post parameters 
        loginusername= request.POST['loginusername']
        loginpassword= request.POST['loginpassword']
        
        user=authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            auth_login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request,"Invalid Username or Password Please try again!")
            return redirect('login')
            
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')