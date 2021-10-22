// function fnt_create_product_validate() {
//     nombreproducto = document.getElementById("nombreproducto");
//     descriproducto = document.getElementById("descripcionprod");
//     selectproveedor = document.getElementById("menuproveedor");
//     count = 0;


//     event.preventDefault();
//     if (nombreproducto.value == "") {
//         document.getElementById("errornomprod").innerHTML = "El campo nombre no puede estar vacio";
//         nombreproducto.focus();
//         count++;
//     }

//     if (descripcionprod.value == "") {
//         document.getElementById("errordescripcion").innerHTML = "El campo descripción no puede estar vacio";
//         descripcionprod.focus();
//         count++;
//     }
//     if (selectproveedor.value == "0") {
//         document.getElementById("errorproveedor").innerHTML = "Debe seleccionar un proveedor";
//         selectproveedor.focus();
//         count++;
//     }

//     if (count > 0) {
//         return false;
//     } else {
//         document.getElementById("formulariocrearprod").submit();
//     }
// }

// function fnt_create_product_validate2() {
//     nombreproducto = document.getElementById("nombreproducto2");
//     descriproducto = document.getElementById("descripcionprod2");
//     selectproveedor = document.getElementById("menuproveedor2");
//     count = 0;


//     event.preventDefault();
//     if (nombreproducto.value == "") {
//         document.getElementById("errornomprod2").innerHTML = "El campo nombre no puede estar vacio";
//         nombreproducto.focus();
//         count++;
//     }

//     if (descripcionprod.value == "") {
//         document.getElementById("errordescripcion2").innerHTML = "El campo descripción no puede estar vacio";
//         descripcionprod.focus();
//         count++;
//     }
//     if (selectproveedor.value == "0") {
//         document.getElementById("errorproveedor2").innerHTML = "Debe seleccionar un proveedor";
//         selectproveedor.focus();
//         count++;
//     }

//     if (count > 0) {
//         return false;
//     } else {
//         document.getElementById("fromularioeditarprod").submit();
//     }
// }

(function ejecutarmodal() {
    'use strict';
    window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
    form.addEventListener('submit', function(event) {
    if (form.checkValidity() === false) {
    event.preventDefault();
    event.stopPropagation();
    }
    form.classList.add('was-validated');
    }, false);
    });
    }, false);


    $(document).ready(function(){
        $("#Searchproducto").on("keyup", function() {
          var value = $(this).val().toLowerCase();
          $("#tablaproducto tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
          });
        });
      });


    })();

// (function abrirmodal () {
//     $(function () {
//             // abrir modal
//           $('#modalNew').modal('show');
//     });
// })();
