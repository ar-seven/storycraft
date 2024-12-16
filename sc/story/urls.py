from django.urls import path
from . import views

urlpatterns = [
    # ... other patterns ...
    path('', views.home, name='home'),
    path('generate/', views.generate, name='generate'),
    path('stories/', views.landing, name='landing'),
    path('story/<str:story_id>', views.story_detail, name='story_detail'),
]