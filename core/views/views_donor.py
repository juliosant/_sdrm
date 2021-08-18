from core.models import Profile
from django.shortcuts import redirect, render
from ..forms import LoginForm, RegisterDonorForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages

# Create your views here.
def user_type(login_url=None):
    return user_passes_test(lambda u: u.profile_type == 'D', login_url=login_url)

def register_donor(request):
    if request.POST:

        post = request.POST.copy()
        post['profile_type'] = Profile.PROFILE_TYPE_CHOICES[0][0]
        post['username'] = post['first_name'].lower() + post['last_name'].lower() + str(7)
        request.POST = post

        register_form = RegisterDonorForm(request.POST)
        
        if register_form.is_valid():
            register_form.save()
            return redirect('login_donor')
        else:
            messages.info(request, 'Não deu certo')
            return redirect('register_donor')
            #return HttpResponse("<h1>Não deu certo</h1>")
    register_form = RegisterDonorForm()
    content = {
        'register_form': register_form
    }
    return render(request, 'profile/donor/register.html', content)


def login_donor(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['user'], password=cd['password'])
            if user is not None and user.profile_type == 'D':
                login(request, user)
                return redirect('userpage_donor')
            else:
                messages.info(request, 'Não autorizado')
                return redirect('login_donor')
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'profile/donor/login.html', content)


def logout_donor(request):
    logout(request)
    return redirect('login_donor')


@login_required(login_url='login_donor')
@user_type(login_url="login_donor")
def userpage(request):
    return render(request, 'profile/donor/home.html')


@login_required(login_url='login_donor')
@user_type(login_url="login_donor")
def about_donor(request):
    return render(request, 'profile/donor/about.html')