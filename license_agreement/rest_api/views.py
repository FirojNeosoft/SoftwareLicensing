from datetime import datetime as dt
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from license_agreement.models import *
from license_agreement.rest_api.serializer import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    filter_fields = ('username', 'email', 'is_staff')


class LicensorViewSet(viewsets.ModelViewSet):
    queryset = Licensor.objects.exclude(status='Delete')
    serializer_class = LicensorSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email')
    ordering_fields = ('first_name', 'last_name', 'email')
    filter_fields = ('status',)


class LicenseeViewSet(viewsets.ModelViewSet):
    queryset = Licensee.objects.exclude(status='Delete')
    serializer_class = LicenseeSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('first_name', 'last_name', 'mobile', 'email')
    ordering_fields = ('first_name', 'last_name', 'email')
    filter_fields = ('status',)


class SoftwareViewSet(viewsets.ModelViewSet):
    queryset = Software.objects.exclude(status='Delete')
    serializer_class = SoftwareSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)
    filter_fields = ('status',)


class SoftwareLicenseAgreementViewSet(viewsets.ModelViewSet):
    queryset = SoftwareLicenseAgreement.objects.exclude(status='Delete')
    serializer_class = SoftwareLicenseAgreementSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('terms_and_conditions', 'limitation_of_liability', 'termination', 'payment_plan',\
                     'maintenance_agreement')
    ordering_fields = ('effective_date', 'expiry_date', 'delivery_date', 'created_at', 'no_of_copies', 'price',\
                       'warrenty_period')
    filter_fields = ('licensor', 'licensee', 'software', 'status')


class CheckValidityOfLicense(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        """
        check validity of license.
        """
        license = SoftwareLicenseAgreement.objects.get(id=id)
        if dt.today() > license.expiry_date:
            data = {
                "is_valid": False,
                "expiry_date": license.expiry_date
            }
        else:
            data = {
                "is_valid": True,
                "expiry_date": license.expiry_date
            }
        return Response(data)
