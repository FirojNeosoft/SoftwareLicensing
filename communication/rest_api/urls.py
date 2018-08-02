from django.urls import path, include

from communication.rest_api.views import *


urlpatterns = [
    path('sms', SMSView.as_view()),
    ]
