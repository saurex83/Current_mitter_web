
function get_measure_chart_config(labels, data1, data2, data3)
{
    var cfg = {
        type: 'line',

        data: 
        {
            labels: labels,
            datasets: 
            [{ 
                data: data1,
                pointRadius : 0,
                borderColor: "#e80c0c",
                backgroundColor: "rgba(34,1,34,0.5)", //Цвет заполнения квадрата 
                borderWidth : 1,
                steppedLine :true,
                strokeColor : "rgba(100, 51, 51, 1)",
                scaleFontColor: "#FF36F00",
                fill: false,
                label : 'Фаза 1'
            },
            { 
                data: data2,
                pointRadius : 0,
                borderWidth : 1,
                borderColor: "#0e0af5",
                fill: false,
                label : 'Фаза 2'
            },
            { 
                data: data3,
                pointRadius : 0,
                borderWidth : 1,
                borderColor: "#ff9e0d",
                fill: true,
                label : 'Фаза 3'
            }]
        },

        options: 
        {
            title: {display: false, text: 'Ток потребления по фазам'},
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
                    ticks: {beginAtZero:true, max: 100}
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
                            enabled: true,
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