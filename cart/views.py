from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView

from books.models import Book
from .models import Order, OrderItem
from users.models import CustomUser, UserPurchase, UserPurchaseSession

import json
import stripe
import math


@login_required
def get_cart_count(request):
    customer = request.user
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    items = order.orderitem_set.all()
    number = items.count()
    response = {'number': number}
    return JsonResponse(response)


@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except:
            order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items, 'order': order}
    return render(request, 'cart/cart.html', context)


@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        except:
            order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # print(order.__dict__)
        items = order.orderitem_set.all()
        # if request.method == "POST":
        #     form = PurchaseForm(request.POST)
        #     if form.is_valid():
        #         address = form.cleaned_data['address']
        #         city = form.cleaned_data['city']
        #         state = form.cleaned_data['state']
        #         zipcode = form.cleaned_data['zipcode']
        #         for item in items:
        #             book_id = item.book_id
        #             book = Book.objects.get(id=book_id)
        #             UserPurchase.objects.create(
        #                 seller=CustomUser.objects.get(id=book.seller_id),
        #                 buyer=CustomUser.objects.get(id=request.user.id),
        #                 book=Book.objects.get(id=book_id),
        #                 address=address,
        #                 city=city,
        #                 state=state,
        #                 zipcode=zipcode,
        #                 # is_complete=True,
        #             )
        #             # user_purchase, new_user_purchase = UserPurchase.objects.get_or_create(
        #             #     seller=CustomUser.objects.get(id=book.seller_id),
        #             #     buyer=CustomUser.objects.get(id=request.user.id),
        #             #     book=Book.objects.get(id=book_id),
        #             #     address=address,
        #             #     city=city,
        #             #     state=state,
        #             #     zipcode=zipcode,
        #             #     is_complete=True,
        #             # )
        #         # order.complete = True
        #         # order.save()
        #         items.delete()
        #         messages.add_message(request, messages.SUCCESS, 'Thank You for buying book')
        #         return redirect('users:profile')
        # else:
        #     form = PurchaseForm()
    else:
        items = []
    context = {'items': items, 'order': order}
    return render(request, 'cart/checkout.html', context)


@login_required
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user
    book = Book.objects.get(id=product_id)
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print(order)
    orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)
    if action == 'add':
        orderItem.quantity = 1
    elif action == 'remove':
        orderItem.quantity = 0
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse({action: action}, safe=False)


@csrf_exempt
@login_required
def checkout_stripe(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
@login_required
def stripe_checkout_session(request):

    customer = request.user
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = order.get_cart_total * 100
    total = math.trunc(total)
    total = str(total)
    # print(total)
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                shipping_rates=['shr_1Jh890AljoQr5S9XKs1t2Lk7'],
                shipping_address_collection={
                    'allowed_countries': ['AU', 'NP'],
                },
                line_items=[
                    {
                        'name': 'Pasal Bill Amount',
                        'quantity': 1,
                        'currency': 'aud',
                        'amount': total,
                    }
                ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer = request.user
    try:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer, complete=False).order_by('id').last()
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    user_purchase_session_ids = list(UserPurchaseSession.objects.values_list('session_id', flat=True))
    try:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        session_id = request.GET['session_id']
        if session_id not in user_purchase_session_ids and session['payment_status'] == 'paid':
            address_line1 = session['shipping']['address']['line1']
            address_line2 = session['shipping']['address']['line2']
            city = session['shipping']['address']['city']
            zipcode = session['shipping']['address']['postal_code']
            name = session['shipping']['name']
            for item in items:
                book_id = item.book_id
                book = Book.objects.get(id=book_id)
                book.is_sold = True
                book.save()
                UserPurchase.objects.create(
                    seller=CustomUser.objects.get(id=book.seller_id),
                    buyer=CustomUser.objects.get(id=request.user.id),
                    book=Book.objects.get(id=book_id),
                    address_line1=address_line1,
                    address_line2=address_line2,
                    city=city,
                    zipcode=zipcode,
                    shipping_address_name=name
                    # is_complete=True,
                )
            order.complete = True
            order.save()
            items.delete()
            UserPurchaseSession.objects.create(session_id=session_id)

    except Exception as e:
        return redirect('books:book-list')
    context = {'message': 'Thank you for purchasing on Pasal'}
    return render(request, 'cart/success.html', context)


@login_required
def cancelled(request):
    context = {'message': 'You cancelled your payment.'}
    return render(request, 'cart/cancel.html', context)


@csrf_exempt
@login_required
def stripe_payout_session(request):
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        account = stripe.Account.create(
            type='express',
        )
        account_links = stripe.AccountLink.create(
            account=account['id'],
            refresh_url=domain_url + 'reauth',
            return_url=domain_url + 'return',
            type='account_onboarding',
        )
        return JsonResponse({'account_links': account_links})
    except Exception as e:
        return JsonResponse({'error': str(e)})
