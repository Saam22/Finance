from django.shortcuts import render , redirect
from django.views import View
from financetracker.forms import RegisterForm , TransactionForm , GoalForm
from django.contrib.auth import login ,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from . models import Transaction , Goal
# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        
        form = RegisterForm
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print("saad")
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login (request, user)
            return redirect('dashboard')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm(request, data=request.POST)
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")
            return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class DashboardView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')
    
class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, 'transaction_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
        return render(request, 'transaction_form.html', {'form': form})
    
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()
        return render(request, 'transaction_list.html', {'transactions': transactions})
    
class GoalCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        return render(request, 'goal_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
        return render(request, 'goal_form.html', {'form': form})
    