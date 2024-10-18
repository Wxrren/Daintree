from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q3EBiRxoa5wCjJhNY3eAdIY7epiGUlMFqo8tHTZdeIGmZL9nH1Xv4yToWq1gqxtXkuCWo75xL010knXM7s0Wujt002t9xQqF6',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)