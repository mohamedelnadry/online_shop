from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderForm()

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})