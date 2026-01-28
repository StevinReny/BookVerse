from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DetailView,TemplateView,View

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Q
from books.forms import BookForm
from books.models import Books, Cart, CartItem
# Create your views here.

from .models import Books, Order, OrderItem

from django.db import transaction

class AddBook(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    form_class=BookForm
    template_name="books/create_book.html"
    model=Books
    success_url=reverse_lazy("book-list")

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()


class BookList(ListView):
    template_name='books/book_list.html'
    context_object_name='books'
    model=Books
    ordering=["-id"]


    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(genre__icontains=query)
            )
        return queryset



class BookEdit(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Books
    form_class=BookForm
    template_name='books/book_edit.html'
    success_url=reverse_lazy("book-list")


    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

class BookDetail(LoginRequiredMixin,DetailView):
    model=Books
    template_name='books/book_detail.html'
    context_object_name="book"


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Books, id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        if quantity > book.stock:
            messages.error(request, "Requested quantity exceeds available stock.")
            return redirect('book-detail', pk=book.id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if created:
            cart_item.quantity = quantity
        else:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.stock:
                messages.error(request, "Total quantity in cart exceeds available stock.")
                return redirect('book-detail', pk=book.id)
            cart_item.quantity = new_quantity

        cart_item.save()
        messages.success(request, f"Added {quantity} to cart.")
        return redirect('view-cart')

class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "books/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        context["items"] = cart.items.all()
        context["total"] = sum(item.get_total_price() for item in cart.items.all())
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        return redirect('view-cart')
    


class CreateOrderView(LoginRequiredMixin, View):
     def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)

        if not cart.items.exists():
            return HttpResponse("Your cart is empty.")

        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            for item in cart.items.all():
                if item.quantity > item.book.stock:
                    return HttpResponse(f"Not enough stock for '{item.book.title}'.")

                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity
                )

                item.book.stock -= item.quantity
                item.book.save()

            cart.items.all().delete()

        return redirect('order-success') 
     
     
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'books/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'books/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')