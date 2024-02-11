//bar chart data
var chart = document.querySelector("#seller_chart")
var data = JSON.parse(chart.dataset.dictionary)
console.log(data)
var dates_array = []
var revenues_array = []
for(var i =0; i <data.length; i++){
dates_array.push(data[i]['date'])
revenues_array.push(data[i]['revenue'])
}
var xValues = dates_array;
var yValues = revenues_array;
var barColors = ["orange"];

//pie chart data
var pieChart = document.querySelector("#stock_chart")
var pieData = JSON.parse(pieChart.dataset.dictionary)
console.log(pieData)

//bar chart
new Chart("seller_chart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {
    display: false,
    },
    title: {
      display: true,
      text: "Revenues within last week"
    },
    scales: {
    y: {
        min: 0,
      },
     yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Revenue in SGD ($)'
          },
          ticks: {
            beginAtZero: true,
              }
    }],
    xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Last 7 days'
          }
    }]
  },
    }
});

new Chart("stock_chart",{
type: 'pie',
data : {
  labels: [
    'stock_left',
    'sold_out',
  ],
  datasets: [{
    label: 'Number of Items',
    data: pieData,
    backgroundColor: [
      '#2b91ff',
      '#f22b2b',
    ],
    hoverOffset: 4
  }],

},
 options : {
  responsive: true,
   plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Pie Chart'
      }
    },
  elements: {
    arc: {
      borderWidth: 0,
    }
  }
}

})


