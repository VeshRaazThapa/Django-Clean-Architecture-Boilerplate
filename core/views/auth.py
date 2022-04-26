from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect

from user.forms import UserCreationForm
from user.models import UserProfile

User = get_user_model()


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            # if isinstance(username, int):
            #     # username is a house_number in this case
            #     user = authenticate(house_number=username, password=password)
            # else:
            # username is the actual username in this case
            user = authenticate(username=username, password=password)
            if not user:
                return render(request, 'accounts/login.html', {'msg': 'Username or password mismatch.'})
            else:
                if user.is_active:
                    login(request, user)
                    try:
                        if user.roles.group.name == "General":
                            return redirect('house-information-view')
                        else:
                            return redirect("/")
                    except:
                        return redirect("/")
                else:
                    return render(request, 'accounts/login.html', {'msg': 'This user is not active.'})
        else:
            return render(request, 'accounts/login.html', {'msg': 'Username or password missing.'})
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            # save the profile of the user
            profile = UserProfile()
            profile.user = user
            profile.house_number = form.cleaned_data.get('house_number', '')
            profile.save()
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')
    else:
        return redirect('/login')
