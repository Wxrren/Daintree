from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages


def view_wishlist(request):
    """ A view that renders the wishlist contents page """
    wishlist = request.session.get('wishlist', {})
    wishlist_items = []

    for item_id in wishlist.keys():
        try:
            product = get_object_or_404(Product, pk=item_id)
            wishlist_items.append({
                'id': item_id,
                'name': product.name,
                'image_url': product.image.url,
                'price': product.price,
                'sku': product.sku.upper(),
                'url': f"/products/{item_id}",
            })
        except Product.DoesNotExist:
            messages.warning(request, f"Product with ID {item_id} not found in the database.")

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
        messages.success(request, f"'{product.name}' is added to your wishlist.")
        wishlist[str(item_id)] = 1

    request.session['wishlist'] = wishlist
    print(request.session['wishlist'])
    return redirect(redirect_url)