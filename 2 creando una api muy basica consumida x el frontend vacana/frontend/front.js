BASE_URL="http://127.0.0.1:5000";

let traerProductos=document.getElementById("traerProductos");

let lista=document.getElementById("lista");

let btnAgregar=document.getElementById("btnAgregar");

let inputNombre=document.getElementById("inputNombre");

let inputPrecio=document.getElementById("inputPrecio");

// fetch(`${BASE_URL}/`)
//?recuerda que fetch al colocar la url y el metodo nos retorna la respuesta en una promesa y para consumir esa promesa debemos usar el .then
// fetch(BASE_URL+"/productos",{method:"GET"}).then(respuesta =>{
    //     console.log(respuesta.status);
    // })
crearElemento=(element)=>{
    return document.createElement(element);
}
mostrarProductos=(productos)=>{
    console.log(productos);
    // let contenido="";
    productos.forEach(objProducto => {
        let li=crearElemento("li")
        // contenido +=`<li>${objProducto.nombre} ${objProducto.precio}</li>`;
        li.innerText=`${objProducto.nombre}`;
        lista.appendChild(li);
    });
    // lista.innerHTML = contenido;
}
traerProductos.onclick=()=>{
    //este fecth retorna una promesa con un objeto como status,header,url, json() este metodo va tener el contenido que esta mandando el servidor pero es en formato de promesa x eso debemos hacer nuevamente el then para consumir esa promesa(eso es un anidamiento de promesas promesa tras promesa)

    // como json() retorna un problema tambien puedo consumirla defrente asi pero para ser mas ordenado mejor un anidamiento de promesas
    // respuesta.json().then(res=>{console.log(res)})

    fetch(BASE_URL+"/productos",{method:"GET"}).then(respuesta=>{
        return respuesta.json();
    }).then(resp=>{
        console.log(resp);
        mostrarProductos(resp.content)
    })
}
//Content-Type:application/json;  xk te le doy esa cabecera xk le estoy enviando al body un json como podemos ver si fuera texto seria application/text
btnAgregar.onclick=(e)=>{
    e.preventDefault();
    fetch(`${BASE_URL}/productos`,
    {
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({
            nombre:inputNombre.value,
            precio:+inputPrecio.value
        })
    })
    .then(respuesta=>{
        return respuesta.json()
    })
    .then(resp=>{
        console.log(resp);
    })
}

// otra forma de usarlo con js actualizado mas facil
// traerProductos.onclick=async()=>{
//     const respuesta= await fetch(BASE_URL+"/productos",{method:"GET"})
//     const productos= await respuesta.json();
//     console.log(productos);
// }