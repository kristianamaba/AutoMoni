$(document).ready(function () {

    $('#submitL').click(function () {
        if (checkFormC("loginfrm")) {
            $.ajax({
                url: BASE_URL + 'crud/login_account',
                method: 'post',
                data: $("#loginfrm").serialize(),
                success: function (output, status, xhr) {
                    const return_obj = JSON.parse(output);
                    if (return_obj.status == 1) {
                        window.localStorage.setItem("s", return_obj.s);
                        sAlert(return_obj.message, './home');
                    }
                    else
                        fAlert(return_obj.message);
                }
            });
        }
    });



});





// checkUrl();

// function showToast(text, type) {
//     $.toast({
//         text: text,
//         showHideTransition: 'slide',
//         icon: type,
//         position: 'bottom-right'
//     });
// }

// function getUrlVars() {
//     var vars = {};
//     var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
//         vars[key] = value;
//     });
//     return vars;
// }

// function getUrlParam(parameter, defaultvalue) {
//     var urlparameter = defaultvalue;
//     if (window.location.href.indexOf(parameter) > -1) {
//         urlparameter = getUrlVars()[parameter];
//     }
//     return urlparameter;
// }

// $("#loginForm").on('submit', function () {
//     SignIn();
//     return false;
// });

// $(".form-signindetails").on('submit', function () {
//     SignIn();
//     return false;
// });

// $(".form-reset").on('submit', function () {
//     ResetPWReq();
//     return false;
// });

// $(".form-passreset").on('submit', function () {
//     ResetPW();
//     return false;
// });

// $(".form-signup").on('submit', function () {
//     SignUp();
//     return false;
// });

// $("#cancel_resetPW").on('click', function () {
//     toggleResetPW();
// })

// function getUrlVars() {
//     var vars = {};
//     var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
//         vars[key] = value;
//     });
//     return vars;
// }

// function getUrlParam(parameter, defaultvalue) {
//     var urlparameter = defaultvalue;
//     if (window.location.href.indexOf(parameter) > -1) {
//         urlparameter = getUrlVars()[parameter];
//     }
//     return urlparameter;
// }

// function checkUrl() {
//     var status = decodeURI(getUrlParam('status', 'null'));
//     var page = getUrlParam('page', 'null');

//     if (status != 'null' && page == 'login') {
//         showToast("Sign In Failed: " + status, 'error');
//         window.history.pushState({}, document.title, "");
//     }

//     if (getUrlParam('sessid', null) && getUrlParam('user', null)) {
//         toggleResetPW();
//     }

//     if (page == 'register') {
//         $('#logreg-forms .form-signin').toggle(); // display:block or none
//         $('#logreg-forms .form-signup').toggle(); // display:block or none
//     }
// }

// var Xdata;

// function SignIn() {

//     let btnSI = $("#btnSI").html();
//     $('#btnSI').attr('disabled', true).html(processingSpinner);

//     let btnSID = $("#btnSID").html();
//     $('#btnSID').attr('disabled', true).html(processingSpinner);

//     $('#usernameSI').attr('readonly', true);
//     $('#passwordSI').attr('readonly', true);

//     $.ajax({
//         url: BASE_URL + "Login/login",
//         type: 'post',
//         data: $("#loginForm").serialize(),
//         success: function (resp) {
//             console.log(resp);
//             const obj = JSON.parse(resp);
//             if (obj.success) {
//                 // sAlert(obj.data, './admin_dashboard')
//                 location = BASE_URL + obj.Homepage;
//             }
//             else {
//                 fAlert(obj.data);
//                 $('#btnSI').attr('disabled', false).html(btnSI);
//                 $('#btnSID').attr('disabled', false).html(btnSID);
//                 $('#usernameSI').attr('readonly', false);
//                 $('#passwordSI').attr('readonly', false);
//             }
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             fAlert("Error: " + errorThrown);
//             $('#btnSI').attr('disabled', false).html(btnSI);
//             $('#btnSID').attr('disabled', false).html(btnSID);
//             $('#usernameSI').attr('readonly', false);
//             $('#passwordSI').attr('readonly', false);
//         }
//     });


