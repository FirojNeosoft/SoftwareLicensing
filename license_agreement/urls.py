from django.contrib import admin
from django.urls import path, include

from license_agreement.views import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('users/', ListUsersView.as_view(), name='list_users'),
    path('user/add/', CreateUserView.as_view(), name='add_user'),
    path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
    path('user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

]