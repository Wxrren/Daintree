from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Product, Wishlist
from django.contrib import messages


def view_wishlist(request):
    """ A view that renders the wishlist contents page """
    
    return render(request, 'wishlist/wishlist.html')


def add_to_wishlist(request, item_id):
    """ Add a specified product to the wishlist """

    product = get_object_or_404(Product, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    wishlist = request.session.get('wishlist', {})

    if str(item_id) in wishlist:
        messages.info(request, f"'{product.name}' is already in your wishlist.")
    else:
        wishlist[str(item_id)] = 1

    request.session['wishlist'] = wishlist
    print(request.session['wishlist'])
    return redirect(redirect_url)
