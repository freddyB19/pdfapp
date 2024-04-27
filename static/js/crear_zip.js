import * as js_z from "./jszip.js";

const ObtenerImagenes = ({}) => {
	const lista_imagenes = document.querySelectorAll("a[class='btn btn-success']");
	return [...lista_imagenes];
};

const CrearArchivoZip = ({imagenes = []}) => {
	const zip = new JSZip();

	const carpeta = zip.folder('imagenes');

	imagenes.forEach((ele) => {
		let textEncoder = new TextEncoder().encode(ele.href)
		carpeta.file(ele.download, textEncoder, {uint8array: true});
	})

	const gen_zip = zip.generateAsync({type: 'base64'});

	return gen_zip
};

const CrearBotonDescarga = ({archivo_zip}) => {
	const a = document.createElement('a');
	a.href = `data:application/zip;base64, ${archivo_zip}`;
	a.className = 'btn btn-outline-info'
	a.textContent = "Descargar Todo";


	document.querySelector("#descargar-todo").appendChild(a);
}


const Main = async ({}) => {
	let lista_imagenes = ObtenerImagenes({});

	if (lista_imagenes.length > 0){
		lista_imagenes
		let archivo_zip = await CrearArchivoZip({imagenes: lista_imagenes});

		CrearBotonDescarga({archivo_zip})
	} 
};


window.addEventListener('load', Main);
