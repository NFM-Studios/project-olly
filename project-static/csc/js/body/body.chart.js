const app = require('../../js/utils/app.core');

const ctx = document.querySelector('.chart-bars');
const chartBarsData = {
  type: 'bar',
  data: {
    labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
    datasets: [
      {
        label: 'WINS',
        data: [8, 10, 5, 6, 9, 11, 8, 4, 7, 10, 4, 9],
        backgroundColor: "#7442ce"
      }, 
      {
        label: 'WINS',
        data: [4, 2, 7, 6, 3, 1, 4, 8, 5, 2, 8, 3],
        backgroundColor: "#00e3d0"
      }
    ]
  },
  options: {
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "#363636",
      titleFontSize: 0,
      titleSpacing: 0,
      titleMarginBottom: 0,
      bodyFontSize: 8,
      bodyFontStyle: 'bold',
      bodySpacing: 0,
      cornerRadius: 4,
      xPadding: 10,
      yPadding: 6,
      displayColors: false
    },
    scales: {
      xAxes: [
        {
          barThickness: 16,
          gridLines: {
            display: false
          }
        }
      ],
      yAxes: [
        {
          gridLines: {
            color: "#f1f1f1",
            drawBorder: false,
            drawTicks: false,
            zeroLineColor: "#f1f1f1"
          },
          ticks: {
            beginAtZero: true
          }
        }
      ]
    }
  }
};

app.createChart(ctx, chartBarsData);

const ctx1 = document.querySelector('.chart-bars-single');
const chartBarsSingleData = {
  type: 'bar',
  data: {
    labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    datasets: [
      {
        label: 'SUBSCRIBERS',
        data: [98, 53, 68, 43, 80, 110, 68, 78, 46, 87, 100, 76, 42, 8, 82, 26, 0, 90, 66, 99, 76, 102, 65, 78, 98, 70, 90, 62, 78, 95, 70],
        backgroundColor: "#7442ce"
      }
    ]
  },
  options: {
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "#363636",
      titleFontSize: 0,
      titleSpacing: 0,
      titleMarginBottom: 0,
      bodyFontSize: 8,
      bodyFontStyle: 'bold',
      bodySpacing: 0,
      cornerRadius: 4,
      xPadding: 10,
      yPadding: 6,
      displayColors: false
    },
    scales: {
      xAxes: [
        {
          barThickness: 16,
          gridLines: {
            display: false
          }
        }
      ],
      yAxes: [
        {
          gridLines: {
            color: "#f1f1f1",
            drawBorder: false,
            drawTicks: false,
            zeroLineColor: "#f1f1f1"
          },
          ticks: {
            beginAtZero: true
          }
        }
      ]
    }
  }
};

app.createChart(ctx1, chartBarsSingleData);

const ctx2 = document.querySelector('.chart-lines');
const chartLinesData = {
  type: 'line',
  data: {
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    datasets: [
      {
        data: [18, 28, 16, 21, 37, 26, 29, 16, 28, 20, 26, 52, 38, 21, 27, 24, 31, 17, 22, 23, 19, 26, 29, 20, 33, 32, 38, 27],
        label: "KILLS",
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        borderColor: "#107df8",
        borderCapStyle: 'bevel',
        borderDash: [],
        borderDashOffset: 0,
        borderJoinStyle: 'bevel',
        pointBorderColor: "#108fe9",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 2,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#108fe9",
        pointHoverBorderWidth: 4,
        pointRadius: 4,
        pointHitRadius: 10
      },
      {
        data: [12, 9, 22, 17, 25, 34, 39, 26, 23, 31, 20, 16, 26, 27, 22, 19, 39, 26, 16, 19, 23, 21, 34, 41, 23, 28, 24, 37],
        fill: false,
        label: "KILLS",
        lineTension: 0,
        borderWidth: 2,
        borderColor: "#dee807",
        borderCapStyle: 'bevel',
        borderDash: [],
        borderDashOffset: 0,
        borderJoinStyle: 'bevel',
        pointBorderColor: "#ffdc1b",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 2,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#ffdc1b",
        pointHoverBorderWidth: 4,
        pointRadius: 4,
        pointHitRadius: 10
      }
    ]
  },
  options: {
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "#363636",
      titleFontSize: 0,
      titleSpacing: 0,
      titleMarginBottom: 0,
      bodyFontSize: 8,
      bodyFontStyle: 'bold',
      bodySpacing: 0,
      cornerRadius: 4,
      xPadding: 10,
      yPadding: 6,
      displayColors: false
    },
    scales: {
      xAxes: [
        {
          gridLines: {
            color: "#f1f1f1",
            drawBorder: false,
            zeroLineColor: "#f1f1f1"
          }
        }
      ],
      yAxes: [
        {
          gridLines: {
            color: "#f1f1f1",
            drawBorder: false,
            zeroLineColor: "#f1f1f1"
          },
          ticks: {
            beginAtZero: true
          }
        }
      ]
    }
  }
};

app.createChart(ctx2, chartLinesData);