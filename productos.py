import sqlite3


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
        "SELECT p.idProducto, p.nombre, p.descripcion, p.cantminima, p.cantdisponible, c.nombre, p.idProveedor, (SELECT ROUND(AVG(valor),1) as avg_amount FROM calificacion WHERE p.idProducto = idProducto GROUP BY idProducto) AS promedio FROM producto p join proveedores c WHERE p.idProveedor = c.idProveedor")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def validarexistenciadeproducto(codigo):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM producto  WHERE idProducto = ?", (codigo,))
    filas = cursor.fetchone()
    conexion.close()
    if filas is None:
        return False
    else:
        return True


def registrarproducto(codigo, nombre, descripcion, cantmin, cantdisp, proveedor):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO producto VALUES (?,?,?,?,?,?)",
                   (codigo, nombre, descripcion, cantmin, cantdisp, proveedor))
    conexion.commit()
    return True


def eliminarproducto(codigo):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM producto WHERE idProducto = ?", (codigo,))
    conexion.commit()
    conexion.close()
    return True


def actualizarproducto(codigo, nombre, descripcion, cantmin, cantdisp, proveedor):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    print(codigo, nombre, descripcion, cantmin, cantdisp, proveedor)
    cursor.execute(
        "UPDATE producto SET nombre = ?, descripcion = ?, cantminima = ?, cantdisponible = ?, idProveedor = ? WHERE idProducto = ?", (nombre, descripcion, cantmin, cantdisp, proveedor, codigo))
    conexion.commit()
    conexion.close()
    return True


def registrarcalifiacion(codigo, valor):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("INSERT INTO calificacion (valor, idProducto) VALUES (?,?)",
                   (valor, codigo))
    conexion.commit()
    return True


def buscarproductoporproveedor(codigo):
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("SELECT p.idProducto, p.nombre, p.descripcion, p.cantminima, p.cantdisponible, c.nombre, ( SELECT ROUND(AVG(valor), 1) AS avg_amount FROM calificacion WHERE p.idProducto=idProducto GROUP BY idProducto) AS promedio FROM producto p JOIN proveedores c WHERE p.idProveedor=c.idProveedor and p.idProveedor=?", (codigo,))
    filas = cursor.fetchall()
    conexion.close()
    print(filas)
    return filas


def listardisponibles():
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("SELECT p.idProducto, p.nombre, p.descripcion, p.cantminima, p.cantdisponible, c.nombre, ( SELECT ROUND(AVG(valor), 1) AS avg_amount FROM calificacion WHERE p.idProducto=idProducto GROUP BY idProducto) AS promedio FROM producto p JOIN proveedores c WHERE p.idProveedor=c.idProveedor and p.cantdisponible>0")
    filas = cursor.fetchall()
    conexion.close()
    print(filas)
    return filas


def productosdebajominimo():
    conexion = sqlite3.connect("Polaris")

    cursor = conexion.cursor()
    cursor.execute("SELECT p.idProducto, p.nombre, p.descripcion, p.cantminima, p.cantdisponible, c.nombre, ( SELECT ROUND(AVG(valor), 1) AS avg_amount FROM calificacion WHERE p.idProducto=idProducto GROUP BY idProducto) AS promedio FROM producto p JOIN proveedores c WHERE p.idProveedor=c.idProveedor and p.cantdisponible<p.cantminima")
    filas = cursor.fetchall()
    conexion.close()
    print(filas)
    return filas
