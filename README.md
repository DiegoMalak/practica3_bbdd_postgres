# practica3_bbdd_postgres
## Polideportivo

Actividad 3 de la asignatura Sistemas de Gestión Empresarial. Actividad sobre creación de tablas en referencia a un  
Polideportivo e insertar datos.

Este proyecto es un programa en Python para la gestión de un polideportivo. Los clientes pueden matricularse en  
diferentes deportes y toda la información se guarda en una base de datos Postgres.

### Descripción
El programa muestra un menú con opciones para:
1. Dar de alta a un cliente con sus datos personales (nombre completo, DNI, fecha de nacimiento y teléfono).
2. Dar de baja a un cliente.
3. Mostrar los datos personales de un cliente o de todos.
4. Matricular a un cliente en un deporte (tenis, natación, atletismo, baloncesto, futbol).
5. Desmatricular a un cliente en un deporte.
6. Mostrar los deportes de un cliente.
7. Salir.

La clase Clientes tiene atributos para guardar los datos personales y un método llamado `__datos__` para mostrarlos.  
También tiene un método llamado `__deportes__` que muestra los deportes matriculados con su precio. Al matricular a  
un cliente en un deporte, se guarda el nombre del deporte y el horario elegido.

### Requisitos
- Última versión estable de Python
- Servidor Postgres con Docker

### Pasos de ejecución
1. Ejecutar el servidor Postgres con Docker
2. Iniciar el programa con `python menu_polideportivo.py`
3. Seguir las opciones en el menú para gestionar los clientes y deportes.
