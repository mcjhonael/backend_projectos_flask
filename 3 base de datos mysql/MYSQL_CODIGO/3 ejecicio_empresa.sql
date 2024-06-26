CREATE TABLE departamentos(
id int primary key not null auto_increment,
nombre varchar(30)
);
-- un personal a la vez puede ser superior de otro personal
CREATE TABLE personales(
id int not null primary key auto_increment,
identificador text,
nombre varchar(30),
apellido varchar(30),
departamento_id int,
supervisor_id int,
foreign key (departamento_id) references departamentos(id),
foreign key (supervisor_id) references personales(id)
);

-- 1. TRAER TODAS LAS PERSONAS CUYO NOMBRES SEA KEVIN
SELECT * 
FROM PERSONALES
WHERE NOMBRE="KEVIN";




-- 2. TRAER TODAS LAS PERSONAS CUYO DEPARTAMENTO SEA EL 2
SELECT *
FROM PERSONALES
WHERE DEPARTAMENTO_ID=2;



-- 3. DEL EJERCICIO NUMERO 2, ADD EL NOMBRE DEL DEPARTAMENTO NO 
-- SOLAMENTE DIGA DEPARTAMENTO_ID=2 | SI NO "PUBLICIDAD"
-- SIN EL wHERE ME TRAE TODOS LOS DATOS DE LA UNION
-- ONLY GET NOMBRE,APELLIDO,NOMBRE_DEPARTAMENTO
-- COLOCAR EL AS ES LA FORMA FORMAL PARA PODER LLENAR A 
-- hay casos donde las columnas sin iguales en otras tablas para no confundirse mejor
-- le colocamos un alias
-- ENTENDER PERO SI NO SE VE FEO
-- PROFE NO ES MUY LARGO ESCRIBIR ESTO SE ME VA IR LA VIDA ESCRIBIENDO ESTO




SELECT PERSONALES.NOMBRE AS 
NOMBRE_PERSONAL,PERSONALES.APELLIDO AS 
PERSONAL_APELLIDO, 
DEPARTAMENTOS.ID,DEPARTAMENTOS.NOMBRE AS 
NOMBRE_DEPARTAMENTO
FROM PERSONALES
INNER JOIN DEPARTAMENTOS 
ON PERSONALES.DEPARTAMENTO_ID=DEPARTAMENTOS.ID
WHERE DEPARTAMENTO_ID=2;


-- ALIAS EN LAS TABLAS
SELECT P.x AS 
NOMBRE_PERSONAL,P.APELLIDO AS 
PERSONAL_APELLIDO, D.ID,D.NOMBRE AS 
NOMBRE_DEPARTAMENTO
FROM PERSONALES AS P
INNER JOIN DEPARTAMENTOS  AS D
ON P.DEPARTAMENTO_ID=D.ID;
-- WHERE DEPARTAMENTO_ID=2;

-- NOMBRE_EMPLEADO | APELLIDO_EMPLEADO | NOMBRE_SUPERVISOR |
--  APELLIDO_SUPERVISOR | NOMBRE_DEPARTAMENTO
-- EUNIN DE EMPLEADO Y EMPLEADO(SUPERVISOR)
-- RECUERDA QUE EL INNER JOIN VA DEVOLVER TODO LO QUE TENGA EN 
-- COMUN AMBOS LADOS SI NO TIENE UNLADO ALGO NO LO VA TRAER LUEGO
--  SI HAGO UN RIGHT JOIN
-- ENTONCES ME TRAERA TODOS LOS EMPLEADOS(SUPERVISOR)
-- SI HACEMOS LEFT JOIN TRAERA TODOS LOS EMPLEADOS AUN
--  ASI TENGAN O NO TENGAN SUPERVISOR
-- JOIN QUE TENGAN COSAS EN COMUN AMBOS


SELECT P.NOMBRE AS 
NOMBRE_EMPLEADO,P.APELLIDO AS 
APELLIDO_EMPLEADO,S.NOMBRE AS 
NOMBRE_SUPERVISOR,S.APELLIDO AS 
APELLIDO_SUPERVISOR
FROM PERSONALES AS P 
LEFT JOIN PERSONALES AS S
ON P.SUPERVISOR_ID = S.ID;

