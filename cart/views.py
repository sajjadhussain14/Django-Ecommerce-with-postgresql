from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    JsonResponse,
)
from ecommerce.models import Products
import json
from django.db.models import Q
from django.core import serializers
from random import sample
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from authentications.models import UserProfile  # Import the UserProfile model
from .models import Wishlist, WishlistItem

# Create your views here.


def add_to_cart(request):

    cart = request.session.get("cart", {})
    res = {"status": 400, "msg": "Failed to Add", "cartTotal": 0}
    related_products = {}
    if request.method == "POST":

        # Get the JSON data from the request body
        data = json.loads(request.body.decode("utf-8"))

        # Now you can access product_id and attributes
        product_id = data.get("product_id")
        attributes = data.get("attributes")

        try:
            attributes = eval(attributes)
        except:
            pass

        product = Products.objects.get(id=product_id)

        # Retrieve the correct image for the product
        product_image = product.images.first() if product.images.exists() else None
        image_url = product_image.image.url if product_image else "default.jpg"

        # Define the number of random related products you want (e.g., 8)
        num_related_products = 8

        # Get related products based on the category of the target product
        related_products = Products.objects.filter(category=product.category).exclude(
            id=product_id
        )

        # Shuffle the related products randomly and select the desired number
        related_products = sample(
            list(related_products), min(num_related_products, related_products.count())
        )

        # Serialize the first 4 related products to JSON
        related_products_data = serializers.serialize("json", related_products[:4])

        cart = request.session.get("cart", {})
        if product_id in cart:
            cart[product_id]["quantity"] += 1
            cart[product_id]["price_total"] = (
                cart[product_id]["price"] * cart[product_id]["quantity"]
            )
        else:
            cart[product_id] = {
                "product_id": product_id,
                "quantity": 1,
                "attributes": attributes,
                "title": product.title,
                "slug": product.slug,
                "price": float(product.price),
                "image_url": image_url,
                "price_total": float(product.price) * 1,
            }

        request.session["cart"] = cart

        cart = request.session.get("cart", {})
        res["status"] = 200
        res["msg"] = "Added to Cart"
    else:
        res["status"] = 400
        res["msg"] = "Failed to Add"

    total_quantity = sum(item["quantity"] for item in cart.values())
    res["cartTotal"] = total_quantity

    cart = request.session.get("cart", {})
    total_quantity = sum(item["quantity"] for item in cart.values())

    cart_total_amount = 0

    # Iterate through the items in the cart and calculate the total amount
    for item in cart.values():

        # Calculate the subtotal for each item (quantity * price)
        subtotal = item["quantity"] * item["price"]
        # Add the subtotal to the total amount
        cart_total_amount += subtotal
        cart_total_amount = round(cart_total_amount, 2)

    try:
        last_element = list(cart.values())[-1]
    except:
        last_element = {}

    return JsonResponse(
        {
            "product": last_element,
            "total_qty": total_quantity,
            "cart_total_amount": cart_total_amount,
            "related_products": related_products_data,
        }
    )


def cart_calculations(shipping, cart):

    tax_amount = 0
    discount_amount = 0
    shipping_amount = 0
    subtotal = 0
    total = 0
    total_cart_quantity = 0
    ship = 0
    # get shipping
    try:
        ship = shipping["shipping_amount"]
    except:
        ship = 0
    if ship > 0:
        shipping_amount = ship
    else:
        shipping_amount = 0

    # get cart total quantity of items
    quantity = sum(item["quantity"] for item in cart.values())
    if quantity > 0:
        total_cart_quantity = quantity
    else:
        total_cart_quantity = 0

    # get cart subtotal
    for item in cart.values():
        amt = item["quantity"] * item["price"]
        subtotal += amt
        subtotal = round(subtotal, 2)

    # get total amount
    if cart:
        total = (subtotal + shipping_amount + tax_amount) - discount_amount
        total = round(total, 2)
    else:
        total = 0.00

    # get Fist element of cart
    first_element = {}
    try:
        first_element = list(cart.values())[0]
    except:
        first_element = {}

    cart_data = {
        "total_cart_quantity": total_cart_quantity,
        "subtotal": subtotal,
        "shipping": shipping_amount,
        "tax": tax_amount,
        "discount": discount_amount,
        "total": total,
        "first_element": first_element,
    }

    return cart_data


