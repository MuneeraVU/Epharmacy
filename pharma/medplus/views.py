# views.py

from django.http import HttpResponse, request, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import UserRegistrationForm, PrescriptionForm, ShippingAddressForm
from .models import Category, Medicine, Prescription, CartItem, ShippingAddress
from django.contrib.auth.decorators import login_required
import stripe


# for stripe integration
# stripe.api_key = settings.STRIPE_SECRET_KEY


# Create views here

# views for about
def about(request):
    return render(request, 'about.html')


# Home page view by passing category slug
def home(request, cat_slug=None):
    cat_page = None  # set category page as none
    medicines = None
    # If category slug present
    if cat_slug != None:
        cat_page = get_object_or_404(Category, slug=cat_slug)
        medicines = Medicine.objects.all().filter(category=cat_page,
                                                  available=True)  # Filter all medicines according to category slug and display avilable medicines
    else:  # If no category slug , display all available medicines.
        medicines = Medicine.objects.all().filter(available=True)
    return render(request, 'home.html', {'category': cat_page, 'medicines': medicines})


# Medicine page view by passing category slug and medicine slug
def med_details(request, cat_slug, med_slug):
    try:
        medicine = Medicine.objects.get(category__slug=cat_slug, slug=med_slug)
    except Exception as e:
        raise e
    return render(request, 'medicine.html', {'medicine': medicine})  # Display medicine page by passing context


# Signin view
def signin(request):
    if request.method == 'POST':  # If post request
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Authenticate using username and password
        if user is not None:  # If user exists
            login(request, user)  # Redirect to signin page
            return redirect('home')  # Redirect to home page after successfull signin.
        else:  # No registered user
            error_message = 'Invalid Username or Password.'
    else:  # Request not post
        error_message = None
    return render(request, 'signin.html', {'error message': error_message})


# Signout view
def signout(request):
    logout(request)  # Logout the requested user
    return redirect('home')


# Profile view
def profile(request):
    return render(request, 'accounts.html',
                  {'userName': request.user.username})  # Display profile page by passing requested username


# Signup view for new user registration
def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})


# Prescription view for uploading prescription
def prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shipping')
    else:
        form = PrescriptionForm()
    return render(request, 'prescription.html', {'form': form})


# Add items to cart view by passing id.
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    cart_item, created = CartItem.objects.get_or_create(medicine=medicine, user=request.user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


# Remove from cart view
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# View to display user's cart
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.medicine.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# Shipping view to enter shipping address
def shipping(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = ShippingAddressForm()
    return render(request, 'shipping.html', {'form': form})


# View to display saved addresses of the requested user
def address(request):
    addresses = ShippingAddress.objects.filter(user=request.user)
    return render(request, 'address.html', {'addresses': addresses})


# To search items through Search form displayed in navbar
def search(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']

        # Filter items by  comparing slug and passed search query
        medicines = Medicine.objects.filter(slug__contains=search_query)
        return render(request, 'search.html', {'search_query': search_query, 'medicines': medicines})
    else:
        return render(request, 'search.html')

# view for checkout
def checkout(request):
    if request.method == 'POST':
        stripe.api_key = 'sk_test_51O8JsXSE1mKdIWZKZ8zDiQNNahW6Zbuox3jE2bJvXF7VljKiaQomvNnuDq4y3sKAhKnjIHDUIfr9trhV5PfBGGsJ00CEsSixTe'

        amount = 1000
        try:
            charge = stripe.PaymentIntent.create(amount=amount, currency='usd', description='ePharmacy Order')
            return redirect('thanks')

        except stripe.error.CardError as e:
            # Handle card error
            return JsonResponse({'error': str(e)})
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return JsonResponse({'error': str(e)})

    return render(request, 'payment.html')


def thanks(request):
    return render(request, 'Thanks.html')
