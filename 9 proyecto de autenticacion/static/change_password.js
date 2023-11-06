const pwd1 = document.getElementById("pwd1");
const pwd2 = document.getElementById("pwd2");
const btnEnviar = document.getElementById("btn-enviar");
const correo = document.getElementById("correo");
const formulario = document.getElementById("form-pwd");

btnEnviar.onclick = async (e) => {
    // cuando intente enviar las claves y que no coincidan entonces me mandara un alert y un return para que paralice toda la continuacion del codigo Super!!!
  if (pwd1.value !== pwd2.value) {
    alert("Las contraseñas no coinciden");
    return;
  }

  //cuando haga una peticion ala ruta /change-password alli en esa ruta es donde se debe ejecutar y enviar el correo y la clave
  //es decir como que estuvieramos creando una nueva contrasenia
  //? te voy a explicar xk no hemos considera la url del dominio es que cuando trabajamos con plantillas x defecto se considera fetch que estamos trabajando en un entorno htpp://12.0.0.1:5000 x eso no lo consideramos
  //^ .innerText que sirve para poder sacar el contenido de una etiqueta como la de correo
  const respuesta = await fetch("/change-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: correo.innerText,
      password: pwd1.value,
    }),
  });

  const json = await respuesta.json();
  console.log(respuesta.status);
  console.log(json);

  if (respuesta.status === 400) {
    swal({
      title: json.message,
      icon: "error",
    });
  } else {
    swal({
      title: json.message,
      icon: "success",
    });

    //elimina todo ese contenido del formulario hasta desaparecerlo del body hay personas que intentaran manosearlo o rebar la info x consola entonces xk eso la remuevo
    formulario.remove();
  }
};
