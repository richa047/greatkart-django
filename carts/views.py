from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from carts.models import Cart, CartItem

# Create your views here.
#add cart button
# to get cart_id from session key ie cart id will be session id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create() # create new session if session not there
    return cart 

def add_cart(request, product_id):
    current_user = request.user
    #1. get product to store in cart
    product = Product.objects.get(id=product_id) #get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method =='POST':
            # to loop through all attributes color,size,brand etc
            for item in request.POST:
                key = item
                value = request.POST[key]
                #print(key,value)
                # value in req post are matching with model values in admin NU(F11,v5 3.50) so write below stmt
            #--
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #print(variation)
                    product_variation.append(variation)
                except:
                    pass 
    #-----

        
        

        is_cart_item_exists = CartItem.objects.filter(product=product, user =current_user ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)# you have product,cart ,create new product with new variation in different block in cart page
            ## enter variations for allready existing cart item
            #existing variation->db
            #current variation->product_variation
            #item_id-> db
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
            # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1
                item.save()
                ##return HttpResponse('false')
            else:
                #create a new cart item
                item =CartItem.objects.create(product=product, quantity=1, user =current_user)
            if len(product_variation) > 0:  # to see if product variation(color,size) is empty 
                item.variations.clear()
                item.variations.add(*product_variation)
                # cart_item.variations.add(item)#if empty add varition to cart item
            #cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1 
            item.save()
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            # enter variation for new cart item
            # to see if product variation(color,size) is empty 
            if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
     #if the user is not authenticated
    else: 
        product_variation = []
        if request.method =='POST':
            # to loop through all attributes color,size,brand etc
            for item in request.POST:
                key = item
                value = request.POST[key]
                #print(key,value)
                # value in req post are matching with model values in admin NU(F11,v5 3.50) so write below stmt
            #--
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #print(variation)
                    product_variation.append(variation)
                except:
                    pass 
    #-----

#t       2.       
        try:
            cart = Cart.objects.get(cart_id =_cart_id(request)) # get the cart using the cart_id present in the session 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )    
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, quantity =1 , cart =cart ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,  cart=cart)# you have product,cart ,create new product with new variation in different block in cart page
            ## enter variations for allready existing cart item
            #existing variation->db
            #current variation->product_variation
            #item_id-> db
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
            # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1
                item.save()
                ##return HttpResponse('false')
            else:
                #create a new cart item
                item =CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:  # to see if product variation(color,size) is empty 
                item.variations.clear()
                item.variation.add(*product_variation)
                # cart_item.variations.add(item)#if empty add varition to cart item
            #cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1 
            item.save()
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            # enter variation for new cart item
            # to see if product variation(color,size) is empty 
            if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
                # for item in product_variation:
                # cart_item.variations.add(item)#if empty add varition to cart item
                #cart_item.save()
        

# remove product - button
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
           cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
           cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
           cart_item.quantity -=1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass
    return redirect('cart')

#remove button for independent item ie removing the whole product
def remove_cart_item(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
           cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    else:
           cart = Cart.objects.get(cart_id = _cart_id(request))
           cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0,quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        #for logged in user
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        # for non logged in users    
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total)/100
        grand_total = total+ tax
    except ObjectDoesNotExist:
        pass 

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'        :tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

    ''' 
    1.session key is used as cart id
    '''
@login_required(login_url ='login')
def checkout(request, total=0,quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total)/100
        grand_total = total+ tax
    except ObjectDoesNotExist:
        pass 

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'        :tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
    
        

            