var chart = document.querySelector("#myChart")
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
var barColors = ["#005ca8","#725bb4","#b653ac","#e94e93","#ff5b6e","#ff7d43","#ffa600"];







new Chart("myChart", {
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


