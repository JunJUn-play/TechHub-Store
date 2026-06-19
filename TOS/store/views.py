from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Product, Order, OrderItem, Category, Brand
from .forms import UserRegisterForm, UserLoginForm
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import ProductSerializer, RegisterSerializer
from .permissions import IsStaffOrAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate

# ==========================================
# CLIENT LAYER: PRODUCT BROWSING
# ==========================================
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is out of stock
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('product_detail', pk=product.id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:

        # Don't allow quantity to exceed stock
        if cart[product_id]['quantity'] < product.stock:
            cart[product_id]['quantity'] += 1
        else:
            messages.warning(request, "You cannot add more than the available stock.")

    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['cart'] = cart

    return redirect('view_cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=product_id)

    product_id = str(product_id)

    if product_id in cart:

        # Prevent quantity from exceeding stock
        if cart[product_id]['quantity'] < product.stock:
            cart[product_id]['quantity'] += 1
        else:
            messages.warning(request, "Maximum stock reached!")

    request.session['cart'] = cart

    return redirect('view_cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] -= 1

        if cart[product_id]['quantity'] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('view_cart')

def checkout_view(request):
    cart = request.session.get('cart', {})

    total = 0

    for item in cart.values():
        total += item['price'] * item['quantity']

    return render(request, 'checkout.html', {
        'cart': cart,
        'total': total,
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')

    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    form = UserLoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')

class OrderCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        # 1. Create the Base Order
        order = Order.objects.create(customer=user, status='pending')

        # 2. Create Order Items and Update Database Layer (SQLite)
        for item in data['items']:
            product = Product.objects.get(id=item['product_id'])
            
            # Inventory Safety Logic
            if product.stock >= item['quantity']:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
                product.stock -= item['quantity']
                product.save()
            else:
                return Response({"error": f"Not enough stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"order_id": order.id}, status=status.HTTP_201_CREATED)
class ProductAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be edited by Staff/Admin only.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # This line triggers the "Access Denied" JSON for Customers
    permission_classes = [IsStaffOrAdmin]
class ProductManagementViewSet(viewsets.ModelViewSet):
    """
    Staff/Admin API for managing TechHub inventory.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # This is the "Gatekeeper" for the Application Layer
    permission_classes = [IsStaffOrAdmin] 

    def perform_create(self, serializer):
        # Extra logic: logs which staff member added the item
        serializer.save()


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'role': user.role,
        })


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all()

        category_id = self.request.GET.get('category')
        brand_id = self.request.GET.get('brand')

        if category_id:
            products = products.filter(category_id=category_id)

        if brand_id:
            products = products.filter(brand_id=brand_id)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        category_id = self.request.GET.get('category')
        brand_id = self.request.GET.get('brand')

        if category_id:
            context['selected_category'] = Category.objects.get(id=category_id)

            context['brands'] = Brand.objects.filter(
                products__category_id=category_id
            ).distinct()
        else:
            context['selected_category'] = None
            context['brands'] = []

        if brand_id:
            context['selected_brand'] = Brand.objects.get(id=brand_id)
        else:
            context['selected_brand'] = None

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


# ==========================================
# CLIENT LAYER: CART WORKSPACE (MOCK)
# ==========================================
def view_cart(request):
    cart = request.session.get("cart", {})

    grand_total = 0

    for item in cart.values():
        item["total"] = float(item["price"]) * item["quantity"]
        grand_total += item["total"]

    return render(request, "cart.html", {
        "cart": cart,
        "grand_total": grand_total
    })


# ==========================================
# APPLICATION LAYER: ORDER PROCESSING & EXTERNAL SERVICES
# ==========================================
@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your shopping cart is empty!")
        return redirect('product_list')

    if request.method == 'POST':
        # 1. Create Order instance in SQLite
        order = Order.objects.create(customer=request.user, status='pending')
        
        # 2. Move items from Session Cart to Database Order Items
        for item_id, item_data in cart.items():
            product = get_object_or_404(Product, id=item_id)
            
            # Inventory validation (Business Logic safety rule)
            if product.stock >= item_data['quantity']:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item_data['quantity']
                )
                # Deduct inventory stock
                product.stock -= item_data['quantity']
                product.save()
            else:
                messages.error(request, f"Sorry, {product.name} is out of stock.")
                order.delete() # Roll back order creation
                return redirect('view_cart')

        # 3. Clear the session cart
        request.session['cart'] = {}

        # 4. Hand off to External Payment Gateway Process
        return redirect('process_payment', order_id=order.id)

    return render(request, 'checkout.html', {'cart': cart})


# ==========================================
# EXTERNAL SERVICES LAYER INTEGRATION
# ==========================================
@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    # Simulating API connection to Third-Party Payment Gateway
    # In production, this would initialize a gateway session payload (e.g., Stripe/PayPal)
    payment_successful = True 
    mock_transaction_id = f"TXN-{order.id}XYZ789"

    if payment_successful:
        # Update SQLite layer
        order.status = 'paid'
        order.payment_intent_id = mock_transaction_id
        order.save()

        # Trigger External Notification/Email Service (Asynchronous Task recommended)
        send_order_confirmation_email(order)

        messages.success(request, f"Payment successful! Order #{order.id} is being processed.")
        return redirect('payment_success')
    else:
        order.status = 'cancelled'
        order.save()
        messages.error(request, "Payment transaction failed.")
        return redirect('view_cart')


def send_order_confirmation_email(order):
    """
    Mock function representing the Third Party Email Service
    as detailed under the 'External Services' block in image_a5c306.jpg
    """
    subject = f"TechHub Order Confirmation - #{order.id}"
    message = f"Hello {order.customer.username},\n\nThank you for shopping at TechHub! Your payment was received successfully. We are preparing your tech package."
    recipient = order.customer.email
    
    # django.core.mail.send_mail(subject, message, 'noreply@techhub.com', [recipient])
    print(f"DEBUG: Sent confirmation email to {recipient} via External Email API.")


def payment_success(request):
    return render(request, 'success.html')