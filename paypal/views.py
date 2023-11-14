# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from paypalrestsdk import Payment, configure
from core.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_SECRET, BASE_URL
from paypalrestsdk.exceptions import MissingParam

# Configure PayPal SDK with your credentials
configure(
    {
        "mode": PAYPAL_MODE,  # Change to "live" for production
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_SECRET,
    }
)


def index(request):
    return render(request, "index.html")


def paypal_checkout(request):
    payload = request.session.get("payment", {})

    try:
        # Create a PayPal payment
        payment = Payment(payload)

        if payment.create():

            for link in payment.links:
                if link.rel == "approval_url":
                    # Redirect the user to PayPal for approval
                    return redirect(link.href)
        else:
            raise MissingParam("Failed to create PayPal payment", payment.error)
    except MissingParam as e:
        print("error ", e)
        return redirect("payment_error")


def execute_payment(request):

    payer_id = request.GET.get("PayerID")
    payment_id = request.GET.get("paymentId")

    data = {"payer_id": payer_id, "payment_id": payment_id}
    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):

        request.session["paypal_data"] = data

        # Payment is successful, perform post-payment actions
        # Update order status, send confirmation emails, etc.
        return redirect("/paypal/thank-you/")
    else:
        raise MissingParam("Failed to execute PayPal payment", payment.error)

    return render(request, "checkout/payment_error.html")


def cancel_payment(request):
    return render(request, "checkout/payment_cancel.html")


def thank_you(request):
    data = request.session.get("paypal_data", {})
    data["order"] = request.session["order"]
    request.session["cart"]={}
    return render(request, "checkout/thank-you.html", {"paypal_data": data})
