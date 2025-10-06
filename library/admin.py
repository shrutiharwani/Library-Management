from django.contrib import admin
from .models import Book, CartItem, IssuedBook, SavedBook

admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(IssuedBook)
admin.site.register(SavedBook)
