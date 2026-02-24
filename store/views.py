from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from carts.models import CartItem
from carts.views import _cart_id
from .models import Product, Category

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug = None):
    """
    Display products in the store, optionally filtered by category.
    
    This view handles both the main store page and category-specific product listings.
    It retrieves all available products or filters them by a specific category slug.
    
    Args:
        request (HttpRequest): The HTTP request object
        category_slug (str, optional): The slug of the category to filter products by.
                                     If None, displays all available products.
    
    Returns:
        HttpResponse: Rendered store template with products and product count
    
    Context:
        products (QuerySet): Available products (filtered by category if specified)
        product_count (int): Total number of products in the result set
    """
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.all().filter(category = categories, is_available = True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available = True).order_by("id")
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products' : paged_products, 
        'product_count':product_count, 
    }

    return render(request, 'store/store.html', context=context)

def product_detail(request, category_slug = None, product_slug = None):
    """
    Display detailed information for a specific product.
    
    This view retrieves a single product based on its category and product slugs,
    and displays detailed product information including description, price, and image.
    
    Args:
        request (HttpRequest): The HTTP request object
        category_slug (str, optional): The slug of the product's category
        product_slug (str, optional): The slug of the specific product
    
    Returns:
        HttpResponse: Rendered product detail template with product information
    
    Context:
        single_product (Product): The product object with all its details
    
    Raises:
        Exception: Re-raises any exception that occurs during product retrieval
    """
    try:
        product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), products = product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product' : product,
        'in_cart': in_cart, 
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    if "keyword" in request.GET:
        context = None
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

            context = {
                'products': products,
                'product_count': products.count(),
            }

    return render(request, "store/store.html", context)