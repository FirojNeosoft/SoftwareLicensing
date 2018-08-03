from django.contrib import admin
from django.urls import path, include

from license_agreement.views import *


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('users/', ListUsersView.as_view(), name='list_users'),
    path('user/add/', CreateUserView.as_view(), name='add_user'),
    path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
    path('user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    path('licensors/', ListLicensorsView.as_view(), name='list_licensors'),
    path('licensor/add/', CreateLicensorView.as_view(), name='add_licensor'),
    path('licensor/<int:pk>/edit/', UpdateLicensorView.as_view(), name='update_licensor'),
    path('licensor/<int:pk>/delete/', DeleteLicensorView.as_view(), name='delete_licensor'),

    path('licensees/', ListLicenseesView.as_view(), name='list_licensees'),
    path('licensee/add/', CreateLicenseeView.as_view(), name='add_licensee'),
    path('licensee/<int:pk>/edit/', UpdateLicenseeView.as_view(), name='update_licensee'),
    path('licensee/<int:pk>/delete/', DeleteLicenseeView.as_view(), name='delete_licensee'),

    path('softwares/', ListSoftwaresView.as_view(), name='list_softwares'),
    path('software/add/', CreateSoftwareView.as_view(), name='add_software'),
    path('software/<int:pk>/edit/', UpdateSoftwareView.as_view(), name='update_software'),
    path('software/<int:pk>/delete/', DeleteSoftwareView.as_view(), name='delete_software'),

    path('agreements/', ListSoftwareLicenseAgreementsView.as_view(), name='list_agreements'),
    path('agreement/add/', CreateSoftwareLicenseAgreementView.as_view(), name='add_agreement'),
    path('agreement/<int:pk>/edit/', UpdateSoftwareLicenseAgreementView.as_view(), name='update_agreement'),
    path('agreement/<int:pk>/delete/', DeleteSoftwareLicenseAgreementView.as_view(), name='delete_agreement'),

]