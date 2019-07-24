
function get_history_chart_config(labels, data, data_pic, graph_name)
{
    var cfg = {
        type: 'line',

        data: 
        {
            labels: ['a','b','c'],
            datasets: 
            [{  label : 'Первый',
                data: [1,2,30],
                pointRadius : 0,
                borderColor: "lime",
                borderWidth : 2,
                steppedLine :false,
                fill: false
            },
            { 
                label : 'Второй',
                data: [50,20,30],
                pointRadius : 0,
                borderColor: "Aqua",
                borderWidth : 2,
                steppedLine :false,
                strokeColor : "rgba(10, 51, 51, 0.2)",
                scaleFontColor: "rgba(34, 51, 51, 0.3)",
                fill: false
            },
            { 
                label : 'Третий',
                data: [70,90,80],
                pointRadius : 0,
                borderColor: "yellow",
                borderWidth : 2,
                steppedLine :false,
                strokeColor : "rgba(10, 51, 51, 0.2)",
                scaleFontColor: "rgba(34, 51, 51, 0.3)",
                fill: false
            },
            ]
        },

        options: 
        {
            legend: {
                display: true
            },
            title: {display: false, text: 'graph_name', 
                    fontColor: 'rgb(255, 255, 255,0.6)',
                    fontSize : 14},
            elements: 
            {
                //line: {
                //tension: 0 // disables bezier curves
                //}
            },
            animation: {duration: 0},
            hover: {animationDuration: 0},
            responsiveAnimationDuration: 0,
               
            pan: 
            {
                enabled: true,
                mode: 'y',
                rangeMin: {x: 0, y: 0},
                rangeMax: {x: 1200,y: 100},
            },

            zoom: {
                enabled: true,
                drag: false,
                mode: 'y',
                rangeMin: { y: 0},
                rangeMax: {y: 100},
            },

            scales: 
            {
                yAxes: 
                [{
                    ticks: {beginAtZero:true, max: 100,
                            fontColor : 'rgb(255, 255, 255,0.6)'},
                    scaleLabel: {
                        display: false,
                        labelString: graph_name,
                        fontColor: 'white',
                        fontSize : 16
                    },
                    gridLines: { color: 'rgb(100, 100, 100,0.4)'}
                }],

                xAxes: 
                [{
                    ticks: {autoSkip: true, maxTicksLimit: 10,
                            fontColor : 'rgb(255, 255, 255,0.6)',
                            maxRotation: 0,
                            minRotation: 0},
                    gridLines: { color: 'rgb(100, 100, 100,0.4)'}
                }],
            },

                annotation: {
                    annotations: 
                    [{
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y-axis-0',
                        borderDash: [5,5],
                        value: 65,
                        borderColor: 'Magenta ',
                        borderWidth: 1,
                        label: 
                        {
                            enabled: false,
                            fontSize: 10,
                            position : "left",
                            backgroundColor: "rgba(34,1,34,0.3)",
                            content: 'Максимально допустимый ток'
                        }
                    }]
                },
                responsive: true,
                maintainAspectRatio: false,
            }
        }
    

return cfg
}