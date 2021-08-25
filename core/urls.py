from django.urls import path
from .views import views_donor, views_recyclingcenter


urlpatterns = [
    path('donor/', views_donor.userpage, name="userpage_donor"),
    path('donor/login/', views_donor.login_donor, name="login_donor"),
    path('donor/register/', views_donor.register_donor, name="register_donor"),
    path('donor/logout/', views_donor.logout_donor, name='logout_donor'),
    path('donor/about/', views_donor.about_donor, name='about_donor'),
    path('donor/search_rc/', views_donor.search_rc, name='search_rc'),
    path('donor/attendance/<id>/', views_donor.attendance, name='attendance'),
    path('donor/notifications_donor/', views_donor.notifications_donor, name='notifications_donor'),
    path('donor/receipt/<id>/', views_donor.receipt, name='receipt'),
    path('donor/confirm_donation/<id>', views_donor.confirm_donation, name='confirm_donation'),

    path('recyclingcenter/', views_recyclingcenter.userpage, name="userpage_recyclingcenter"),
    path('recyclingcenter/login/', views_recyclingcenter.login_recyclingCenter, name="login_recyclingcenter"),
    path('recyclingcenter/register/', views_recyclingcenter.register_recyclingCenter, name="registern_recyclingcenter"),
    path('recyclingcenter/logout/', views_recyclingcenter.logout_recyclingCenter, name="logout_recyclingCenter"),
    path('recyclingcenter/notifications/', views_recyclingcenter.notifications, name='notifications'),
    path('recyclingcenter/att_confirmation/<id>/', views_recyclingcenter.attending_confirmation, name='att_confirmation'),
    path('recyclingcenter/schedule/', views_recyclingcenter.schedule, name='schedule'),

    path('recyclingcenter/search/', views_recyclingcenter.search_donor, name="search_donor"),
    path('recyclingcenter/donation/<id>/', views_recyclingcenter.register_donation, name="register_donation"),
    
]