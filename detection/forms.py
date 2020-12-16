from django import forms
from .models import *
from PIL import Image


class CitizenForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = CitizenProfile
        fields = ('first_name', 'last_name', 'birth_date', 'gender', 'address', 'phone_number', 'nationality', 'citizenship_number',
                  'bio', 'citizen_image', 'status', 'x', 'y', 'width', 'height')
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                   'address': forms.TextInput(attrs={'class': 'form-control'}),
                   'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'nationality': forms.TextInput(attrs={'class': 'form-control'}),
                   'citizenship_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   # 'citizen_image': forms.FileInput(attrs={'accept': 'image/*'}),
                   'bio': forms.Textarea(attrs={'class': 'form-control'}),
                   }

    def save(self, commit=True):
        photo = super(CitizenForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.citizen_image)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.citizen_image.path)

        return photo

