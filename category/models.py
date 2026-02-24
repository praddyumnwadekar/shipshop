from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to= 'photos/categories', blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        """
        Generate the URL for this category's product listing page.
        
        This method creates a URL that points to the category view
        using the category's slug.
        
        Returns:
            str: The URL path for the category product listing page
        """
        return reverse('category_slug', args = [self.slug])
    
    def __str__(self):
        """
        Return a string representation of the Category instance.
        
        Returns:
            str: The category name
        """
        return self.category_name
    


