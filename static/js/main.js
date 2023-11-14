/**********************START INDEX JS CODE ************************* */

$(document).ready(function () {
  /*** START INDEX CAROUSEL JS CODE ***/
  $(".owl-carousel").owlCarousel({
    items: 1, // Number of items to display in a row
    loop: false, // Infinite loop
    margin: 10, // Space between items
    responsiveClass: true,
    responsive: {
      0: {
        items: 1,
        nav: true,
      },
      600: {
        items: 3,
        nav: true,
      },
      1000: {
        items: 5,
        nav: true,
        loop: true,
      }
    }
  });
  /*** END INDEX CAROUSEL JS CODE ***/
});

/**********************END INDEX JS CODE ************************* */




/**********************START CATEGORY JS CODE ************************* */

/*** START SORT PRODUCTS JS CODE ***/
function sortProducts() {
  const sortSelect = document.getElementById("sort");
  const selectedOption = sortSelect.value;
  // Get the current URL
  const currentUrl = window.location.href;
  const url = new URL(currentUrl);
  // Set the "sorting" parameter in the URL to the selected option
  url.searchParams.set('sorting', selectedOption);
  // Redirect to the updated URL with the sorting parameter
  window.location.href = url.toString();
}
/*** END SORT PRODUCTS JS CODE ***/

$(document).ready(function () {
  /*** START AVAILABILITY FILTERS CODE ***/
  $('input[name="availabilityFilter"]').on('change', function () {
    // Get the selected value
    var selectedValue = $(this).val();
    // Construct the URL with the selected availability filter
    var currentUrl = window.location.href;
    var url = new URL(currentUrl);
    url.searchParams.set('availabilityFilter', selectedValue);
    // Redirect to the filtered URL
    window.location.href = url.toString();
  });
  /*** START AVAILABILITY FILTERS CODE ***/


  /*** START SMART SEARCH CODE ***/
  const inputElement = document.getElementById('searchInput'); // Replace 'yourInputId' with the actual ID of your input field
  let typingTimer;
  const typingDelay = 2000; // Adjust the delay as needed (in milliseconds)
  // Reference to the search input field
  const searchInput = $('#searchInput');
  // Function to make the AJAX request and update the product list
  function updateProductList() {

    const searchQuery = searchInput.val();  // Get the search query
    const categorySlug = window.location.href;  // Replace with your category slug
    const url = new URL(window.location.href);
    url.searchParams.set('search_query', searchQuery);
    setTimeout(() => {
      // Replace the URL without triggering a page refresh
      window.history.replaceState({}, document.title, url.href);
      window.location.reload();
      if (searchQuery.trim() == "") {
        url.searchParams.delete('search_query');
        window.history.replaceState({}, document.title, url.href);
        window.location.reload();
      }
    }, 0);

  }
  try {
    inputElement.addEventListener('input', function () {
      document.getElementById("catproducts").innerHTML = `<div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
          </div>`
      clearTimeout(typingTimer);
      // Attach the event listener to the search input
      typingTimer = setTimeout(updateProductList, typingDelay);
    });
  } catch (err) { }
  /*** END SMART SEARCH CODE ***/

});
/**********************END CATEGORY JS CODE ************************* */




/**********************START PRODUCT JS CODE ************************* */

$(document).ready(function () {
  $('.nav-pills a').click(function () {
    $(this).tab('show');
  });


});

/**********************END PRODUCT JS CODE ************************* */


/**********************START ACCOUNT PAGE JS CODE ************************* */


$(document).ready(function () {





  $("#account-update-form").submit(function (e) {
    e.preventDefault();

    // Format the date using moment.js to YYYY-MM-DD format
    var formattedBirthday = moment($("#birthday-input").val(), "MMM. D, YYYY").format("YYYY-MM-DD");

    // Set the formatted date back to the input field
    $("#birthday-input").val(formattedBirthday);

    // Serialize form data
    var formData = $(this).serialize();

    // Send a POST request to the update_account URL
    $.ajax({
      type: "POST",
      url: "/auth/update-account/",
      data: formData,
      success: function (data) {
        if (data.success) {
          // Show a success message
          alert(data.message);
        } else {
          // Show an error message
          alert("Error: " + data.message);
        }
      }
    });
  });

  // Add a click event handler to the "Save changes" button
  $("#save-changes-button").click(function () {
    $("#account-update-form").submit(); // Submit the form when the button is clicked
  });










});






/**********************END ACCOUNT PAGE JS CODE ************************* */
const changePassword = (csrfToken) => {

  let username = document.getElementById('username').value
  let currenntPassword = document.getElementById('current_password').value
  let newPassword = document.getElementById('new_password1').value
  let confirmNewPassword = document.getElementById('new_password2').value

  let data = {
    username: username,
    current_password: currenntPassword,
    new_password1: newPassword,
    new_password2: confirmNewPassword
  }


  $.ajax({
    type: "POST",
    url: "/auth/update-password/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {
        // Show a success message
        alert(data.message);
      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });



}

