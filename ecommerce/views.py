from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import (
    Categories,
    Products,
    ProductAttribute,
    VariationAttribute,
    Brands,
    MainBanner,
    MiniBanner,
)

# Create your views here.
from django.views.generic import ListView
from django.core.paginator import Paginator
from urllib.parse import unquote  # Import the unquote function
from django.db.models import Q, Subquery, OuterRef
from django.template.loader import render_to_string
from django.db.models import Count
from django.db.models import OuterRef, Subquery
from django.http import QueryDict
from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings  # Import settings to access STATIC_URL

recent_products = {}


def index(request):

    products = Products.objects.filter(featured=True)[:10]
    main_banners = MainBanner.objects.filter(is_active=True)

    # Retrieve MiniBanner instances based on their content_id
    try:
        mini_banner_1 = MiniBanner.objects.get(
            content_id="adec1f4d-684d-4bde-90ec-ff7183a4dca7"
        )

    except ObjectDoesNotExist:
        # Handle the case where no matching MiniBanner is found
        mini_banner_1 = None

    try:
        mini_banner_2 = MiniBanner.objects.get(
            content_id="1fbbb48e-3bd2-4a22-ada5-071f4bfc161d"
        )
    except ObjectDoesNotExist:
        # Handle the case where no matching MiniBanner is found
        mini_banner_2 = None

    try:
        mini_banner_3 = MiniBanner.objects.get(
            content_id="9895d066-0bbb-44f1-ba07-3cf2eccaa606"
        )

    except ObjectDoesNotExist:
        # Handle the case where no matching MiniBanner is found
        mini_banner_3 = None

    try:
        mini_banner_4 = MiniBanner.objects.get(
            content_id="22313686-fe47-4a34-bcdb-f538bef884a4"
        )

    except ObjectDoesNotExist:
        # Handle the case where no matching MiniBanner is found
        mini_banner_4 = None

    try:
        mini_banner_5 = MiniBanner.objects.get(
            content_id="d0fea918-7cbb-44a3-94be-8baaefc67db4"
        )

    except ObjectDoesNotExist:
        # Handle the case where no matching MiniBanner is found
        mini_banner_5 = None

    return render(
        request,
        "ecommerce/index.html",
        {
            "featuredProducts": products,
            "mainBanners": main_banners,
            "miniBanner1": mini_banner_1,
            "miniBanner2": mini_banner_2,
            "miniBanner3": mini_banner_3,
            "miniBanner4": mini_banner_4,
            "miniBanner5": mini_banner_5,
        },
    )


def get_breadcrumbs(category):
    breadcrumbs = []
    while category:
        breadcrumbs.insert(0, (category.name, category.slug))
        category = category.parent
    return breadcrumbs


