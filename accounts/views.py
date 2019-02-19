from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import LoginForm
from administration.views import service_base


# Create your views here.
def user_login(request):
    err = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(service_base)
                else:
                    err = 'Disabled account'
            else:
                err = 'Invalid login'
            form.password = ""
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'errMsg': err})


def user_logout(request):
    logout(request)
    return redirect(user_login)
