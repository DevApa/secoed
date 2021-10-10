let input = document.getElementById('autocomplete-input');
const formatJson = {
    course: "BD",
    questions:[
        {
            question:"Pregunta 1",
            choices:[
                {
                    descripcion:"respuesta 1",
                    isCorrect: true,
                },
                {
                    descripcion:"respuesta 2",
                    isCorrect: false,
                },
                {
                    descripcion:"respuesta 3",
                    isCorrect: true,
                },
                {
                    descripcion:"respuesta 4",
                    isCorrect: false,
                },
            ],
        },
    ]
}
// console.log(JSON.stringify(formatJson,null,2))

let autocomplete_results = document.getElementById("autocomplete-results");

let tb = document.getElementById("tb");

console.log(new Date(1629781200 * 1000).toLocaleDateString())
input.addEventListener("keyup",(e) =>{
    autocomplete_results.style.display = "block";

    let key = e.target.value;

    if (key.length > 0){
        //buscar 
        // search(key);
        tabla(key);

    }
    else{
        tabla(null)
    }
});

const search = (key) =>{
    console.log("key")
    const url = `/components/cursoFiltro/${key}`;
    fetch(url, {
        method: "get",
        headers: new Headers(),
        mode: "cors",
        cache: "default",
    })
    .then((res) => res.json())
    .then((data)=>{
        // if(Array.isArray(data)){
            build_list(
                data.data.map((item) =>{
                    items = [item.id_curso,item.tipo]
                    return items;
                })
            );
        // }
        // else{
        //     build_list()
        // }


    })
    .catch(e =>{console.log(e)})
}


function eventos(){
    let inputs = [...document.getElementsByName("asesores[]")];//El operador "..." spread sirve para convertir a array
    // let autos = [...document.getElementsByName("autocomplet[]")]; 
    ///
    const build_list = (items = [],ulSelected) =>{

        ulSelected.innerHTML = "";
        items.map((item) => {
            ulSelected.innerHTML += `<li value ="${item[1]}">${item[0]}</li>`
        })
    }
    // autos.map((autocompleteField,index) => {
    //     autocompleteField.style.display = 'block';
    inputs.map(input =>{        
        input.addEventListener("keyup", ({target})=>{
            let key = target.value;
            if (key.length > 0){

                let ulSelected = input.parentElement.lastElementChild;
                ulSelected.style.display = 'block';
                buscar(key, ulSelected);
                ulSelected.addEventListener("click",(e) =>{
                    target.value = e.target.innerHTML;
                    ulSelected.style.display = 'none';
                })
            }
        })
        return input;
    })


    //////
    const buscar = (key,autocompleteField) =>{
        const url = `/components/asesor/${key}`;
        fetch(url, {
            method: "get",
            headers: new Headers(),
            mode: "cors",
            cache: "default",
        })
        .then((res) => res.json())
        .then((data)=>{
            // if(Array.isArray(data)){
                return build_list(
                    data.data.map((item) =>{
                        items = [item.nombre,item.id_asesor]
                        return items;
                    }), autocompleteField
                );
            // }
            // else{
            //     build_list()
            // }
        })
        .catch(e =>{console.log(e)})
    }   
}


var curso;
console.log(cursoTodos());

console.log(curso);


function cursoTodos(){
    const url =  `/components/cursos/`;
    fetch(url, {
        method: "get",
        headers: new Headers(),
        mode : "cors",
        cache : "default",
    })
    .then((res) => res.json())
    .then((data)=>{
        
            curso = data.data.context.map((item) =>{
                // 'id_curso_asesor','curso__tipo'
                var items = [item.id,item.fullname]
                
                return items;
            })

    })
    .catch(e =>{console.log(e)})
}


//se encarga de escribir la lista que se obtiene
const build_lista = (items = []) =>{
    tb.innerHTML = "";
    i=0;
    items.map((item) => {
        tb.innerHTML += `<tr>
        <td>${item[0]}</td>
        <td>${item[1]}</td>
        <td> <div class = "autocomplet">
                <input name = "asesores[]"  type="text" autofocus= "true" placeholder = "Buscar Asesor..."/>
                <ul name ="autocomplet[]" class = "autocomplet-results">
                </ul>
            </div>
        </td>
        <td>
            <a class="btn btn-outline-secondary btn-sm edit" title="Edit" name ="boton[]">
                <i class = "fas fa-pencil-alt"></i>
            </a>
        </td>
        </tr>`

    })

}

const tabla = (key) =>{

    const url = `/components/cursoAsignado/${key}`;
    
    fetch(url, {
        method: "get",
        headers: new Headers(),
        mode: "cors",
        cache: "default",
    })
    .then((res) => res.json())

    .then((data)=>{
        // if(Array.isArray(data)){
            build_lista(
                data.data.context.map((item) =>{
                    // 'id_curso_asesor','curso__tipo'
                    items = [item.id,item.fullname]
                    return items;
                })
            );

            eventos();
            handleClick();
        // }
        // else{
        //     build_list()
        // }
    })
    .catch(e =>{console.log(e)})
}

tabla(null);