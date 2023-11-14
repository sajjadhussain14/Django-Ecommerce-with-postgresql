from .models import Categories, Logo


def logo_img(request):

    try:
        logo = Logo.objects.all()

        if logo.exists():
            # If there are records in the queryset, use the first one
            logo_img = logo[0].image.url
        else:
            # If there are no records, set logo_img to the default image path
            logo_img = "/static/images/logo.png"  # Replace with the actual path to your default image
    except Logo.DoesNotExist:
        # Handle any exceptions that may occur
        logo_img = "/static/images/logo.png"  # Set logo_img to the default image path in case of an exception

    return {"logo_img": logo_img}


def categories(request):

    top_categories = Categories.objects.filter(parent__isnull=True)

    return {"categories": top_categories}


def cartGlobal(request):

    cart = request.session.get("cart", {})
    
    total_quantity =0
    try:
     total_quantity = sum(item["quantity"] for item in cart.values())
    except:
        pass 

    cart_total_amount = 0

    # Iterate through the items in the cart and calculate the total amount
    for item in cart.values():
        # Calculate the subtotal for each item (quantity * price)
        subtotal = item["quantity"] * item["price"]
        # Add the subtotal to the total amount
        cart_total_amount += subtotal

    # Get the first element from the cart_items dictionary
    cart_first_element = {}
    try:
        cart_first_element = list(cart.values())[0]
    except:
        pass

    return {
        "cart_total": total_quantity,
        "cart_first_element": cart_first_element,
        "cart_total_amount": cart_total_amount,
    }