/**********************START CHECKOUT PAGE JS CODE ************************* */

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


  $('.nav-tabs').on('click', 'li', function () {
    $('.nav-tabs li.active').removeClass('active');
    $(this).addClass('active');
  });
});

function nextTab(elem) {
  $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
  $(elem).prev().find('a[data-toggle="tab"]').click();
}


/**********************END CHECKOUT PAGE JS CODE ************************* */

const guest_checkout = (csrfToken) => {

  let email = document.getElementById('guest-email').value
  let password = document.getElementById('guest-Password').value

  let data = {
    email: email,
    password: password,
  }


  $.ajax({
    type: "POST",
    url: "/checkout/guest-checkout/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {
        // Show a success message

        location.reload()

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}


const returning_customer = (csrfToken) => {

  let username = document.getElementById('returning-email').value
  let password = document.getElementById('returning-Password').value

  let data = {
    username: username,
    password: password,
  }


  $.ajax({
    type: "POST",
    url: "/checkout/returning-customer/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {
        // Show a success message

        location.reload()

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}




const update_billing = (csrfToken) => {

  let billing_first_name = document.getElementById('billing_first_name').value
  let billing_last_name = document.getElementById('billing_last_name').value
  let billing_phone = document.getElementById('billing_phone').value
  let billing_address_line1 = document.getElementById('billing_address_line1').value
  let billing_address_line2 = document.getElementById('billing_address_line2').value
  let billing_city = document.getElementById('billing_city').value
  let billing_state = document.getElementById('billing_state').value
  let billing_country = document.getElementById('billing_country').value




  let data = {
    billing_first_name: billing_first_name,
    billing_last_name: billing_last_name,
    billing_phone: billing_phone,
    billing_address_line1: billing_address_line1,
    billing_address_line2: billing_address_line2,
    billing_city: billing_city,
    billing_state: billing_state,
    billing_country: billing_country,
  }

  $.ajax({
    type: "POST",
    url: "/checkout/update-billing/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}



const update_shipping = (csrfToken) => {

  let billing_first_name = document.getElementById('billing_first_name').value
  let billing_last_name = document.getElementById('billing_last_name').value
  let billing_phone = document.getElementById('billing_phone').value
  let billing_address_line1 = document.getElementById('billing_address_line1').value
  let billing_address_line2 = document.getElementById('billing_address_line2').value
  let billing_city = document.getElementById('billing_city').value
  let billing_state = document.getElementById('billing_state').value
  let billing_country = document.getElementById('billing_country').value

  let shipping_first_name = document.getElementById('shipping_first_name').value
  let shipping_last_name = document.getElementById('shipping_last_name').value
  let shipping_phone = document.getElementById('shipping_phone').value
  let shipping_address_line1 = document.getElementById('shipping_address_line1').value
  let shipping_address_line2 = document.getElementById('shipping_address_line2').value
  let shipping_city = document.getElementById('shipping_city').value
  let shipping_state = document.getElementById('shipping_state').value
  let shipping_country = document.getElementById('shipping_country').value




  let data = {

    billing_first_name: billing_first_name,
    billing_last_name: billing_last_name,
    billing_phone: billing_phone,
    billing_address_line1: billing_address_line1,
    billing_address_line2: billing_address_line2,
    billing_city: billing_city,
    billing_state: billing_state,
    billing_country: billing_country,



    shipping_first_name: shipping_first_name,
    shipping_last_name: shipping_last_name,
    shipping_phone: shipping_phone,
    shipping_address_line1: shipping_address_line1,
    shipping_address_line2: shipping_address_line2,
    shipping_city: shipping_city,
    shipping_state: shipping_state,
    shipping_country: shipping_country,
  }

  $.ajax({
    type: "POST",
    url: "/checkout/update-shipping/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}



const update_billing_shipping = (csrfToken) => {

  let billing_first_name = document.getElementById('billing_first_name').value
  let billing_last_name = document.getElementById('billing_last_name').value
  let billing_phone = document.getElementById('billing_phone').value
  let billing_address_line1 = document.getElementById('billing_address_line1').value
  let billing_address_line2 = document.getElementById('billing_address_line2').value
  let billing_city = document.getElementById('billing_city').value
  let billing_state = document.getElementById('billing_state').value
  let billing_country = document.getElementById('billing_country').value

  let shipping_first_name = document.getElementById('shipping_first_name').value
  let shipping_last_name = document.getElementById('shipping_last_name').value
  let shipping_phone = document.getElementById('shipping_phone').value
  let shipping_address_line1 = document.getElementById('shipping_address_line1').value
  let shipping_address_line2 = document.getElementById('shipping_address_line2').value
  let shipping_city = document.getElementById('shipping_city').value
  let shipping_state = document.getElementById('shipping_state').value
  let shipping_country = document.getElementById('shipping_country').value


  let data = {
    billing_first_name: billing_first_name,
    billing_last_name: billing_last_name,
    billing_phone: billing_phone,
    billing_address_line1: billing_address_line1,
    billing_address_line2: billing_address_line2,
    billing_city: billing_city,
    billing_state: billing_state,
    billing_country: billing_country,

    shipping_first_name: shipping_first_name,
    shipping_last_name: shipping_last_name,
    shipping_phone: shipping_phone,
    shipping_address_line1: shipping_address_line1,
    shipping_address_line2: shipping_address_line2,
    shipping_city: shipping_city,
    shipping_state: shipping_state,
    shipping_country: shipping_country,
  }

  $.ajax({
    type: "POST",
    url: "/checkout/update-billing/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}


const get_Billing_shipping = (csrfToken) => {

  let billing_first_name = document.getElementById('billing_first_name').value
  let billing_last_name = document.getElementById('billing_last_name').value
  let billing_phone = document.getElementById('billing_phone').value
  let billing_address_line1 = document.getElementById('billing_address_line1').value
  let billing_address_line2 = document.getElementById('billing_address_line2').value
  let billing_city = document.getElementById('billing_city').value
  let billing_state = document.getElementById('billing_state').value
  let billing_country = document.getElementById('billing_country').value

  let shipping_first_name = document.getElementById('shipping_first_name').value
  let shipping_last_name = document.getElementById('shipping_last_name').value
  let shipping_phone = document.getElementById('shipping_phone').value
  let shipping_address_line1 = document.getElementById('shipping_address_line1').value
  let shipping_address_line2 = document.getElementById('shipping_address_line2').value
  let shipping_city = document.getElementById('shipping_city').value
  let shipping_state = document.getElementById('shipping_state').value
  let shipping_country = document.getElementById('shipping_country').value



  let data = {
    billing_first_name: billing_first_name,
    billing_last_name: billing_last_name,
    billing_phone: billing_phone,
    billing_address_line1: billing_address_line1,
    billing_address_line2: billing_address_line2,
    billing_city: billing_city,
    billing_state: billing_state,
    billing_country: billing_country,

    shipping_first_name: shipping_first_name,
    shipping_last_name: shipping_last_name,
    shipping_phone: shipping_phone,
    shipping_address_line1: shipping_address_line1,
    shipping_address_line2: shipping_address_line2,
    shipping_city: shipping_city,
    shipping_state: shipping_state,
    shipping_country: shipping_country,
  }

  $.ajax({
    type: "POST",
    url: "/checkout/get_billing_shipping/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {

      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}

const paypalPayment = (csrfToken) => {
  let billing_first_name = document.getElementById('billing_first_name').value
  let billing_last_name = document.getElementById('billing_last_name').value
  let billing_phone = document.getElementById('billing_phone').value
  let billing_address_line1 = document.getElementById('billing_address_line1').value
  let billing_address_line2 = document.getElementById('billing_address_line2').value
  let billing_city = document.getElementById('billing_city').value
  let billing_state = document.getElementById('billing_state').value
  let billing_country = document.getElementById('billing_country').value

  let shipping_first_name = document.getElementById('shipping_first_name').value
  let shipping_last_name = document.getElementById('shipping_last_name').value
  let shipping_phone = document.getElementById('shipping_phone').value
  let shipping_address_line1 = document.getElementById('shipping_address_line1').value
  let shipping_address_line2 = document.getElementById('shipping_address_line2').value
  let shipping_city = document.getElementById('shipping_city').value
  let shipping_state = document.getElementById('shipping_state').value
  let shipping_country = document.getElementById('shipping_country').value




  let data = {

    billing_first_name: billing_first_name,
    billing_last_name: billing_last_name,
    billing_phone: billing_phone,
    billing_address_line1: billing_address_line1,
    billing_address_line2: billing_address_line2,
    billing_city: billing_city,
    billing_state: billing_state,
    billing_country: billing_country,



    shipping_first_name: shipping_first_name,
    shipping_last_name: shipping_last_name,
    shipping_phone: shipping_phone,
    shipping_address_line1: shipping_address_line1,
    shipping_address_line2: shipping_address_line2,
    shipping_city: shipping_city,
    shipping_state: shipping_state,
    shipping_country: shipping_country,
  }

  $.ajax({
    type: "POST",
    url: "/checkout/get-billing-shipping/",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function (data) {
      if (data.success) {

        window.location.href = "/paypal/checkout/"


      } else {
        // Show an error message
        alert("Error: " + data.message);
      }
    }
  });


}

const same_billing_shipping = () => {

  document.getElementById('shipping_first_name').value = document.getElementById('billing_first_name').value
  document.getElementById('shipping_last_name').value = document.getElementById('billing_last_name').value
  document.getElementById('shipping_phone').value = document.getElementById('billing_phone').value
  document.getElementById('shipping_address_line1').value = document.getElementById('billing_address_line1').value
  document.getElementById('shipping_address_line2').value = document.getElementById('billing_address_line2').value
  document.getElementById('shipping_city').value = document.getElementById('billing_city').value
  document.getElementById('shipping_state').value = document.getElementById('billing_state').value
  document.getElementById('shipping_country').value = document.getElementById('billing_country').value

}
