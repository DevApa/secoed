/*metodos para categorias*/
$(document).ready ( function(){
    cargarlista();
   $("#divCategoria").hide();
   $("#divCursos").hide();
    $("#botonesCategoria").show();
});

function editarCategoria(item) {
    llenarModalCategoria(item);
    $("#botonesCategoria").show();
}

function visualizarCategoria(item) {
    llenarModalCategoria(item);
    $("#botonesCategoria").hide();
}

function llenarModalCategoria(item) {
    var descripcion = item.description.replace(/(<([^>]+)>)/gi, "");
    let texto=item.path.split('/');
    var tamañoarray=texto.length;
    $("#idCategoria").val(item.id);
    $("#menuPadre").val(tamañoarray-2==0?0:texto[tamañoarray-2])
    $("#nombreCategoria").val(item.name);
    $("#descripcionCategoria").val(descripcion);
}

function limpiarCamposCategoria() {
    $("#idCategoria").val("");
    $("#menuPadre").val(0);
    $("#nombreCategoria").val("");
    $("#descripcionCategoria").val("");
}

function eliminarCategoria(item) {
    Swal.fire({
        "title": "¿Está seguro que desea eliminar esta categoria?",
        "text": "Esta acción no se puede revertir",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "NO",
        "confirmButtonText": "SI",
        "cancelButtonColor": "#f46a6a",
        "confirmButtonColor": "#34c38f",
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "deleteCategoria/" + item.id
            }
        })
}

/*fin metodos para eliminar categorias*/



/*metodos para cursos*/
function visualizarCurso(item) {
    llenarModalCurso(item);
    $("#botonesCursos").hide();
}

function llenarModalCurso(item) {
    var fechaactual=new Date(0);
    var fechaactual2=new Date(0);
    fechaactual.setUTCSeconds(item.startdate);
    fechaactual2.setUTCSeconds(item.enddate);
    var descripcion = item.summary.replace(/(<([^>]+)>)/gi, "");
    $("#idCurso").val(item.id);
    $("#nombreCurso").val(item.fullname);
    $("#nombreCorto").val(item.shortname);
    $("#resumen").val(descripcion);
    $("#calificaciones").prop("checked", item.showgrades === 1 ? true : false);
    $("#fechaInicio").datepicker("setDate", fechaactual);
    $("#fechaFin").datepicker("setDate", fechaactual2);
    $("#mostrarInforme").prop("checked", item.showreports === 1 ? true : false);
    $("#mostrarSeccionesOcultas").prop("checked", item.hiddensections === 1 ? true : false);
    $("#NotificarFinalizar").prop("checked", item.completionnotify === 1 ? true : false);
    $("#visibleAlumno").prop("checked", item.visible  === 1 ? true : false);
    $("#comboCategorias").val(item.categoryid)
}
function cargarlista() {
    const csrftoken = getCookie('csrftoken');
    var url = window.location.href + "allCategorias";
    $.ajax({
        url: url,
        dataType: "json",
        type: 'POST',
        headers: {"X-CSRFToken": csrftoken},
/*        async:false,*/
        success: function (data) {
            $("#comboCategorias").empty();
            // $("#comboCategorias").append('<option value="0">RAIZ</option>');
            for (var i=0; i <= data.context.length; i++) {
                $("#comboCategorias").append('<option value="' + data.context[i].id + '">' + data.context[i].name + '</option>');
            }
        }, error: function (xhr, status, error) {
            console.log(xhr);
        }
    })
}

 function  getCookie(name){
    let cookieValue=null;
    if(document.cookie && document.cookie!= ''){
        const cookies=document.cookie.split(';');
        for (let i=0;i<cookies.length;i++){
            const cookie=cookies[i].trim();
            if(cookie.substring(0,name.length+1)===(name+'=')){
                cookieValue=decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
 }

 function limpiarCamposCursos(){
    const fecha = new Date();
    $("#botonesCursos").show();
    $("#idCurso").val("");
    $("#nombreCurso").val("");
    $("#nombreCorto").val("");
    $("#resumen").val("");
    $("#calificaciones").prop("checked", false);
    $("#fechaInicio").datepicker("setDate", fecha);
    $("#fechaFin").datepicker("setDate", fecha);
    $("#mostrarInforme").prop("checked", false);
    $("#mostrarSeccionesOcultas").prop("checked", false);
    $("#NotificarFinalizar").prop("checked", false);
    $("#visibleAlumno").prop("checked", false);
    $("#comboCategorias").val(0);
 }
function editarCursos(item) {
    limpiarCamposCursos();
    llenarModalCurso(item);
    $("#botonesCursos").show();
}

function eliminarCurso(item) {
    Swal.fire({
        "title": "¿Está seguro que desea eliminar el curso?",
        "text": "Esta acción no se puede revertir",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "NO",
        "confirmButtonText": "SI",
        "cancelButtonColor": "#f46a6a",
        "confirmButtonColor": "#34c38f",
    })
        .then(function (result) {
            if (result.isConfirmed) {
                window.location.href = "deleteCourse/" + item.id
            }
        })
}
/*fin metodos para crear cursos*/