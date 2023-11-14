

function addToCart(product_id, csrfToken) {
    // Create an object to store selected attribute values
    let attrForm = '';
    let selectElements = '';
    try {
        attrForm = document.querySelector('form[name="attr-form"]');
        selectElements = attrForm.querySelectorAll('select');
    }
    catch (err) {

    }
    const selectedAttributes = {};
    let shouldExitFunction = false;
    // Loop through select elements and store selected values
    for (let i = 0; i < selectElements.length; i++) {
        const select = selectElements[i];
        const attributeName = select.name;
        const selectedValue = select.value;
    
        if (selectedValue == "") {
            alert("Please select the Attributes");
            shouldExitFunction = true;
            break;
            
        }
        if (selectedValue) {
            selectedAttributes[attributeName] = selectedValue;
        }
    }
    if (shouldExitFunction) {
        return; // Exit the current function if the flag is true
    }

    // Include the selected product ID in the request data
    const data = {
        product_id: product_id,
        attributes: selectedAttributes,
    };

    $.ajax({
        type: "POST",
        url: "/cart/add-to-cart", // Update the URL to match your Django endpoint
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            setTimeout(() => {

                document.getElementById("cart-count").innerHTML = response.total_qty
                document.getElementById("pop-title").innerHTML = response.product.title
                document.getElementById("pop-price").innerHTML = response.product.price
                document.getElementById("pop-quantity").innerHTML = response.product.quantity
                document.getElementById("pop-img").src = response.product.image_url
                document.getElementById("pop-cart_total_amount").innerHTML = response.cart_total_amount
                document.getElementById("pop-cart_total_qty").innerHTML = response.total_qty

                // Update the attributes list
                const attrGroup = document.getElementById("attr-group");
                attrGroup.innerHTML = ""; // Clear the previous content
                for (var key in response.product.attributes) {
                    if (response.product.attributes.hasOwnProperty(key)) {
                        var li = document.createElement("li");
                        li.className = "list-group-item d-flex justify-content-between align-items-center";
                        li.innerHTML = '<span>' + key + ':</span><span class="badge badge-primary badge-pill text-dark">' + response.product.attributes[key] + '</span>';
                        attrGroup.appendChild(li);
                    }
                }

                const myModal2 = new bootstrap.Modal(document.getElementById("modalCart"));
                myModal.show();

            }, 0);
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });
}

const clearcart = (csrfToken) => {
    data = {}
    $.ajax({
        type: "POST",
        url: "/cart/clear-cart",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: data,
        success: function (response) {
            window.location.href = "/cart";
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });
}

const removeItem = (product_id, csrfToken) => {
    data = {
        product_id: product_id,
    }

    $.ajax({
        type: "POST",
        url: "/cart/remove-cart-item",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: data,
        success: function (response) {
            window.location.href = "/cart";
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });
}

function decrementQuantity(id, product_id, csrfToken) {
    let new_quantity = 1
    const quantityInput = document.getElementById(id);
    if (quantityInput.value > 1) {
        quantityInput.value = parseInt(quantityInput.value) - 1;
        new_quantity = parseInt(quantityInput.value)
    }
    data = {
        product_id: product_id,
        new_quantity: parseInt(new_quantity),
    }
    $.ajax({
        type: "POST",
        url: "/cart/update-cart-item",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: data,
        success: function (response) {
            location.reload();
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });


}

function incrementQuantity(id, product_id, csrfToken) {
    let new_quantity = 1
    const quantityInput = document.getElementById(id);
    quantityInput.value = parseInt(quantityInput.value) + 1;
    new_quantity = parseInt(quantityInput.value)


    data = {
        product_id: product_id,
        new_quantity: parseInt(new_quantity)
    }
    $.ajax({
        type: "POST",
        url: "/cart/update-cart-item",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: data,
        success: function (response) {
            location.reload();
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });
}


function updateShippingMethodRequest(shp_method, shp_amount, csrfToken) {

    data = {
        shipping_method: shp_method,
        shipping_amount: shp_amount,
    }
    $.ajax({
        type: "POST",
        url: "/cart/update-shipping",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: data,
        success: function (response) {
            location.reload();
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });



    // checkout wizard

    // ------------step-wizard-------------
    $(document).ready(function () {
        $('.nav-tabs > li a[title]').tooltip();

        //Wizard
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

            var target = $(e.target);

            if (target.parent().hasClass('disabled')) {
                return false;
            }
        });

        $(".next-step").click(function (e) {

            var active = $('.wizard .nav-tabs li.active');
            active.next().removeClass('disabled');
            nextTab(active);

        });
        $(".prev-step").click(function (e) {

            var active = $('.wizard .nav-tabs li.active');
            prevTab(active);

        });
    });

    function nextTab(elem) {
        $(elem).next().find('a[data-toggle="tab"]').click();
    }
    function prevTab(elem) {
        $(elem).prev().find('a[data-toggle="tab"]').click();
    }

    $('.nav-tabs').on('click', 'li', function () {
        $('.nav-tabs li.active').removeClass('active');
        $(this).addClass('active');
    });

}



const addToWishList = (product_id, csrfToken) => {
    // Create an object to store selected attribute values
    const attrForm = document.querySelector('form[name="attr-form"]');
    const selectElements = attrForm.querySelectorAll('select');

    const selectedAttributes = {};

    let shouldExitFunction = false;
    // Loop through select elements and store selected values
    for (let i = 0; i < selectElements.length; i++) {
        const select = selectElements[i];
        const attributeName = select.name;
        const selectedValue = select.value;
    
        if (selectedValue == "") {
            alert("Please select the Attributes");
            shouldExitFunction = true;
            break;
            
        }
       
        if (selectedValue) {
            selectedAttributes[attributeName] = selectedValue;
        }
    }

    if (shouldExitFunction) {
        return; // Exit the current function if the flag is true
    }

    // Include the selected product ID in the request data
    const data = {
        product_id: product_id,
        attributes: selectedAttributes,
    };



    $.ajax({
        type: "POST",
        url: "/cart/add-to-wishlist",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            if (response.code == 400) {
                window.location.href = '/auth';
            }
            else if (response.code == 200) {
                window.location.href = '/auth/account';
            }


        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error("Error posting data:", status, error);
        },
    });
}



const toggleCartAndWishlist = (e, csrfToken) => {




    const product_id = e.getAttribute('data-product-id');


    let selectedAttributes = {}

    try {
        selectedAttributes = document.getElementById(product_id + "-wish-attr-values").value;

    }
    catch (err) { console.log(err) }


    const btnElement = e;

    // Disable the button to prevent multiple clicks
    btnElement.disabled = true;




    // Include the selected product ID in the request data
    const data = {
        product_id: product_id,
        attributes: selectedAttributes,
    };

    $.ajax({
        type: "POST",
        url: "/cart/add-to-cart", // Update the URL to match your Django endpoint
        headers: {
            "X-CSRFToken": csrfToken,
        },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            // Enable the button
            btnElement.disabled = false;

            removeFromWishlist(e, csrfToken);
            location.reload();

        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error('Error posting data:', status, error);
        },
    });
};

const removeFromWishlist = (e, csrfToken) => {
    const product_id = e.getAttribute('data-product-id');
    const data = {
        product_id: product_id,
    };

    $.ajax({
        type: 'POST',
        url: '/cart/remove-from-wishlist',  // URL to remove the product from the wishlist
        headers: {
            'X-CSRFToken': csrfToken,
        },
        data: data,
        success: function (response) {
            location.reload();
        },
        error: function (xhr, status, error) {
            // Handle errors here
            console.error('Error posting data:', status, error);
        },
    });
};



