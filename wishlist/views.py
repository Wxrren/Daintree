from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Product, Wishlist
from django.contrib import messages
from .forms import WishlistForm


def view_wishlist(request):
    """ A view that renders the wishlist contents page """
    
    return render(request, 'wishlist/wishlist.html')
