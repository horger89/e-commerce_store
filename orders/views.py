from carts.models import CartItem
from django.shortcuts import redirect, render

# Create your views here.
def place_order(request):
    current_user = request.user

    #if the cart is less then or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
