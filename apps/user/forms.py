import re

from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import UserRole, UserProfile

User = get_user_model()


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('user', 'group')

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        user = User.objects.get(id=user_id)
        super().__init__(*args, **kwargs)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('middle_name', 'gender', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['middle_name'].widget.attrs['class'] = "form-control"
        self.fields['gender'].widget.attrs['class'] = "form-control"
        self.fields['phone'].widget.attrs['class'] = "form-control"


class UserCreationForm(forms.Form):
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('User already exists.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if not password1 == password2:
            raise ValidationError({"password2": "Passwords don't match."})

        if not len(password1) >= 8:
            raise ValidationError({"password1": "Password must be at least 8 characters long."})

        pattern = re.compile(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError({"password1": "Password must contain alphabet characters, special characters and numbers"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control"
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password"


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError('Password must contain alphabet characters, special characters and numbers')

        return password1


class ValidatingPasswordResetForm(auth.forms.SetPasswordForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[.@$!%*#?&'/~,;:_`{}()<>^\-\\|+])[A-Za-z\d.@$!%*#?&'/~,;:_`{}()<>^\-\\|+]{8,}$")
        if not bool(pattern.search(password1)):
            raise ValidationError('Password must contain alphabet characters, special characters and numbers')

        return password1