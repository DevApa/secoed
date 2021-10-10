

Highcharts.chart('container2', {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Actividad de la Pagina'
    },
    subtitle: {
      text: ''
    },
    xAxis: {
      categories: [
        'Lunes',
        'Martes',
        'Miercoles',
        'Jueves',
        'Viernes',
        'Sabado',
        'Domingo'
      ],
      crosshair: true
    },
    yAxis: {
      min: 0,
      max: 24,
      tickInterval: 2,
      title: {
        text: 'Horas'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        '<td style="padding:0"><b>{point.y: -0f} hora/s </b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0
      }
    },
    series: [{
      name: 'Activo',
      data: [ 16, 10, 9, 15, 17, 18, 20]
  
    }, {
      name: 'Inactivo',
      data: [ 10, 10, 9, 19, 22, 8, 15]
  
    },]
  });

  
  
  //Usuarios conectados//
  Highcharts.chart('container3', {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Usuario Conectados'
    },
    subtitle: {
      text: ''
    },
    xAxis: {
      categories: [
        'Lunes',
        'Martes',
        'Miercoles',
        'Jueves',
        'Viernes',
        'Sabado',
        'Domingo',
      ],
      crosshair: true
    },
    yAxis: {
      min: 0,
      max: 200,
      tickInterval: 20,
      title: {
        text: 'Numero de Usuarios'
      }
    },
    tooltip: {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{}</td>' +
        '<td style="padding:0"><b>{point.y: -0f} Usuarios</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0
      }
    },
    series: [{
      name: 'Dias de la semana',
      data: [ 140, 10, 9, 15, 17, 18, 200]
  
    },]
  });


  const {Pool} = require('pg')

  const config = {
    user: 'postgres',
    host: 'localhost',
    password: 'root',
    port: 5432,
    database: 'universidad'
  };
  
  const pool = new Pool(config);
  
  const getmateria = async () => {
    const res = await pool.query('SELECT * FROM pt_materia');
    console.log(res);
  };
  
  getmateria();