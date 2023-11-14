from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile  # Import the UserProfile model
from .models import CustomUser  # Import your custom user model
from cart.models import Wishlist, WishlistItem
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import json


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


def sign_up_page(request):
    error_message = None  # Initialize error_message variable

    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]  # Change to 'password1'
        password2 = request.POST["password2"]  # Change to 'password2'
        bio = ""  # New field
        birthday = ""  # New field
        phone = request.POST["phone"]  # New field

        country = ""

        if not birthday:
            birthday = None

        if password1 == password2:  # Check if passwords match

            try:
                # Create the CustomUser instance without extra fields
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )

                # Set the additional fields
                user.bio = bio
                user.birthday = birthday
                user.phone = phone
                user.billing_address = ""
                user.shipping_address = ""
                user.country = country

                user.save()  # Save the user with additional fields

                login(request, user)
                return redirect("/auth/account")

            except Exception as e:
                print(str(e))
                error_message = f"There was an error with your registration: {str(e)}"
        else:
            error_message = "Passwords do not match. Please try again."
    else:
        error_message = "Invalid request method"

    return render(
        request, "authentications/sign-up.html", {"error_message": error_message}
    )


def account_page(request):
    # Retrieve the user's information
    user = request.user

    # Assuming UserProfile has a one-to-one relationship with User
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.user.is_authenticated:
        user = request.user
        wishlist_items = WishlistItem.objects.filter(wishlist__user=user)

        # Ensure item.attributes is a dictionary
        for item in wishlist_items:
            if isinstance(item.attributes, str):
                item.attributes = json.loads(item.attributes)

    context = {
        "user": user,
        "user_profile": user_profile,
        "wishlist_items": wishlist_items,
    }
    return render(request, "authentications/account.html", context)


def logout_view(request):

    cart_data = request.session.get("cart", {})

    logout(request)  # Logs out the user

    request.session["cart"] = cart_data

    return redirect(
        "/auth"
    )  # Redirect to your login page (change 'login_page' to the actual name of your login view)


def update_account(request):
    if request.method == "POST":
        user = request.user
    try:
        # Retrieve updated data from the request
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.bio = request.POST.get("bio", user.bio)
        user.birthday = request.POST.get("birthday", user.birthday)
        user.country = request.POST.get("country", user.country)
        user.phone = request.POST.get("phone", user.phone)

        user.billing_first_name = request.POST.get(
            "billing_first_name", user.billing_first_name
        )
        user.billing_last_name = request.POST.get(
            "billing_last_name", user.billing_last_name
        )
        user.billing_address_line1 = request.POST.get(
            "billing_address_line1", user.billing_address_line1
        )
        user.billing_address_line2 = request.POST.get(
            "billing_address_line2", user.billing_address_line2
        )
        user.billing_city = request.POST.get("billing_city", user.billing_city)
        user.billing_state = request.POST.get("billing_state", user.billing_state)
        user.billing_country = request.POST.get("billing_country", user.billing_country)
        user.billing_phone = request.POST.get("billing_phone", user.billing_phone)

        user.shipping_first_name = request.POST.get(
            "shipping_first_name", user.shipping_first_name
        )
        user.shipping_last_name = request.POST.get(
            "shipping_last_name", user.shipping_last_name
        )
        user.shipping_address_line1 = request.POST.get(
            "shipping_address_line1", user.first_name
        )
        user.shipping_address_line2 = request.POST.get(
            "shipping_address_line2", user.last_name
        )
        user.shipping_city = request.POST.get("shipping_city", user.bio)
        user.shipping_state = request.POST.get("shipping_state", user.birthday)
        user.shipping_country = request.POST.get("shipping_country", user.country)
        user.shipping_phone = request.POST.get("shipping_phone", user.phone)

        # Save the updated user data
        user.save()
        return JsonResponse(
            {"success": True, "message": "Account information updated successfully"}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})


def update_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        current_password = data.get("current_password")
        new_password1 = data.get("new_password1")
        new_password2 = data.get("new_password2")

        user = authenticate(request, username=username, password=current_password)

        if user is not None:
            # User authentication successful, change the password
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Both New password and Confirm password do not match ",
                    }
                )

            # Log the user in with the new password if necessary
            login(request, user)

            return JsonResponse(
                {"success": True, "message": "Password updated successfully"}
            )
        else:
            # User authentication failed
            messages.error(request, "Current password is incorrect!")
            return JsonResponse({"success": False, "message": "Authentication failed"})
    else:
        # Handle non-POST requests (e.g., GET requests)
        return JsonResponse({"success": False, "message": "Invalid request method"})
