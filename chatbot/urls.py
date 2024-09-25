from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatbot_view, name='chat'),
    path('login/', views.user_login, name='login'),  # Make sure this is 'login/'
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),  # Redirect root URL to 'home'
    path('predict/', views.predict_disease, name='predict_disease'),
]   
