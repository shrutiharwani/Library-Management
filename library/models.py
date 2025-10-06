from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_image = models.URLField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issued_records')
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True)
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = timezone.now().date() + timedelta(days=14)
        super().save(*args, **kwargs)


class SavedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
