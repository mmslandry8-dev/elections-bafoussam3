from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Appeal

# class RegisterForm(UserCreationForm):
#     """
#     Formulaire d'inscription
#     """
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

class RegisterForm(UserCreationForm):
    """
    Formulaire d'inscription avec rôle
    """

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full p-2 mb-3 rounded text-black"
            })

class AppealForm(forms.ModelForm):
    """
    Formulaire de demande de réactivation
    """
    class Meta:
        model = Appeal
        fields = ['message']