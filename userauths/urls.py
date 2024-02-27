from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from userauths.views import userProfile, editProfile,CustomLogoutView

urlpatterns = [
    # Profile Section
    path('profile/edit', editProfile, name="editprofile"),
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name='sign-in.html', redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/',views.CustomLogoutView.as_view(),name='sign-out'), 
    


]
