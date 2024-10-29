from django.urls import path
from .views import ExampleDetail, ExampleList, devedor_detail, devedor_list
from . import views

urlpatterns = [
    path('devedores/', devedor_list, name='devedor_list'),
    path('devedores/<int:pk>/', devedor_detail, name='devedor_detail'),
    path('exemplo/', ExampleList.as_view(), name='exemplo-list'),
    path('exemplo/<int:devedor_id>/', ExampleDetail.as_view(), name='exemplo-detail'),
]
