const app = require('../utils/app.core');

// POLL RESULTS
app.createProgressBar({
  container: '#poll-result-1',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#poll-result-1',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 68
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkUnits: '%',
  linkText: true,
  decimalPoints: 0
});

app.createProgressBar({
  container: '#poll-result-2',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#poll-result-2',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 12
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkUnits: '%',
  linkText: true,
  decimalPoints: 0
});

app.createProgressBar({
  container: '#poll-result-3',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#poll-result-3',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 15
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkUnits: '%',
  linkText: true,
  decimalPoints: 0
});

app.createProgressBar({
  container: '#poll-result-4',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#poll-result-4',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 5
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkUnits: '%',
  linkText: true,
  decimalPoints: 0
});

/**
 *  SIDEBAR PROGRESS BARS
 */
app.createProgressBar({
  container: '#sd-pg-1',
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
  linkTo: '#tlw-kills-stat-sd1',
  buttEnd: true
});

app.createProgressBar({
  container: '#sd-pg-1',
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
  linkTo: '#rrh-kills-stat-sd1',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#sd-pg-2',
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
  linkTo: '#tlw-deaths-stat-sd2',
  buttEnd: true
});

app.createProgressBar({
  container: '#sd-pg-2',
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
  linkTo: '#rrh-deaths-stat-sd2',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#sd-pg-3',
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
  linkTo: '#tlw-assists-stat-sd3',
  buttEnd: true
});

app.createProgressBar({
  container: '#sd-pg-3',
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
  linkTo: '#rrh-assists-stat-sd3',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#t-cr-pgb-01',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-01',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 92.58
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-cr-pgb-02',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-02',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 85.50
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-cr-pgb-03',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-03',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 79.71
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-cr-pgb-04',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-04',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 63.33
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-cr-pgb-05',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-05',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 42.20
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-cr-pgb-06',
  width: 120,
  height: 6
});

app.createProgressBar({
  container: '#t-cr-pgb-06',
  width: 120,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 63.33
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  linkText: true,
  decimalPoints: 2,
  animateOnScroll: true
});

app.createProgressBar({
  container: '#t-pr-pgb-01',
  width: 70,
  height: 6
});

app.createProgressBar({
  container: '#t-pr-pgb-01',
  width: 70,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 55
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: '/'
});

app.createProgressBar({
  container: '#t-pr-pgb-02',
  width: 70,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#t-pr-pgb-02',
  width: 70,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 100,
    stop: 79.03
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 12,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#t-pr-pgb-03',
  width: 70,
  height: 6
});

app.createProgressBar({
  container: '#t-pr-pgb-03',
  width: 70,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 5
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: '/'
});

app.createProgressBar({
  container: '#t-pr-pgb-04',
  width: 70,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#t-pr-pgb-04',
  width: 70,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 100,
    stop: 90
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 12,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#t-pr-pgb-05',
  width: 70,
  height: 6
});

app.createProgressBar({
  container: '#t-pr-pgb-05',
  width: 70,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 27
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: '/'
});

app.createProgressBar({
  container: '#t-pr-pgb-06',
  width: 70,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#t-pr-pgb-06',
  width: 70,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 100,
    stop: 36.57
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 12,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#t-pr-pgb-07',
  width: 70,
  height: 6
});

app.createProgressBar({
  container: '#t-pr-pgb-07',
  width: 70,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 13
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: '/'
});

app.createProgressBar({
  container: '#t-pr-pgb-08',
  width: 70,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#t-pr-pgb-08',
  width: 70,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 100,
    stop: 52.04
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 12,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-17',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-17',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#713fcb', '#00e3d0']
  },
  scale: {
    start: 0,
    end: 24,
    stop: 9
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: 'HOURS'
});

app.createProgressBar({
  container: '#ew3-pgb-os-18',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-18',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#713fcb', '#00e3d0']
  },
  scale: {
    start: 0,
    end: 20,
    stop: 17.764
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-os-19',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-19',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#713fcb', '#00e3d0']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 18.04
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-20',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-20',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 6.076,
    stop: 6.076
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-os-21',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-21',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 10,
    stop: 8.5
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-22',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-22',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 1000,
    stop: 465.23
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-23',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-23',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 33.25,
    stop: 15.662
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-os-24',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-24',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 63.33
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-25',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-25',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 13.50
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-26',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-26',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 10
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#ew3-pgb-os-27',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-27',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 68
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#ew3-pgb-os-28',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-28',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 23,
    stop: 10
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false
});

app.createProgressBar({
  container: '#ew3-pgb-os-29',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-29',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 23,
    stop: 23
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-30',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-30',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 33.5,
    stop: 33.5
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-31',
  width: 76,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-31',
  width: 76,
  height: 6,
  lineCap: 'butt',
  gradient:{
    colors: ['#00e3d0', '#62fff2']
  },
  scale: {
    start: 0,
    end: 10,
    stop: 10
  },
  split: {
    parts: 13,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-tp-01',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#ew3-pgb-tp-01',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 72
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    partItems: [
      {
        width: 30,
        gap: 4
      },
      {
        width: 40,
        gap: 4
      },
      {
        width: 50,
        gap: 4
      },
      {
        width: 60,
        gap: 4
      },
      {
        width: 74,
        gap: 4
      }
    ],
    color: '#fff'
  }
});

app.createProgressBar({
  container: '#ew3-pgb-crd-01',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-01',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 30.092
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-02',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-02',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 26.596
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-03',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-03',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 25.386
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-04',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-04',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 23.447
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-05',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-05',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 16.480
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-06',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-06',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 14.906
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-07',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-07',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 11.346
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-08',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-08',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 9.871
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-09',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-09',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 8.467
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-crd-10',
  width: 124,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-crd-10',
  width: 124,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 31,
    stop: 8.102
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 21,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#ew3-pgb-hs-01',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-hs-01',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  scale: {
    start: 0,
    end: 10,
    stop: 9.652
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 3
});

app.createProgressBar({
  container: '#es-home-pp-pgb-01',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#es-home-pp-pgb-01',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 64
  },
  speed: 30,
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#es-home-pp-pgb-02',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#es-home-pp-pgb-02',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 14
  },
  speed: 30,
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#es-home-pp-pgb-03',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#es-home-pp-pgb-03',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 10
  },
  speed: 30,
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#es-home-pp-pgb-04',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#es-home-pp-pgb-04',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#es-home-pp-pgb-05',
  width: 240,
  height: 6
});

app.createProgressBar({
  container: '#es-home-pp-pgb-05',
  width: 240,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 4
  },
  speed: 30,
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  animateOnScroll: true,
  linkText: true
});