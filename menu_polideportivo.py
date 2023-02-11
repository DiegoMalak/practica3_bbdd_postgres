import psycopg2
import psycopg2.extras
import pprint
import sys
# Importamos la clase Cliente en la que hemos definido los datos de los clientes.
from cliente import Cliente

# Destruimos cualquier base de datos que hubiera.
conex = None
print("Conexión a la base de datos PostgreSQL...")

try:
    conex = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="diego12345678",
        port = "5432"
    )

    # Creamos un cursor para poder ejecutar las sentencias SQL.
    cursor = conex.cursor()
    print("Conexión exitosa.\n")

    # Eliminamos las tablas para refrescarlas.
    cursor.execute("DROP TABLE IF EXISTS CLIENTES_DEPORTES")
    cursor.execute("DROP TABLE IF EXISTS CLIENTES")
    cursor.execute("DROP TABLE IF EXISTS DEPORTES")
    print("Tablas eliminadas para refrescar...\n")

    # Creamos las tablas de la base de datos y en la tabla clientes deportes creamos un delete cascade para que cuando
    # se borre un cliente se borren sus datos sin tener que borrarlos manualmente, ni que borre nada indeseado.
    cursor.execute("CREATE TABLE CLIENTES (DNI VARCHAR PRIMARY KEY, NOMBRE VARCHAR UNIQUE, FNAC DATE, TELEFONO INTEGER)")
    cursor.execute("CREATE TABLE DEPORTES (NOMBRE VARCHAR PRIMARY KEY, PRECIO INTEGER)")
    cursor.execute("CREATE TABLE CLIENTES_DEPORTES (DNI VARCHAR, NOMBRE VARCHAR, HORARIO TIME, CONSTRAINT FK_CLIENTES FOREIGN KEY(DNI) REFERENCES CLIENTES(DNI) ON DELETE CASCADE, CONSTRAINT FK_DEPORTES FOREIGN KEY(NOMBRE) REFERENCES DEPORTES(NOMBRE), CONSTRAINT PK_CLIENTES_DEPORTES PRIMARY KEY(DNI, NOMBRE, HORARIO))")
    print("Tablas creadas.\n")

    # Hacemos insert en la tabla clientes.
    cursor.execute("INSERT INTO CLIENTES (DNI, NOMBRE, FNAC, TELEFONO) VALUES ('12345678A', 'Diego', '1990-01-01', 123456789)")
    cursor.execute("INSERT INTO CLIENTES (DNI, NOMBRE, FNAC, TELEFONO) VALUES ('87654321B', 'Juan', '1996-01-21', 198765432)")
    cursor.execute("INSERT INTO CLIENTES (DNI, NOMBRE, FNAC, TELEFONO) VALUES ('12345678C', 'Pedro', '1997-01-11', 123456780)")
    cursor.execute("INSERT INTO CLIENTES (DNI, NOMBRE, FNAC, TELEFONO) VALUES ('87654321D', 'Luis', '1994-01-09', 124356789)")
    cursor.execute("INSERT INTO CLIENTES (DNI, NOMBRE, FNAC, TELEFONO) VALUES ('12345678E', 'Ana', '1992-01-02', 123456781)")

    # Hacemos insert en la tabla deportes.
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES ('tenis', 10)")
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES ('natacion', 15)")
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES ('atletismo', 20)")
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES ('baloncesto', 25)")
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES ('futbol', 30)")

    # Hacemos insert en la tabla clientes_deportes.
    # Como le hemos puesto clave primaria a la unión del dni, nombre y horario así me permite inscribir a la misma persona
    # en el mismo deporte en diferentes horarios.
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('12345678A', 'tenis', '10:00:00')")
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('87654321B', 'natacion', '11:00:00')")
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('12345678C', 'atletismo', '12:00:00')")
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('87654321D', 'baloncesto', '13:00:00')")
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('12345678E', 'futbol', '14:00:00')")
    cursor.execute("INSERT INTO CLIENTES_DEPORTES (DNI, NOMBRE, HORARIO) VALUES ('12345678A', 'tenis', '15:00:00')")

    # Hacemos commit para que se guarden los cambios.
    conex.commit()
    # Cerramos el cursor.
    cursor.close()
    print("Datos insertados.\n")

# Añadimos un except para que nos muestre un mensaje de error si no se ha podido conectar a la base de datos.
except (Exception, psycopg2.DatabaseError) as error:
    print("Error al conectar a la base de datos: ", error)

