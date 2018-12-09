from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.ESearchView.as_view(), name='search'),
    path('filter/', views.EFilterView.as_view(), name='filter'),
]
