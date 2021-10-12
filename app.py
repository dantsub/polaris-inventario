import re
from flask import Flask, render_template, request
import utils
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/productos')
def productos():
    return render_template('modules/products.html')


@app.route('/crearproductos', methods=['POST'])
def crearproductos():
    data1 = ""
    data2 = ""
    data3 = ""
    error = False
    nombre = ""
    if request.method == 'POST':
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


@app.route('/crearproductos')
def crearproductossin():
    return render_template('modules/products.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["login-email"]
        clave = request.form["login-password"]
        error = " "

        if not utils.isUsernameValid(usuario):
            error = "El usuario debe ser alfanumérico y/o contener -_."
            # Aquí poner la vista de error que va contener el formulario
            return render_template("modules/login.html")

        if not utils.isPasswordValid(clave):
            error = "La clave debe tener debe tener mínimo 8 caracteres, una mayúscula, una minuscula, un número y un caracter:@$!%*?&."
            # Aquí poner la vista de error que va contener el formulario
            return render_template("modules/login.html")

        return render_template("index.html")

    return render_template("modules/login.html")


@app.route('/providers')
def providers():
    return render_template('modules/providers.html')


@app.route('/users')
def users():
    return render_template('modules/users.html')


if __name__ == '__main__':
    app.run(debug=True, port=5504)