def view_cart(request):
    shipping = request.session.get("shipping", {})
    cart = request.session.get("cart", {})
    cart_data = {}
    cart_data = cart_calculations(shipping, cart)

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart,
            "total_items": cart_data["total_cart_quantity"],
            "cart_subtotal": cart_data["subtotal"],
            "shippingData": shipping,
            "grand_total": cart_data["total"],
            "first_element": cart_data["first_element"],
        },
    )


def clear_cart(request):
    if request.method == "POST":
        request.session["cart"] = {}
    return JsonResponse({})


def back_to_shopping(request):
    back_url = request.session.get("shop", {})
    if back_url and back_url != "":
        pass
    else:
        back_url = "/"

    return redirect(back_url)


def remove_cart_item(request):

    if request.method == "POST":
        cart = request.session.get("cart", {})
        product_id = request.POST.get("product_id")
        # Check if the product_id exists in the cart
        if product_id in cart:
            # Remove the item from the cart
            del cart[product_id]
            request.session["cart"] = cart  # Update the session with the modified cart

    # Redirect to a page or URL of your choice after removing the item
    return redirect("/cart")  # Adjust the URL as needed


def update_item_quantity(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        new_quantity = int(request.POST.get("new_quantity"))

        if new_quantity < 1:
            pass
        else:
            cart = request.session.get("cart", {})
            if product_id in cart:
                cart[product_id]["quantity"] = new_quantity
                cart[product_id]["price_total"] = round(
                    cart[product_id]["price"] * cart[product_id]["quantity"], 2
                )
                request.session["cart"] = cart
            # You can add a success message or any other response logic here
    return JsonResponse({})


def update_shipping_method(request):
    if request.method == "POST":
        shipping = request.session.get("shipping", {})
        shipping_method = request.POST.get("shipping_method")
        shipping_amount = int(request.POST.get("shipping_amount"))

        request.session["shipping"] = {
            "shipping_method": shipping_method,
            "shipping_amount": shipping_amount,
        }
        # You can add a success message or any other response logic here
    return JsonResponse({})


def add_to_wishlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            product_id = data.get("product_id")
            attributes = data.get("attributes")

            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                print("Product not found")
                return JsonResponse({"code": 400, "message": "Product not found"})

            try:
                user = request.user
            except Exception as e:
                print("Error is User related: " + str(e))

            # Retrieve or create the user's wishlist
            wishlist, created = Wishlist.objects.get_or_create(
                user=user, name="Default Wishlist"
            )

            # Check if the product is already in the wishlist
            try:
                wishlist_item = WishlistItem.objects.get(
                    wishlist=wishlist, product=product
                )
                wishlist_item.quantity += 1
                wishlist_item.save()
                print("Product is already in your wishlist.")

            except WishlistItem.DoesNotExist:
                # Product is not in the wishlist, add it
                wishlist_item = WishlistItem.objects.create(
                    wishlist=wishlist,
                    product=product,
                    quantity=1,
                    attributes=attributes,
                )
                print("Added product in wishlist")

            return JsonResponse({"code": 200, "message": "Added Product to Wishlist"})

        else:
            messages.error(request, "Invalid request method.")
            return JsonResponse({"code": 400, "message": "Invalid request method"})
    else:
        messages.error(request, "You must be logged in to add to your wishlist.")
        return JsonResponse(
            {"code": 400, "message": "You must be logged in to add to your wishlist"}
        )


def remove_from_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        user = request.user  # Assuming you're using authentication

        # Check if the user is authenticated
        if user.is_authenticated:
            # Get the wishlist for the current user
            wishlist = get_object_or_404(Wishlist, user=user)

            try:
                # Attempt to remove the product with the given ID from the wishlist
                product_id = int(product_id)  # Ensure it's an integer
                product_to_remove = wishlist.products.get(id=product_id)
                wishlist.products.remove(product_to_remove)
                wishlist.save()

                return JsonResponse(
                    {"message": "Item removed from wishlist"}, status=200
                )
            except Products.DoesNotExist:
                return JsonResponse(
                    {"error": "Product not found in wishlist"}, status=400
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({"error": "User is not authenticated"}, status=401)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
