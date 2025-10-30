from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from financetracker.models import Transaction ,Goal
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md w-full'}),
            'title': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md w-full'}),
            'amount': forms.NumberInput(attrs={'class': 'border-gray-300 rounded-md w-full'}),
            'transaction_type': forms.Select(attrs={'class': 'border-gray-300 rounded-md w-full'}),
            'category': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md w-full'}),
        }
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border-gray-300 rounded-md w-full'}),
            'target_amount': forms.NumberInput(attrs={'class': 'border-gray-300 rounded-md w-full'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'border-gray-300 rounded-md w-full'}),
        }