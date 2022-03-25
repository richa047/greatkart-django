from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug !=None: # for category
        categories = get_object_or_404(Category, slug=category_slug)# bring us category else display 404
        products = Product.objects.filter(category=categories, is_available=True)#display all product which belong to above category
        paginator = Paginator(products, 1)#take 6 products on 1 pg
        page = request.GET.get('page') # ?page=2
        paged_products = paginator.get_page(page)# 6 product here
        product_count = products.count()
    else: #for product
        products = Product.objects.all().filter(is_available =True).order_by('id')#all together 8 product here
        paginator = Paginator(products, 3)#take 6 products on 1 pg
        page = request.GET.get('page') # ?page=2
        paged_products = paginator.get_page(page)# 6 product here
        product_count = products.count()
    
    context =   {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

# create link for detail pg
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product= single_product).exists()#?to see if the selected item is there in cart if yes return true ,f9v3(2.16)
        #return HttpResponse(in_cart)
        #exit()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart' : in_cart
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:# if keyword is in url  GET request
        keyword = request.GET['keyword']# take value of that keyword ie keyword=jeans from url and store it in keyword
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))# to search keyword value ie jeans in descriptions
            product_count = products.count()
    context = {
        'products': products,
        'product_count': products.count,
    }
    return render(request, 'store/store.html', context) 