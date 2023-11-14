(function ($) {
    $(document).ready(function () {
        const attributeSelect = $('#id_productattribute_set-0-attribute');
        const attributeValueSelect = $('#id_productattribute_set-0-value');
        
        // Function to update attribute values based on the selected attribute
        function updateAttributeValues() {
            const selectedAttribute = attributeSelect.val();
            attributeValueSelect.empty();

            if (selectedAttribute) {
                // Fetch and populate attribute values based on the selected attribute
                $.get(`/admin/products/fetch_attribute_values/?attribute_id=${selectedAttribute}`, function (data) {
                    attributeValueSelect.html(data);
                });
            }
        }

        // Bind the updateAttributeValues function to the attribute select change event
        attributeSelect.on('change', updateAttributeValues);

        // Initial load
        updateAttributeValues();
    });
})(django.jQuery);
