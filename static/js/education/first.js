
function handleClick(){
    let boton = [...document.getElementsByName("boton[]")];
    boton.map(buton =>{
        buton.addEventListener("click",(e) =>{
            buton.setAttribute("disabled", "disabled");
            let button = buton.parentElement.parentElement.getElementsByTagName("td");
            let id = button[0].innerHTML;
            let curso = button[1].innerHTML;
            let asesor = button[2].firstElementChild.firstElementChild.value;
            let json = { result:[id,curso,asesor]}
            if (asesor == ""){
                alert("agregue al asesor para poder asignar curso");
            }
            else{
                guardar(json);
            }
        })
        return buton
    });

}

const enviarPost = (json) => {
	return {
		method: 'POST', // or 'PUT'
		body: JSON.stringify(json), // data can be `string` or {object}!
		headers: {
			'Content-Type': 'application/json'
		}
	}
}

const guardar = (json) =>{
    const url = `/components/guardarAsesorCurso`;	
	fetch(url, enviarPost(json))
		.then(response => response.json())		
		.catch(error => alert('Error:' + error))
		.then(response => {
            alert(response.estado);
            if (response.estado == "Se le asignó curso correctamente al asesor"){                
                tabla(null)
            }
			
            


		});	
}