var data1= [];
var data2= [];
var data3= [];
var requests = $.get('/Scatter_OP30');  // $. <- 제이쿼리,
   var tm = requests.done(function(result) // 성공하면 result 값을 받아옴
        {
//                var data1= []; // [[[ ]]]  [[ ]]
            data1.push(result[0][0]);
            console.log(data1)
            data2.push(result[0][1]);
            data3.push(result[0][2]);// 값 업데이트
//            //data1 = data1[0];
//            console.log(result)
//            console.log(data1)  // 값 업데이트
//            //data2 = data2;
//            console.log(data2)
//            //data3 = data3;
//            console.log(data3)

Highcharts.chart("container", {
title: {
text: "Electricity vs Length",
},
subtitle: {
text: "",
},
xAxis: {
gridLineWidth: 1,
title: {
  enabled: true,
  text: "Electricity",
},
startOnTick: true,
endOnTick: true,
showLastLabel: true,
},
yAxis: {
title: {
  text: "Length (mm)",
},
},
legend: {
layout: "vertical",
align: "right",
verticalAlign: "middle",
},
series: [
{
  name: "Observations",
  type: "scatter",
  color: "red",
  data: data1[0]
},
],
tooltip: {
headerFormat: "<b>{series.name}</b><br>",
pointFormat: "{point.x} , {point.y} ",
},
responsive: {
rules: [
  {
    condition: {
      maxWidth: 500,
    },
    chartOptions: {
      legend: {
        align: "center",
        layout: "horizontal",
        verticalAlign: "bottom",
      },
    },
  },
],
},
});

Highcharts.chart("container2", {
  title: {
    text: "Electricity vs Width",
  },
  subtitle: {
    text: "",
  },
  xAxis: {
    gridLineWidth: 1,
    title: {
      enabled: true,
      text: "Electricity",
    },
    startOnTick: true,
    endOnTick: true,
    showLastLabel: true,
  },
  yAxis: {
    title: {
      text: "Width (mm)",
    },
  },
  legend: {
    layout: "vertical",
    align: "right",
    verticalAlign: "middle",
  },
  series: [
    {
      name: "Observations",
      type: "scatter",
      color: "blue",
      data: data2[0]
    },
  ],
  tooltip: {
    headerFormat: "<b>{series.name}</b><br>",
    pointFormat: "{point.x} , {point.y} ",
  },
  responsive: {
    rules: [
      {
        condition: {
          maxWidth: 500,
        },
        chartOptions: {
          legend: {
            align: "center",
            layout: "horizontal",
            verticalAlign: "bottom",
          },
        },
      },
    ],
  },
});

Highcharts.chart("container3", {
  title: {
    text: "Electricity vs Height",
  },
  subtitle: {
    text: "",
  },
  xAxis: {
    gridLineWidth: 1,
    title: {
      enabled: true,
      text: "Electricity",
    },
    startOnTick: true,
    endOnTick: true,
    showLastLabel: true,
  },
  yAxis: {
    title: {
      text: "Height (mm)",
    },
  },
  legend: {
    layout: "vertical",
    align: "right",
    verticalAlign: "middle",
  },
  series: [
    {
      name: "Observations",
      type: "scatter",
      color: "yellow",
      data: data3[0]
    },
  ],
  tooltip: {
    headerFormat: "<b>{series.name}</b><br>",
    pointFormat: "{point.x} , {point.y} ",
  },
  responsive: {
    rules: [
      {
        condition: {
          maxWidth: 500,
        },
        chartOptions: {
          legend: {
            align: "center",
            layout: "horizontal",
            verticalAlign: "bottom",
          },
        },
      },
    ],
  },
});

});
