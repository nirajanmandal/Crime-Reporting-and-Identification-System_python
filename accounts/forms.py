import re

from django import forms
from PIL import Image
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Profile
        fields = ['profile_image', 'citizenship_number', 'nationality', 'address',
                  'bio', 'birth_date', 'gender', 'phone_number',
                  'x', 'y', 'width', 'height']

        widgets = {'address': forms.TextInput(attrs={'class': 'form-control'}),
                   # 'profile_image': forms.FileInput(attrs={'accept': 'image/*', 'required': 'false'}),
                   'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
                   'citizenship_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'nationality': forms.TextInput(attrs={'class': 'form-control'}),
                   'bio': forms.Textarea(attrs={'class': 'form-control'}),
                   'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                   }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        PHONE_NUMBER_REGEX = re.compile(r"^(([+]?\d{3})-?)?\d{7,10}$")
        if not PHONE_NUMBER_REGEX.match(phone_number):
            raise forms.ValidationError('''Phone Number format is not valid. Some examples of supported
              phone numbers are numbers are 9811111111, 08256666,
              977-9833333333, +977-9833333333, 977-08256666''')
        return phone_number

    def save(self, commit=True):
        photo = super(UserProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_image)
        if x and y and w and h:
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.profile_image.path)
        return photo


class LoginUser(forms.Form):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
