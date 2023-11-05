# context_processors.py

from medplus.models import Category, CartItem


def my_links(request):
    links = Category.objects.all()
    return dict(links=links)


def cart_total(request):
    total_price = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.medicine.price * item.quantity for item in cart_items)

    return {
        'cart_total': total_price,
    }
