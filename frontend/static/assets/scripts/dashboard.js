var height = 200;
var width = 200;

var obj = JSON.parse(percentages);
var percent1 = obj[0]["percent_1_1"];
percentAwakeTime("cvs_1", percent1);
var percent2 = obj[0]["percent_2_2"];
percentAwakeTime("cvs_2", percent2);

function percentAwakeTime(id, percent){
    var canvas = document.getElementById(id);
    canvas.width = 200;
    canvas.height = 200;
    var ctx = canvas.getContext("2d");

    // var element = document.getElementById("percent_duty_cycle_device_1");
    // console.log(element.innerHTML);
    // var percent = element.innerHTML;

    ctx.beginPath();
    ctx.arc(width/2, height/2, 65, 0, Math.PI * 2);
    // ctx.strokeStyle = "#2d1f73"; // l
    // ctx.strokeStyle = "#393b72"; // kinda gray
    ctx.strokeStyle = "#7784e3";
    ctx.lineWidth = 25;
    ctx.stroke();
    ctx.closePath();

    ctx.beginPath();
    ctx.arc((width/2), (height/2), 75, 0, 2 * Math.PI, false);
    ctx.lineWidth = 1;
    ctx.fillStyle = "#171d4b";
    ctx.fill();
    ctx.strokeStyle = '#171d4b';
    ctx.stroke();

    var angle = percent/100 * 360;
    ctx.beginPath();
    ctx.arc(width/2, height/2, 75, -90 * Math.PI/180, (angle - 90) * Math.PI/180);
    // ctx.strokeStyle = "#c7d8fc"; //
    ctx.strokeStyle = "#6054D3";
    ctx.lineWidth = 25;
    ctx.stroke();
    ctx.closePath();

    

    ctx.textBaseline = "middle";
    ctx.textAlign = "center";
    ctx.font = "30px Noto Sans";
    ctx.fillStyle = "#fff"
    ctx.fillText(percent + "%", width/2, height/2);
}
var obj2 = JSON.parse(rx_num_packets);
var obj3 = JSON.parse(tx_num_packets);

var xValues1 = ["# Received Packets", "# Transmitted Packets"];
var yValues1 = [obj2[0]["rx_packets_1_1"], obj3[0]["tx_packets_1_1"]];
var barColors1 = ["#171d4b", "#6054D3"];
packetsBarChart("cvs_rx_num_packets_1", xValues1, yValues1, barColors1);

var xValues2 = ["# Received Packets", "# Transmitted Packets"];
var yValues2 = [obj2[0]["rx_packets_2_2"], obj3[0]["tx_packets_2_2"]];
var barColors2 = ["#171d4b", "#6054D3"];
packetsBarChart("cvs_rx_num_packets_2", xValues2, yValues2, barColors2);

function packetsBarChart(id, xValues, yValues, barColors) {
    new Chart(id, {
        type: "bar",
        data: {
          labels: xValues,
          color: "#fff",
          datasets: [{
              color: "#fff",
              backgroundColor: barColors,
              data: yValues,
          }]
        },
        
        options: {
          legend: {display: false},
          scales: {
              xAxes: [{
                  display: true,
                  gridLines: {
                    drawBorder: true,
                    // scaleLineColor: '#fff',
                    // display: false,
                    // color: "#CCD7E4"
                    display: true,
                    drawOnChartArea: false,
                    color: "#fff"
                  },
                  scaleLabel: {
                      display: false,
                      fontColor: "#fff"
                  },
                  ticks: {
                      fontColor: '#fff'
                  },
                  
              }],
              yAxes: [{
                  display: true,
                  color: "#fff",
                  gridLines: {
                      drawBorder: true,
                      // scaleLineColor: '#fff',
                      // display: false,
                      // color: "#CCD7E4"
                      display: true,
                      drawOnChartArea: false,
                      color: "#fff"
                  },
                  scaleLabel: {
                      display: true,
                      labelString: 'Number of Packets',
                      fontColor: "#fff"
                  },
                  ticks: {
                      fontColor: '#fff'
                  },
                  grid: {
                      borderColor: "#fff",
                      borderWidth: 1
                  }
              }],
              }
        }
      });
}


// var chart = new CanvasJS.Chart("cvs_rx_num_packets", {
// 	animationEnabled: true,
// 	theme: "light2", // "light1", "light2", "dark1", "dark2"
//     backgroundColor: "rgb(119, 132, 227)",
// 	// title:{
// 	// 	text: "Packets Received and Transmitted"
// 	// },
// 	axisY: {
// 		title: "Number of Packets",
//         gridColor: "#fff"
// 	},
	// data: [{        
	// 	type: "column",  
    //     // backgroundColor: "rgb(119, 132, 227)",
	// 	// showInLegend: true, 
	// 	// legendMarkerColor: "grey",
	// 	// legendText: "MMbbl = one million barrels",
	// 	dataPoints: [      
	// 		{ y: obj2[0]["rx_packets_1_1"], label: "# Received Packets" },
	// 		{ y: obj3[0]["tx_packets_1_1"],  label: "# Transmitted Packets" }
	// 	]
	// }]
// });
// chart.render();
