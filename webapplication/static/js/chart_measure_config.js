
function get_measure_chart_config(labels, data, data_pic, graph_name)
{
    var cfg = {
        type: 'line',

        data: 
        {
            labels: labels,
            datasets: 
            [{ 
                data: data,
                pointRadius : 0,
                borderColor: "#90780c",
                backgroundColor: "rgba(34,34,34,0.1)", //Цвет заполнения квадрата 
                borderWidth : 2,
                steppedLine :false,
                strokeColor : "rgba(10, 51, 51, 0.2)",
                scaleFontColor: "rgba(34, 51, 51, 0.3)",
                fill: true
            },
            { 
                data: data_pic,
                pointRadius : 0,
                borderColor: "#ffffff",
                backgroundColor: "rgba(34,34,34,0.1)", //Цвет заполнения квадрата 
                borderWidth : 1,
                borderDash: [2,2],
                steppedLine :false,
                strokeColor : "rgba(10, 51, 51, 0.2)",
                scaleFontColor: "rgba(34, 51, 51, 0.3)",
                fill: false
            }]
        },

        options: 
        {
            legend: {
                display: false
            },
            title: {display: false, text: graph_name},
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
                mode: 'xy',
                rangeMin: {x: 0, y: 0},
                rangeMax: {y: 100},
            },

            scales: 
            {
                gridLines: {color: "red", lineWidth: 3},

                yAxes: 
                [{
                    ticks: {beginAtZero:true, max: 100},
                    scaleLabel: {
                        display: true,
                        labelString: graph_name
                    },
                }],

                xAxes: 
                [{
                    ticks: {autoSkip: true, maxTicksLimit: 20}
                }],
            },

                annotation: {
                    annotations: 
                    [{
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y-axis-0',
                        borderDash: [10,5],
                        value: 65,
                        borderColor: 'rgb(200, 10, 2,0.5)',
                        borderWidth: 2,
                        label: 
                        {
                            enabled: false,
                            fontSize: 10,
                            position : "left",
                            backgroundColor: "rgba(34,1,34,0.3)",
                            content: 'Максимально допустимый ток'
                        }
                    }]
                }
            }
        }
    

return cfg
}