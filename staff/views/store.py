from staff.auth import staff_required, StaffRequiredMixin
from django.http import HttpResponseNotAllowed

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

from profiles.forms import SortForm
from staff.forms import *
from store.models import Transaction, Transfer, Product


@staff_required
def store_index(request):
    if request.method == 'GET':
        products = len(Product.objects.all())
        transactions = len(Transaction.objects.all())
        transfers = len(Transfer.objects.all())
        return render(request, 'staff/store/store.html',
                      {'products': products, 'transactions': transactions, 'transfers': transfers})


class TransactionView(StaffRequiredMixin, View):
    template_name = 'staff/store/transaction_list.html'
    form_class = SortForm

    def get(self, request, **kwargs):
        transaction_list = Transaction.objects.order_by('date')  # sort by date default
        form = self.form_class(None)
        return render(request, self.template_name, {'transaction_list': transaction_list, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        transaction_list = Transaction.objects.order_by('date')  # sort by date default
        return render(request, self.template_name, {'transaction_list': transaction_list, 'form': form})


class TransferView(StaffRequiredMixin, View):
    template_name = 'staff/store/transfer_list.html'

    def get(self, request, **kwargs):

        query = request.GET.get('q')
        if query:
            transfer_list = Transfer.objects.filter(
                Q(origin__contains=query)).order_by('-date')
            return render(request, self.template_name, {'transfer_list': transfer_list})
        else:
            transfer_list = Transfer.objects.order_by('-date')  # sort by username default
            return render(request, self.template_name, {'transfer_list': transfer_list})


@staff_required
def products(request):
    if request.method == 'GET':
        product_list = Product.objects.all().order_by('id')
        return render(request, 'staff/store/product_list.html', {'product_list': product_list})


@staff_required
def product_detail(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(id=pk)
        return render(request, 'staff/store/product_detail.html', {'product': product, 'pk': pk})


@staff_required
def create_product(request):
    if request.method == 'GET':
        form = CreateProductForm(None)
        return render(request, 'staff/store/product_create.html', {'form': form})
    else:
        form = CreateProductForm(request.POST)
        if form.is_valid():
            product = form.instance
            product.business = settings.PAYPAL_EMAIL
            product.save()
            return redirect('staff:product_detail', pk=product.id)
        else:
            return render(request, 'staff/store/product_create.html', {'form': form})


@staff_required
def edit_product(request, pk):
    if request.method == 'GET':
        form = CreateProductForm(instance=Product.objects.get(id=pk))
        return render(request, 'staff/store/product_edit.html', {'form': form, 'pk': pk})
    else:
        form = CreateProductForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=pk)
            product.amount = form.cleaned_data['amount']
            product.item_name = form.cleaned_data['item_name']
            product.name = form.cleaned_data['name']
            product.active = form.cleaned_data['active']
            product.save()
            return redirect('staff:product_detail', pk=product.id)
        else:
            return render(request, 'staff/store/product_edit.html', {'form': form, 'pk': pk})


@staff_required
def delete_product(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    product = Product.objects.get(pk=pk)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('staff:product_list')
