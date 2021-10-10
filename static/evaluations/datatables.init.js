$(document).ready(function() {
    $("#datatable").DataTable({
        language: {
            url: '/static/evaluations/language.json',
        },

    }).$(".dataTables_length select").addClass("form-select form-select-sm")
});

