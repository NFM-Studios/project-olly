const app = require('../utils/app.core');

/**
 *  ESPORTS PROGRESS BARS
 */
app.createProgressBar({
  container: '#mn-pg-1',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 62,
    stop: 34
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-kills-stat',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-1',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 62,
    stop: 28
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-kills-stat',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-2',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 36,
    stop: 15
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-deaths-stat',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-2',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 36,
    stop: 21
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-deaths-stat',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-3',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 39,
    stop: 26
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-assists-stat',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-3',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 39,
    stop: 13
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-assists-stat',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-4',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 62,
    stop: 34
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-kills-stat-mn4',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-4',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 62,
    stop: 28
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-kills-stat-mn4',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-5',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 36,
    stop: 15
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-deaths-stat-mn5',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-5',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 36,
    stop: 21
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-deaths-stat-mn5',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-6',
  width: 210,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 39,
    stop: 26
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-assists-stat-mn6',
  buttEnd: true
});

app.createProgressBar({
  container: '#mn-pg-6',
  width: 210,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 39,
    stop: 13
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-assists-stat-mn6',
  reverse: true,
  buttEnd: true
});