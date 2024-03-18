-- --------- BASE DE DATOS DE UNA CLINICA -----------

-- esto es para decir que es un comentario
-- comando para crear la base de datos
-- CREATE DATABASE pruebas;
 
-- usar la BD que hemos creado
-- use pruebas;

-- ctrl + entrer = ejecutar el codigo  
-- los nombres de las tablas es bueno crearlos en plural
-- buscar en la doc. de mysql type data for mysql

-- ahora definiremos las columnas de la tabla personas
-- las llaves primarias siempre deben ser unicas e irrepetibles
-- name_col | type_data | [primary key | not null ]
-- unique = el valor no se puede repetir co otro
-- ingresado anteriormente, mas no obliga al usuario a ingresarlo
-- enum (valores que solamente va aceptar)
-- https://dev.mysql.com/doc/refman/8.0/en/data-types.html

CREATE TABLE personas(
-- vamos a definir las columnas de la tabla personas
	id int primary key not null auto_increment unique,
    documento varchar(20),
    tipo_document enum('DNI','C.E.','PASAPORTE','S/ DOCUMENTO'),
	nombre varchar(25),
	apellido varchar(50),
    correo varchar(100) unique,
	sexo enum('FEMENIMO','MASCULINO','NOBINARIO') not null,
	fecha_nacimiento date
);

-- para insertar debemos decirle name_tabla(campos por orden) values(los valores deacuerdo a esos campos)
INSERT INTO personas (documento,tipo_document,nombre,apellido,correo,fecha_nacimiento,sexo)
VALUES('2','DNI','titolas','maquera','mc.jhonaelgmail.com','1990-08-21','MASCULINO');

INSERT INTO personas (documento,tipo_document,nombre,apellido,correo,fecha_nacimiento,sexo)
VALUES('2342432','DNI','ttie','maquera','mc.titolas.com','1990-03-21','MASCULINO');

INSERT INTO personas (documento,tipo_document,nombre,apellido,correo,fecha_nacimiento,sexo)
VALUES('2323423','DNI','jhonatan','23','mc.3e.com','1998-01-3','MASCULINO');

INSERT INTO personas (documento,tipo_document,nombre,apellido,correo,fecha_nacimiento,sexo)
VALUES('3434545','C.E.','mirko','garcia','mc.mirko.com','2345-01-3','FEMENIMO');

-- para mostrar seleccionamos las o (a) columnas que deseamos ver o los campos  y de k tabla
-- el * para selecionar todos los campos
-- si quieres poner campos vacios debemos colocar en los campos null
SELECT * 
FROM personas;

--^ PARA PODER ALTERAR UNA COLUMNA ESTOS COMANDOS
-- para modificar una columna no debe tener valores
-- ALTER TABLE SIRVE PARA ADD, DELETE, CHANGE Y MODIFICAR UNA COLUMNA solamente cambiamos el verbo 
-- ADD = AGREGAR UNA COLUMNA
-- DELETE = ELIMINAR UNA COLUMNA
-- MODIFY = MODIFICAR TIPOS_DATOS UNA COLUMNA
-- CHANGE = CAMBIA EL NOMBRE DE UNA COLUMNA
ALTER TABLE personas MODIFY COLUMN documento varchar(20) unique;
ALTER TABLE personas CHANGE COLUMN NAME_OLD  NAME_NEW TIPO_DATOS;
--  ALTER TABLE personas MODIFY apellido varchar(23);




--^ FILTRACIONNES DE INFORMACION
-- filtrar datos desde una tabla
-- seleccionare todos los campos o columnas de la tabla persona donde el nombre_campo
-- sea igual a jhonatan 
-- filtrar por nombre(nos traera todos los datos con el nombre jhonatan)
-- PODEMOS FILTRAR LOS DATOS DE SUPER ASI CON CONECTORES PARA ESPEFICIAR SUPER FILTRO
SELECT * FROM personas WHERE nombre="jhonatan" AND apellido="23";

-- ELIMINAR UN REGISTRO solo uno si en el apellido no especifica que es unico
-- entonces no lo elimina 
-- xk tomara encueta que hay millones y esto solo borra 1 registro unico 

DELETE FROM personas WHERE apellido = "garcia";

-- drop table personas;

-- ACTUALIZAR UNO O VARIOS REGISTROS
-- actualizar la tabla persona el campo nombre con este valor cuando el id=1 si no le ponen el where fuimos.. por que a todos los registros se le pondran en ese valor

UPDATE PERSONAS 
SET apellido="Ramiro" 
where id=2;

set SQL_SAFE_UPDATES=0;



