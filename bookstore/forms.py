from django import forms
from django.contrib.auth.models import User
from bookstore.models import Chat, Book, User

# Chat form
class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message',)

# Book form
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'year', 'uploaded_by', 'desc')

# User form (for updating user fields like username, first_name, last_name, email)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user
