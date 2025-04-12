from django.urls import path
from . import views
from .views import record_view

urlpatterns = [
    path('', record_view, name='record'),
]
