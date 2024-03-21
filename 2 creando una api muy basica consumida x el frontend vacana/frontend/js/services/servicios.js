import { BASE_URL } from "../enviroments/enviroments.js";
// traer todos los productos - una sintaxis nueva
// export const getProductos=async()=>{
//     const response=await fetch(`${BASE_URL}`);
//     const json=await response.json();
//     return json;
// }

// sintaxis anteror
export async function getProductos() {
    try {
        const response = await fetch(`${BASE_URL}/productos`, { method: "GET" });
        const json = await response.json();
        return json;
        
    } catch (error) {
        console.log(`El error es: ${error} `)
    }
}

// enviar al servidor los productos
export const postProductos = async (producto) => {
    try {
        const response = await fetch(`${BASE_URL}/productos`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(producto),
        });
        const json = await response.json();
        return json;
        
    } catch (error) {
        console.log(`Error: ${error} `)
        
    }
};

//traer un producto
export const getProducto = async (id) => {
    try {
        const response = await fetch(`${BASE_URL}/producto/${id}`, {
          method: "GET",
        });
        const json = await response.json();
        return json;
        
    } catch (error) {
        console.log(`Error: ${error} `)
        
    }
};

//actualizar un producto
export const putProducto = async (producto, id) => {
    try {
        const response = await fetch(`${BASE_URL}/producto/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: json.stringify(producto),
        });
        const json = response.json();
        return json;
        
    } catch (error) {
        console.log(`Error: ${error} `)
        
    }
};

//eliminar un producto
export const deleteProducto = async (id) => {
    try {
        const response = await fetch(`${BASE_URL}/producto/${id}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        });
        const json = response.json();
        return json;
        
    } catch (error) {
        console.log(`Error: ${error} `)
        
    }
};
