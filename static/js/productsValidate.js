(function ejecutarmodal() {
  "use strict";
  window.addEventListener(
    "load",
    function () {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName("needs-validation");
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });
    },
    false
  );

  // $(document).ready(function () {
  //   $("#Searchproducto").on("keyup", function () {
  //     var value = $(this).val().toLowerCase();
  //     $("#tablaproducto tr").filter(function () {
  //       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
  //     });
  //   });
  // });
})();
