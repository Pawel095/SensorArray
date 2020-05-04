from django.urls import path
from . import views

urlpatterns = [
    path("identify/", views.IdentifySelf.as_view()),
    path("register/", views.RegisterSensor.as_view()),
    path("log_data/<str:sensor_id>/", views.LogData.as_view()),
]
