from django.urls import path
from . import views

urlpatterns = [
    path("identify/", views.IdentifySelf.as_view()),
    path("log_data/<string:sensor_id>", views.LogData.as_view()),
]
