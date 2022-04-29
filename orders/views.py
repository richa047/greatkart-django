from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order
import json



def payments(request):
    body = json.loads(request.body)
    print(body)
    return render(request, 'orders/payments.html')

    
# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    print(current_user)

   

    #if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user= current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
       return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        print(cart_items)
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method =='POST':
        form = OrderForm(request.POST)
        print('hi POST request')
        if form.is_valid():
           
            '''Order.objects.create(user=current_user, first_name=form.cleaned_data['first_name'],last_name = form.cleaned_data['last_name'], phone = form.cleaned_data['phone'],
            email = form.cleaned_data['email'], address_line_1 = form.cleaned_data['address_line_1'], address_line_2 = form.cleaned_data['address_line_2'], country=form.cleaned_data['country'],
            state=form.cleaned_data['state'], city=form.cleaned_data['city'], order_note = form.cleaned_data['order_note']
            )'''
            # Store all the billing information inside Order table
            print('hi valid')
            
            data = Order() # create order object
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            print(data.first_name)
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total= grand_total
            data.tax= tax
    
            data.ip = request.META.get('REMOTE_ADDR')# this will give user ip
            data.save()
            print(data)

            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number= order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax':tax,
                'grand_total': grand_total,
            }
            return render(request,'orders/payments.html', context)
        else:
            print(form.errors)
    else:
        form = OrderForm()# else display empty form if form is not valid
        
    return redirect('checkout')    

    #return redirect('checkout')  