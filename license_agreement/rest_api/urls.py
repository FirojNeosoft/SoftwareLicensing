from django.urls import path, include

from rest_framework import routers

from license_agreement.rest_api.views import *

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'licensors', LicensorViewSet)
router.register(r'licensees', LicenseeViewSet)
router.register(r'softwares', SoftwareViewSet)
router.register(r'agreements', SoftwareLicenseAgreementViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('agreements/<int:id>/validity', CheckValidityOfLicense.as_view()),
    ]
