USE EMPRESA;

DESC PERSONALES;

-- order by clausula permite ordenar la consulta deacuerdo puede ser asc o desc
select *
from departamentos
order by nombre asc;

drop table personales;
drop table departamentos;

-- now() metodo que nos trae la fecha y la hora actual
select now();

-- curdate() metodo que nos trae dia mes y anio 
select curdate();

-- metodo que nos da solamente la hora actual
select curtime();


-- este conjunto de metodos me los devuelve por separado  los de arriba los agrupa
select YEAR(NOW());  #Selecciona el año
select MONTH (NOW()) as mes;  #Selecciona el mes
select DAY(NOW()) as dia; #Selecciona el día
select TIME(NOW()) as hora;  #Selecciona la hora
Select LAST_DAY(NOW()); # Selecciona el ultimo dia del mes

select YEAR("2005-10-12");  #Selecciona el año
select MONTH ("2005-10-12") as mes;  #Selecciona el mes
select DAY(NOW()) as dia; #Selecciona el día
select TIME(NOW()) as hora;  #Selecciona la hora
Select LAST_DAY(NOW()); # Selecciona el ultimo dia del mes

-- como dar formato a las fecha o sea como queremos que sea el orden
-- el metodo Date_format(fecha,formato) nos permite poder hacer eso algunos ejemplos
select Date_format(now(),'%Y/%M/%d'); # '2010/January/12'
select Date_format(now(),'%Y-%M-%d %h:%i:%s %p'); #'2010-January-12 12:34:29 AM'
select Date_format(now(),'%W %d %M %Y'); # 'Tuesday 12 January 2010'
select Date_format(now(),'El año actual es %Y'); # 'El año actual es 2010'

-- algunos formatos que podemos usar
-- %d #Día del mes numérico (00...31)
-- %H #Hora (00...23)
-- %h #Hora (01...12)
-- %i #Minutos, numérico (00...59)
-- %M #Nombre mes (January...December)
-- %m #Mes, numérico (00...12)
-- %p #AM o PM
-- %W #Nombre día semana (Sunday...Saturday)
-- %Y #Año, numérico, cuatro dígitos
-- %y #Año, numérico (dos dígitos)
-- %s #Segundos (00...59)

-- para poder restar 2 fechas
-- DATEDIFF(fecha_1,fecha_2) devuelve el número de días entre la fecha fecha_1 y la fecha_2
SELECT DATEDIFF(NOW(),'2002-11-02'); #cuantos días han pasado
SELECT DATEDIFF(NOW(),'2010-03-20'); #Cuantos días faltan	

-- PARA PODER SACAR LA EDAD RECIBE 1RO EN QUE QUIERES QUE TE DEVUELVA LA DIFERENCIA DE LAS FECHAS
-- PUEDE SER YEAR , MONTH, DAY  2DO FECHA ANTIGUA Y COMO 3ERA PARAMETRO FECHA ACTUAL
-- Y ESE METODO ARA AUTOMATICAMENTE LA DIFERENCIA DE LAS FECHAS
SELECT TIMESTAMPDIFF(MONTH,"1992-08-17",CURDATE()) AS edad;



-- ¿Con qué frecuencia aparece cierto tipo de datos en una tabla? 
-- CON ESTA PREMISA DECIMOS EJMP CUANTOS PERROS TIENE UN DUENO COSAS ASI
-- si usamos el selec nombre tambien al agrupar debemos usar el nombre para agrupacion
#CUANTAS PERSONAS TIENE CADA DEPARTAMENTO
-- la combinacion que hace el gruop by junto con el count es magico por que decimos 
-- cuenta cuantos personas en cada distrito (agrupar por distritos y saber cuantas personas
-- hay en cada distrito)
SELECT COUNT(DEPARTAMENTO_ID) AS CANT_PERSONAS, D.NOMBRE
FROM PERSONALES AS P
INNER JOIN DEPARTAMENTOS AS D
ON D.ID = P.DEPARTAMENTO_ID
GROUP BY DEPARTAMENTO_ID;

SELECT *
FROM PERSONALES;

-- lista de bae de datos
show databases;

-- indica la base de datos seleccionada
select database();
describe personales;

select count(departamento_id),departamentos.nombre
from departamentos
inner join personales
on departamentos.id=personales.departamento_id
order by departamento_id;


#CUANTAS VECES SE REPITE EL NOMBRE DE UNA PERSONA EN CADA DEPARTAMENTO
-- SI EN EL GROUP BY LE HUBIERA PUESTO DEPARTAMENTO_ID SOLO HUBIERA CONTADO DE ESE Y RECUERDA QUE ESE GRUPO 
-- TIENE 5 DATOS NADA MAS ENTONCES LE PONGO DE NOMBRE GROUP BY PARA QUE ME CUENTE DE TODOS LOS NOMBRES REPETI2
SELECT COUNT(DEPARTAMENTO_ID) AS CANT_PERSON, DEPARTAMENTO_ID,NOMBRE
FROM PERSONALES
GROUP BY DEPARTAMENTO_ID,NOMBRE
ORDER BY CANT_PERSON ASC,DEPARTAMENTO_ID ASC,NOMBRE ASC;


# MOSTRAR CUANTOS EMPLEADOS HAY EN EL DEPARTAMENTO-2
#PODEMOS CREAR UNA COLUMNA FICTICIA
SELECT 'DEPARTAMENTO 2' DEPARTAMENTO, COUNT(*) TOTAL
FROM PERSONALES
WHERE DEPARTAMENTO_ID=2;

-- CUANTAS PERSONAS NO TIENE JEFE Y CUANTAS PERSONAS CORRESPONDE A CADA AREA
-- DEPARTAMENTO   |   TOTAL
-- 		1				10
-- 		2				3
-- 		3				5
-- 		4				4

#IS NULL MUY BUENA ES VEZDE USAR EL IGUAL BUENAZO
SELECT COUNT(*),P.NOMBRE,P.APELLIDO,D.NOMBRE,P.DEPARTAMENTO_ID,P.SUPERVISOR_ID
FROM PERSONALES AS P
INNER JOIN DEPARTAMENTOS AS D
ON D.ID=P.DEPARTAMENTO_ID
WHERE P.SUPERVISOR_ID IS NULL
GROUP BY DEPARTAMENTO_ID
ORDER BY 1 DESC;



SELECT PERSONALES.SUPERVISOR_ID
FROM PERSONALES
LEFT JOIN DEPARTAMENTOS
ON PERSONALES.DEPARTAMENTO_ID  != DEPARTAMENTOS.ID;
#WHERE PERSONALES.SUPERVISOR_ID = null;


-- MOSTRAR EL NOMBRE DEL DEPARTAMENTO Y SU CANTIDAD DE EMPLEADOS

-- 		DEPARTAMENTO		|		CANTIDAD DE EMPLEADOS
-- 		VENTAS				|				150
-- 		ADMINISTRACION		|				200
-- 		FINANZAS			|				85
-- 		MARKETING			|				56

SELECT D.NOMBRE,COUNT(P.ID) AS 'CANT_EMPLEADOS'
FROM DEPARTAMENTOS AS D
INNER JOIN PERSONALES AS P
ON D.ID = P.DEPARTAMENTO_ID
GROUP BY D.NOMBRE;





