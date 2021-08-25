from core.models import Attending, Profile, Donation, RecyclabelMaterial
from django.shortcuts import redirect, render
from ..forms import AttendanceForm, LoginForm, RegisterDonationForm, RegisterDonorForm, SearchRecyclingCenterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib import messages
from django.db.models.query_utils import Q

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


def search_rc(request):
    content_search = None
    if request.POST:
        if len(request.POST['search']) >= 3:
            # Quando id informado tiver 0's à esquerda
            search_id_str = request.POST.copy()
            while True:
                if search_id_str['search'][0] == '0':
                    search_id_str['search'] = search_id_str['search'].replace(search_id_str['search'][0], '')
                else:
                    break
            request.POST = search_id_str
            
            try:
                search_id = request.POST['search']
            except ValueError:
                pass
            search = Q(
                Q(
                    Q(id__contains=search_id) | 
                    Q(first_name__contains=request.POST['search']) | 
                    Q(last_name__contains=request.POST['search'])) & 
                Q(profile_type__exact='P'))

            content_search = Profile.objects.filter(search)
        else:
            messages.info(request, 'Digite no mínimo 3 caracteres')

    search_form = SearchRecyclingCenterForm()
    content = {
        'search_form': search_form,
        'content_search': content_search
    }
    return render(request, 'profile/donor/search_rc.html', content)


def attendance(request, id):
    rc = Profile.objects.get(id=id)
    
    attendance_form = AttendanceForm()

    if request.POST:
        post = request.POST.copy()
        post['requester'] = request.user
        post['recipient'] = rc
        post['place'] = 'Rua X nº Y - Bairro M, Fortaleza, CE'
        post['status_attending'] = Attending.STATUS_ATTENING_CHOICES[1][0]
        post['confirmed'] = None
        post['return_recipient'] = 'add coment'
        post['points_attending'] = 0
        request.POST = post

        attendance_form = AttendanceForm(request.POST)

        is_register_form = False
        print(attendance_form.is_valid())
        if attendance_form.is_valid():
            attendance_form.save()
            return redirect('search_rc')

    content ={
        'attendance': attendance_form,
        'rc': rc
    }
    return render(request, 'profile/donor/attendance.html', content)


def notifications_donor(request):
    query = Q(
        Q(requester=request.user.id) &

        Q(
            Q(status_attending__exact='CA')| 
            Q(status_attending__exact='CC')|
            Q(status_attending__exact='AD')
            
        )&
        Q(
            Q(confirmed=True)|
            Q(confirmed=False)
        )
    )

    attendings = Attending.objects.filter(query).order_by('-id')
    content = {
        'attendings': attendings
    }
    return render(request, 'profile/donor/notifications.html', content)


def receipt(request, id):
    receipt = Attending.objects.get(id=id)
    content = {
        'receipt': receipt
    }
    return render(request, 'profile/donor/receipt.html', content)


def confirm_donation(request, id):
    selected_attending = Attending.objects.get(id=id)
    selected_donation = Donation.objects.get(attending=selected_attending.id)
    materials = RecyclabelMaterial.objects.filter(donation_id=selected_donation.id)

    donation_form = RegisterDonationForm(request.POST or None, instance=selected_donation)
    print(donation_form)

    if request.POST:
        
        print(request.POST['confirmed'])
        if request.POST['confirmed'] == 'true':
            selected_donation.confirmed = True
            selected_attending.status_attending = Attending.STATUS_ATTENING_CHOICES[4][0]
            

        elif request.POST['confirmed'] == 'false':
            selected_donation.confirmed = False
            selected_attending.status_attending = Attending.STATUS_ATTENING_CHOICES[2][0]

        selected_donation.save()
        selected_attending.save()
        return redirect('search_rc')
    
    content = {
        'donation_form': donation_form,
        'materials': materials,
        'attending': selected_attending,
        'description': selected_donation.description
    }
    return render(request, 'profile/donor/confirm_donation.html', content)

