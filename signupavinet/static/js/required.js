odoo.define('user.required', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var isValid = false;

    $(document).ready(function () {
        var btnNext = $('#next_btn'); // Updated to use the ID "next_btn"
        var check1 = $('.check_1');
        var check2 = $('.check_2');
        var agrem = $('#agrem');
        var expAgrem = $('#exp_agrem');
        var scan = $('#scan');
        var fileAlert = $('.file_alert');
        var doc = $('.doc');
        var cities = document.querySelector('#ville');
        var fileAlertShown = false;

        // Function to update required attribute based on checkbox status
        function updateRequiredAttribute() {
            if (check2.is(':checked') || check1.is(':checked')) {
                $('.req_mark').show();
                agrem.attr('required', 'required');
                expAgrem.attr('required', 'required');
            } else {
                $('.req_mark').hide();
                agrem.removeAttr('required');
                expAgrem.removeAttr('required');
            }
        }

        // Function to check file type and size before upload
        function validateFile(file) {
            var allowedFileTypes = ['image/jpeg', 'image/png', 'application/pdf'];
            var maxFileSizeInBytes = 5 * 1024 * 1024; // 5 MB

            if (!allowedFileTypes.includes(file.type)) {
                alert('Type de ficher invalide. Veuillez choisir un fichier de type: JPEG, PNG, ou PDF.');
                scan.val('');
                return false;
            }

            if (file.size > maxFileSizeInBytes) {
                if (!fileAlertShown) {
                    alert('La taille de chaque fichers sélectionner ne dois pas dépasser 5 MB.');
                    fileAlertShown = true;
                }
                scan.val('');
                return false;
            }

            return true;
        }

        // Function to enable the Next button and associated anchor tag
        function enableNextButton() {
            var isButtonEnabled = isValid;
            btnNext.prop('disabled', !isButtonEnabled);
            console.log('Button enabled:', isButtonEnabled);

            // Disable/enable the anchor tag associated with btnNext
            var anchorTag = btnNext.closest('a');
            if (anchorTag.length) {
                anchorTag.prop('disabled', !isButtonEnabled);
                console.log('Anchor tag enabled:', isButtonEnabled);
            }
        }

        // Attach onchange event to the checkboxes
        check1.add(check2).on('change', function () {
            updateRequiredAttribute();
            validateFields();
        });

        // Attach onchange event to the scan input
        scan.on('change', function () {
            var a = scan[0] ? scan[0].files : [];
            if (a.length > 4) {
                alert('Vous Pouvez Choisir Un Maximum de 4 Fichers.');
                fileAlert.show();
                doc.prop('disabled', true);
                // Clear the scan input to remove file names
                scan.val('');
            } else {
                fileAlert.hide();
                doc.prop('disabled', false);
                fileAlertShown = false; // Reset the file alert status
            }

            // Validate each file before upload
            for (var i = 0; a.length > 0 && i < a.length; i++) {
                if (!validateFile(a[i])) {
                    // Clear the file input if any file is invalid
                    scan.val('');
                    break;
                }
            }

            validateFields();
        });
        // Add a change event listener to the file input
        $('#scan').on('change', function () {
        var input = $(this)[0];
        var label = $(this).next('.custom-file-label');
    
        if (input.files.length > 0) {
            var files = [];
            for (var i = 0; i < input.files.length; i++) {
                files.push(input.files[i].name);
            }
    
            if (files.length > 1 && files.lenght < 5) {
                label.text(files.length + ' Fichiers Sélectionner');
            } else {
                label.text(files.join(', '));
            }
                } else {
            label.text('Choisir Fichers...');
            scan.val('');
            }
        });
        
        //handles fetching dairas(city) for selected willaya(state)
        $('#State').on('change', function () {
            var id = $('#State').val()
            var cit = $('#city').val();
            $('#ville').find('option').remove();

            var model = 'res.city';
            var domain = [['state_id.id', '=', id]];
            var field = ['name'];

            rpc.query({
                route: "/get/city",
                params: {
                    'domain': id,
                },
            }).then(function (data) {
                for (let i = 0; i < data.length; i++) {
                    var option = new Option(data[i][0], data[i][1]);
                    cities.add(option);
                }
                validateFields();
            });
        });

        // Function to validate all required fields and enable/disable the Next button
        function validateFields() {
            console.log('Validating fields...');
            isValid = true; // Set isValid to true initially

            var excludeFields = ['login', 'password', 'confirm_password'];

            // Check all required fields and get invalid fields
            var invalidFields = $(':input[required]').filter(function () {
                // Exclude specific fields from validation
                if (excludeFields.includes($(this).attr('id'))) {
                    return false;
                }

                if (!$(this).val()) {
                    console.log('Empty field detected:', this);
                    isValid = false;
                    return true; // Include in invalidFields
                }
                return false;
            }).map(function () {
                return $(this).attr('id');
            }).get();

            // Check the size of each file individually
            var files = scan[0] ? scan[0].files : [];
            for (var i = 0; files.length > 0 && i < files.length; i++) {
                if (!validateFile(files[i])) {
                    isValid = false;
                    console.log('Invalid file detected:', files[i]);
                    invalidFields.push('scan');
                    break;
                }
            }

            console.log('isValid:', isValid);
            enableNextButton();

            return invalidFields;
        }
        // Function to associate label text with form fields
        function associateLabelsWithFields() {
            var labelMap = {};
            $('label').each(function () {
                var labelText = $(this).text().trim();
                var inputId = $(this).attr('for');
                if (inputId) {
                    labelMap[inputId] = labelText;
                }
            });
            return labelMap;
        }
        // Call the function to associate labels with form fields
        var labelMap = associateLabelsWithFields();
        
        // Function to get label text or fallback to field ID
        function getLabelText(fieldId) {
            return labelMap[fieldId] || fieldId;
        }
                
        

        btnNext.on('click', function (event) {
            console.log('Next button clicked! ID:', btnNext.attr('id'));
            console.log('Button disabled:', btnNext.prop('disabled'));
            if (btnNext.prop('disabled')) {

                // Track and display information about fields that haven't been validated
                var invalidFields = validateFields();
                if (invalidFields.length > 0) {
                    var invalidFieldMessages = invalidFields.map(getLabelText);
                    var alertMessage = 'Veuillez remplir les champs suivants:\n' + invalidFieldMessages.join('\n');
                    alert(alertMessage);


                    // Prevent default action after showing the alert
                    event.preventDefault();

                    console.log('Default action prevented.');
                    return false; // Ensure the default action is prevented
                }
                 return !btnNext.prop('disabled');
            }
            return true; // Allow navigation to the next form
        });

        // Initial setup
        updateRequiredAttribute();
        validateFields();
        btnNext.prop('disabled', true); // Disable the Next button initially
    });
});
