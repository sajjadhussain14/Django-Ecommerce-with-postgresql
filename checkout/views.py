from django.shortcuts import render, redirect
from core.settings import BASE_URL

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from authentications.models import UserProfile  # Import the UserProfile model
from authentications.models import CustomUser  # Import your custom user model
from django.http import JsonResponse
import json
from authentications.models import UserProfile  # Import the UserProfile model
from authentications.models import CustomUser  # Import your custom user model
import uuid
import datetime

# Create your views here.
from cart.views import cart_calculations


def checkout(request):
    shipping = request.session.get("shipping", {})
    cart = request.session.get("cart", {})

    cart_data = cart_calculations(shipping, cart)

    total = cart_data["total"]
    subtotal = cart_data["subtotal"]
    tax = cart_data["tax"]
    shipping = cart_data["shipping"]

    if not request.session.get("cart"):
        # If it's empty, redirect to the /cart page
        return redirect("/cart")

    # Retrieve the user's information
    user = request.user

    # Assuming UserProfile has a one-to-one relationship with User

    if request.user.is_authenticated:
        user = request.user

    return render(
        request,
        "checkout/checkout.html",
        {
            "checkout_data": {
                "subtotal": subtotal,
                "shipping": shipping,
                "tax": tax,
                "total": total,
                "user": user,
            }
        },
    )


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(
                    0
                )  # Session will expire when the user closes the browser
            return redirect(
                "/auth/account"
            )  # Redirect to your home page or any other desired page after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "authentications/login.html")


def guest_chekout_Create_account(request):
    error_message = None  # Initialize error_message variable

    if request.method == "POST":

        data = json.loads(request.body)
        username = data.get("email")
        password = data.get("password")
        first_name = ""
        last_name = ""
        email = data.get("email")
        bio = ""
        birthday = ""
        phone = ""

        billing_address = ""
        shipping_address = ""
        country = ""

        if not birthday:
            birthday = None

        try:
            # Create the CustomUser instance without extra fields
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            # Set the additional fields
            user.bio = bio
            user.birthday = birthday
            user.phone = phone
            user.billing_address = billing_address
            user.shipping_address = shipping_address
            user.country = country

            user.save()  # Save the user with additional fields

            login(request, user)

            return JsonResponse(
                {"success": True, "message": "Account Created successfully"}
            )

        except Exception as e:
            print(str(e))
            error_message = f"There was an error with your registration: {str(e)}"
            return JsonResponse({"success": False, "message": error_message})

    else:
        error_message = "Invalid request method"
        messages.success(request, error_message)
        return JsonResponse({"success": False, "message": error_message})


