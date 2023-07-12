from django import forms

from apps.website.models import EmailForPostNotification


class EmailPostNotificationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-row__field form-row__mail",
                                       "placeholder": "e-mailadres"})
    )

    class Meta:
        model = EmailForPostNotification
        fields = ("email",)


