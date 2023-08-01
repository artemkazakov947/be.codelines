from django import forms
from phonenumber_field.formfields import PhoneNumberField

from apps.website.models import EmailForPostNotification, RequestFromUser


class EmailPostNotificationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "e-mailadres"})
    )

    class Meta:
        model = EmailForPostNotification
        fields = ("email",)


class RequestFromUserForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "voor- en achternaam"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "e-mailadres"})
    )
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "gsm"})
    )
    question = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "mijn vraag"})
    )

    class Meta:
        model = RequestFromUser
        fields = "__all__"
        exclude = ("created",)
