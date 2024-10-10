from django.urls import path
from .views import ConverterView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('rates/', ConverterView.as_view()),
]