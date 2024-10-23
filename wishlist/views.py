from django.shortcuts import render, redirect, get_object_or_404, reverse
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

def remove_from_wishlist(request, item_id):
    """ Remove a specified product from the wishlist """
    wishlist = request.session.get('wishlist', {})
    product = get_object_or_404(Product, pk=item_id)
    
    if str(item_id) in wishlist:
        del wishlist[str(item_id)]
        messages.success(request, f"'{product.name}' has been removed from your wishlist.")
    else:
        messages.warning(request, f"'{item_id}' was not found in your wishlist.")

    request.session.pop('removed_product', None)
    
    request.session['wishlist'] = wishlist
    return redirect(reverse('view_wishlist'))