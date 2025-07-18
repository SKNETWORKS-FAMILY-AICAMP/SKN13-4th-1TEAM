from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm # PasswordResetForm 임포트

class UserChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '닉네임'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']

class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(label="아이디", max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and email:
            try:
                User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "입력하신 아이디와 이메일 주소가 일치하는 사용자가 없습니다."
                )
        return cleaned_data

class CommentForm(forms.ModelForm):
    author_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': '이름'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '내용을 입력하세요', 'rows': 3}))

    class Meta:
        model = Comment
        fields = ['author_name', 'password', 'content']