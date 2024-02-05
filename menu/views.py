from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from .models import Product, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def menu(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})

def home(request):
    return render(request, 'home.html')

def catering(request):
    return render(request, 'catering.html')

def order(request):
    return render(request, 'order.html')

def gallery(request):
    return render(request, 'gallery.html')

def Glendale(request):
    return render(request, 'Glendale.html')

def Panorama_City(request):
    return render(request, 'Panorama_City.html')

def Reseda(request):
    return render(request, 'Reseda.html')


def checkout(request):
    return render(request, 'checkout.html')

# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'menu.html', {'products': products})
 
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cart_items = CartItem.objects.filter(user=request.user)
        total = 0
        for cart_item in cart_items:
            total += cart_item.price
        context = {
            'email': email,
            'cart_items': cart_items,
            'total': total
        }
        return render(request, 'checkout.html', context)

def create_checkout_session(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for cart_item in cart_items:
        total += cart_item.price
    session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name
                    },
                    'unit_amount': int(product.price * 100)
                },
                'quantity': cart_item.quantity
            }
        ],
        mode='payment',
        success_url=f'http://127.0.0.1:8000/success/{product_id}',
        cancel_url=f'http://127.0.0.1:8000/cancel'
    )
    return JsonResponse({'id': session.id})

def create_payment_intent(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for cart_item in cart_items:
        total += cart_item.price
    payment_intent = stripe.PaymentIntent.create(
        amount=int(total * 100),
        currency='usd',
        payment_method_types=['card']
    )
    return JsonResponse({'clientSecret': payment_intent.client_secret})

stripe.api_key = settings.STRIPE_SECRET_KEY

# def create_charge(request):
#     # Logic to create a charge
#     stripe.Charge.create(
#         amount=2000,
#         currency="usd",
#         source=request.POST['stripeToken'], # Use the token created by Stripe Elements in the frontend
#         description="Charge for food order"
#     )
class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"

class ProductLandingPage(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context = super(ProductLandingPage, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context



class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + 'success',
            cancel_url=YOUR_DOMAIN + 'cancel',
        )
        return JsonResponse({
            'id': checkout_session.id
        })



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"Checkout Session Completed for:{session['id']}")
        print(f"Checkout Session Completed customer:{session['customer']}")
        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Order confirmation",
            message=f"Thanks for your purchase. Your order will be ready soon.",
            # message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL
    
    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Order confirmation",
            message=f"Thanks for your purchase. Your order will be ready soon.",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    return HttpResponse(status=200)

class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })
