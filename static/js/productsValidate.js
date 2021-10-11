function fnt_create_product_validate() {
    nombreproducto = document.getElementById("nombreproducto");
    descriproducto = document.getElementById("descripcionprod");
    selectproveedor = document.getElementById("menuproveedor");
    count = 0;


    event.preventDefault();
    if (nombreproducto.value == "") {
        document.getElementById("errornomprod").innerHTML = "El campo nombre no puede estar vacio";
        nombreproducto.focus();
        count++;
    }

    if (descripcionprod.value == "") {
        document.getElementById("errordescripcion").innerHTML = "El campo descripción no puede estar vacio";
        descripcionprod.focus();
        count++;
    }
    if (selectproveedor.value == "0") {
        document.getElementById("errorproveedor").innerHTML = "Debe seleccionar un proveedor";
        selectproveedor.focus();
        count++;
    }

    if (count > 0) {
        return false;
    } else {
        document.getElementById("formulariocrearprod").submit();
    }
}

function fnt_create_product_validate2() {
    nombreproducto = document.getElementById("nombreproducto2");
    descriproducto = document.getElementById("descripcionprod2");
    selectproveedor = document.getElementById("menuproveedor2");
    count = 0;


    event.preventDefault();
    if (nombreproducto.value == "") {
        document.getElementById("errornomprod2").innerHTML = "El campo nombre no puede estar vacio";
        nombreproducto.focus();
        count++;
    }

    if (descripcionprod.value == "") {
        document.getElementById("errordescripcion2").innerHTML = "El campo descripción no puede estar vacio";
        descripcionprod.focus();
        count++;
    }
    if (selectproveedor.value == "0") {
        document.getElementById("errorproveedor2").innerHTML = "Debe seleccionar un proveedor";
        selectproveedor.focus();
        count++;
    }

    if (count > 0) {
        return false;
    } else {
        document.getElementById("fromularioeditarprod").submit();
    }
}

(function () {
    $(function () {
        $('#modalNew').modal();
    });
})();