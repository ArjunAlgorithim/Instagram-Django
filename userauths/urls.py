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
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"), 
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"), 
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"), 
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"), 
    


]
