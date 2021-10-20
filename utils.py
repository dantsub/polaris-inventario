import re
import sqlite3
from validate_email import validate_email
from datetime import datetime, date


#pass_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
# Esta expresión de password indica que el debe tener mínimo 8 caracteres, una mayúscula, una minuscula, un número y un caracter:@$!%*?&.
pass_regex = "^[a-zA-Z0-9\d@$!%*?&._-]{6,}$"
user_regex = "^[a-zA-Z0-9_.-]+$"
# ^ matches the beginning of the string
# $ matches the end of the string
# + means the previous expression matches once or more
# Esta expresión de user indica que el nombre de usuario solo puede tener letras may o min, números y estos tres caracter: ._-

F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid


def isUsernameValid(user):
    if re.search(user_regex, user):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_regex, password):
        return True
    else:
        return False


def consultarproveedores():
    conexion = sqlite3.connect('Polaris')

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM proveedores")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def consultartodoslosproductos():
    conexion = sqlite3.connect('Polaris')

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT E.idProducto, E.nombre, E.descripcion, E.cantminima, E.cantdisponible, P.nombre FROM producto E join proveedores P where E.idProveedor = P.idProveedor")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def validarexistenciadeproducto(codigo):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM producto  where idProducto = ?", (codigo,))
    filas = cursor.fetchone()
    conexion.close()
    if filas is None:
        return False
    else:
        return True


def registrarproducto(codigo, nombre, descripcion, cantmin, cantdisp, proveedor):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO PRODUCTO VALUES (?,?,?,?,?,?)",
                   (codigo, nombre, descripcion, cantmin, cantdisp, proveedor))
    conexion.commit()
    return True


def eliminarproducto(codigo):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM PRODUCTO WHERE idProducto = ?", (codigo,))
    conexion.commit()
    conexion.close()
    return True


def actualizarproducto(codigo, nombre, descripcion, cantmin, cantdisp, proveedor):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(codigo, nombre, descripcion, cantmin, cantdisp, proveedor)
    cursor.execute(
        "UPDATE PRODUCTO SET nombre = ?, descripcion = ?, cantminima = ?, cantdisponible = ?, idProveedor = ? WHERE idProducto = ?", (nombre, descripcion, cantmin, cantdisp, proveedor, codigo))
    conexion.commit()
    conexion.close()
    return True

def consultartodoslosusuarios():
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT U.user_name,  U.nombres, U.apellidos, U.documento, U.correo,  U.fecha_creacion, U.fecha_vencimiento, R.Descripcion, U.idrol FROM Usuarios U Join Roles R Where U.idrol = R.idrol")
    filas = cursor.fetchall()
    conexion.close()
    return filas

def actualizarusuario(user_name, documento, nombres, apellidos, correo,  idRol):            
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(user_name, documento, nombres, apellidos, correo, idRol)
    cursor.execute(
        "UPDATE USUARIOS SET documento = ?, nombres = ?, apellidos = ?, correo = ?, idRol = ? WHERE user_name = ?", (documento, nombres, apellidos, correo, idRol, user_name))
    conexion.commit()
    conexion.close()
    return True

def eliminarusuario(user_name):            
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(user_name)
    Fecha=date.today()
    cursor.execute(
        "UPDATE USUARIOS SET fecha_vencimiento = ? WHERE user_name = ?", (Fecha, user_name))
    conexion.commit()
    conexion.close()
    return True

def fecha():
    Fecha=date.today()
    return Fecha
