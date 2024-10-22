from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Product, Wishlist
from django.contrib import messages
from .forms import WishlistForm


def user_wishlist(request):
    """ A view to show users wishlists """

    if not request.user.is_authenticated:
        messages.info(
            request,
            "Please sign in to view your wishlist."
        )
        return redirect('account_login')

    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_items = profile.wishlists.all()

    if not wishlist_items.exists():
        messages.warning(
            request,
            "Your wishlist is currently empty."
            "Add some products to see them here!"
        )

    template = 'wishlist/wishlist.html'
    context = {
        'wishlist_items': wishlist_items,
        'profile': profile,
        'on_profile_page': False,
    }

    return render(request, template, context)


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist_item, created = Wishlist.objects.get_or_create(
                user_profile=request.user.userprofile,
                product=product
            )
            
            if created:
                messages.success(
                    request,
                    f"{product.name} added to your wishlist!"
                    )
            else:
                messages.info(
                    request,
                    f"{product.name} already exists in your wishlist."
                    )
            
            return redirect('product_detail', product_id=product_id)
    else:
        form = WishlistForm(initial={'product': product})
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'form': form,
    })