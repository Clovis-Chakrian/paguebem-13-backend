from django.urls import path
from .views import devedor_list, devedor_detail

urlpatterns = [
    path('devedores/', devedor_list, name='devedor_list'),
    path('devedores/<int:pk>/', devedor_detail, name='devedor_detail'),
]
