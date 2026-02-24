from django.db import models
from store.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id     = models.CharField(max_length= 250, blank=True)
    date_added  = models.DateField(auto_now_add=True)


    def __str__(self):
        """
        Return a string representation of the Cart instance.
        
        Returns:
            str: The cart ID
        """
        return self.cart_id
    

class CartItem(models.Model):
    products     =  models.ForeignKey(Product, on_delete=models.CASCADE)
    cart         =  models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity     =  models.IntegerField()
    is_active    =  models.BooleanField(default=True)

    
    def sub_total(self):
        """
        Calculate the subtotal for this cart item.
        
        This method multiplies the product price by the quantity
        to get the total cost for this specific cart item.
        
        Returns:
            int: The subtotal (product price × quantity)
        """
        return self.products.price * self.quantity
     
    def __str__(self):
        """
        Return a string representation of the CartItem instance.
        
        Returns:
            str: The product name associated with this cart item
        """
        return self.cart.cart_id