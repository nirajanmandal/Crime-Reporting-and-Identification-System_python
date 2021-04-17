from django import forms
from PIL import Image
# from tempus_dominus.widgets import DateTimePicker
from .models import *


class CaseForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = CasesModel
        fields = '__all__'

        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'address': forms.TextInput(attrs={'class': 'form-control'}),
                   'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'nationality': forms.TextInput(attrs={'class': 'form-control'}),
                   'date_of_case': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
                   # 'date_of_crime': DateTimePicker(options={'useCurrent': True, 'collapse': False},
                   #                                 attrs={'append': 'fa fa-calendar', 'icon_toggle': True}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   }

    def save(self, commit=True):
        photo = super(CaseForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        p_image = Image.open(photo.image)
        cropped_image = p_image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo