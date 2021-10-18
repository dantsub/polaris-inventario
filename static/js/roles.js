// Show html based on role


$(function () {
        'use strict';
        var role= 'superadmin'
        var usuarios = $('.nav-item-usuarios');
        var crearroladmin = $('.select-crear-admin');
        var crearrolsuper = $('.select-crear-super');
        var editarroladmin = $('.select-editar-admin');
        var editarrolsuper = $('.select-editar-super');
      
        // jQuery Validation
        // --------------------------------------------------------------------
        if (role=='usuario'){
            usuarios.hide();
 
        } 
        if (role=='administrador'){
            crearroladmin.hide();
            crearrolsuper.hide();
            editarroladmin.hide();
            editarrolsuper.hide();
 
        } 

        if (role=='superadmin'){
            crearroladmin.show();
            crearrolsuper.show();
            editarroladmin.show();
            editarrolsuper.show();
            usuarios.show();
 
        }  
        
});
       