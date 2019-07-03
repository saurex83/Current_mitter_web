function get_stat_bars_config(labels, max_curr, avr_cur, valid_cur)
{
  var cfg =
  {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: "Максимальный ток, А",
            borderWidth: 1,
            fill: true,
            backgroundColor: ["#700000", "#700000","#700000"],
            data: max_curr,
           // yAxisID: 'y-axis-2',
            xAxisID: "bar-x-axis1",
          },
          {
            label: "Ток, А",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: avr_cur,
          },
          {
            label: "Допустимый ток, А",
            borderWidth: 1,
            fill: false,
            data: valid_cur,
          },
   
        ]
      },
      options: 
      {
      	legend: { display: false },
        	title: 
        	{
          	display: true,
          	text: 'Текущие значения',
          	fontSize: 14,
      		fontColor: "gray"
        	},
        	scales: {
      		xAxes: 
      		[{
      			stacked: true,
      			barThickness : 50,
      		},
      		{
      			stacked: true,
      			display: false,
      			offset : true,
            		id: "bar-x-axis1",
            		barThickness: 10,
      		}],
      		yAxes: 
      		[{ 
      			stacked: false, 
      			beginAtZero:true,
      			ticks: {min:0, max: 100,source: 'auto'},
      			minBarLength: 5,
      		}],
      		minBarLength : 3
    		},
//        "animation": {
//              "duration": 1,
//              "onComplete": function () {
//                  var chartInstance = this.chart,
//                  ctx = chartInstance.ctx;
//
//                  ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
//                  ctx.textAlign = 'center';
//                  ctx.textBaseline = 'bottom';
//
//                  this.data.datasets.forEach(function (dataset, i) {
//                      var meta = chartInstance.controller.getDatasetMeta(i);
//                      meta.data.forEach(function (bar, index) {
//                          var data = dataset.data[index];                            
//                          ctx.fillText(data, bar._model.x+20, bar._model.y - 5);
//                      });
//                  });
//              }
//          },
      }
  }
	return cfg
}