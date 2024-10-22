def wishlist_contents(request):

    wishlist_items = []
    product_count = 0

    context = {
        'wishlist_items': wishlist_items,
        'product_count': product_count,
    }

    return context