from django.contrib.auth import login, logout, authenticate
from django.db.models.query_utils import Q
from django.forms.models import inlineformset_factory
from core.models import Donation, Profile, RecyclabelMaterial
from django.http.response import HttpResponse
from core.forms import LoginForm, RegisterDonationForm, RegisterMaterialForm, RegisterPlaceForm, RegisterRecyclingForm, SearchDonorForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


def user_type(login_url=None):
    return user_passes_test(lambda u: u.profile_type == 'P', login_url=login_url)


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
@user_type(login_url="login_recyclingcenter")
def userpage(request):
    return render(request, 'profile/recyclingCenter/home.html')


@login_required(login_url='login_recyclingcenter')
@user_type(login_url="login_recyclingcenter")
def search_donor(request):

    content_search = None
    
    if request.POST:
        if len(request.POST['search']) >= 3:
            try:
                search_id = request.POST['search']
            except ValueError:
                pass

            search = Q(
                Q(
                    Q(id__contains=search_id) | 
                    Q(first_name__contains=request.POST['search']) | 
                    Q(last_name__contains=request.POST['search'])) & 
                Q(profile_type__exact='D'))

            content_search = Profile.objects.filter(search)
        else:
            messages.info(request, 'Digite no mínimo 3 caracteres')
    
    search_donor_form = SearchDonorForm()
    content = {
        'search_donor_form': search_donor_form,
        'content_search': content_search
    }
    return render(request, 'profile/recyclingCenter/search_donor.html', content)


@login_required(login_url='login_recyclingcenter')
@user_type(login_url="login_recyclingcenter")
def register_donation(request, id):

    print(id, id)
    donor = Profile.objects.get(id=id)

    if request.POST:
        post = request.POST.copy()
        post['recyclingCenter_id'] = request.user
        post['donor_id'] = donor
        post['confirmed'] = False
        post['modification_date'] = None
        post['added_points'] = 0
        request.POST = post

        register_donation_form = RegisterDonationForm(request.POST)
        material_form_factory = inlineformset_factory(Donation, RecyclabelMaterial, form=RegisterMaterialForm)
        register_material_form = material_form_factory(request.POST)

        print(register_donation_form.is_valid(), register_material_form.is_valid())
        if register_donation_form.is_valid() and register_material_form.is_valid():
            donation = register_donation_form.save()
            register_material_form.instance =donation
            register_material_form.save()
        return HttpResponse("<h1>Criado</h1>")

    register_donation_form = RegisterDonationForm()
    
    material_form_factory = inlineformset_factory(Donation, RecyclabelMaterial, form=RegisterMaterialForm, extra=1)
    register_material_form = material_form_factory()
    content = {
        'donation_form': register_donation_form,
        'material_form': register_material_form,
        'donor': donor
    }
    return render(request, 'profile/recyclingCenter/donate.html', content)