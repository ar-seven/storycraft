from django.urls import path
from . import views

urlpatterns = [
    # ... other patterns ...
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]