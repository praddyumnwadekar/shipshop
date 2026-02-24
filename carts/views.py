from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from store.models import Product

# Create your views here.

def _cart_id(request):
    """
    Get or create a cart ID for the current session.
    
    This helper function retrieves the session key to use as cart ID.
    If no session exists, it creates a new one.
    
    Args:
        request (HttpRequest): The HTTP request object containing session data
    
    Returns:
        str: The session key to be used as cart ID
    """
    cart = request.session.session_key
    
    if not cart:
        cart = request.session.create()
    
    return cart

def remove_cart(request, product_id):
    """
    Remove one quantity of a product from the cart.
    
    This function decreases the quantity of a specific product in the cart by 1.
    If the quantity becomes 0, the cart item is completely removed.
    
    Args:
        request (HttpRequest): The HTTP request object
        product_id (int): The ID of the product to remove from cart
    
    Returns:
        HttpResponseRedirect: Redirects to the cart page after removal
    
    Raises:
        Http404: If the product with given ID doesn't exist
    """
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(products = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
    
def remove_cart_item(request, product_id):
    """
    Completely remove a product from the cart.
    
    This function removes all quantities of a specific product from the cart,
    regardless of how many items were in the cart.
    
    Args:
        request (HttpRequest): The HTTP request object
        product_id (int): The ID of the product to completely remove from cart
    
    Returns:
        HttpResponseRedirect: Redirects to the cart page after removal
    
    Raises:
        Http404: If the product with given ID doesn't exist
    """
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(products = product, cart = cart)

    cart_item.delete()
    
    return redirect('cart')
    

def add_cart(request, product_id):
    """
    Add a product to the cart or increase its quantity if already present.
    
    This function adds a product to the user's cart. If the product is already
    in the cart, it increases the quantity by 1. If not, it creates a new
    cart item with quantity 1.
    
    Args:
        request (HttpRequest): The HTTP request object
        product_id (int): The ID of the product to add to cart
    
    Returns:
        HttpResponseRedirect: Redirects to the cart page after adding
    
    Raises:
        Product.DoesNotExist: If the product with given ID doesn't exist
    """
    product = Product.objects.get(id = product_id) # get the productusing product_id

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) # get the cart using Cart_id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    try:
        cart_item =  CartItem.objects.get(products = product, cart = cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item  = CartItem.objects.create(
            products = product,
            quantity = 1,
            cart = cart,
        )
    
    cart_item.save()

    return redirect('cart')

def cart(request, total = 0, quantity = 0, cart_items = None):
    """
    Display the shopping cart with calculated totals.
    
    This view retrieves all active cart items for the current session and
    calculates the total price, quantity, tax (5%), and grand total.
    
    Args:
        request (HttpRequest): The HTTP request object
        total (int, optional): Initial total amount (default: 0)
        quantity (int, optional): Initial quantity count (default: 0)
        cart_items (QuerySet, optional): Initial cart items (default: None)
    
    Returns:
        HttpResponse: Rendered cart template with cart data
    
    Context:
        total (int): Subtotal of all cart items
        quantity (int): Total number of items in cart
        cart_items (QuerySet): All active cart items
        tax (float): Calculated tax amount (5% of total)
        grand_total (float): Total amount including tax
    """
    try:
        tax = grand_total = 0
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)

        for cart_item in cart_items:
            total += (cart_item.products.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (5 * total)/100
        grand_total = total + tax

    except CartItem.DoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }

    return render(request, "store/cart.html", context)