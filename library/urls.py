# library/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, 
    CartViewSet, 
    CheckoutView, 
    SaveForLaterView,
    ReturnBookView,
    IssuedBookListView,
    SavedBookListView
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('return-book/', ReturnBookView.as_view(), name='return-book'),
    path('issued-books/', IssuedBookListView.as_view(), name='issued-books-list'),
    path('save-for-later/', SaveForLaterView.as_view(), name='save-for-later'),
    path('saved-books/', SavedBookListView.as_view(), name='saved-books-list'),
]