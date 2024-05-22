from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['image']:
            user.image = self.cleaned_data['image']
        if commit:
            user.save()
        return user
