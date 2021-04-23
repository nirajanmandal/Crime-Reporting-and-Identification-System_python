import re
from django import forms
from PIL import Image
# from tempus_dominus.widgets import DateTimePicker
from .models import *


class CaseForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CasesModel
        fields = '__all__'

        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'address': forms.TextInput(attrs={'class': 'form-control'}),
                   'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
                   'nationality': forms.TextInput(attrs={'class': 'form-control'}),
                   'date_of_case': forms.DateInput(attrs={'class': 'datepicker form-control', 'type': 'date'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        CONTACT_NUMBER_REGEX = re.compile(r"^(([+]?\d{3})-?)?\d{7,10}$")
        if not CONTACT_NUMBER_REGEX.match(contact_number):
            raise forms.ValidationError('''Phone Number format is not valid. Some examples of supported
              phone numbers are numbers are 9811111111, 08256666,
              977-9833333333, +977-9833333333, 977-08256666''')
        return contact_number

    def save(self, commit=True):
        photo = super(CaseForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        p_image = Image.open(photo.image)
        if x and y and w and h:
            cropped_image = p_image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.image.path)
        return photo