// }

// function ResetPWReq() {

//     $("#btnResetPW").attr('disabled', true);
//     $("#btnResetPW").html(`<div class="spinner-border spinner-border-sm" role="status"> <span class="sr-only">Processing...</span> </div>`);

//     $.ajax({
//         url: '/login/ResetPassRequest',
//         data: { email: $("#emailRPW").val() },
//         type: 'POST',
//         success: function (resp) {
//             if (resp.success) {
//                 showToast("Please check your email " + $("#emailRPW").val() + " for confirmation.", 'success');
//                 $("#emailRPW").val("");
//             } else {
//                 showToast(resp.data[0], 'error');
//             }

//             $("#btnResetPW").attr('disabled', false);
//             $("#btnResetPW").html(`<i class="far fa-envelope"></i> Reset my password`);
//         }
//     });

// }

// var password = $("#resetPW");
// var confirm_password = $("#resetPWconfirm");

// function validatePassword() {
//     if (password.value != confirm_password.value) {
//         confirm_password.setCustomValidity("Passwords do not match");
//     } else {
//         confirm_password.setCustomValidity('');
//     }
// }

// password.onchange = validatePassword;
// confirm_password.onkeyup = validatePassword;

// function ResetPW() {

//     $("#btnPWReset").html(`<div class="spinner-border spinner-border-sm" role="status"> <span class="sr-only">Processing...</span> </div>`);
//     $('#btnPWReset').attr('disabled', true);

//     $.ajax({
//         url: '/login/ResetPass',
//         data: { data_id: getUrlParam('sessid', 'null'), email: getUrlParam('user', 'null'), pass: $("#resetPW").val() },
//         type: 'POST',
//         success: function (data) {
//             switch (data) {
//                 case "Success":
//                     window.history.pushState({}, document.title, "");
//                     showToast("Password changed successfully.", 'success');
//                     toggleSignUp();
//                     break;
//                 default:
//                     showToast(data, 'error');
//                     $('#btnPWReset').attr('disabled', false);
//                     break;
//             }
//             $('#btnPWReset').html(`<i class="fas fa-sync-alt"></i> Reset Password`);
//         }
//     });

// }

// $(".toggle-password").click(function () {

//     $(this).toggleClass("fa-eye fa-eye-slash");
//     var input = $($(this).attr("toggle"));
//     if (input.attr("type") == "password") {
//         input.attr("type", "text");
//     } else {
//         input.attr("type", "password");
//     }
// });

// function toggleResetPswdReq(e) {
//     e.preventDefault();
//     $('#logreg-forms .form-signin').toggle() // display:block or none
//     $('#logreg-forms .form-reset').toggle() // display:block or none
// }

// function toggleSignUp() {
//     //e.preventDefault();
//     $('#logreg-forms .form-signin').toggle(); // display:block or none
//     $('#logreg-forms .form-signup').toggle(); // display:block or none
// }

// function toggleResetPW() {
//     $('#logreg-forms .form-signin').toggle(); // display:block or none
//     $('#logreg-forms .form-passreset').toggle(); // display:block or none
// }

// function toggleSignUpDetails() {
//     $('#logreg-forms .form-signin').toggle(); // display:block or none
//     $('#logreg-forms .form-signindetails').toggle(); // display:block or none
// }

// $(() => {
//     // Login Register Form
//     $('#logreg-forms #forgot_pswd').click(toggleResetPswdReq);
//     $('#logreg-forms #cancel_reset').click(toggleResetPswdReq);
//     $('#logreg-forms #btn-signup').click(toggleSignUp);
//     $('#logreg-forms #cancel_signup').click(toggleSignUp);
// })

// var logintoken = "";