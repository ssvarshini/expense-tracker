from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Transactions  
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request, "home.html")

def profile_view(request):
    return render(request, "profile.html")

def about(request):
    return render(request, "about.html")

def pricing(request):
    return render(request, "pricing.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def dashboard(request):
    return render(request, "dashboard.html")



def categories(request):
    return render(request, "categories.html")

def budget(request):
    return render(request, "budget.html")

def goals(request):
    return render(request, "goals.html")

@login_required
def transactions_view(request):
    user_transactions = Transactions.objects.filter(user=request.user).order_by('-date')

    total_expenses = user_transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = user_transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0

    if request.method == 'POST':
        title = request.POST['title']
        amount = request.POST['amount']
        trans_type = request.POST['type']
        category = request.POST.get('category') if trans_type == 'expense' else None

        Transactions.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            type=trans_type,
            category=category
        )
        return redirect('transactions')

    return render(request, 'transactions.html', {
        'transactions': user_transactions,
        'total_expenses': total_expenses,
        'total_income': total_income
    })

@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(Transactions, id=id, user=request.user)

    if request.method == 'POST':
        transaction.title = request.POST['title']
        transaction.amount = request.POST['amount']
        transaction.type = request.POST['type']
        transaction.save()
        return redirect('transactions')

    return render(request, 'edit_transaction.html', {'transaction': transaction})

@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(Transactions, id=id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions')
