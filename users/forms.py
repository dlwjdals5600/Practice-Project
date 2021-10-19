from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise forms.ValidationError('정보가 잘못되었습니다.')
        except models.User.DoesNotExist:
            raise forms.ValidationError('존재하지 않는 유저입니다.')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First_name (이름)"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last_name (성)"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
        }
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError('이미 존재하고 있는 이메일입니다.')
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError('패스워드가 일치하지 않습니다.')
        else:
            return password
    
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user.username = email
        user.set_password(password)
        user.save()
