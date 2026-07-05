from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('add/', views.add_contact, name='add_contact'),
    path('view/<int:id>/', views.view_contact, name='view_contact'),
    path('edit/<int:id>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:id>/', views.delete_contact, name='delete_contact'),
]