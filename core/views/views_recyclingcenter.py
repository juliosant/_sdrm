from django.contrib.auth import login, logout, authenticate
from core.models import Profile
from django.http.response import HttpResponse
from core.forms import LoginForm, RegisterPlaceForm, RegisterRecyclingForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register_recyclingCenter(request):
    if request.POST:
        post = request.POST.copy()
        post['last_name'] = 'PANDURATA'
        post['username'] = 'empresai'
        post['profile_type'] = Profile.PROFILE_TYPE_CHOICES[1][0]
        request.POST = post

        print(request.POST)

        register_recycling_form = RegisterRecyclingForm(request.POST)
        register_place_form = RegisterPlaceForm(request.POST)

        if register_recycling_form.is_valid() and register_place_form.is_valid():
            place = register_place_form.save()
            recycling = register_recycling_form.save(commit=False)
            recycling.place = place
            recycling.save()
            return redirect('login_recyclingcenter')
        else:
            return HttpResponse("<h1>Não rolou!</h1>")

    register_recycling_form  = RegisterRecyclingForm()
    register_place_form = RegisterPlaceForm()
    
    content = {
        'reg_recycling_form': register_recycling_form,
        'register_place_form': register_place_form
    }
    return render(request, 'profile/recyclingCenter/register.html', content)


def login_recyclingCenter(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['user'], password=cd['password'])
 
            if user is not None and user.profile_type == 'P':
                login(request, user)
                return redirect('userpage_recyclingcenter')
            else:
                messages.info(request, 'Não deu certo')
                return redirect('login_recyclingcenter')
    
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'profile/recyclingCenter/login.html', content) 


def logout_recyclingCenter(request):
    logout(request)
    return redirect('login_recyclingcenter')


@login_required(login_url='login_recyclingcenter')
def userpage(request):
    return render(request, 'profile/recyclingCenter/home.html')





