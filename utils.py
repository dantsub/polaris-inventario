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


def consultartodoslosusuarios():
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT U.user_name,  U.nombres, U.apellidos, U.documento, U.correo,  U.fecha_creacion, U.fecha_vencimiento, R.Descripcion, U.idrol FROM Usuarios U Join Roles R WHERE U.idrol = R.idrol ORDER BY U.fecha_vencimiento ASC, R.idRol DESC")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def consultartodoslosusuariosadmin():
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT U.user_name,  U.nombres, U.apellidos, U.documento, U.correo,  U.fecha_creacion, U.fecha_vencimiento, R.Descripcion, U.idrol FROM Usuarios U LEFT JOIN Roles R ON U.idrol = R.idrol WHERE R.idrol=3 ORDER BY U.fecha_vencimiento ASC ")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def actualizarusuario(user_name, documento, nombres, apellidos, correo,  idRol):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(user_name, documento, nombres, apellidos, correo, idRol)
    cursor.execute(
        "UPDATE usuarios SET documento = ?, nombres = ?, apellidos = ?, correo = ?, idRol = ? WHERE user_name = ?", (documento, nombres, apellidos, correo, idRol, user_name))
    conexion.commit()
    conexion.close()
    return True


def eliminarusuario(user_name):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(user_name)
    Fecha = date.today()
    cursor.execute(
        "UPDATE usuarios SET fecha_vencimiento = ? WHERE user_name = ?", (Fecha, user_name))
    conexion.commit()
    conexion.close()
    return True


def fecha():
    Fecha = date.today()
    return Fecha

def registrarprovedor(id, nombre, correo, direccion, telefono, pais):
    conexion = sqlite3.connect("Polaris")
    print("Esto ingresa desde la funcion: "+pais)
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO proveedores VALUES (?,?,?,?,?,?)",
        (id, nombre,  correo, direccion, telefono, pais))
        conexion.commit()
        return True


    except:
        return False 
    

# Consultar Pais
def consultarpais():
    conexion = sqlite3.connect('Polaris')

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pais")
    filas = cursor.fetchall()
    conexion.close()
    return filas

def consultarproveedorpais():
    conexion = sqlite3.connect('Polaris')

    cursor = conexion.cursor()
    cursor.execute("SELECT P.idProveedor, P.nombre, P.correo, P.direccion, P.telefono, C.nombrePais FROM proveedores P JOIN pais C WHERE P.idPais = C.idPais")
    filas = cursor.fetchall()
    conexion.close()
    return filas

def actualizarproveedor(id, nombre, correo, direccion, telefono, pais):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(id, nombre, correo, direccion, telefono, pais)
    try:
        cursor.execute(
            "UPDATE proveedores SET nombre = ?, correo = ?, direccion = ?, telefono = ?, idPais = ? WHERE idProveedor = ?", (nombre, correo, direccion, telefono, pais, id))
        conexion.commit()
        conexion.close()
        return True
    except:
        return False

def eliminarproveedor(id):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM proveedores WHERE idProveedor = ?", (id,))
        conexion.commit()
        conexion.close()
        return True
    except:
        return False

def validarproveedorproductos(codigo):
    with sqlite3.connect("Polaris") as conn:
        sql = "select * from producto where idProveedor = ?",(codigo)
        cur = conn.cursor()
        proceso=cur.execute(sql)
        if proceso !=0:
           return True
        else:
            return False


def accion(sql)->int:
    with sqlite3.connect(DBvar) as conn:
        cur = conn.cursor()
        var2 = cur.execute(sql).rowcount()
        if var2 != 0:
            conn.commit()
        return var2

def pruebaborrar(sql)->int:
    
    with sqlite3.connect("Polaris") as conn:

        cur = conn.cursor()
        proceso=cur.execute(sql)
        if proceso !=0:
            print ("hay registros")
        else:
            print("No hay registros")

def borrarproveedor(codigo):
    conexion = sqlite3.connect("Polaris")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM proveedores WHERE idProveedor= ? AND idProveedor NOT IN (SELECT idProveedor FROM producto)", (codigo,))
    resultado = cursor.rowcount
    if resultado != 0:
        conexion.commit()
        conexion.close()
        return True
    else:
        conexion.close()
        return False