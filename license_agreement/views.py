import logging

from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from license_agreement.models import *

logger = logging.getLogger('licensing_log')


class DashboardView(LoginRequiredMixin, View):
    """
    Dashboard
    """
    def get(self, request):
        """
          dashboard
        """
        data = { "licensors_count" : Licensor.objects.exclude(status='Delete').count(),
        "licensees_count" : Licensee.objects.exclude(status='Delete').count(),
        "softwares_count" : Software.objects.exclude(status='Delete').count(),
        "licenses_count" : SoftwareLicenseAgreement.objects.exclude(status='Delete').count()}
        return render(request, 'dashboard.html', data)


class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'


class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was created successfully"
    success_url = reverse_lazy('list_users')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_user')
        return HttpResponseRedirect(reverse('list_users'))


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')


class ListLicensorsView(LoginRequiredMixin, ListView):
    """
    List Licensors
    """
    model = Licensor
    queryset = Licensor.objects.exclude(status='Delete')
    template_name = 'licensor_list.html'


class CreateLicensorView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new licensor
    """
    model = Licensor
    fields = ['first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status']
    template_name = 'licensor_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_licensors')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            licensor = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    licensor.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
                                                            country=country,zip_code=int(zip_code))
                    licensor.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a licensor.".format(e))
                    messages.error(request, "Error occured while saving address of a licensor.")
                    return redirect('add_licensor')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_licensor')
        messages.success(request,"{}, licensor added successfully.".format(licensor.full_name))
        return HttpResponseRedirect(reverse('list_licensors'))


class UpdateLicensorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing licensor
    """
    model = Licensor
    fields = ['first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status']
    template_name = 'edit_licensor_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_licensors')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Licensor.objects.get(id=pk)
        return render(request, 'edit_licensor_form.html', {'obj': obj})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Licensor.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            licensor = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            # import pdb; pdb.set_trace()
            if city and country and state and zip_code:
                try:
                    if licensor.address:
                        licensor.address.line1=line1
                        licensor.address.line2=line2
                        licensor.address.city_or_village=city
                        licensor.address.state=state
                        licensor.address.country=country
                        licensor.address.zip_code=int(zip_code)
                        licensor.address.save()
                    else:
                        licensor.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
                                                                state=state, country=country, zip_code=int(zip_code))
                        licensor.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a licensor.".format(e))
                    messages.error(request, "Error occured while saving address of a licensor.")
                    return redirect('update_licensor', pk)
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_licensor', pk)
        messages.success(request,"{}, licensor updated successfully.".format(licensor.full_name))
        return HttpResponseRedirect(reverse('list_licensors'))


class DeleteLicensorView(LoginRequiredMixin, DeleteView):
    """
    Delete existing licensor
    """
    model = Licensor
    template_name = 'licensor_confirm_delete.html'
    success_url = reverse_lazy('list_licensors')


class ListLicenseesView(LoginRequiredMixin, ListView):
    """
    List Licensees
    """
    model = Licensee
    queryset = Licensee.objects.exclude(status='Delete')
    template_name = 'licensee_list.html'


class CreateLicenseeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new licensee
    """
    model = Licensee
    fields = ['first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status']
    template_name = 'licensee_form.html'
    success_message = "%(first_name)s was created successfully"
    success_url = reverse_lazy('list_licensees')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            licensee = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            if city and country and state and zip_code:
                try:
                    licensee.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city, state=state,\
                                                            country=country,zip_code=int(zip_code))
                    licensee.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a licensee.".format(e))
                    messages.error(request, "Error occured while saving address of a licensee.")
                    return redirect('add_licensee')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_licensee')
        messages.success(request, "{}, licensee created successfully.".format(licensee.full_name))
        return HttpResponseRedirect(reverse('list_licensees'))


class UpdateLicenseeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing licensee
    """
    model = Licensee
    fields = ['first_name', 'last_name', 'designation', 'organization_name', 'mobile', 'email', 'status']
    template_name = 'edit_licensee_form.html'
    success_message = "%(first_name)s was updated successfully"
    success_url = reverse_lazy('list_licensees')

    def get(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        obj = Licensee.objects.get(id=pk)
        return render(request, 'edit_licensee_form.html', {'obj': obj})

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Licensee.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            licensee = form.save()
            line1 = request.POST['line1']
            line2 = request.POST['line2']
            city = request.POST['location']
            country = request.POST['country']
            state = request.POST['state']
            zip_code = request.POST['zip']
            # import pdb; pdb.set_trace()
            if city and country and state and zip_code:
                try:
                    if licensee.address:
                        licensee.address.line1=line1
                        licensee.address.line2=line2
                        licensee.address.city_or_village=city
                        licensee.address.state=state
                        licensee.address.country=country
                        licensee.address.zip_code=int(zip_code)
                        licensee.address.save()
                    else:
                        licensee.address = Address.objects.create(line1=line1, line2=line2, city_or_village=city,
                                                                state=state, country=country, zip_code=int(zip_code))
                        licensee.save()
                except Exception as e:
                    logger.error("{}, error occured while saving address of a licensee.".format(e))
                    messages.error(request, "Error occured while saving address of a licensee.")
                    return redirect('update_licensee', pk)
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_licensee', pk)
        messages.success(request, "{}, licensee updated successfully.".format(licensee.full_name))
        return HttpResponseRedirect(reverse('list_licensees'))


class DeleteLicenseeView(LoginRequiredMixin, DeleteView):
    """
    Delete existing licensee
    """
    model = Licensee
    template_name = 'licensee_confirm_delete.html'
    success_url = reverse_lazy('list_licensees')


class ListSoftwaresView(LoginRequiredMixin, ListView):
    """
    List softwares
    """
    model = Software
    queryset = Software.objects.exclude(status='Delete')
    template_name = 'software_list.html'


class CreateSoftwareView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new software
    """
    model = Software
    fields = ['name', 'specification', 'user_guide_document', 'indemnity', 'status']
    template_name = 'software_form.html'
    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('list_softwares')


class UpdateSoftwareView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing software
    """
    model = Software
    fields = ['name', 'specification', 'user_guide_document', 'indemnity', 'status']
    template_name = 'software_form.html'
    success_message = "%(name)s was updated successfully"
    success_url = reverse_lazy('list_softwares')


class DeleteSoftwareView(LoginRequiredMixin, DeleteView):
    """
    Delete existing software
    """
    model = Software
    template_name = 'software_confirm_delete.html'
    success_url = reverse_lazy('list_softwares')


class ListSoftwareLicenseAgreementsView(LoginRequiredMixin, ListView):
    """
    List license agreements
    """
    model = SoftwareLicenseAgreement
    queryset = SoftwareLicenseAgreement.objects.exclude(status='Delete')
    template_name = 'agreement_list.html'


class CreateSoftwareLicenseAgreementView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new license agreement
    """
    model = SoftwareLicenseAgreement
    fields = ['effective_date', 'licensor', 'licensee', 'software', 'valid_ip_addresses', 'terms_and_conditions',\
              'limitation_of_liability', 'termination', 'expiry_date', 'price', 'payment_plan', 'no_of_copies',\
              'delivery_date', 'warrenty_period', 'maintenance_agreement', 'status']
    template_name = 'agreement_form.html'
    success_message = "Agreement was created successfully"
    success_url = reverse_lazy('list_agreements')


class UpdateSoftwareLicenseAgreementView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing license agreement
    """
    model = SoftwareLicenseAgreement
    fields = ['effective_date', 'licensor', 'licensee', 'software', 'valid_ip_addresses', 'terms_and_conditions',\
              'limitation_of_liability', 'termination', 'expiry_date', 'price', 'payment_plan', 'no_of_copies',\
              'delivery_date', 'warrenty_period', 'maintenance_agreement', 'status']
    template_name = 'agreement_form.html'
    success_message = "Agreement was updated successfully"
    success_url = reverse_lazy('list_agreements')


class DeleteSoftwareLicenseAgreementView(LoginRequiredMixin, DeleteView):
    """
    Delete existing license agreement
    """
    model = SoftwareLicenseAgreement
    template_name = 'agreement_confirm_delete.html'
    success_url = reverse_lazy('list_agreements')
