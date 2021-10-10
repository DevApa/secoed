$(function() {


});

function graphAutoEvaluation(data) {
        console.log(response);
        if(data.message===''){
            Highcharts.chart('auto', {
                chart: {
                    type: 'pie',
                    options3d: {
                        enabled: true,
                        alpha: 45
                    }
                },
                title: {
                    text: 'Resultados Autoevaluación'
                },
                subtitle: {
                    text: '3D donut in Highcharts'
                },
                plotOptions: {
                    pie: {
                        innerSize: 100,
                        depth: 45
                    }
                },
                series: [{
                    name: 'Delivered amount',
                    data: data
                }]
            });
        }
        else{
            $('#auto').hide()
            notification('Notificación', data.message, 'warning')
        }
    }