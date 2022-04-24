from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests


def register(request):
    if request.method == 'POST':
         form = RegistrationForm(request.POST)
        #if form is valid enter clean data anad crete object
         if form.is_valid():
             first_name= form.cleaned_data['first_name']
             last_name= form.cleaned_data['last_name']
             phone_number= form.cleaned_data['phone_number']
             email= form.cleaned_data['email']
             password= form.cleaned_data['password']
             username=email.split("@")[0]
             user = Account.objects.create_user(first_name=first_name, last_name= last_name, email=email,username=username,password=password)
             user.phone_number = phone_number #since u do not have phone no in create user(model.py) so u need to specify it here
             user.save()
             
             #User Activation
             current_site = get_current_site(request)
             mail_subject = 'Please activate your account'
             message = render_to_string('account/account_verification_email.html',{
                 'user': user,
                 'domain': current_site,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),# it encode user primary key
                 'token': default_token_generator.make_token(user),
             })
             to_email = email
             send_email =EmailMessage(mail_subject, message, to=[to_email])
             send_email.send()
             #messages.success(request, 'Thank you for registering with us.We have sent you a verification email to your email adddress.Please verify it.')
             return redirect ('/accounts/login/?command=verification&email='+email)
    else:
         form = RegistrationForm()
    context = {
        'form': form,

    }

    return render(request,'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email= email, password=password)

        if user is not None:
            try:
                print('entering inside try block')
                cart = Cart.objects.get(cart_id=_cart_id(request))#check if there are cart items inside the cart before user has logged in
                is_cart_item_exists = CartItem.objects.filter( cart =cart ).exists()
                print(is_cart_item_exists)

                if  is_cart_item_exists:
                    cart_item  = CartItem.objects.filter(cart=cart)
                    print(cart_item)
                     
                    #Getting the product variations by card id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))





                    #Get the cart items from the user to access his product variations
                        cart_item = CartItem.objects.filter( user=current_user)# you have product,cart ,create new product with new variation in different block in cart page
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                    # for item in cart_item:#assigning user name to cart item
                    #     item.user = user
                    #     item.save()

                    #product_variation =[1,2,3,4,6]
                    #ex_var_list =[4,6,3,5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = cartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                print('entering inside except block')
                pass
            auth.login(request, user)
            messages.success(request, 'You are not logged in')
            url = request.META.get('HTTP_REFERER')# requests used for dynamic redirect usr to nxt page
            #HTTP_REFERER grabs previous url from where u came
            try:
                query = requests.utils.urlparse(url).query
                print('query ->', query)#no output 6.39 v7 f16
                #next=/cart/checkout/
                params = dict(x.split('=')for x in query.split('&'))
                print('param ->', params)
                if 'next' in params:
                    nextPage= params['next']
                    return redirect(nextPage) 
                
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):# u shd be able to logout only if u are login
    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('login') 

def activate(request, uidb64, token):
    #return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
         user = None
    if user is not None and default_token_generator.check_token(user,token):# want to take out user from token that u have
       user.is_active = True
       user.save()
       messages.success(request, 'Congratulations! Your account is activated')# when user click on link sent by the sytem to their mail id u display this msg on login pg
       return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():#will return true or false
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                 'user': user,
                 'domain': current_site,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)), # it encode user primary key
                 'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
       
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')



def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid') # getting uid from the session
            user = Account.objects.get(pk=uid)
            user.set_password(password)# so that system allow you to work with that password
            user.save()
            messages.success(request,'Password reset successfulS')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
        return redirect('resetPassword')  
    else: 
        return render(request, 'accounts/resetPassword.html')

