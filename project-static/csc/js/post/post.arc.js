const app = require('../utils/app.core');

app.createArc({
  container: '#post-open-rate1',
  width: 112,
  height: 112,
  lineWidth: 10,
  gradient: {
    colors: ['#5216fd', '#ff055d']
  },
  scale: {
    start: 0,
    end: 10,
    stop: 8.7
  },
  shadow: true
});

app.createArc({
  container: '#po-arc-1',
  width: 170,
  height: 170,
  lineWidth: 18,
  lineColor: '#ebebeb',
  linkText: false
});

app.createArc({
  container: '#po-arc-1',
  width: 170,
  height: 170,
  lineWidth: 18,
  gradient: {
    colors: ['#5216fd', '#ff055d']
  },
  animateOnScroll: true,
  speed: 50,
  scale: {
    start: 0,
    end: 10,
    stop: 8.7
  }
});