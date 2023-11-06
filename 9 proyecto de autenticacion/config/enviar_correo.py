# / esta libreria permite enviar email
# https://docs.python.org/3/library/email.examples.html
# para crear correo electronicos https://docs.python.org/3/library/email.mime.html
# MIME=MultiPurpose Internet Mail Extensions

from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv

load_dotenv()


mensaje = MIMEMultipart()


# AQUI VAMOS A COLOCAR LAS CREDENCIALES DEL ADMINISTRADOR QUE VA ENVIAR LOS CORREOS NO HAY K COLOCAR LAS CREDENCIALES DE LA BASE DE DATOS QUE QUEDE CLARO
# indica desde que correo voy a enviar el correo
mensaje['From'] = environ.get('EMAIL')

# EL SUJETO O EL MOTIVO DE LO QUE ESTAMOS REALIZANDO
mensaje['Subject'] = 'Solicitud de restauracion de la contrasenia'

# LA CLAVE DE MI CORREO
password = environ.get('EMAIL_PASSWORD')


def enviarCorreo(destinatario, cuerpo):
    """funcion que se encarga de enviar el correo"""

    # a quien voy a mandar el correo puede ser un [] o uno solo destinatario
    mensaje['To'] = destinatario

    texto = cuerpo
    # Luego de definir el cuerpo del correo agregamos al mensaje mediante su metodo attach y en formato MIMEText en el cual recibira un texto y luego el format a convertir, si quieres enviar un html entonces pondremos en 'html', si queremos enviar un texto 'plain' va poder renderizar html vacano o texto nada mas todo lo que le mandemos
    mensaje.attach(MIMEText(texto, 'html'))

    try:
        # configurar el servidor SMTP como nuestro correo es gmail entonces debemos buscar smtp gmail si fuera otro smtp outlook etc

        # smtplib.SMTP recibe 2 parametros Nombre de dominio completo del servicio SMTP y el puerto que es 587

        # para mayor informacion recibe la doc
        # https://support.google.com/a/answer/176600?hl=es#zippy=%2Cutilizar-el-servidor-smtp-de-gmail

        #otro caso profe si tenemos correo institucionales que hacemos entonces en tu CPanel deberias tener las credenciales de SMTP
        servidorSMTP = smtplib.SMTP('smtp.gmail.com', 587)

        #luego indicar el protocolo de tranferencia (tls = 587)
        servidorSMTP.starttls()

        # Inicio sesion en el servidor de correos con las credenciales asignadas previamente
        #sirve para logearnos a nuestro servidor de gmail o lo que sea
        servidorSMTP.login(user=mensaje.get('From'), password=password)

        #lo ultimo que nos falta seria enviar el correo ya que estamos logeados
        servidorSMTP.sendmail(
            #emisor del mensaje osea el administrador
            from_addr=mensaje.get('From'),
            #destinarato
            to_addrs=mensaje.get('To'),
            #ese metodo as_string() va convertir el mensaje a string para ser enviado correctamente
            msg=mensaje.as_string()
        )
        # cerrar la sesion de mi correo
        servidorSMTP.quit()
    except Exception as e:
        print(e)


#con esto puedes adjuntar imagenes o doc normal al correcto


#antes solamente se podia acceder solamente al backend tabm se renderizaba codigo html entonces
# si nosotros renderizamos html en nuestro backend dejaria de ser una tecnologia api rest xk api rest solamente es de front k consume servicios y el backend que responde de esa peticion y no pasa eso entonces null