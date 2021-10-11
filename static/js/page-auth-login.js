/*=========================================================================================
  File Name: form-validation.js
  Description: jquery bootstrap validation js
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: PIXINVENT
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(function () {
  'use strict';

  var pageLoginForm = $('.auth-login-form');

  // jQuery Validation
  // --------------------------------------------------------------------
  if (pageLoginForm.length) {
    pageLoginForm.validate({
      onkeyup: function (element) {
        $(element).valid();
      },
      /*
      * ? To enable validation onkeyup
      onkeyup: function (element) {
        $(element).valid();
      },*/
      /*
      * ? To enable validation on focusout
      onfocusout: function (element) {
        $(element).valid();
      }, */
      rules: {
        'login-email': {
          required: true
        },
        'login-password': {
          required: true,
          minlength: 6, 
        }
      },
      messages : {
        'login-email': {
          required: "El campo usuario no puede estar vacío",
        },
        'login-password': {
          required: "El campo contraseña no puede estar vacío",
          minlength: "La contraseña debe ser de mínimo 6 caracteres"
        }
      }
    });
  }
});
