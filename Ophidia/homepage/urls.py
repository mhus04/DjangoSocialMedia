from django.urls import path
from homepage.views import Index

urlpatterns = [
    path('', Index.as_view(), name = 'index'),
]