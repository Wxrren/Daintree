from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import WishlistForm
from django.core.paginator import Paginator
from django.db.models.functions import Lower

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # Pagination
    paginator = Paginator(products, 100)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    params.pop('page', None) 
    params['page'] = page_obj.number 

    context = {
        'products': page_obj,
        'search_term': query,
        'current_categories': categories,
        'params': request.GET.copy(),
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = WishlistForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user_profile = request.user.userprofile
            form.instance.product = product
            form.save()
            messages.success(request, f"{product.name} added to your wishlist!")
            return redirect('product_detail', product_id=product_id)
    else:
        form = WishlistForm(initial={'product': product})

    context = {
        'product': product,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)
