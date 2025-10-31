from django.shortcuts import render , redirect ,HttpResponse
from django.views import View
from financetracker.forms import RegisterForm , TransactionForm , GoalForm
from django.contrib.auth import login ,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from . models import Transaction , Goal
from django.db.models import Sum
from decimal import Decimal
from .admin import TransactionResource

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
        transactions = Transaction.objects.filter(user=request.user)
        goals =Goal.objects.filter(user=request.user)
        total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense
        remaning_save = balance
        goal_progress = []        
        for goal in goals:
            if remaning_save>=goal.target_amount:
                goal_progress.append({'goal': goal, 'progress': 100})
                remaning_save -= goal.target_amount
            elif remaning_save>0:
                progress= (remaning_save/goal.target_amount)*100    
                goal_progress.append({'goal': goal, 'progress': progress})
                remaning_save = 0
            else:
                goal_progress.append({'goal': goal, 'progress': 0})
        context={
            'transactions':transactions,
            'total_income':total_income,
            'total_expense':total_expense,
            'balance':balance,
            'goal_progress':goal_progress
        }
        return render(request, 'dashboard.html', context)
    
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
    
from django.db.models import Sum
from .models import Transaction  # بافتراض إن عندك موديل للعمليات المالية

class GoalCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        # حساب الرصيد الحالي للمستخدم
        current_balance = Transaction.objects.filter(user=request.user).aggregate(
            total=Sum('amount')
        )['total'] or 0
        return render(request, 'goal_form.html', {'form': form, 'current_balance': current_balance})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        current_balance = Transaction.objects.filter(user=request.user).aggregate(
            total=Sum('amount')
        )['total'] or 0

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('dashboard')

        return render(request, 'goal_form.html', {'form': form, 'current_balance': current_balance})

def export_transactions(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    transaction_resource = TransactionResource()
    dataset=transaction_resource.export(queryset=user_transactions)
    excel_data = dataset.export('xlsx')
    response = HttpResponse(excel_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'
    return response