CREATE TABLE medicos(
id int primary key auto_increment not null,
cmp varchar(5) not null,
nombre varchar(30) not null,
apellido varchar(30) not null
);
-- INSERCION DE MEDICIOS
INSERT INTO medicos(cmp,nombre,apellido) VALUES 
('111','titolas','maquera'),
('222','willy','cohaila'),
('333','solange','pardo'),
('44','pamela','rojas');

SELECT  * FROM medicos;


-- ^asi se crean las relaciones en una BD
-- 1ro crea el campo de alli ese campo lo vas a referenciar sobre cual
-- deseas unirlo tabla(campo)

CREATE TABLE historial_vacunaciones(
id int primary key auto_increment not null,
vacuna enum("PFIZER","SINOPHARM","ASTRAZENECA"),
lote varchar(10),
fecha date,
-- CREA LOS CAMPOS Y LUEGO UNELOS REFERENCIANDO
medico_id int,
paciente_id int,
foreign key(medico_id) references medicos(id),
foreign key(paciente_id) references personas(id)
);
DROP TABLE historial_vacunaciones;
select * from historial_vacunaciones;

INSERT INTO historial_vacunaciones(vacuna,lote,fecha,medico_id,paciente_id) VALUES
('PFIZER','678','2020-02-01',1,1),
('PFIZER','185','2020-03-20',1,2),
('SINOPHARM','158','2020-04-05',2,3),
('SINOPHARM','995',now(),2,4),
('ASTRAZENECA','853',now(),2,4);

-- es recomendable poner las foreign key al final por buenas practicas
-- aveces hay problemas de autogenerado por lo cual queremos eliminar
--  tods los registros que como ivan practiado se expandio arto 
-- entonces tenemos que autogenerarlo desde cero

-- sirve para quitar el modo seguro  a nuestra base de datos por defecto 
-- esta en 1 eso indicara que no podemos eliminar una registro sin usar un where 
-- al poner 0 le decimos que somos pro y podemos hacer lo que sea eliminar
--  ese  registro totalmente siempre con cuidado
-- DELETE FROM HISTORIAL_VACUNACIONES

-- SET SQL_SAFE_UPDATES = 1 //1ro le pones 0 de alli lo cambias a 1 pero lo

-- otro tema de los inner en otro video
-- personas vacunas con la vacuna PFIZER o ASTRAZENECA
SELECT * FROM historial_vacunaciones where vacuna="PFIZER" OR vacuna="ASTRAZENECA";


-- unir consultas de entre 2 tablas el famoso JOIN	
-- es mejor usar intersecciones tablas que esten en interseccion para poder hacer match
-- deben tener algo en comun 
-- lee: traer todos los campos de historial y(inner join) medico on aqui colocamos el
 -- valor en cuyo juntos 
-- nos trae la vacuna y el medicoy asi traemos a la persona mas


-- nos traera 1 la tabla historial junto a la otra tabla medico
-- ON historial_vacunaciones.medico_id =medicos.id; es super poderoso xk dice tiene que estar tanto medico_id como en el medico.id
-- en el caso no este o digamos un medico no tenga historial entonces no lo traera
SELECT * 
FROM historial_vacunaciones 
INNER JOIN medicos
ON historial_vacunaciones.medico_id =medicos.id;


-- se interpreta como historial -> medico E historial -> paciente
SELECT * 
FROM historial_vacunaciones
INNER JOIN medicos 
ON historial_vacunaciones.medico_id=medicos.id
INNER JOIN personas 
ON historial_vacunaciones.paciente_id = personas.id;


-- nos muestra la descripcion de la tabla para saber que campos colocar
-- las fechas es en string osea en 'fecha'
DESC medicos;

--^ tipo de documentos es siempre en caracteres
-- left join(todo lo que concierne en el lado izquierdo y adicionalmente
-- si esta en el lado derecho)
-- traeme todos los medicos cuando en la izquierda haya una inter con 
-- historial cuando medicos.id 
-- sea igual a historial de vacunaciones .id
-- traer todo lo de la izquirda si y no hay igual traelo
-- si se puede hacer join sin tener una relacion o interseccion
-- el on es para hcer match con las 2 tablas tanto con su id
-- me trae todos los medicos (5) y tdos las vacunaciones que han hecho 
-- los medicos y si hay medicos k no han vacuna
-- igual los trae completando valores nulos
-- TRAEME TODO LO DE LA IZQUIERA Y SI HAY UN MATCH CON LA DERECHO TBM TRAELO
select * from medicos
left join historial_vacunaciones
on medicos.id=historial_vacunaciones.medico_id;

-- tengo 4 medicos
select * from medicos;
-- tengo 5 personas con historial que fueron vacunados por 2 medicos nada mas
select * from historial_vacunaciones;

-- es lo mismo inverido hacia la derecha
select * from medicos
right join historial_vacunaciones
on medicos.id=historial_vacunaciones.medico_id;