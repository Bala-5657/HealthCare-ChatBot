/******menu toggle*******/
$('.menu-toggle').on('click', function () {
    $('body').toggleClass('menu-open');
});
/******menu toggle*******/

/******Toast start*******/
// Default Configuration
$(document).ready(function () {
    toastr.options = {
        'closeButton': true,
        'debug': false,
        'newestOnTop': false,
        'progressBar': false,
        'positionClass': 'toast-top-right',
        'preventDuplicates': false,
        'showDuration': '1000',
        'hideDuration': '1000',
        'timeOut': '5000',
        'extendedTimeOut': '1000',
        'showEasing': 'swing',
        'hideEasing': 'linear',
        'showMethod': 'fadeIn',
        'hideMethod': 'fadeOut',
    }
});

// // Toast Type
//   $('#success').click(function(event) {
//     toastr.success('You clicked Success toast');
//   });
//   $('#info').click(function(event) {
//     toastr.info('You clicked Info toast')
//   });
//   $('#error').click(function(event) {
//     toastr.error('You clicked Error Toast')
//   });
//   $('#warning').click(function(event) {
//     toastr.warning('You clicked Warning Toast')
//   });

// Toast Image and Progress Bar
$('#image').click(function (event) {
    toastr.options.progressBar = true,
        toastr.info('<img src="https://image.flaticon.com/icons/svg/34/34579.svg" style="width:150px;">', 'Toast Image')
});


// Toast Position
$('#position').click(function (event) {
    var pos = $('input[name=position]:checked', '#positionForm').val();
    toastr.options.positionClass = "toast-" + pos;
    toastr.options.preventDuplicates = false;
    toastr.info('This sample position', 'Toast Position')
});
/******Toast end*******/


class ErrorMessageDisplay {

    validateForm(errorMessages) {
        this.clearErrorMessages();
        let is_error = false;
        for (const errorMessageObject of errorMessages) {
            const { fieldId, errorMessage, type, maxlength = 256, minlength = 0, is_required = true, styles = "", classes = "", direct_style = false } = errorMessageObject;
            const field = document.getElementById(fieldId).value.trim();
            // const checkBox_field = document.getElementById(fieldId);
            switch (type) {

                case "email":
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (is_required) {
                        if (field.length == 0) {
                            this.displayErrorMessages(fieldId, errorMessage, styles, classes, direct_style);
                            is_error = true;
                        } else if (!emailRegex.test(field)) {
                            this.displayErrorMessages(fieldId, "Invalid Email Format", styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length > maxlength) {
                            this.displayErrorMessages(fieldId, `Email exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length < minlength) {
                            this.displayErrorMessages(fieldId, `Email is below minimum length of ${minlength}`, styles, classes, direct_style);
                            is_error = true;
                        }
                    } else {
                        if (field.length > 0) {
                            if (!emailRegex.test(field)) {
                                this.displayErrorMessages(fieldId, "Invalid Email Format", styles, classes, direct_style);
                                is_error = true;
                            } else if (field.length > maxlength) {
                                this.displayErrorMessages(fieldId, `Email exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                                is_error = true;
                            } else if (field.length < minlength) {
                                this.displayErrorMessages(fieldId, `Email is below minimum length of ${minlength}`, styles, classes, direct_style);
                                is_error = true;
                            }
                        }
                    }
                    break;

                case "phone_number":
                    const phoneNoRegex = /^\+?[0-9]+$/;
                    if (is_required) {
                        if (field.length == 0) {
                            this.displayErrorMessages(fieldId, errorMessage, styles, classes, direct_style);
                            is_error = true;
                        } else if (phoneNoRegex.test(field) == false) {
                            this.displayErrorMessages(fieldId, "Invalid Phone Number Format", styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length > maxlength) {
                            this.displayErrorMessages(fieldId, `Phone Number exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length < minlength) {
                            this.displayErrorMessages(fieldId, `Phone Number is below minimum length of ${minlength}`, styles, classes, direct_style);
                            is_error = true;
                        }
                    } else {
                        if (field.length > 0) {
                            if (phoneNoRegex.test(field) == false) {
                                this.displayErrorMessages(fieldId, "Invalid Phone Number Format", styles, classes, direct_style);
                                is_error = true;
                            } else if (field.length > maxlength) {
                                this.displayErrorMessages(fieldId, `Phone Number exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                                is_error = true;
                            } else if (field.length < minlength) {
                                this.displayErrorMessages(fieldId, `Phone Number is below minimum length of ${minlength}`, styles, classes, direct_style);
                                is_error = true;
                            }
                        }
                    }
                    break;


                case "general":
                    if (is_required) {
                        if (field.length == 0) {
                            this.displayErrorMessages(fieldId, errorMessage, styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length > maxlength) {
                            this.displayErrorMessages(fieldId, `Field exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                            is_error = true;
                        } else if (field.length < minlength) {
                            this.displayErrorMessages(fieldId, `Field is below minimum length of ${minlength}`, styles, classes, direct_style);
                            is_error = true;
                        }
                    } else {
                        if (field.length > 0) {
                            if (field.length > maxlength) {
                                this.displayErrorMessages(fieldId, `Field exceeds maximum length of ${maxlength}`, styles, classes, direct_style);
                                is_error = true;
                            } else if (field.length < minlength) {
                                this.displayErrorMessages(fieldId, `Field is below minimum length of ${minlength}`, styles, classes, direct_style);
                                is_error = true;
                            }
                        }
                    }

                    break;

                default:
                    break;
            }
        }
        return !is_error;
    }

    clearErrorMessages() {
        const errorMessages = document.querySelectorAll('.text-danger');
        errorMessages.forEach(errorMessage => errorMessage.parentNode.removeChild(errorMessage));
    }

    displayErrorMessages(fieldId, errorMessage, styles = "", classes = "", direct_style = false) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'text-danger '.concat(classes);
        if (!direct_style) {
            errorContainer.style = 'position:absolute;font-size:13px;'.concat(styles);
        } else {
            errorContainer.style = styles
        }
        errorContainer.innerHTML = errorMessage;

        const field = document.getElementById(fieldId);
        field.parentNode.appendChild(errorContainer);
    }
}