# Creamos una función para el menú.
def menu():
    print("\n-----------------------------------------------------------")
    print("Bienvenido al gimnasio. Elige una opción del menú: ")
    print("-----------------------------------------------------------")
    # Imprimimos las opciones del menú.
    print('''
        1. Dar de alta un cliente con sus datos personales
        2. Dar de baja un cliente
        3. Mostrar los datos personales de un cliente o de todos
        4. Matricular a un cliente en un deporte
        5. Desmatricular a un cliente en un deporte
        6. Mostrar los deportes de un cliente
        7. Salir
        ''')
    # Pedimos al usuario que elija una opción del 1 al 7.
    opcion = input("Elige una opción: ")
    # Hacemos un if y elif para cada opción del menú y llamamos a la función correspondiente a cada opción.
    # Si el usuario elige una opción que no está en el menú le saldrá un mensaje de error.
    if opcion == "1":
        alta_cliente()
    elif opcion == "2":
        baja_cliente()
    elif opcion == "3":
        mostrar_cliente()
    elif opcion == "4":
        matricular_cliente()
    elif opcion == "5":
        desmatricular_cliente()
    elif opcion == "6":
        mostrar_deportes()
    elif opcion == "7":
        print("Hasta pronto")
        if conex is not None:
            conex.close()
        sys.exit()
    else:
        print("Opción INCORRECTA, elige una opción del 1 al 7")

# Creamos una función para dar de alta un cliente.
def alta_cliente():
    # Pedimos los datos del cliente nuevo.
    nombre = input("Nombre: ")
    dni = input("DNI: ")
    fecha_nacimiento = input("Fecha de nacimiento: ")
    telefono = input("Teléfono: ")
    # Creamos la consulta SQL para insertar los datos del cliente en la tabla clientes
    sql = "INSERT INTO clientes (nombre, dni, fnac, telefono) VALUES (%s, %s, %s, %s)"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    # Le pasamos los datos del cliente a la consulta SQL para que se inserten en la tabla clientes.
    cursor.execute(sql, (nombre, dni, fecha_nacimiento, telefono))
    # Guardamos los cambios en la base de datos
    conex.commit()
    print("Cliente insertado correctamente")

    # Cerramos el cursor
    cursor.close()

# Creamos una función para dar de baja un cliente.
def baja_cliente():
    # Pedimos el dni del cliente que queremos dar de baja.
    dni = input("DNI: ")
    # Creamos la consulta SQL para eliminar el cliente de la tabla clientes con el dni que hemos introducido.
    sql = "DELETE FROM clientes WHERE dni = %s"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    # Le pasamos el dni del cliente a la consulta SQL para que se elimine de la tabla clientes.
    cursor.execute(sql, (dni,))
    # Comprobamos si el cliente existe, si no existe le saldrá un mensaje de error.
    # Si existe se eliminará el cliente de la tabla clientes.
    if cursor.rowcount == 0:
        print("No existe ningún cliente con ese DNI")
    else:
        # Guardamos los cambios en la base de datos.
        conex.commit()
        # Mensaje de confirmación de que el cliente se ha eliminado correctamente.
        print("Cliente eliminado")

    # Cerramos el cursor.
    cursor.close()

# Creamos una función para mostrar los datos de un cliente o de todos los clientes.
def mostrar_cliente():
    # Pedimos al usuario que elija si quiere ver los datos de un cliente o de todos los clientes.
    opcion = None
    # Hacemos un while para que el usuario tenga que elegir una opción correcta. (1 o 2)
    while opcion != "1" and opcion != "2":
        # Pedimos al usuario que elija una opción.
        opcion = input("1. Dni. 2. Todos. (1/2): ")

    # Iniciamos el cursor.
    cursor = conex.cursor()
    # Hacemos un if y elif para cada opción del menú y llamamos a la función correspondiente a cada opción.
    # En caso de que no se elija una opción correcta le saldrá un mensaje de error.
    # Con la opción 1 mostramos los datos de un cliente con el dni que hemos introducido.
    if opcion == "1":
        # Pedimos el dni del cliente que queremos mostrar.
        dni = input("DNI: ")
        # Creamos la consulta SQL para mostrar los datos del cliente con el dni que hemos introducido.
        sql = "SELECT * FROM clientes WHERE dni = %s"
        # Ejecutamos la consulta SQL.
        cursor.execute(sql, (dni,))
        # Usamos el método fetchone() para obtener el cliente con el dni que hemos introducido.
        cliente = cursor.fetchone()
        # Comprobamos si el cliente existe, si no existe le saldrá un mensaje de error.
        # Si existe se mostrarán los datos del cliente.
        if cliente is None:
            print("No existe ningún cliente con ese DNI")
        else:
            # Creamos un objeto de la clase Cliente y le pasamos los datos del cliente.
            c = Cliente(cliente[0], cliente[1], cliente[2], cliente[3], [])
            # Mostramos los datos del cliente.
            print(c.__datos__())
    # Con la opción 2 mostramos los datos de todos los clientes.
    elif opcion == "2":
        # Creamos la consulta SQL para mostrar los datos de todos los clientes.
        sql = "SELECT * FROM clientes"
        # Ejecutamos la consulta SQL.
        cursor.execute(sql)
        # Usamos el for para recorrer todos los clientes y mostrar sus datos.
        for cliente in cursor:
            # Creamos un objeto de la clase Cliente y le pasamos los datos del cliente.
            c = Cliente(cliente[0], cliente[1], cliente[2], cliente[3], [])
            # Mostramos los datos del cliente.
            print(c.__datos__())
    # En caso de que no se elija una opción correcta le saldrá un mensaje de error.
    else:
        print("Opción incorrecta")

    # Cerramos el cursor.
    cursor.close()

