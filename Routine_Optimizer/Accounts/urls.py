from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/personal_details/', views.Personal_details_update ,name='personal_details_update'),
    path('dashboard/update_password/', views.Update_password ,name='update_password'),
]
