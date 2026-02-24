from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/product')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        """
        Generate the URL for this product's detail page.
        
        This method creates a URL that points to the product detail view
        using the product's category slug and product slug.
        
        Returns:
            str: The URL path for the product detail page
        """
        return reverse('product_detail', args = [self.category.slug, self.slug])

    def __str__(self):
        """
        Return a string representation of the Product instance.
        
        Returns:
            str: The product name
        """
        return self.product_name