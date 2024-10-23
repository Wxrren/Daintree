from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages


def view_wishlist(request):
    """ A view that renders the wishlist contents page """
    wishlist = request.session.get('wishlist', {})
    wishlist_items = []

    for item_id in wishlist.keys():
        product = get_object_or_404(Product, pk=item_id)
        wishlist_items.append({
            'item_id': item_id,
            'product': product,
        })

    context = {
        'wishlist_items': wishlist_items,
        'product_count': len(wishlist),
    }
    return render(request, 'wishlist/wishlist.html', context)


def add_to_wishlist(request, item_id):
    """ Add a specified product to the wishlist """

    product = get_object_or_404(Product, pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    wishlist = request.session.get('wishlist', {})

    if str(item_id) in wishlist:
        messages.info(request, f"'{product.name}' is already in your wishlist.")
    else:
        messages.success(request, f"'{product.name}' is addec to your wishlist.")
        wishlist[str(item_id)] = 1

    request.session['wishlist'] = wishlist
    print(request.session['wishlist'])
    return redirect(redirect_url)
