from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import MyUserCreationForm


User = get_user_model()

def register_user(request):

    form_template = MyUserCreationForm()

    if request.method == 'POST':

        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("room:home")
        else:
            return render(request, 'room/login.html', {
                "message": "an error occured during registration. Please try again",
                "form": form_template,
            })

    return render(request, 'room/register.html', {
        "form": form_template,
    })


def login_page(request):

    if request.method == 'POST':

        if request.user.is_authenticated:
            return redirect("room:home")
        
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = None
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, 'room/login.html', {
                "message": "Email does not exist"
            })
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("room:home")
            return render(request, 'room/login.html', {
                "message": "Invalid login credentials"
            })

    # if there is a get request        
    return render(request, 'room/login.html')


def logout_page(request):

    if request.user.is_authenticated:
        logout(request)
    
    return redirect("room:login")