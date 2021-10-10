$(function(){
    let url_dashboard = '';
    let parameters = {};
    let url = '';
    let method = '';
    let answers = {
        user: '',
        co_evaluator: '',
        cycle: '',
        questions: [],
    };

    $('#form_evaluacion').on('submit', function (e) {
        e.preventDefault();
        confirmarEnvio();
    });

    /*
    $('#btnGuardar').on('click', function () {
        //e.preventDefault();
        confirmarEnvio();
    });
    */

    function getData() {
        answers.user = $('input:hidden[name=user]').val();
        answers.co_evaluator = $('input:hidden[name=identify]').val();
        answers.cycle = $('input:hidden[name=cycle]').val();
        answers.type = $('input:hidden[name=type]').val();
        $('#preguntas tbody tr.parent td > input[type="radio"]:checked').each(function (index, input) {
            let item = {};
            item.question = $(input).parent().parent().find('input:hidden[name=pregunta]').val();
            item.category = $(input).parent().parent().find('input:hidden[name=category]').val();
            item.parameter = $(input).val();
            answers.questions.push(item);
        });
    }

     function saveEvaluation(url, redirection) {
        getData();
        parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('answers', JSON.stringify(answers));
        sendRequest(url, parameters, redirection);
    }

    function confirmarEnvio() {
        Swal.fire({
          title: 'Notificación',
          text: '¿Desea enviar su evaluación ahora?',
          icon: 'question',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, proseguir!'
        }).then(function(result){
          if (result.isConfirmed) {
              url = $('#form_evaluacion').attr('action');
              url_dashboard = $('input:hidden[name=dashboard]').val();

              saveEvaluation(url, url_dashboard);
          }
        });
    }

    function sendRequest(url, parameters, redirection) {
        $.ajax({
            url: url,
            data: parameters,
            type: 'POST',
            dataType: 'json',
            processData: false,
            contentType: false,
        }).done(function (response) {
            if (response.error === '') {
                notification('Excelente!', response.message, 'success');
                window.setTimeout(function () {
                    window.location.href = redirection;
                }, 1500);
                return true;
            }
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ' ' + errorThrown);
            notification('Error!', response.message, 'error');
        }).always(function (response) {

        });
    }

    function confirmAction(title, content, icon, url, redirection) {
        Swal.fire({
          title: title,
          text: content,
          icon: icon,
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, proseguir!'
        }).then(function(result){
          if (result.isConfirmed) {
              sendRequest(url, parameters, redirection);
          }
        });
    }
});