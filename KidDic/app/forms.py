from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import User, Child, Quote, Comment, Category
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.forms.widgets import SelectDateWidget
import datetime

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("認証に失敗しました")
        return self.cleaned_data

class AccountInfoForm(forms.Form):
    username = forms.CharField(label='名前／ニックネーム', max_length=100)
    email = forms.EmailField(label='メールアドレス', required=False)  # オプショナルに設定
    current_password = forms.CharField(label='現在のパスワード', widget=forms.PasswordInput)
    password1 = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='新しいパスワード確認', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_user = self.initial.get('current_user')
        
        if email and email != current_user.email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスはすでに登録されています")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("新しいパスワードが一致しません。")
        
        return cleaned_data

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['nickname', 'birthdate']

class QuoteForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Quote
        fields = ['child', 'content', 'description', 'start_date', 'end_date', 'image', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        