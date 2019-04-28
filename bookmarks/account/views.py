from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


# Form for authenticate user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # CHECK - Do ktorej bazy sie laczy aby sprawdzić? Gdzie to jest trzymane?
            # SOL. django.contrib.auth dostarcza modele do tego. Baza main.auth_user
            # authenticate - check user correctness and return not null if all is ok
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    # login - set user in current session
                    login(request, user)
                    return HttpResponse("Authenticated " \
                                        "successfully")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
