from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name= models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)
    
    
    # to change name in admin panel from categorys to categories 
    class Meta:
        verbose_name = 'category'
        verbose_name_plural ='categories'
    
    # to get url using slug by category, name='products_by_category'(store app->urls.py),get url for category, this will get url of particular category
    def get_url(self):
            return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