def update_billing(request):
    if request.method == "POST":

        user = request.user
        try:

            data = json.loads(request.body)
            # Retrieve updated data from the request
            user.billing_first_name = data.get("billing_first_name")
            user.billing_last_name = data.get("billing_last_name")
            user.billing_city = data.get("billing_city")
            user.billing_state = data.get("billing_state")
            user.billing_country = data.get("billing_country")
            user.billing_phone = data.get("billing_phone")
            user.billing_address_line1 = data.get("billing_address_line1")
            user.billing_address_line2 = data.get("billing_address_line2")

            # Save the updated user data
            user.save()

            billing_address = {
                "billing_first_name": data.get("billing_first_name"),
                "billing_last_name": data.get("billing_last_name"),
                "billing_city": data.get("billing_city"),
                "billing_state": data.get("billing_state"),
                "billing_country": data.get("billing_country"),
                "billing_phone": data.get("billing_phone"),
                "billing_address_line1": data.get("billing_address_line1"),
                "billing_address_line2": data.get("billing_address_line2"),
            }
            request.session["billing"] = billing_address

            return JsonResponse(
                {"success": True, "message": "Account information updated successfully"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


def update_shipping(request):

    if request.method == "POST":

        user = request.user
        try:

            data = json.loads(request.body)
            # Retrieve updated data from the request

            user.billing_first_name = data.get("billing_first_name")
            user.billing_last_name = data.get("billing_last_name")
            user.billing_city = data.get("billing_city")
            user.billing_state = data.get("billing_state")
            user.billing_country = data.get("billing_country")
            user.billing_phone = data.get("billing_phone")
            user.billing_address_line1 = data.get("billing_address_line1")
            user.billing_address_line2 = data.get("billing_address_line2")

            user.shipping_first_name = data.get("shipping_first_name")
            user.shipping_last_name = data.get("shipping_last_name")
            user.shipping_city = data.get("shipping_city")
            user.shipping_state = data.get("shipping_state")
            user.shipping_country = data.get("shipping_country")
            user.shipping_phone = data.get("shipping_phone")
            user.shipping_address_line1 = data.get("shipping_address_line1")
            user.shipping_address_line2 = data.get("shipping_address_line2")

            # Save the updated user data
            user.save()

            billing_address = {
                "billing_first_name": data.get("billing_first_name"),
                "billing_last_name": data.get("billing_last_name"),
                "billing_city": data.get("billing_city"),
                "billing_state": data.get("billing_state"),
                "billing_country": data.get("billing_country"),
                "billing_phone": data.get("billing_phone"),
                "billing_address_line1": data.get("billing_address_line1"),
                "billing_address_line2": data.get("billing_address_line2"),
            }
            shipping_address = {
                "shipping_first_name": data.get("shipping_first_name"),
                "shipping_last_name": data.get("shipping_last_name"),
                "shipping_city": data.get("shipping_city"),
                "shipping_state": data.get("shipping_state"),
                "shipping_country": data.get("shipping_country"),
                "shipping_phone": data.get("shipping_phone"),
                "shipping_address_line1": data.get("shipping_address_line1"),
                "shipping_address_line2": data.get("shipping_address_line2"),
            }

            request.session["billing"] = billing_address
            request.session["shipping"] = shipping_address

            return JsonResponse(
                {"success": True, "message": "Account information updated successfully"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


def update_billing_shipping(request):
    if request.method == "POST":

        user = request.user
        try:

            data = json.loads(request.body)

            # Retrieve updated data from the request
            user.billing_first_name = data.get("billing_first_name")
            user.billing_last_name = data.get("billing_last_name")
            user.billing_city = data.get("billing_city")
            user.billing_state = data.get("billing_state")
            user.billing_country = data.get("billing_country")
            user.billing_phone = data.get("billing_phone")
            user.billing_address_line1 = data.get("billing_address_line1")
            user.billing_address_line2 = data.get("billing_address_line2")

            user.shipping_first_name = data.get("shipping_first_name")
            user.shipping_last_name = data.get("shipping_last_name")
            user.shipping_city = data.get("shipping_city")
            user.shipping_state = data.get("shipping_state")
            user.shipping_country = data.get("shipping_country")
            user.shipping_phone = data.get("shipping_phone")
            user.shipping_address_line1 = data.get("shipping_address_line1")
            user.shipping_address_line2 = data.get("shipping_address_line2")

            # Save the updated user data
            user.save()
            return JsonResponse(
                {"success": True, "message": "Account information updated successfully"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


def returning_customer(request):

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            # Retrieve updated data from the request
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse(
                    {"success": True, "message": "Logged in successfully"}
                )
            else:
                return JsonResponse({"success": False, "message": "Logged In Failed"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})


def get_billing_shipping(request):

    if request.method == "POST":

        user = request.user

        data = json.loads(request.body)

        billing_address = {
            "billing_first_name": data.get("billing_first_name"),
            "billing_last_name": data.get("billing_last_name"),
            "billing_city": data.get("billing_city"),
            "billing_state": data.get("billing_state"),
            "billing_country": data.get("billing_country"),
            "billing_phone": data.get("billing_phone"),
            "billing_address_line1": data.get("billing_address_line1"),
            "billing_address_line2": data.get("billing_address_line2"),
        }
        shipping_address = {
            "shipping_first_name": data.get("shipping_first_name"),
            "shipping_last_name": data.get("shipping_last_name"),
            "shipping_city": data.get("shipping_city"),
            "shipping_state": data.get("shipping_state"),
            "shipping_country": data.get("shipping_country"),
            "shipping_phone": data.get("shipping_phone"),
            "shipping_address_line1": data.get("shipping_address_line1"),
            "shipping_address_line2": data.get("shipping_address_line2"),
        }

        request.session["billing"] = billing_address
        request.session["shipping"] = shipping_address

    shipping = request.session.get("shipping", {})
    cart = request.session.get("cart", {})

    cart_data = cart_calculations(shipping, cart)

    total = cart_data["total"]
    subtotal = cart_data["subtotal"]
    tax = cart_data["tax"]
    shipping = cart_data["shipping"]
    discount = cart_data["discount"]
    uuid_number = uuid.uuid4()
    order_num = uuid.uuid4()
    order_number = str(order_num)
    invoice_number = str(uuid_number)

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    try:
        bill = request.session["billing"]
    except:
        bill = {}
    try:
        ship = request.session["shipping"]
    except:
        ship = {}

    # add shiping address in paypal format

    try:
        shipping_data = {
            "recipient_name": ship["shipping_first_name"],
            "line1": ship["shipping_address_line1"],
            "line2": ship["shipping_address_line2"],
            "city": ship["shipping_city"],
            "phone": ship["shipping_phone"],
            "state": ship["shipping_state"],
            "country_code": "US",
            "country_code": "US",
            "postal_code": "73001",
        }
    except:
        shipping_data = {}

    amount = {
        "total": total,
        "currency": "USD",
        "details": {
            "subtotal": subtotal,
            "tax": tax,
            "shipping": shipping,
            "handling_fee": "0.00",
            "insurance": "0.00",
            "shipping_discount": discount,
        },
    }

    items = [
        {
            "name": cart[item]["title"],
            "sku": cart[item]["title"],
            "price": cart[item]["price"],
            "currency": "USD",
            "quantity": cart[item]["quantity"],
        }
        for item in cart
    ]

    # for paypal
    payment = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [
            {
                "amount": amount,
                "description": "The payment transaction description.",
                "invoice_number": invoice_number,
                "order_number": invoice_number,
                "payment_options": {"allowed_payment_method": "INSTANT_FUNDING_SOURCE"},
                "item_list": {"items": items, "shipping_address": shipping_data},
            }
        ],
        "note_to_payer": "Contact us for any questions on your order.",
        "redirect_urls": {
            "return_url": BASE_URL + "/paypal/execute_payment/",
            "cancel_url": BASE_URL + "/paypal/cancel_payment/",
        },
    }

    print(payment)

    # for thank you page
    order = {
        "invoice_number": invoice_number,
        "order_number": invoice_number,
        "order_date": formatted_datetime,
        "amount": {
            "total": total,
            "currency": "USD",
            "details": {
                "subtotal": subtotal,
                "tax": tax,
                "shipping": shipping,
                "handling_fee": "0.00",
                "insurance": "0.00",
                "shipping_discount": discount,
            },
        },
        "cart": request.session["cart"],
        "billing_address": bill,
        "shipping_address": ship,
        "payment_mode": "paypal",
    }
    request.session["payment"] = payment
    request.session["order"] = order

    return JsonResponse(
        {"success": True, "message": "Update Billing Shipping in Session"}
    )
