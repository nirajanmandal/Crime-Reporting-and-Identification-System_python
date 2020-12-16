from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View, CreateView, TemplateView, UpdateView, FormView, DetailView, ListView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from accounts.forms import UserForm, UserProfileForm, LoginUser, UserPasswordChangeForm, UserUpdateForm
from accounts.models import *
from PIL import Image

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from detection.models import CitizenProfile
from .tokens import account_activation_token


@method_decorator(login_required, name='dispatch')
class UserDashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'


# @method_decorator(staff_member_required, name='dispatch')
class RegisterUserView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserForm
    second_form_class = UserProfileForm
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        profile_form = self.second_form_class()
        if request.user.is_authenticated:
            messages.warning(request, 'Please logout to register a new user')
            return redirect('accounts:dashboard')
        else:
            return render(request, self.template_name, {'form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        profile_form = self.second_form_class(request.POST, request.FILES)
        # import ipdb
        # ipdb.set_trace()
        if form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = form.save()
                user.is_active = False
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.warning(request, 'Please Confirm your email to complete registration.')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form, 'profile_form': profile_form})


@method_decorator(login_required, name='dispatch')
class ListStaffView(ListView):
    template_name = 'accounts/view_staff.html'
    model = Profile
    context_object_name = 'staff'


@login_required
def delete_staff(request, pk):
    if request.user.is_superuser and request.user.is_active and request.user.is_authenticated:
        try:
            staff = Profile.objects.get(pk=pk)
            # staff = request.user.objects.get(pk=pk)
            # staff = User.objects.get(pk=pk)
        except User.DoesNotExist:
            messages.warning(request, "Staff not found")
            return redirect('accounts:view-staff')
        staff.delete()
        messages.success(request, "Staff deleted successfully")
        return redirect('accounts:view-staff')

    messages.warning(request, 'Access Denied')
    return render(request, 'accounts/view_staff.html', {})


class UserLoginView(FormView):
    form_class = LoginUser
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if request.user.is_authenticated:
            messages.success(request, 'Already logged in')
            return redirect('news:list-news')
        else:
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # messages.success(request, 'logged in')
                    return redirect('news:list-news')
                else:
                    messages.error(request, 'account not activated')
                    return HttpResponseRedirect(request.path_info)

            messages.error(request, 'invalid username or password')
            return HttpResponseRedirect(request.path_info)


@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


@method_decorator(login_required, name='dispatch')
class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:logout')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, request, *args, **kwargs):
        view = Home.as_view(template_name='accounts/welcome.html')
        return view(request, *args, **kwargs)


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            messages.success(request, 'Your account have been confirmed.')
            return redirect('accounts:login')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('accounts:register')


@method_decorator(login_required, name='dispatch')
class ProfileEditView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = UserUpdateForm
    second_form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:view-staff')
    success_message = 'Profile was successfully updated'

    def post(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            profile = None
        profile_form = UserProfileForm(self.request.POST or None, self.request.FILES or None, instance=profile)
        user_form = UserUpdateForm(self.request.POST or None, instance=profile.user)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                profile = profile_form.save(commit=False)
                user.save()
                profile.user = user
                profile.save()

                # messages.success(request, 'Profile was successfully updated')
                return redirect('accounts:view-staff')
        print(profile_form)
        messages.warning(request, 'Please check your credentials')
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            profile = None
        profile_form = UserProfileForm(self.request.POST or None, self.request.FILES or None, instance=profile)
        user_form = UserUpdateForm(self.request.POST or None, instance=profile.user)

        context['profile_form'] = profile_form
        context['user_form'] = user_form
        context['profile'] = profile
        return context


@method_decorator(login_required, name='dispatch')
class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = UserUpdateForm
    second_form_class = UserProfileForm
    template_name = 'accounts/update_staff.html'
    success_url = reverse_lazy('accounts:view-staff')
    success_message = 'Profile was successfully updated'

    def post(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            profile = None
        profile_form = UserProfileForm(self.request.POST or None, self.request.FILES or None, instance=profile)
        user_form = UserUpdateForm(self.request.POST or None, instance=profile.user)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                profile = profile_form.save(commit=False)
                user.save()
                profile.user = user
                profile.save()

                # messages.success(request, 'Profile was successfully updated')
                return redirect('accounts:view-staff')
        messages.warning(request, 'Please check your credentials')
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = self.get_object()
        except Profile.DoesNotExist:
            profile = None
        profile_form = UserProfileForm(self.request.POST or None, self.request.FILES or None, instance=profile)
        user_form = UserUpdateForm(self.request.POST or None, instance=profile.user)

        context['profile_form'] = profile_form
        context['user_form'] = user_form
        context['profile'] = profile
        return context





