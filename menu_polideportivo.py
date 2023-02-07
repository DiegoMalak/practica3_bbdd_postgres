'''
Crea un proyecto nuevo en Python llamado Polideportivo.
• Escribe un programa en Python para la gestión de un Polideportivo cuyos clientes pueden
matricularse en varios deportes. La aplicación creada se conectará con una base de datos
Postgres para guardar y consultar los datos.
• El programa mostrará un menú con las siguientes opciones:
1. Dar de alta un cliente con sus datos personales
2. Dar de baja un cliente
3. Mostrar los datos personales de un cliente o de todos
4. Matricular a un cliente en un deporte
5. Desmatricular a un cliente en un deporte
6. Mostrar los deportes de un cliente
7. Salir
• Crea una clase llamada Clientes con los siguientes atributos para guardar los datos personales
de los clientes: nombre completo, dni, fecha de nacimiento y teléfono.
• Los deportes que ofrece el polideportivo son: tenis, natación, atletismo, baloncesto y futbol.
• Los datos que deben guardarse de los deportes son nombre del deporte y precio/hora.
• La clase Clientes tendrá un método llamado __datos__ que permita mostrar los datos
personales de un cliente.
• La clase Clientes tendrá un método llamado __deportes__ que permita mostrar el nombre de
los deportes con su precio en los que está matriculado un cliente.
• Al matricular a un cliente en un deporte se guardará el nombre del deporte y el horario
elegido.
• El programa realizará todas las operaciones tanto de creación de la base de datos como de la
gestión del polideportivo.
• Toda la información relativa a los clientes se guardará en la base de datos Postgres.
• Diagrama Entidad-Relación de la Base de Datos en Postgres
'''

import psycopg2
import psycopg2.extras
import pprint
import sys

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

    cursor = conex.cursor()
    print("Conexión exitosa.\n")

    cursor.execute("DROP TABLE IF EXISTS CLIENTES_DEPORTES")
    cursor.execute("DROP TABLE IF EXISTS CLIENTES")
    cursor.execute("DROP TABLE IF EXISTS DEPORTES")
    print("Tablas eliminadas para refrescar...\n")

    cursor.execute("CREATE TABLE CLIENTES (DNI VARCHAR PRIMARY KEY, NOMBRE VARCHAR UNIQUE, FNAC DATE, TELEFONO INTEGER)")
    cursor.execute("CREATE TABLE DEPORTES (NOMBRE VARCHAR PRIMARY KEY, PRECIO INTEGER)")
    cursor.execute("CREATE TABLE CLIENTES_DEPORTES (DNI VARCHAR, NOMBRE VARCHAR, HORARIO TIME, CONSTRAINT FK_CLIENTES FOREIGN KEY(DNI) REFERENCES CLIENTES(DNI), CONSTRAINT FK_DEPORTES FOREIGN KEY(NOMBRE) REFERENCES DEPORTES(NOMBRE), CONSTRAINT PK_CLIENTES_DEPORTES PRIMARY KEY(DNI, NOMBRE, HORARIO))")
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

    cursor.close()

    print("Datos insertados.\n")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error al conectar a la base de datos: ", error)


def menu():
    print('''
        1. Dar de alta un cliente con sus datos personales
        2. Dar de baja un cliente
        3. Mostrar los datos personales de un cliente o de todos
        4. Matricular a un cliente en un deporte
        5. Desmatricular a un cliente en un deporte
        6. Mostrar los deportes de un cliente
        7. Salir
        ''')
    opcion = input("Elige una opción: ")
    # Hacemos un if y elif para cada opción del menú y llamamos a la función correspondiente a cada opción
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

def alta_cliente():
    # Pedimos los datos del cliente
    nombre = input("Nombre: ")
    dni = input("DNI: ")
    fecha_nacimiento = input("Fecha de nacimiento: ")
    telefono = input("Teléfono: ")
    # Creamos la consulta SQL para insertar los datos del cliente en la tabla clientes
    sql = "INSERT INTO clientes (nombre, dni, fecha_nacimiento, telefono) VALUES (%s, %s, %s, %s)"
    # Ejecutamos la consulta SQL
    cursor.execute(sql, (nombre, dni, fecha_nacimiento, telefono))

    # Guardamos los cambios en la base de datos
    conex.commit()
    # Cerramos el cursor
    cursor.close()

def baja_cliente():
    pass

def mostrar_cliente():
    pass

def matricular_cliente():
    pass

def desmatricular_cliente():
    pass
