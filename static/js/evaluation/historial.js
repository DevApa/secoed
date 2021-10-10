let url = "/components/notify/email"

const syncButton = document.getElementById('sync-button')
syncButton.addEventListener('click',()=>{
    fetch(url)
        .then(res => res.json())
        .then(res => {
            if(res.finished_courses.length === 0)
                Swal.fire('No hay cursos terminados')
            else 
                Swal.fire(`Email enviado a: ${res.finished_courses}`)
        })
        .catch(err => Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: err,
          }))
})