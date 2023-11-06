#mirar el tutorial de la doc de mysql
from faker import Faker
from faker.providers import person

fake=Faker()
fake.add_provider(person)

for alumno in range(1,51):
    nombre=fake.first_name()
    apellido=fake.last_name()
    correo=fake.email()
    query=f"INSERT INTO ALUMNOS (nombre,apellido,correo) VALUES('{nombre}','{apellido}','{correo}');"
    print(query)
for alumno_curso in range(75):
    curso=fake.random_int(1,5)
    alumno=fake.random_int(1,50)
    query=f"INSERT INTO ALUMNOS_CURSOS(ID_ALUMNO,ID_CURSO) VALUES ({curso},{alumno});"
    print(query)

#no olvides que para imprimir esto en una archivo aparte tienes que hacer
#py simulador_calificaciones.py > data_calificaciones.sql