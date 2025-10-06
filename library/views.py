from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.db.models import Count
from .models import Book, CartItem, IssuedBook, SavedBook
from .serializers import BookSerializer, CartItemSerializer, IssueSerializer, SavedBookSerializer
from .permissions import IsLibrarian
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from django.db import transaction

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create','destroy','update','partial_update']:
            return [IsAuthenticated(), IsLibrarian()]
        return [AllowAny()]

    def get_queryset(self):
        qs = Book.objects.all().annotate(issued_count=Count('issued_records'))
        
        sort = self.request.query_params.get('sort')
        author = self.request.query_params.get('author')

        if author:
            qs = qs.filter(author__icontains=author)
        
        if sort == 'most_issued':
            qs = qs.order_by('-issued_count')
        elif sort == 'least_issued':
            qs = qs.order_by('issued_count')
            
        return qs

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data['book']
        qty = serializer.validated_data.get('quantity', 1)
        obj, created = CartItem.objects.get_or_create(user=request.user, book=book, defaults={'quantity': qty})
        if not created:
            obj.quantity += qty
            obj.save()
        return Response({'detail': 'Added to cart'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        items = CartItem.objects.filter(user=request.user)
        if not items.exists():
            return Response({'detail': 'Cart empty'}, status=status.HTTP_400_BAD_REQUEST)

        issued_list = []
        total = 0

        with transaction.atomic():
            for it in items:
                book = it.book
                book.refresh_from_db()
                if book.available_copies < it.quantity:
                    return Response({'detail': f'Not enough copies for {book.title}'}, status=status.HTTP_400_BAD_REQUEST)
                
                book.available_copies -= it.quantity
                book.save()
                
                for _ in range(it.quantity):
                    issued = IssuedBook.objects.create(user=request.user, book=book)
                    issued_list.append(issued)
                    total += book.price

            items.delete()

        serializer = IssueSerializer(issued_list, many=True)
        bill = {
            'issued_count': len(issued_list),
            'total_amount': total,
            'items': serializer.data
        }
        return Response(bill, status=status.HTTP_201_CREATED)

class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        issued_book_id = request.data.get('issued_book_id')
        try:
            issued_book = IssuedBook.objects.get(id=issued_book_id, user=request.user, returned=False)
        except IssuedBook.DoesNotExist:
            return Response({'detail': 'Issued book record not found or already returned.'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            issued_book.returned = True
            issued_book.save()

            book = issued_book.book
            book.available_copies += 1
            book.save()
        
        return Response({'detail': f'Book "{book.title}" returned successfully.'}, status=status.HTTP_200_OK)

class IssuedBookListView(generics.ListAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return IssuedBook.objects.filter(user=self.request.user).order_by('-issue_date')

class SaveForLaterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        obj, created = SavedBook.objects.get_or_create(user=request.user, book=book)
        
        if created:
            return Response({'detail': 'Book saved for later.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Book was already in your saved list.'}, status=status.HTTP_200_OK)

class SavedBookListView(generics.ListAPIView):
    serializer_class = SavedBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedBook.objects.filter(user=self.request.user)
