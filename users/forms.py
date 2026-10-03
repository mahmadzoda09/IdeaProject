from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Brand.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This brand already exists.")
        return name

class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = '__all__'

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["brand" , "model" , "year" , "price" , "fuel_type" , "transmission" , "color" , "location" , "description"]


class CarImageForm(forms.ModelForm):
    def __init__(self, *args, owner=None, car=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.owner = owner
        self.car = car

    def clean(self):
        cleaned_data = super().clean()
        if self.car.owner != self.owner:
            raise forms.ValidationError( "Только владелец автомобиля может добавлять фотографии.")

        return cleaned_data

    class Meta:
        model = CarImage
        fields = ["image"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
    widgets = {
            "text": forms.Textarea(attrs={"rows": 1, "placeholder": "Type a message..."}),
        }