from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Category, Transaction
from datetime import datetime, date

@login_required(login_url='account:login')
def main_page(request):
    total_income = Transaction.objects.filter(user=request.user, category__is_income=True).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=request.user, category__is_income=False).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    cash_income = Transaction.objects.filter(user=request.user, category__is_income=True, type='cash').aggregate(Sum('amount'))['amount__sum'] or 0
    card_income = Transaction.objects.filter(user=request.user, category__is_income=True, type='card').aggregate(Sum('amount'))['amount__sum'] or 0
    cash_expense = Transaction.objects.filter(user=request.user, category__is_income=False, type='cash').aggregate(Sum('amount'))['amount__sum'] or 0
    card_expense = Transaction.objects.filter(user=request.user, category__is_income=False, type='card').aggregate(Sum('amount'))['amount__sum'] or 0

    total = total_income + total_expense if total_income + total_expense > 0 else 1  # 0 ga bo‘linishni oldini olish
    income_percentage = (total_income / total) * 100 if total_income > 0 else 0
    expense_percentage = (total_expense / total) * 100 if total_expense > 0 else 0

    income_data = Category.objects.filter(user=request.user, is_income=True).annotate(total=Sum('transaction__amount')).values('name', 'total')
    expense_data = Category.objects.filter(user=request.user, is_income=False).annotate(total=Sum('transaction__amount')).values('name', 'total')

    return render(request, 'transactions/main.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'cash_income': cash_income,
        'card_income': card_income,
        'cash_expense': cash_expense,
        'card_expense': card_expense,
        'income_percentage': income_percentage,
        'expense_percentage': expense_percentage,
        'income_data': list(income_data),
        'expense_data': list(expense_data),
    })

@login_required(login_url='account:login')
def manage_categories(request, category_type):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.get_or_create(user=request.user, name=category_name, is_income=(category_type == 'income'))
            messages.success(request, f"Yangi {'kirim' if category_type == 'income' else 'chiqim'} kategoriyasi qo‘shildi.")
        return redirect(f'transactions:{category_type}_categories')

    default_categories = {
        'income': ['oylik', 'biznes', 'kunlik ish haqlari'],
        'expense': ['oila', 'ovqat', 'kiyim', 'transport', 'sayohat', 'bayramlar', 'o\'quv kurslari', 'soliqlar', 'uy hayvoni uchun xarajatlar', 'magazin xaridlar']
    }
    categories = Category.objects.filter(user=request.user, is_income=(category_type == 'income'))
    for cat in default_categories[category_type]:
        Category.objects.get_or_create(user=request.user, name=cat, is_income=(category_type == 'income'))

    context = {
        'categories': categories,
        'category_type': category_type,
        'total': Transaction.objects.filter(user=request.user, category__is_income=(category_type == 'income')).aggregate(Sum('amount'))['amount__sum'] or 0
    }
    return render(request, f'transactions/{category_type}.html', context)

@login_required(login_url='account:login')
def add_transaction(request, category_type, category_id):
    category = Category.objects.get(id=category_id, user=request.user, is_income=(category_type == 'income'))

    category_total = Transaction.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0

    transactions = Transaction.objects.filter(user=request.user, category=category).order_by('-date')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('type', 'cash')  # Default: naqd
        description = request.POST.get('description', '')
        date_str = request.POST.get('date', datetime.now().strftime('%Y-%m-%d'))  # Agar sana kiritilmasa, bugungi sana

        if not amount:
            messages.error(request, 'Miqdor kiritish majburiy.')
            return redirect(f'transactions:add_{category_type}', category_id=category_id)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Miqdor 0 dan katta bo‘lishi kerak.")
        except ValueError:
            messages.error(request, 'Miqdor noto‘g‘ri kiritildi.')
            return redirect(f'transactions:add_{category_type}', category_id=category_id)

        Transaction.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            type=transaction_type,
            description=description,
            date=date_str
        )
        messages.success(request, f"{'Kirim' if category_type == 'income' else 'Chiqim'} muvaffaqiyatli qo‘shildi.")
        return redirect(f'transactions:add_{category_type}', category_id=category_id)

    return render(request, f'transactions/add_{category_type}.html', {
        'category': category,
        'category_total': category_total,
        'transactions': transactions,
        'today': date.today()
    })

income_categories = lambda request: manage_categories(request, 'income')
expense_categories = lambda request: manage_categories(request, 'expense')
add_income = lambda request, category_id: add_transaction(request, 'income', category_id)
add_expense = lambda request, category_id: add_transaction(request, 'expense', category_id)