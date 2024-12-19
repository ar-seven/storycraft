from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate, name='generate'),
    path('stories/', views.landing, name='landing'),
    path('story/<str:story_id>', views.story_detail, name='story_detail'),
    path('ask-gpt/', views.ask_gpt, name='ask_gpt'),  # Add this line
]