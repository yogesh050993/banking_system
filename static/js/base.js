

    //----------------CODE FOR ALLOWING ONLY NUMERIC CHARACTERS WITHOUT DECIMALS----------------//
    $(document).on("keypress keyup blur", ".allownumericwithoutdecimal", function (event) {
       $(this).val($(this).val().replace(/[^\d].+/, ""));
        if ((event.which < 48 || event.which > 57)) {
            event.preventDefault();
        }
    });
    //----------------END CODE FOR ALLOWING ONLY NUMERIC CHARACTERS WITHOUT DECIMALS----------------//


    //----------------CODE FOR ALLOWING ONLY EMAIL SPECIFIC CHARS AT ON INPUT EVENT----------------//
    $(document).on("keypress keyup blur", ".email_field", function (event) {
        var character = String.fromCharCode(event.keyCode);
        return isValidEmailInput(character);

    });

    function isValidEmailInput(str) {
        return !/[ ~`!_#$%\^&*()+=\-\[\]\\';,/{}|\\":<>\?]/g.test(str);
    }
    //----------------END CODE FOR ALLOWING ONLY EMAIL SPECIFIC CHARS AT ON INPUT EVENT----------------//


    //----------------------------CODE FOR VALIDATING EMAIL SYNTACTICALLY ONLY----------------------------//
    function isValidEmail(email) {
        var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
        return pattern.test(email);
    }
    //----------------------------END CODE FOR VALIDATING EMAIL SYNTACTICALLY ONLY----------------------------//


    //--------------CODE FOR CHECKING MANDATORY FIELDS WHILE SAVING/SUBMIT THE FORM-----------//
    function checkMandatoryField(class_name) {
        console.log(class_name)
        var emptyFlag = 0;
        var firstError = 0;

        $('.' + class_name).filter(function () {
            if (this.id) {
                if (!this.value.replace(/\s/g, '').length) {
                    emptyFlag = 1;
                    console.log(this.id);

                    $('#' + this.id).addClass('redborder');

                    if (firstError == 0) {
                        console.log('#' + this.id);
                        $('#' + this.id).focus();
                        firstError = 1;
                    }

                    if ($('#' + this.id).hasClass('selectpicker')) {
                        $('#' + this.id).selectpicker('refresh');
                    }
                } else {
                    if ($('#' + this.id).hasClass('redborder')) {
                        $('#' + this.id).removeClass('redborder');
                    }
                    if ($('#' + this.id).hasClass('selectpicker')) {
                        $("#" + this.id).closest("div").removeClass("redborder");
                        $('#' + this.id).selectpicker('refresh');
                    }
                }
            }
        });
        return emptyFlag;
    }
    //--------------END CODE FOR CHECKING MANDATORY FIELDS WHILE SAVING/SUBMIT THE FORM-----------//


    // -----------CODE FOR VALIDATING REQUIRED FIELDS AND ADD & REMOVE REDBORDER ACCORDINGLY---------//

    function requiredField(id) {
        var value = $('#' + id).val();

        if (!value) {
            $('#' + id).addClass("redborder");
            $('#' + id).focus();
        } else {
            $('#' + id).removeClass("redborder");
            if ($('#' + id).hasClass("selectpicker")) {
                $("#" + id).closest("div").removeClass("redborder");
            }

            if ($('#' + id).hasClass("email")) {
                var user_email_id = $('#' + id).val();
                if (isValidEmail(user_email_id)) {
                    if ($('#' + id).hasClass("redborder")) {
                        $('#' + id).removeClass('redborder');
                    }
                } else {
                    $('#' + id).addClass('redborder');
                    $('#' + id).focus();
                }
            }
        }

        if ($('#' + id).hasClass("selectpicker")) {
            $('#' + id).selectpicker('refresh');
        }
    }

    $(document).on('keyup', '.isRequired', function () {
        requiredField($(this).attr('id'))
    });

    $('.decimal').keypress(function (e) {
        if (e.which === 32) {
            return false;
        }
        var character = String.fromCharCode(e.keyCode)
        var newValue = this.value + character;
        if (isNaN(newValue) || hasDecimalPlace(newValue, 3)) {
            e.preventDefault();
            return false;
        }
    });

    function hasDecimalPlace(value, x) {
        var pointIndex = value.indexOf('.');
        return pointIndex >= 0 && pointIndex < value.length - x;
    }

    // -----------END CODE FOR VALIDATING REQUIRED FIELDS AND ADD & REMOVE REDBORDER ACCORDINGLY---------//



    Datepicker = (function () {
    var e = $(".datepicker");
    e.length &&
      e.each(function () {
        $(this).datepicker({ disableTouchKeyboard: !0, autoclose: !1 });
      });
  })()