def category_page(request, slug):

    # Get the search query from the request's GET parameters
    search_query = request.GET.get("search_query")

    try:
        category = get_object_or_404(Categories, slug=slug)

    except Categories.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=404)
    # Create a queryset for products in the current category
    products = Products.objects.filter(category=category)

    # Get the availability filter from the request's GET parameters
    availability_filter = request.GET.get("availabilityFilter")

    # Get additional filters from the request's GET parameters
    filter_parameters = request.GET

    # Create an empty Q object to build the dynamic filter
    dynamic_filter = Q()

    # Create a set to store unique filter combinations
    unique_filters = set()

    # Get the sorting parameter from the request's GET parameters
    sort_option = request.GET.get("sorting")

    # Create a variable to store the brand filter as a list
    brand_filter = []

    # Iterate through the filter parameters (excluding availabilityFilter)
    filter_parameters = request.GET.copy()  # Create a copy of GET parameters
    filter_parameters.pop("availabilityFilter", None)  # Remove availabilityFilter
    filter_parameters.pop("search_query", None)  # Remove search_query
    filter_parameters.pop("page", None)  # Remove availabilityFilter

    # Iterate through the filter parameters
    for attribute_name, attribute_values in filter_parameters.items():

        print("attribute_name", attribute_name)

        if attribute_name != "page" or attribute_name != "search_query":
            # Check if the parameter is "sorting"
            if attribute_name == "sorting":
                sort_option = attribute_values
            elif attribute_name == "brand":
                # Append multiple brand values to the list
                brand_filter.extend(attribute_values.split(","))
            else:
                attribute_values = attribute_values.split(
                    ","
                )  # Split values into a list

                # Create a sorted tuple of attribute name and values
                attribute_filter_tuple = tuple(
                    sorted([(attribute_name, value) for value in attribute_values])
                )

                # Check if this combination of filters is unique
                if attribute_filter_tuple not in unique_filters:
                    unique_filters.add(attribute_filter_tuple)

                    # Create an empty Q object for each filter
                    attribute_filter = Q()

                    # Iterate through the values of the current attribute
                    for value in attribute_values:
                        attribute_filter |= Q(
                            productattribute__attribute__name__iexact=attribute_name,
                            productattribute__value__value__iexact=value,
                        )

                    # Combine the attribute filter with the dynamic filter using the | operator
                    dynamic_filter |= attribute_filter

    # Apply the dynamic filter to the products queryset
    if dynamic_filter:
        products = products.filter(dynamic_filter)

    # Handle brand filtering
    if brand_filter:
        # Remove leading/trailing spaces
        brand_filter_values = [brand.strip() for brand in brand_filter]
        # Create a list to hold Q objects for each brand
        brand_filters = [Q(brand__name__iexact=brand) for brand in brand_filter_values]
        # Combine the Q objects using the | (OR) operator
        combined_brand_filter = Q()
        for brand_q in brand_filters:
            combined_brand_filter |= brand_q
        # Apply the combined brand filter to the products queryset
        products = products.filter(combined_brand_filter)

    # Filter products based on availability
    if availability_filter == "outofstock":
        products = products.filter(in_stock=False)
    elif availability_filter == "instock":
        products = products.filter(in_stock=True)

    # Apply sorting to the products queryset
    if sort_option == "priceLowHigh":
        products = products.order_by("price")
    elif sort_option == "priceHighLow":
        products = products.order_by("-price")

    elif sort_option == "nameAsc":
        products = products.order_by("title")

    elif sort_option == "nameDesc":
        products = products.order_by("-title")

    elif sort_option == "brands":
        products = products.order_by("brand")

    # Add distinct() to remove duplicate products
    products = products.distinct()

    if search_query and search_query != "":
        products = Products.objects.filter(Q(title__icontains=search_query))

    # Create a Paginator object with the products and specify the number of products per page.
    # Adjust the number of products per page as needed.
    paginator = Paginator(products, per_page=8)

    # Get the current page number from the request's GET parameters.
    page_number = request.GET.get("page")

    # Get the Page object for the current page number.
    page = paginator.get_page(page_number)

    # Fetch attribute data efficiently based on the current category's products
    product_ids_in_category = products.values_list("id", flat=True)

    product_attributes = ProductAttribute.objects.filter(
        product_id__in=product_ids_in_category
    ).select_related("attribute", "value")

    variation_attributes = VariationAttribute.objects.filter(
        variation__product_id__in=product_ids_in_category
    ).select_related("attribute", "value")

    attribute_hierarchy = {}

    # Iterate through product attributes
    for attribute in product_attributes:
        attr_name = attribute.attribute.name
        attr_value = attribute.value.value.lower()  # Convert to lowercase

        # Check if the value already exists in the set for this attribute (case-insensitive)
        if attr_value not in attribute_hierarchy.setdefault(attr_name, set()):
            attribute_hierarchy[attr_name].add(attr_value)

    # Iterate through variation attributes
    for attribute in variation_attributes:
        attr_name = attribute.attribute.name
        attr_value = attribute.value.value.lower()  # Convert to lowercase

        # Check if the value already exists in the set for this attribute (case-insensitive)
        if attr_value not in attribute_hierarchy.setdefault(attr_name, set()):
            attribute_hierarchy[attr_name].add(attr_value)

    # Fetch breadcrumbs
    breadcrumbs = get_breadcrumbs(category)

    # Pass the category name to the template context

    # Fetch the list of brands that have products in the current category
    product_ids_in_category = products.values_list("id", flat=True)
    brands = Brands.objects.filter(products__id__in=product_ids_in_category).distinct()

    # store here jiiiii

    recent_products = page

    # Filter distinct child categories with associated products
    subcategories_to_display = category.subcategories.filter(
        products__isnull=False
    ).distinct()

    # If no child categories with products found, do not display the parent category
    if not subcategories_to_display.exists():
        subcategories_to_display = None

    # Get the selected filters from the request's GET parameters
    selected_filters = request.GET

    request.session["shop"] = "/category/" + slug

    # Store the current page number in the session
    request.session["current_page"] = page_number

    return render(
        request,
        "ecommerce/category.html",
        {
            "category": category,
            "products": page,
            "attribute_hierarchy": attribute_hierarchy,
            "breadcrumbs": breadcrumbs,
            "brands": brands,
            "subcategories_to_display": subcategories_to_display,
            "selected_filters": selected_filters,
        },
    )


def filter_data(request, slug):
    # Get all key-value pairs sent in the GET request
    filter_data = dict(request.GET)

    # Loop through the dictionary to access all keys and values
    for key, value in filter_data.items():
        # Remove square brackets from the key
        key = key.rstrip("[]")
        # Process each key-value pair as needed
        print(f"Key: {key}, Value: {value}")

    return JsonResponse({"data": "hello"})


def product_page(request, slug):
    try:
        product = get_object_or_404(Products, id=slug)
    except:
        return JsonResponse({"error": "Product not found"}, status=404)

    def get_breadcrumbs(category_slug):
        category = get_object_or_404(Categories, slug=category_slug)
        breadcrumbs = []
        while category:
            breadcrumbs.insert(0, (category.name, category.slug))
            category = category.parent
        return breadcrumbs

    # Retrieve the category associated with the product
    category = product.category

    # Generate breadcrumbs for the category and product pages
    category_breadcrumbs = get_breadcrumbs(category.slug)
    # Breadcrumb for the product itself
    product_breadcrumbs = [(product.title, "")]

    # Combine the category and product breadcrumbs
    breadcrumbs = category_breadcrumbs + product_breadcrumbs

    # Get products that users may also buy based on the category of the current product
    related_products = (
        Products.objects.filter(category=category)
        .exclude(id=product.id)
        .order_by("?")[:4]
    )

    cart = request.session.get("cart", {})

    total_quantity = 0
    try:
        total_quantity = sum(item["quantity"] for item in cart.values())
    except:
        pass

    # Fetch product attributes for the current product
    product_attributes = ProductAttribute.objects.filter(product=product)

    # Create a dictionary to store attribute values for rendering in the template
    attribute_values = {}

    for attribute in product_attributes:
        attribute_name = attribute.attribute.name
        if attribute_name not in attribute_values:
            attribute_values[attribute_name] = set()

        # Get unique attribute values for each attribute name
        attribute_values[attribute_name].add(attribute.value.value)

    context = {
        "product": product,
        "breadcrumbs": breadcrumbs,
        "related_products": related_products,
        "attribute_values": attribute_values,
    }

    return render(request, "ecommerce/product.html", context)
