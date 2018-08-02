from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import serializers

from license_agreement.models import *


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """

    class Meta:
        model = Address
        fields = ('line1', 'line2', 'city_or_village', 'state', 'country', 'zip_code')


class LicensorSerializer(serializers.ModelSerializer):
    """
    Licensor Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Licensor
        fields = ('id', 'first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status',\
                  'address', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        licensor = Licensor.objects.create(**validated_data)
        licensor.address = Address.objects.create(**address_data)
        licensor.save()
        return licensor

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.organization_name = validated_data.get('organization_name', instance.organization_name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()
        return instance


class LicenseeSerializer(serializers.ModelSerializer):
    """
    Licensee Serializer
    """
    address = AddressSerializer()

    class Meta:
        model = Licensor
        fields = ('id', 'first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status',\
                  'address', 'created_at')
        read_only_fields = ('id', 'created_at',)

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        licensee = Licensee.objects.create(**validated_data)
        licensee.address = Address.objects.create(**address_data)
        licensee.save()
        return licensee

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.email = validated_data.get('email', instance.email)
        instance.organization_name = validated_data.get('organization_name', instance.organization_name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        address_data = validated_data.pop('address')
        address = instance.address
        address.line1 = address_data.get('line1', address.line1)
        address.line2 = address_data.get('line2', address.line2)
        address.city_or_village = address_data.get('city_or_village', address.city_or_village)
        address.state = address_data.get('state', address.state)
        address.country = address_data.get('country', address.country)
        address.zip_code = address_data.get('zip_code', address.zip_code)
        address.save()
        return instance


class SoftwareSerializer(serializers.ModelSerializer):
    """
    Software Serializer
    """

    class Meta:
        model = Software
        fields = ('id', 'name', 'specification', 'user_guide_document', 'indemnity', 'status', 'created_at')
        read_only_fields = ('id', 'created_at',)


class SoftwareLicenseAgreementSerializer(serializers.ModelSerializer):
    """
    SoftwareLicenseAgreement Serializer
    """
    licensor = serializers.SlugRelatedField(slug_field='email', queryset=Licensor.objects.exclude(status='Delete'))
    licensee = serializers.SlugRelatedField(slug_field='email', queryset=Licensee.objects.exclude(status='Delete'))
    software = serializers.SlugRelatedField(slug_field='name', queryset=Software.objects.exclude(status='Delete'))

    class Meta:
        model = SoftwareLicenseAgreement
        fields = ('id', 'effective_date', 'licensor', 'licensee', 'software', 'valid_ip_addresses','terms_and_conditions',\
                  'limitation_of_liability', 'termination', 'expiry_date', 'price', 'payment_plan', 'no_of_copies',\
                  'delivery_date', 'warrenty_period', 'maintenance_agreement', 'status', 'created_at')
        read_only_fields = ('id', 'created_at',)
