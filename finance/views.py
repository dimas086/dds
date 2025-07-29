from django.shortcuts import render, redirect
from .models import Transaction, Status, Type, Category, Subcategory
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.objects.all()
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    # Фильтры
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    category_filter = request.GET.get('category')
    subcategory_filter = request.GET.get('subcategory')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if status_filter:
        transactions = transactions.filter(status__name=status_filter)
    if type_filter:
        transactions = transactions.filter(type__name=type_filter)
    if category_filter:
        transactions = transactions.filter(category__name=category_filter)
    if subcategory_filter:
        transactions = transactions.filter(subcategory__name=subcategory_filter)
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)

    context = {
        'transactions': transactions,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'finance/transaction_list.html', context)

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'finance/transaction_form.html', {'form': form})

def transaction_edit(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'finance/transaction_form.html', {'form': form})

def get_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
