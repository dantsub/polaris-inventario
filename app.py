import re
from flask import Flask, render_template, request, session, redirect, url_for
import utils
from markupsafe import escape
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = os.urandom(24) 


@app.route('/index')
def index():
    if 'usuario' in session:
         return render_template('index.html')
    else:
        return redirect(url_for('login'))
   


@app.route('/productos', methods=["GET", "POST"])
def productos():
    if 'usuario' in session:
        data1 = ""
        data2 = ""
        data3 = ""
        error = False
        nombre = ""
        descripcion = ""
        select = None

        if request.method == 'POST':
            formulario = request.form.get("oculto")
            if(formulario == "crear"):

                nombre = request.form.get('nombreproducto')
                descripcion = request.form.get('descripcionprod')
                select = request.form.get('menuproveedor')
                if nombre == "":
                    data1 = "El campo nombre no puede estar vacio"
                    error = True
                if descripcion == "":
                    data2 = "El campo descripcion no puede estar vacio"
                    error = True
                if select == None:
                    data3 = "Seleccione un proveedor"
                    error = True
            return render_template('modules/products.html', data1=data1, data2=data2, data3=data3, error=error, nombre=nombre, select=select, descripcion=descripcion)
        return render_template('modules/products.html')       
    else:
        return redirect(url_for('login'))
    


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["login-email"]
        clave = request.form["login-password"]
        error = False
        errorusuario = ""
        errorclave=""
        if not utils.isUsernameValid(usuario):
            errorusuario = "El usuario debe ser alfanumérico y/o contener -_."
            error= True
        if not utils.isPasswordValid(clave):
            errorclave = "La clave debe tener debe tener mínimo 8 caracteres, una mayúscula, una minuscula, un número y un caracter:@$!%*?&."
            error= True 
        if error==True:
            return render_template("modules/login.html", error=error, errorusuario=errorusuario, errorclave=errorclave, usuario=usuario)
        
        with sqlite3.connect('Polaris') as conn:
            cur =conn.cursor()
            user=cur.execute("SELECT user_name FROM usuarios WHERE user_name=? ", [usuario]).fetchone()
            if user is not None:
                password = cur.execute("SELECT password FROM usuarios WHERE user_name=? ", [usuario]).fetchone()
                if password is not None:
                    password2 = password[0]
                    session.clear()
                    if check_password_hash(password2, clave):
                    #if password2 == clave:
                        session['usuario'] = usuario
                        return redirect(url_for('index'))
                    else: 
                        errorclave = "Password no encontrado"
                        error = True
                        return render_template("modules/login.html", error=error, errorclave=errorclave)
            else: 
                errorusuario = "Usuario no encontrado"
                error = True  
                return render_template("modules/login.html", error=error, errorusuario=errorusuario)    

    return render_template("modules/login.html")
     

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'usuario' in session:
        session.pop('usuario', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/providers', methods=["GET", "POST"])
def providers():
    if 'usuario' in session:
        data1 = ""  # error Idproveedor #id
        data2 = ""  # error nombre #nombre
        data3 = ""  # error correo #correo
        data4 = ""  # error teléfono #telefono
        data5 = ""  # error direccion #direccion
        data6 = ""  # error pais #pais
        error = False
        id = ""
        nombre = ""
        correo = ""
        telefono = ""
        direccion = ""
        pais = ""
        if request.method == 'POST':
            formulario = request.form.get("oculto")
            if(formulario == "crear"):
                id = request.form.get('id')
                nombre = request.form.get('nombre')
                correo = request.form.get('correo')
                telefono = request.form.get('telefono')
                direccion = request.form.get('direccion')
                pais = request.form.get('pais')

                if id == "":
                    data1 = "El campo Id del Proveedor no puede estar vacio"
                    error = True
                if nombre == "":
                    data2 = "El campo Nombre no puede estar vacio"
                    error = True
                if correo == "":
                    data3 = "El campo Correo no puede estar vacio"
                    error = True
                if telefono == "":
                    data4 = "El campo Telefono no puede estar vacio"
                    error = True
                if direccion == "":
                    data5 = "El campo Dirección no puede estar vacio"
                    error = True
                if pais == "":
                    data6 = "El campo país no puede estar vacio"
                    error = True
            return render_template('modules/providers.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, error=error, id=id, nombre=nombre, correo=correo, telefono=telefono, direccion=direccion,  pais=pais)
        return render_template('modules/providers.html')
    else:
        return redirect(url_for('login'))



@app.route('/users', methods=["GET", "POST"])
def users():
    if 'usuario' in session:
        data1 = ""  # error usuario #usuario
        data2 = ""  # error nombres #nombres
        data3 = ""  # error apellidos #apellidos
        data4 = ""  # error documento #cedula
        data5 = ""  # error correo #correo
        data6 = ""  # error rol #rol_crear
        data7 = ""  # error clave #passw
        error = False
        usuario = ""
        nombre = ""
        apellido = ""
        documento = ""
        correo = ""
        rol = ""
        clave = ""
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
                    data4 = "El campo Documentos no puede estar vacio"
                    error = True
                if correo == "":
                    data5 = "El campo Correo no puede estar vacio"
                    error = True
                if rol == None:
                    data6 = "Seleccione un rol"
                    error = True
                if clave == "":
                    data7 = "El campo clave no puede estar vacio"
                    error = True
                if error==True: 
                    return render_template('modules/users.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, error=error, nombre=nombre, usuario=usuario, apellido=apellido, clave=clave, documento=documento, correo=correo, rol=rol)
                else: 
                    clave_encrypt = generate_password_hash(clave)
                    today=date.today()
                    with sqlite3.connect('Polaris') as conn:
                        cur =conn.cursor()
                        cur.execute('INSERT INTO usuarios (user_name, documento, nombres, apellidos, password, fecha_creacion, idRol) VALUES(?,?,?,?,?,?,?)',
                        (usuario, documento, nombre, apellido, clave_encrypt, today, rol))
                        conn.commit()
                        return redirect(url_for('users'))
        return render_template('modules/users.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5504)
