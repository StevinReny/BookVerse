

from django.urls import path
from django.conf.urls.static import static

from books.views import AddBook, AddToCartView, BookDetail, BookEdit, BookList, CartDetailView, CreateOrderView, MyOrdersView, OrderDetailView, RemoveFromCartView
from django.views.generic import TemplateView
from config import settings


urlpatterns=[
     path("create/",AddBook.as_view(),name='create-book'),
     path("",BookList.as_view(),name='book-list'),
     path('edit/<int:pk>/',BookEdit.as_view(),name='book-edit'),
     path("detail/<int:pk>/",BookDetail.as_view(),name='book-detail'),
     path('cart/', CartDetailView.as_view(), name='view-cart'),
     path('cart/add/<int:book_id>/', AddToCartView.as_view(), name='add-to-cart'),

     path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),

      path('order/create/', CreateOrderView.as_view(), name='create-order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
     path('order/success/', TemplateView.as_view(template_name='books/order_sucess.html'), name='order-success'),

    path('orders/', MyOrdersView.as_view(), name='my-orders'),


]


