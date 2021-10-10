Highcharts.chart('container4', {
    chart: {
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 45
      }
    },
    title: {
      text: 'Calificacion de Usuarios'
    },
    subtitle: {
      text: ''
    },
    plotOptions: {
      pie: {
        innerSize: 100,
        depth: 45
      }
    },
    series: [{
      name: 'Numero de Usuarios',
      data: [
        ['Excelente', 8],
        ['Muy Bueno', 3],
        ['Bueno', 1],
        ['Regular', 6],
        ['Malo', 8],
      ]
    }]
  });


