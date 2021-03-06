import re
from flask import Flask, render_template, request, session, redirect, url_for, flash
import utils
from markupsafe import escape
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date
import secrets
from productos import *

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/productos', methods=["GET", "POST"])
def productos():
    data1 = ""
    data2 = ""
    data3 = ""
    data4 = ""
    error = False
    # >Consulta para traer los proveedores existentes
    proveedores = consultarproveedores()
    productos = consultartodoslosproductos()
    if request.method == 'POST':
        formulario = request.form.get("oculto")
        if(formulario == "crear"):
            print("pasar por crear")
            nombre = request.form.get('nombreproducto')
            descripcion = request.form.get('descripcionprod')
            select = request.form.get('menuproveedor')
            codigo = request.form.get('codigoproducto')
            cantmin = request.form.get('cantminima')
            cantexist = request.form.get('cantexistencia')

            if(validarexistenciadeproducto(codigo) == True):
                error = True
                data4 = "Ya existe un producto registrado con este codigo"
                return render_template('modules/products.html', data4=data4, error=error, nombre=nombre, select=select, descripcion=descripcion, codigo=codigo, proveedores=proveedores, productos=productos)
            else:
                if (registrarproducto(codigo, nombre, descripcion, cantmin, cantexist, select) == True):
                    proveedores = consultarproveedores()
                    productos = consultartodoslosproductos()
                    mensaje = "Producto registrado con exito"
                    flash(mensaje)
                    return render_template('modules/products.html', proveedores=proveedores, productos=productos)

        if(formulario == "eliminar"):
            codigo = request.form.get('ocultoborrar')
            if (eliminarproducto(codigo) == True):
                proveedores = consultarproveedores()
                productos = consultartodoslosproductos()
                mensaje = "Producto eliminado con exito"
                flash(mensaje)
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)

        if(formulario == "editar"):
            codigo = request.form.get('ocultoeditar')
            nombre = request.form.get('nombreproducto2')
            descripcion = request.form.get('descripcionprod2')
            select = request.form.get('menuproveedor2')
            cantmin = request.form.get('cantminima2')
            cantexist = request.form.get('cantexistencia2')
            if (actualizarproducto(codigo, nombre, descripcion, cantmin, cantexist, select) == True):
                proveedores = consultarproveedores()
                productos = consultartodoslosproductos()
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)

        if(formulario == "calificar"):
            codigo = request.form.get('ocultocalificar')
            valor = request.form['rating']
            # comentario = request.form.get('comentario')
            # if (utils.registrarcalifiacion(codigo, valor, comentario) == True):
            if (registrarcalifiacion(codigo, valor) == True):
                proveedores = consultarproveedores()
                productos = consultartodoslosproductos()
                mensaje = "Calificacion registrada con exito"
                flash(mensaje)
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)
            else:
                proveedores = consultarproveedores()
                productos = consultartodoslosproductos()
                mensaje = "No se ha podido registrar la calificaci??n del producto"
                flash(mensaje)
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)

        if(formulario == "filtroprov"):
            codigo = request.form.get('provfiltro')
            if (codigo == "Todos"):
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)
            else:
                productos = buscarproductoporproveedor(codigo)
                proveedores = consultarproveedores()
                return render_template('modules/products.html', proveedores=proveedores, productos=productos)

        if(formulario == "filtrodisponibles"):
            productos = listardisponibles()
            disponibles = True
            return render_template('modules/products.html', proveedores=proveedores, productos=productos, disponibles=disponibles)

        if(formulario == "filtrominimos"):
            productos = productosdebajominimo()
            minimos = True
            return render_template('modules/products.html', proveedores=proveedores, productos=productos, minimos=minimos)

    return render_template('modules/products.html', proveedores=proveedores, productos=productos)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = escape(request.form["login-email"])
        clave = escape(request.form["login-password"])
        error = False
        errorusuario = ""
        errorclave = ""
        if not utils.isUsernameValid(usuario):
            errorusuario = "El usuario debe ser alfanum??rico y/o contener -_."
            error = True
        if not utils.isPasswordValid(clave):
            errorclave = "La clave debe tener debe tener m??nimo 6 caracteres y ser alfanum??rica caracter:@$!%*?&."
            error = True
        if error == True:
            return render_template("modules/login.html", error=error, errorusuario=errorusuario, errorclave=errorclave, usuario=usuario)

        with sqlite3.connect('Polaris') as conn:
            cur = conn.cursor()
            user = cur.execute("SELECT user_name,  fecha_vencimiento FROM usuarios WHERE user_name= LOWER(?) ", [
                               usuario]).fetchone()
            if user is not None and user[1] is None:
                password = cur.execute(
                    "SELECT password, salt, descripcion, nombres, apellidos FROM usuarios LEFT JOIN roles ON usuarios.idRol = roles.idRol WHERE user_name=LOWER(?) ", [usuario]).fetchone()
                if password is not None:
                    password2 = password[0]
                    salt = password[1]
                    rol = password[2]
                    nombre = password[3]
                    apellido = password[4]
                    session.clear()
                    if check_password_hash(password2, salt+clave):
                        # if password2 == clave:
                        session['usuario'] = usuario
                        session['nombre'] = nombre
                        session['apellido'] = apellido
                        session['rol'] = rol
                        return redirect(url_for('index'))
                    else:
                        errorusuario = "Usuario y/o contrase??a no encontrado"
                        error = True
                        return render_template("modules/login.html", error=error, errorusuario=errorusuario)
            else:
                errorusuario = "Usuario y/o contrase??a no encontrado"
                error = True
                return render_template("modules/login.html", error=error, errorusuario=errorusuario)

    return render_template("modules/login.html")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'usuario' in session:
        session.pop('usuario', None)
        session.pop('nombre', None)
        session.pop('apellido', None)
        session.pop('rol', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/providers', methods=["GET", "POST"])
def providers():
    data1 = ""
    data2 = ""
    data3 = ""
    data4 = ""
    data5 = ""
    data6 = ""
    error = False
    data12 = ""
    data22 = ""
    data32 = ""
    data42 = ""
    data52 = ""
    erroreditar = False
    # >Consulta para traer los paises
    pais = utils.consultarpais()
    proveedores = utils.consultarproveedorpais()
    if request.method == 'POST':
        formulario = request.form.get("oculto")
        if(formulario == "crear"):
            id = request.form.get('id')
            nombre = request.form.get('nombre')
            correo = request.form.get('correo')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            menupais = request.form.get('menupais')
            print("Este es el id: del pais: "+menupais)

            if id == "":
                data1 = "El campo Id del Proveedor no puede estar vacio"
                error = True
            if nombre == "":
                data2 = "El campo Nombre no puede estar vacio"
                error = True
            if not utils.isEmailValid(correo):
                data3 = "El campo Correo no puede estar vacio"
                error = True
            if telefono == "":
                data4 = "El campo Telefono no puede estar vacio"
                error = True
            if direccion == "":
                data5 = "El campo Direcci??n no puede estar vacio"
                error = True
            if menupais == "":
                data6 = "El campo pa??s no puede estar vacio"
                error = True
            if error == True:
                return render_template('modules/providers.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, error=error, proveedores=proveedores, pais=pais, menupais=menupais)
            else:
                if(utils.validarexistenciadeproveedor(id) == True):
                    error = True
                    data1 = "Ya existe un producto registrado con este id"
                    return render_template('modules/providers.html', data1=data1, error=error, id=id, nombre=nombre, correo=correo, direccion=direccion, telefono=telefono, menupais=menupais, proveedores=proveedores, pais=pais)
                else:
                    if (utils.registrarprovedor(id, nombre, correo, direccion, telefono, menupais) == True):
                        print("Se registr?? el producto")
                        mensaje = "Proveedor registrado con exito"
                        flash(mensaje)
                        proveedores = utils.consultarproveedorpais()
                        pais = utils.consultarpais()
                        return render_template('modules/providers.html', proveedores=proveedores, pais=pais)
                    else:
                        return render_template('modules/providers.html', pais=pais, proveedores=proveedores)
 
        if(formulario == "editar"):

            id = request.form.get('oculto2')
            nombre = request.form.get('nombre2')
            correo = request.form.get('correo2')
            telefono = request.form.get('telefono2')
            direccion = request.form.get('direccion2')
            menupais = request.form.get('menupais2')
            print(id, nombre, correo, direccion, telefono, menupais)
            if nombre == "":
                data12 = "El campo Nombre no puede estar vacio"
                erroreditar = True
            if not utils.isEmailValid(correo):
                data22 = "Por favor digite un correo v??lido"
                erroreditar = True
            if telefono == "":
                data32 = "El campo Tel??fono no puede estar vacio"
                erroreditar = True
            if direccion == "":
                data42 = "El campo Direcci??n no puede estar vacio"
                erroreditar = True
            if menupais == "":
                data52 = "El campo pa??s no puede estar vacio"
                erroreditar = True
            if erroreditar == True:
                return render_template('modules/providers.html', data12=data12, data22=data22, data32=data32, data42=data42, data52=data52, erroreditar=erroreditar, id=id, nombre=nombre, correo=correo, direccion=direccion, telefono=telefono, proveedores=proveedores, pais=pais, menupais=menupais)
            else:
                if(utils.actualizarproveedor(id, nombre, correo, direccion, telefono, menupais)):
                    mensaje = "Proveedor editado con exito"
                    flash(mensaje)
                    proveedores = utils.consultarproveedorpais()
                    pais = utils.consultarpais()
                    return render_template('modules/providers.html', proveedores=proveedores, pais=pais)
                else:
                    return render_template('modules/providers.html', pais=pais, proveedores=proveedores)

        if(formulario == "eliminar"):
            codigo = request.form.get('ocultoborrar')
            if (utils.borrarproveedor(codigo) == True):
                print("Se elimino el proveedor")
                mensaje = "Proveedor eliminado con ??xito"
                flash(mensaje)
                proveedores = utils.consultarproveedorpais()
                pais = utils.consultarpais()
                return render_template('modules/providers.html', proveedores=proveedores, pais=pais)
            else:
                mensaje = "Proveedor no pudo ser eliminado porque est?? siendo usado en la tabla producto"
                flash(mensaje)
                print("No se elimin?? el proveedor por constrain por producto")
                return render_template('modules/providers.html', pais=pais, proveedores=proveedores)
    return render_template('modules/providers.html', pais=pais, proveedores=proveedores)


@app.route('/users', methods=["GET", "POST"])
def users():
    data1 = ""  # error usuario #usuario
    data2 = ""  # error nombres #nombres
    data3 = ""  # error apellidos #apellidos
    data4 = ""  # error documento #cedula
    data5 = ""  # error correo #correo
    data6 = ""  # error rol #rol_crear
    data7 = ""  # error clave #passw
    error = False
    data22 = ""  # error nombres #nombres2
    data32 = ""  # error apellidos #apellidos2
    data42 = ""  # error documento #cedula2
    data52 = ""  # error correo #correo2
    data62 = ""  # error rol #rol_crear2
    erroreditar = False
    usuario = ""
    nombre = ""
    apellido = ""
    documento = ""
    correo = ""
    rol = ""
    clave = ""
    # Consulta para traer los usuarios existentes
    if session.get('rol') == "SuperAdministrador":
        usuarios = utils.consultartodoslosusuarios()
    if session.get('rol') == "Administrador":
        usuarios = utils.consultartodoslosusuariosadmin()
    if request.method == 'POST':
        formulario = request.form.get("oculto")
        if(formulario == "crear"):
            usuario = request.form.get('usuario')
            nombre = request.form.get('nombres')
            apellido = request.form.get('apellidos')
            documento = request.form.get('cedula')
            correo = request.form.get('correo')
            rol = request.form.get('rol_crear')
            clave = request.form.get('passw')

            if usuario == "":
                data1 = "El campo usuario no puede estar vacio"
                error = True
            if nombre == "":
                data2 = "El campo Nombres no puede estar vacio"
                error = True
            if apellido == "":
                data3 = "El campo Apellidos no puede estar vacio"
                error = True
            if documento == "":
                data4 = "El campo Documentos no puede estar vacio y debe ser n??merico"
                error = True
            if not utils.isEmailValid(correo):
                data5 = "Por favor coloque un email v??lido"
                error = True
            if rol == None:
                data6 = "Seleccione un rol"
                error = True
            if not utils.isPasswordValid(clave):
                data7 = "La clave debe tener debe tener m??nimo 6 caracteres y ser alfanum??rica o con caracteres:@$!%*?&."
                error = True
            if error == True:
                return render_template('modules/users.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, error=error, nombre=nombre, usuario=usuario, apellido=apellido, documento=documento, correo=correo, rol=rol, usuarios=usuarios)
            else:
                salt = secrets.token_hex(8)
                clave_encrypt = generate_password_hash(salt+clave)
                today = date.today()
                with sqlite3.connect('Polaris') as conn:
                    cur = conn.cursor()
                    user_validate = cur.execute(
                        "SELECT user_name FROM usuarios WHERE user_name=LOWER(?) ", [usuario]).fetchone()
                    if user_validate is None:
                        cur.execute('INSERT INTO usuarios (user_name, documento, nombres, apellidos, correo, password, fecha_creacion, idRol, salt) VALUES(LOWER(?),?,?,?,?,?,?,?,?)',
                                    (usuario, documento, nombre, apellido, correo, clave_encrypt, today, rol, salt))
                        conn.commit()
                        mensaje = "Usuario registrado con exito"
                        flash(mensaje)
                        if session.get('rol') == "SuperAdministrador":
                            usuarios = utils.consultartodoslosusuarios()
                        if session.get('rol') == "Administrador":
                            usuarios = utils.consultartodoslosusuariosadmin()
                        return render_template('modules/users.html', usuarios=usuarios)
                    else:
                        error = True
                        data1 = "Este nombre de usuario ya existe"
                        return render_template('modules/users.html', data1=data1, error=error, usuarios=usuarios, nombre=nombre, usuario=usuario, apellido=apellido, documento=documento, correo=correo, rol=rol)

        if(formulario == "eliminar"):
            ##codigo = request.form.get('ocultoborrar')
            usuario = request.form.get('ocultoborrar')
            if (utils.eliminarusuario(usuario) == True):
                mensaje = "Usuario eliminado con exito"
                flash(mensaje)
                if session.get('rol') == "SuperAdministrador":
                    usuarios = utils.consultartodoslosusuarios()
                if session.get('rol') == "Administrador":
                    usuarios = utils.consultartodoslosusuariosadmin()
                return render_template('modules/users.html', usuarios=usuarios)

        if (formulario == "editar"):
            # usuario = request.form.get('usuario') esta linea no va
            usuario = request.form.get('ocultoeditar')
            nombre = request.form.get('nombres2')
            apellido = request.form.get('apellidos2')
            documento = request.form.get('cedula2')
            correo = request.form.get('correo2')
            rol = request.form.get('rol_crear2')

            if nombre == "":
                data22 = "El campo Nombres no puede estar vacio"
                erroreditar = True
            if apellido == "":
                data32 = "El campo Apellidos no puede estar vacio"
                erroreditar = True
            if documento == "":
                data42 = "El campo Documentos no puede estar vacio y debe ser n??merico"
                erroreditar = True
            if not utils.isEmailValid(correo):
                data52 = "Por favor coloque un email v??lido"
                erroreditar = True
            if rol == None:
                data62 = "Seleccione un rol"
                erroreditar = True
            if erroreditar == True:
                return render_template('modules/users.html', data22=data22, data32=data32, data42=data42, data52=data52, data62=data62, erroreditar=erroreditar, nombre=nombre, usuario=usuario, apellido=apellido, documento=documento, correo=correo, rol=rol, usuarios=usuarios)
            else:
                if (utils.actualizarusuario(usuario, documento, nombre, apellido,  correo, rol) == True):
                    mensaje = "Usuario editado con exito"
                    flash(mensaje)
                    if session.get('rol') == "SuperAdministrador":
                        usuarios = utils.consultartodoslosusuarios()
                    if session.get('rol') == "Administrador":
                        usuarios = utils.consultartodoslosusuariosadmin()
                    return render_template('modules/users.html', usuarios=usuarios)
    return render_template('modules/users.html', usuarios=usuarios)


@app.before_request
def before_request():
    if 'usuario' not in session and request.endpoint in ['index', 'productos', 'providers', 'users']:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5504)
