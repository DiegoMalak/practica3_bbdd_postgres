CREATE TABLE CLIENTES(
	DNI VARCHAR PRIMARY KEY,
	NOMBRE VARCHAR UNIQUE,
	FNAC TIMESTAMP,
	TELEFONO NUMBER
);

CREATE TABLE DEPORTES(
	NOMBRE VARCHAR PRIMARY KEY,
	PRECIO NUMBER
);

CREATE TABLE CLIENTES_DEPORTES(
	DNI VARCHAR,
	NOMBRE VARCHAR,
	HORARIO TIME,
	CONSTRAINT FK_CLIENTES FOREIGN KEY(DNI) REFERENCES CLIENTES(DNI),
	CONSTRAINT FK_DEPORTES FOREIGN KEY(NOMBRE) REFERENCES CLIENTES(NOMBRE),
	CONSTRAINT PK_CLIENTES_DEPORTES PRIMARY KEY(DNI, NOMBRE, HORARIO)
);

DROP TABLE CLIENTES_DEPORTES IF EXISTS;  
DROP TABLE DEPORTES IF EXISTS;  
DROP TABLE CLIENTES IF EXISTS;  