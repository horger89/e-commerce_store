from carts.models import CartItem
from django.shortcuts import redirect, render
from .forms import OrderForm
from .models import Order, Payment
import datetime
import json

# Create your views here.
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    # store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0,grand_total=0,tax=0):
    current_user = request.user

    #if the cart is less then or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    
    tax= 0
    grand_total= 0
    
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (5 * total)/100
    grand_total = total + tax
    print(grand_total)
    

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print('it is valid')
            #store all billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.phone = form.cleaned_data.get('phone')
            data.email = form.cleaned_data.get('email')
            data.address_line_1 = form.cleaned_data.get('address_line_1')
            data.address_line_2 = form.cleaned_data.get('address_line_2')
            data.country = form.cleaned_data.get('country')
            data.state = form.cleaned_data.get('state')
            data.city = form.cleaned_data.get('city')
            data.order_note = form.cleaned_data.get('order_note')
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # fetch user ip
            
            data.save()
            # Generate order ID
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            return render(request, 'orders/payments.html', context)
        
        else:
            print('went to else')
            return redirect('checkout')
            

