import sqlite3
from datetime import datetime

conn = sqlite3.connect('ventas.db')
c = conn.cursor()
c.execute("""create table IF NOT EXISTS venta(
 venta_id INTEGER PRIMARY KEY,
 fecha varchar(20)
)""")

c.execute("""create table IF NOT EXISTS venta_detalle(
 venta_id_detalle INTEGER PRIMARY KEY,
 articulo varchar(20),
 precio float,
 cantidad int,
 venta_id int
)""")

conn.commit()
conn.close()


def ejecutarComando(query):
    conn = sqlite3.connect('ventas.db')
    c = conn.cursor()
    c.execute(str(query))

    conn.commit()
    conn.close()


def ejecutarConsultaBusqueda(query):
    conn = sqlite3.connect('ventas.db')
    c = conn.cursor()
    data = c.execute(str(query))
    datos = data.fetchall()
    i = 0
    total = 0
    print("::::::::::VENTA:::::::::::")
    for d in datos:
        if (i == 0):
            print("Folio: " + str(d[0]) + " Fecha: " + str(d[1]))
            i = i + 1

        print("Nombre : " + str(d[3]) + " , Precio U: " + str(d[4]) + " Cantidad : " +
              str(d[5]))
        total = total + d[4] * d[5]

    print("IVA: ", str((total * 0.16)))
    print("Total cobrado con IVA ", str((total + (total * 0.16))))
    conn.commit()
    conn.close()
    return data


def ejecutarConsultaBusquedaFecha(query):
    conn = sqlite3.connect('ventas.db')
    c = conn.cursor()
    data = c.execute(str(query))
    datos = data.fetchall()
    i = 0
    total = 0

    for d in datos:
        print("::::::::::VENTA:::::::::::")
        print("Folio: " + str(d[0]) + " Fecha: " + str(d[1]))

        print("Nombre : " + str(d[3]) + " , Precio U: " + str(d[4]) + " Cantidad : " +
              str(d[5]))

        total = total + d[5] * d[4]

    print("IVA: ", str((total * 0.16)))
    print("Total cobrado con IVA ", str((total + (total * 0.16))))
    conn.commit()
    conn.close()
    return data


# opcion del menú se inicia en 0 para prepararse en un bucle repetitivo
opcion = 0

# lista principal de todas las ventas
ventas = []


# función que registrar articulos a la venta
def registrarArticulo(folio):
    venta = []
    descripcion = input("Escriba la descripción\n")
    precio = float(input("Precio unitario\n"))
    while(precio<0):
        print("El precio unitario debe ser mayor a 0")
        precio = float(input("Precio unitario\n"))

    cantidad = int(input("Escriba la cantidad\n"))
    while (cantidad < 0):
        print("La cantidad debe ser mayor a 0")
        cantidad = int(input("Escriba la cantidad\n"))

    # Se carga a la tabla del detalle de la venta

    query = 'insert into venta_detalle (articulo,precio,cantidad,venta_id) values(\'' + str(
        descripcion) + '\' ,\'' + str(precio) + '\',\'' + str(cantidad) + '\',\'' + str(folio) + '\')'
    ejecutarComando(query)

    # Una vez que se pide la información Desc, Precio y Cantidad, se almacenan en una lista
    #para posterior almacenarla en uan lista principal (lista anidadad)
    venta.append(descripcion)
    venta.append(precio)
    venta.append(cantidad)
    print("--Articulo agregado---\n")
    return venta


# función para escribirVentas en memoria, en un archivo CSV
def escribirVentas():
    with open('ventas.csv', 'w') as filehandle:
        for listitem in ventas:
            # Crea el archivo CSV con la información de la lista separados por PIPES |
            filehandle.write('%s|' % listitem)


# Empieza ejecución del programa mediante un menú de opciones, se repetirá hasta que digite la opción 4 que es SALIR
while (opcion != 4):
    opcion = int(input("Menu\n1.-Registrar venta\n2.-Consultar Venta\n3.-Reporte de ventas por fecha\n4.-Salir\n"))

    while(opcion<1 or  opcion>4):
        print("Por favor selecccione una opción valida")
        opcion = int(input("Menu\n1.-Registrar venta\n2.-Consultar Venta\n3.-Reporte de ventas por fecha\n4.-Salir\n"))

    if opcion == 1:
        subopcion = 0
        # Declaramos una lista que almacenara una lista de articulos
        detalles_venta = []
        fecha = ""
        banderaFecha = True
        while banderaFecha:
            try:
                fecha = input("Ingresa una fecha en el formato YYYY-MM-DD: ")
                datetime.strptime(fecha, '%Y-%m-%d')
                banderaFecha = False
            except ValueError:
                print("Fecha inválida")
                banderaFecha=True

        folio = int(input("Escriba el folio\n"))
        while(folio<0):
            print("Por favor escriba un folio mayor a 0")
            folio = int(input("Escriba el folio\n"))
        query = 'insert into venta (venta_id,fecha) values(' + str(folio) + ',\'' + str(fecha) + '\')'
        ejecutarComando(query)

        subdetalle = []
        # Almacenamos fecha y folio de la venta
        subdetalle.append(fecha)
        subdetalle.append(folio)
        detalles_venta.append(subdetalle)
        total = 0
        # se crea un submenú para pedir al usuario si continua agregando articulos a la venta
        while (subopcion != 2):
            subopcion = int(input("1.-Agregar articulo\n2.-Cerrar esta venta\n"))
            while(subopcion<1 or subopcion>2):
                print("Por favor seleccione una opción valida")
                subopcion = int(input("1.-Agregar articulo\n2.-Cerrar esta venta\n"))
            if (subopcion == 1):
                # Si ingresa 1, el programa invocará a la funciión registrarArticulo()
                #para almacenar dicho articulo a la lista subdetalle
                items = []
                items = registrarArticulo(folio)
                total = total + (items[1] * items[2])

                detalles_venta.append(items)

            if (subopcion == 2):
                # Cierra una venta y la termina agregando a la lista principal Ventas
                ventas.append(detalles_venta)
                print("IVA: ", str((total * 0.16)))
                print("Total a pagar con IVA ", str((total + (total * 0.16))))
                print("-----Venta regitrada-----\n")

    if opcion == 2:
        # Consulta venta con el folio
        folio = int(input("Escribe el folio de la venta\n"))

        ejecutarConsultaBusqueda(
            "SELECT * FROM venta inner join venta_detalle on venta.venta_id=venta_detalle.venta_id where venta.venta_id= " + str(
                folio))

    if opcion == 3:
        #Consulta venta con la fecha 
        fecha = input("Fecha de las ventas\n")
        ejecutarConsultaBusquedaFecha(
            "SELECT * FROM venta inner join venta_detalle on venta.venta_id=venta_detalle.venta_id where venta.fecha= '" + str(
                fecha) + "'")

    if opcion == 4:
        # Una vez que finalizamos el programa, las listas serán almacedas en un archivo CSV
        escribirVentas()
        print("Ventas almacenadas en memoria")
        # Finaliza
        print("Hasta luego")

