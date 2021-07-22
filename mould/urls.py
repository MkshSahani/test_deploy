from django.urls import path, include 
from . import views 

urlpatterns = [
    path('registration/', views.mould_registration, name="MouldRegistration"),
    path('<int:mould_id>/', views.mould_view, name = "MouldView"),
    path('update/', views.mould_update,name = "MouldUpdate"),
    path('mouldSearch/', views.mould_search, name = "MouldSearch"),
    path('data/<int:mould_id>/', views.mould_data_update, name = "MouldUpdate"),
]