# Creamos la función para matricular_clientes.
def matricular_cliente():
    # Al matricular un cliente en un deporte se guardará el dni, nombre del deporte y el horario elegido.
    # Pedimos los datos del cliente que queremos matricular.
    dni = input("DNI: ")
    print("Deportes disponibles: ")
    # Creamos una consulta SQL para mostrar los deportes disponibles.
    sql = "SELECT * FROM deportes"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    cursor.execute(sql)
    # Usamos el for para recorrer todos los deportes y mostrar sus datos.
    for deporte in cursor:
        print(deporte)
    # Pedimos el nombre del deporte que queremos matricular.
    nombre = input("Nombre del deporte: ")
    # Pedimos el horario del deporte que queremos matricular.
    horario = input("Horario: ")
    # Creamos la consulta SQL para insertar los datos del cliente en la tabla clientes_deportes.
    sql = "INSERT INTO clientes_deportes (dni, nombre, horario) VALUES (%s, %s, %s)"
    # Ejecutamos la consulta SQL.
    cursor.execute(sql, (dni, nombre, horario))
    # Guardamos los cambios en la base de datos.
    conex.commit()
    # Mensaje de confirmación de que el cliente se ha matriculado correctamente.
    print("Cliente matriculado")

    # Cerramos el cursor.
    cursor.close()

# Creamos la función para desmatricular_clientes.
def desmatricular_cliente():
    # Solicitamos los datos del cliente que queremos desmatricular.
    dni = input("DNI: ")
    '''
    LA SIGUIENTE PARTE ES PARA PODER VER LOS DEPORTES QUE TIENE EL CLIENTE Y PODER ELIMINARLO SIN FALLAR.
    '''
    print("Deportes del cliente: ")
    # Creamos una consulta SQL para mostrar los deportes del cliente con el dni que hemos introducido.
    sql = "SELECT deportes.nombre, deportes.precio, clientes_deportes.horario FROM deportes "
    sql += "INNER JOIN clientes_deportes ON deportes.nombre = clientes_deportes.nombre "
    sql += "WHERE clientes_deportes.dni = %s"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    # Le pasamos el dni del cliente a la consulta SQL para que se muestren los deportes del cliente.
    cursor.execute(sql, (dni,))
    '''
    FIN DE LA PARTE PARA PODER VER LOS DEPORTES QUE TIENE EL CLIENTE Y PODER ELIMINARLO SIN FALLAR.
    '''
    # Usamos el for para recorrer todos los deportes del cliente y mostrarlos.
    for deporte in cursor:
        # Mostramos los deportes del cliente.
        print(deporte)
    # Ahora que sabemos los deportes que tiene el cliente, le pedimos que elija uno de los deportes.
    deporte = input("Deporte: ")
    # Creamos la consulta SQL para eliminar el cliente de la tabla clientes_deportes.
    sql = "DELETE FROM clientes_deportes WHERE dni = %s AND nombre = %s"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    # Le pasamos los datos del cliente a la consulta SQL para que se elimine de la tabla clientes_deportes.
    cursor.execute(sql, (dni, deporte))
    # Comprobamos si el cliente y el deporte existen, si no existen le saldrá un mensaje de error.
    # Si existe el dni y el deporte se eliminará el cliente de la tabla clientes_deportes.
    if cursor.rowcount == 0:
        print("No existe ningún cliente con ese DNI o el deporte no existe")
    else:
        # Guardamos los cambios en la base de datos.
        conex.commit()
        # Mensaje de confirmación de que el cliente se ha desmatriculado correctamente.
        print("Cliente desmatriculado")

    # Cerramos el cursor.
    cursor.close()

# Creamos la función para mostrar los deportes de un cliente.
def mostrar_deportes():
    # Pedimos que ponga el dni del cliente que queremos mostrar los deportes.
    dni = input("DNI: ")
    # Creamos la consulta SQL para mostrar los deportes del cliente con el dni que hemos introducido.
    sql = "SELECT deportes.nombre, deportes.precio, clientes_deportes.horario FROM deportes "
    sql += "INNER JOIN clientes_deportes ON deportes.nombre = clientes_deportes.nombre "
    sql += "WHERE clientes_deportes.dni = %s"
    # Ejecutamos la consulta SQL.
    cursor = conex.cursor()
    # Le pasamos el dni del cliente a la consulta SQL para que se muestren los deportes del cliente.
    cursor.execute(sql, (dni,))

    # Creamos un objeto de la clase Cliente y le pasamos los datos del cliente.
    c = Cliente("", "", "", "", [])
    # Usamos el for para recorrer todos los deportes del cliente y mostrar sus datos.
    for deporte in cursor:
        tupla = (deporte[0], deporte[1], deporte[2])
        # Añadimos los deportes del cliente a la lista de deportes del cliente.
        c.deportes.append(tupla)

    # Imprimimos los deportes del cliente.
    print(c.__deportes__())
    # Cerramos el cursor.
    cursor.close()

# Arrancamos el programa.
if __name__ == "__main__":
    while True:
        menu()
