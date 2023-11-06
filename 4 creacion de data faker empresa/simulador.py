# libreria que se encarga de crear data falsa
from faker import Faker
#tiene un objeto que se encuentra del mismo faker que son los proveedores que se encargan de brindar mayor datos
# los proveedores son algunas opciones que nos brinda faker para poder usarlo
from faker.providers import person,misc

#nos brinda lo basico para tener enteros y esas cosas
fake=Faker()

#ya con esto nuestro faker puede utilizar todos los metodos de proveedor person
#prevee datos de las personas
fake.add_provider(person)

#prevee de numeros aleatorios binarios
fake.add_provider(misc)

# generar 100 personas ficticias
# departamento tiene que ser un numero aleatorio entre 1 y 4
# supervisor tiene que ser aleatorio entre 1 y el valor actual o nula


for id in range(1,151):
    identificador=fake.uuid4()
    nombre=fake.name()
    apellido=fake.last_name()
    departamento=fake.random_int(min=1,max=5)
    if id ==1:
        supervisor="null",
    else:
        supervisor_id=fake.random_int(min=-10,max=id-1)
        supervisor="null" if supervisor_id <=0 else supervisor_id

    texto=f"INSERT INTO PERSONALES(IDENTIFICADOR,NOMBRE,APELLIDO,DEPARTAMENTO_ID,SUPERVISOR_ID) values('{identificador}','{nombre}','{apellido}',{departamento},{supervisor});"
    print(texto)

    # como podemos guardar la impresion de pantalla en un archivo aparte asi
    # python simulador.py > archivo.sql = me guardas toda la impresion en el archivo.sql
    #de esta manera ya creamos nuestra data falsa y solamente lo cargamos a nuestra base de datos y ya