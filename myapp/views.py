from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User  # Ensure this line is present
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout

# def home(request):
#     expenses = Expense.objects.all()
#     total = sum(expense.amount for expense in expenses)
#     return render(request, 'tracker/home.html', {'expenses': expenses, 'total': total})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Expense  # Ensure this import matches your actual model

# @login_required
# def home(request):
#     # Fetch expenses for the logged-in user
#     expenses = Expense.objects.filter()  # Adjust to filter by user
#     total = sum(expense.amount for expense in expenses)  # Calculate total

#     return render(request, 'tracker/home.html', {
#         'expenses': expenses,
#         'total': total,
#         'message': "Here are your existing expenses." if expenses.exists() else "You have no recorded expenses."
#     })
@login_required
def home(request):
    # Fetch expenses for the logged-in user
    expenses = Expense.objects.filter(user=request.user)
    total = sum(expense.amount for expense in expenses)  

    message = "Here are your existing expenses." if expenses.exists() else "You have no recorded expenses."

    return render(request, 'tracker/home.html', {
        'expenses': expenses,
        'total': total,
        'message': message
    })



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'tracker/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  
        return redirect('home')  
    return render(request, 'tracker/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')  


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate the expense with the logged-in user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    
    return render(request, 'tracker/add_expense.html', {'form': form})

def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/update_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('home')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})


