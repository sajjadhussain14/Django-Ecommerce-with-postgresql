let selectedFilters = {};
$(document).ready(function () {
  // Function to update the URL with selected filters and refresh the page
  function updateURLAndRefresh() {
    // Loop through all checked checkboxes
    $(".filter-checkbox:checked").each(function () {
      const paramName = $(this).data("filter");
      const paramValue = $(this).val();

      if (paramName && paramValue) {
        if (!(paramName in selectedFilters)) {
          selectedFilters[paramName] = [];
        }

        selectedFilters[paramName].push(paramValue);
      }
    });

    // Remove the 'category' filter from selectedFilters if present
    delete selectedFilters["category"];
    delete selectedFilters["search_query"];

    // Build the query string
    const queryStringParts = [];

    for (const paramName in selectedFilters) {
      const paramValue = selectedFilters[paramName].join(",");
      queryStringParts.push(paramName + "=" + paramValue);
    }
    let currentUrl = window.location.href;
    // Create a URL object
    const urlObject = new URL(currentUrl);
    // Get the search params from the URL
    const searchParams = urlObject.searchParams;
    // Get the sorting value
    const sortingValue = searchParams.get("sorting");
    const pageValue = searchParams.get("page");
    const search_queryValue = searchParams.get("search_query");
    // Get the current URL path without the query string
    let pathWithoutQuery = window.location.pathname;
    // Construct the updated URL
    let updatedURL =
      queryStringParts.length > 0
        ? pathWithoutQuery + "?" + queryStringParts.join("&")
        : pathWithoutQuery;

    let joiner = "";
    if (queryStringParts.length > 0) {
      joiner = "&";
    } else {
      joiner = "?";
    }

    if (sortingValue && sortingValue != "") {
      updatedURL = updatedURL + joiner + "sorting=" + sortingValue;
    }
    if (pageValue && pageValue != "") {
      updatedURL = updatedURL + joiner + "page=" + pageValue;
    }
    if (search_queryValue && search_queryValue != "") {
      updatedURL = updatedURL + joiner + "search_query=" + search_queryValue;
    }

    // Replace the URL without triggering a page refresh
    window.history.replaceState({}, document.title, updatedURL);

    // Refresh the page to load data based on the updated filters
    window.location.reload();
  }

  // Handle checkbox change events
  $(".filter-checkbox").on("change", function () {
    updateURLAndRefresh();
  });

  // When the page loads, ensure that the checkboxes match the current URL
  const urlSearchParams = new URLSearchParams(window.location.search);
  urlSearchParams.forEach((value, key) => {
    const checkboxes = $(`.filter-checkbox[data-filter="${key}"]`);
    checkboxes.each(function () {
      if (value.split(",").includes($(this).val())) {
        $(this).prop("checked", true);
      } else {
        $(this).prop("checked", false);
      }
    });
  });
});

const removeFilter = (key, val) => {
  // Build the query string
  const queryStringParts = [];
  const urlSearchParams = new URLSearchParams(window.location.search);
  const params = Object.fromEntries(urlSearchParams.entries());
  for (const paramName in params) {
    if (params[paramName].includes(",")) {
      let p = params[paramName].split(",");

      const filteredValues = p.filter((paramVal) => paramVal !== val);
      if (filteredValues.length > 0) {
        queryStringParts.push(paramName + "=" + filteredValues.join(","));
      }
    } else {
      if (key == paramName && val == params[paramName]) {
      } else {
        queryStringParts.push(paramName + "=" + params[paramName]);
      }
    }
  }

  // Get the current URL path without the query string
  const pathWithoutQuery = window.location.pathname;
  // Construct the updated URL
  const updatedURL =
    queryStringParts.length > 0
      ? pathWithoutQuery + "?" + queryStringParts.join("&")
      : pathWithoutQuery;
  // Replace the URL without triggering a page refresh
  window.history.replaceState({}, document.title, updatedURL);
  // Refresh the page to load data based on the updated filters
  window.location.reload();
};
