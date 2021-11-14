from django import forms


class CodeVerificationForm(forms.Form):
    code = forms.IntegerField(min_value=10001, max_value=99999)


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(widget=forms.PasswordInput())
