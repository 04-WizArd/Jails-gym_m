from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

# Classe CSS pour les champs de formulaire
INPUT_CLASSES = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none transition ease-in-out duration-150'

# Formulaire de création d'utilisateur
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'postnom', 'email', 'address')
        labels = {
            'username': 'Nom d\'utilisateur',
            'postnom': 'Noms',
            'email': 'Adresse e-mail',
            'address': 'Adresse',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre nom d\'utilisateur',
            }),
            'postnom': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre postnom',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse e-mail',
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse',
            }),
        }

# Formulaire de modification d'utilisateur
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'postnom', 'address')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre nom d\'utilisateur',
            }),
            'postnom': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre postnom',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse e-mail',
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse',
            }),
        }

# Formulaire de mise à jour du profil
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'postnom', 'address')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre nom d\'utilisateur',
            }),
            'postnom': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre postnom',
            }),
            'email': forms.EmailInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse e-mail',
            }),
            'address': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Votre adresse',
            }),
        }

# Formulaire de connexion stylisé
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Nom d\'utilisateur',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': INPUT_CLASSES,
        'placeholder': 'Mot de passe',
    }))
