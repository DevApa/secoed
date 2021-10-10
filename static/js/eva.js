let $ = jQuery.noConflict();

/******************* Create Modals ******************/
function openModal(url, opModal) {
    $('#'+ opModal).load(url, function () {
        $(this).modal('show');
    });
}

function closeModal(opModal) {
    $('#' + opModal).modal('hide');
    let url = $('input[name="url_list"]').val();
    window.setTimeout(function() {
            window.location.href = url;
    },1500);
    return true;
}

function activeButton(button) {
    if ($('#' + button).prop('disabled')) {
        $('#' + button).prop('disabled',false);
    }else{
        $('#' + button).prop('disabled',true);
    }
}

function validaCiclo(form) {
    if (form=='form_create_ciclo'){
        if ($('#id_is_active').is(":checked"))
        {
           $('input:hidden[name="option"]').val('true');
        }else {
            $('input:hidden[name="option"]').val('false');
        }
   }
}

function ajaxRequest(form, error_tag, button) {
    activeButton(button);
    validaCiclo(form);
    $.ajax({
        data:$('#' + form).serialize(),
        url: $('#' + form).attr('action'),
        type:$('#' + form).attr('method'),
        success:function(response){
            notification('Excelente!', response.message, 'success');
            closeModal();
            $("#datatable").ajax.reload();
        },
        error:function(error){
            notification('Oops...!', error.responseJSON.message, 'error');
            errorAlerts(error_tag, error);
            activeButton(button);
        }
    });
}

function errorAlerts(error_tag, errors) {
    $('#'+ error_tag).html('');
    let error= '';
    for (let item in errors.responseJSON.error) {
        error += '' +
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
                +'<i class="mdi mdi-block-helper me-2"></i>'
            +   '<strong>'+ errors.responseJSON.error[item] + '</strong>' +
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'+
            '</div>';
    }
    $('#'+ error_tag).append(error)
}

function notification(title, message, icon) {
    Swal.fire({
        title: title,
        text: message,
        icon: icon,
        showConfirmButton: false,
        timer:3000
    });
}

function confirmDelete(url) {
    let token = $("[name='csrfmiddlewaretoken']").val();
    Swal.fire({
      title: '¿Estas seguro?',
      text: "¡No podrás revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Si, eliminar!'
    }).then(function(result){
      if (result.isConfirmed) {
         $.ajax({
            data: {csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()},
            url: url,
            type:'post',
            success:function(response){
                notification('Excelente!', response.message, 'success');
                closeModal();
            },
            error:function(error){
                notification('Error!', error.responseJSON.message, 'error');
            }
        });
      }
    });
}