from django.urls import path
from . import views

urlpatterns = [
    # ... other patterns ...
    path('', views.home, name='home'),
    path('generate/', views.generate, name='generate'),
]