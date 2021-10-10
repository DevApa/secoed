Highcharts.chart('container1', {
    chart: {
      type: 'bar'
    },
    title: {
      text: 'Modulos Mas Utilizados'
    },
    xAxis: {
      categories: ['Modulo 1', 'Modulo 2', 'Modulo 3', 'Modulo 4']
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Total Modulos Mas Utilizados'
      }
    },
    legend: {
      reversed: true
    },
    plotOptions: {
      series: {
        stacking: 'normal'
      }
    },
    series: [{
      name: 'Modulos Utilizadas',
      data: [4, 3, 4, 7]
    }, ]
  });