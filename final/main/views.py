from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from django.http import JsonResponse
from .tasks import send_order_confirmation_email, process_payment
from .models import (
    User, 
    Category, 
    Product, 
    Order, 
    OrderItem, 
    ShoppingCart, 
    CartItem,
    Payment,
    Review,
    Wishlist,
    WishlistItem
)
from .serializers import (
    UserSerializer, 
    CategorySerializer, 
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer, 
    ShoppingCartSerializer, 
    CartItemSerializer, 
    PaymentSerializer, 
    ReviewSerializer, 
    WishlistSerializer, 
    WishlistItemSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'products_list'
        cached_products = cache.get(cache_key)
        
        if cached_products:
            return Response(cached_products)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'product_{kwargs["pk"]}'
        cached_product = cache.get(cache_key)
        
        if cached_product:
            return Response(cached_product)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        return response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer


def create_order(request):
    new_order = Order.objects.create(user=request.user, total_amount=100.0)
    

    send_order_confirmation_email.delay(new_order.id)
    process_payment.delay(new_order.id)
    
    return JsonResponse({'message': 'Order created and tasks are being processed.'})