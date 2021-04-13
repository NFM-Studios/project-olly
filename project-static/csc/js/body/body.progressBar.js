const app = require('../utils/app.core');

app.createProgressBar({
  container: '#ew1-pgb-1',
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
  linkTo: '#tlw-kills-stat-1',
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-1',
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
  linkTo: '#rrh-kills-stat-1',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-2',
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
  linkTo: '#tlw-deaths-stat-2',
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-2',
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
  linkTo: '#rrh-deaths-stat-2',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-3',
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
  linkTo: '#tlw-assists-stat-3',
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-3',
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
  linkTo: '#rrh-assists-stat-3',
  reverse: true,
  buttEnd: true
});

app.createProgressBar({
  container: '#ew1-pgb-4',
  width: 812,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 62,
    stop: 34
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-kills-stat-4',
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew1-pgb-4',
  width: 812,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 62,
    stop: 28
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-kills-stat-4',
  reverse: true,
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew1-pgb-5',
  width: 812,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 36,
    stop: 15
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-deaths-stat-5',
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew1-pgb-5',
  width: 812,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 36,
    stop: 21
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-deaths-stat-5',
  reverse: true,
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew1-pgb-6',
  width: 812,
  height: 6,
  lineColor: '#107df8',
  scale: {
    start: 0,
    end: 39,
    stop: 26
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#tlw-assists-stat-6',
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew1-pgb-6',
  width: 812,
  height: 6,
  lineColor: '#dee807',
  scale: {
    start: 0,
    end: 39,
    stop: 13
  },
  linkText: true,
  linkUnits: false,
  linkTo: '#rrh-assists-stat-6',
  reverse: true,
  buttEnd: true,
  breakpoints: {
    960: {
      width: 400,
      height: 6
    },
    480: {
      width: 210,
      height: 6
    }
  }
});

app.createProgressBar({
  container: '#ew3-pgb-large-01',
  width: 268,
  height: 20,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-large-01',
  width: 268,
  height: 20,
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
    parts: 34,
    gap: 4,
    color: '#fff'
  },
  animateOnScroll: true,
  decimalPoints: 2,
  linkText: true,
  linkTo: '#ew3-pgb-large-01-text'
});

app.createProgressBar({
  container: '#ew3-pgb-large-02',
  width: 268,
  height: 20,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-large-02',
  width: 268,
  height: 20,
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
    parts: 34,
    gap: 4,
    color: '#fff'
  },
  animateOnScroll: true,
  decimalPoints: 2,
  linkText: true,
  linkTo: '#ew3-pgb-large-02-text'
});

app.createProgressBar({
  container: '#ew3-pgb-large-03',
  width: 268,
  height: 20,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-large-03',
  width: 268,
  height: 20,
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
    parts: 34,
    gap: 4,
    color: '#fff'
  },
  animateOnScroll: true,
  decimalPoints: 2,
  linkText: true,
  linkTo: '#ew3-pgb-large-03-text'
});

app.createProgressBar({
  container: '#ew3-pgb-large-04',
  width: 268,
  height: 20,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-large-04',
  width: 268,
  height: 20,
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
    parts: 34,
    gap: 4,
    color: '#fff'
  },
  animateOnScroll: true,
  decimalPoints: 2,
  linkText: true,
  linkTo: '#ew3-pgb-large-04-text'
});

app.createProgressBar({
  container: '#ew3-pgb-os-01',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-01',
  width: 88,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 24,
    stop: 22
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: 'HOURS'
});

app.createProgressBar({
  container: '#ew3-pgb-os-02',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-02',
  width: 88,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 15,
    stop: 7.729
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
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
  container: '#ew3-pgb-os-03',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-03',
  width: 88,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 10,
    stop: 3.5
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-04',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-04',
  width: 88,
  height: 6,
  lineCap: 'butt',
  scale: {
    start: 0,
    end: 100,
    stop: 48
  },
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#ew3-pgb-os-05',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-05',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 40,
    stop: 25
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-06',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-06',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 25,
    stop: 10
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-07',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-07',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 1000,
    stop: 760.23
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-08',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-08',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 40,
    stop: 15.765
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
  container: '#ew3-pgb-os-09',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-09',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 3.860,
    stop: 3.860
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
  container: '#ew3-pgb-os-10',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-10',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-11',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-11',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 36
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#ew3-pgb-os-12',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-12',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 2
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#ew3-pgb-os-13',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-13',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 100,
    stop: 60
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true
});

app.createProgressBar({
  container: '#ew3-pgb-os-14',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-14',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 7,
    stop: 7
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
});

app.createProgressBar({
  container: '#ew3-pgb-os-15',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-15',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 63,
    stop: 11
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#ew3-pgb-os-16',
  width: 88,
  height: 6,
  lineCap: 'butt'
});

app.createProgressBar({
  container: '#ew3-pgb-os-16',
  width: 88,
  height: 6,
  lineCap: 'butt',
  gradient: {
    colors: ['#1c95f3', '#18c1ff']
  },
  scale: {
    start: 0,
    end: 7,
    stop: 7
  },
  split: {
    parts: 15,
    gap: 2,
    color: '#fff'
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  decimalPoints: 2
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
  container: '#badge-pgb-novice',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-novice',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 2,
    stop: 2
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-novice-text',
  linkUnits: false,
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-intermediate',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-intermediate',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 101,
    stop: 101
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-intermediate-text',
  linkUnits: false,
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-expert',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-expert',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 501,
    stop: 501
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-expert-text',
  linkUnits: false,
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-legendary',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-legendary',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 1001,
    stop: 1001
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-legendary-text',
  linkUnits: false,
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-staff',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-staff',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-staff-text',
  completeText: 'unlocked!',
  emptyText: 'locked'
});

app.createProgressBar({
  container: '#badge-pgb-moderator',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-moderator',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-moderator-text',
  completeText: 'unlocked!',
  emptyText: 'locked'
});


app.createProgressBar({
  container: '#badge-pgb-level',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-level',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 365,
    stop: 269
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-level-text',
  linkUnits: false,
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-warrior',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-warrior',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-warrior-text',
  completeText: 'unlocked!',
  emptyText: 'locked'
});

app.createProgressBar({
  container: '#badge-pgb-spoiler',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-spoiler',
  width: 160,
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
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-spoiler-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-super-writer',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-super-writer',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 51,
    stop: 51
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-super-writer-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-expert-writer',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-expert-writer',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 201,
    stop: 149
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-expert-writer-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-reviewer',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-reviewer',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 21,
    stop: 21
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-reviewer-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-phantom',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-phantom',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 365,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-phantom-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-thunderstruck',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-thunderstruck',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 51,
    stop: 32
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-thunderstruck-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-traveller',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-traveller',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 11,
    stop: 11
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-traveller-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-super-traveller',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-super-traveller',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 21,
    stop: 21
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-super-traveller-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-liked',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-liked',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 201,
    stop: 201
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-liked-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-super-liked',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-super-liked',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 501,
    stop: 381
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-super-liked-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-ultra-powered',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-ultra-powered',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 40,
    stop: 40
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-ultra-powered-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-contest-winner',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-contest-winner',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-contest-winner-text',
  completeText: 'unlocked!',
  emptyText: 'locked'
});

app.createProgressBar({
  container: '#badge-pgb-collaborator',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-collaborator',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkTo: '#badge-pgb-collaborator-text',
  completeText: 'unlocked!',
  emptyText: 'locked'
});

app.createProgressBar({
  container: '#badge-pgb-caffeinated',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-caffeinated',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 101,
    stop: 101
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-caffeinated-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-ultra-caffeinated',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-ultra-caffeinated',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 201,
    stop: 127
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-ultra-caffeinated-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#badge-pgb-villain',
  width: 160,
  height: 6
});

app.createProgressBar({
  container: '#badge-pgb-villain',
  width: 160,
  height: 6,
  scale: {
    start: 0,
    end: 501,
    stop: 71
  },
  speed: 30,
  gradient: {
    colors: ['#f30a5c', '#1c95f3']
  },
  animateOnScroll: true,
  linkText: true,
  linkUnits: false,
  linkTo: '#badge-pgb-villain-text',
  completeText: 'unlocked!',
  emptyText: 'locked',
  invertedProgress: true
});

app.createProgressBar({
  container: '#progress-bar-lc-01',
  width: 226,
  height: 6
});

app.createProgressBar({
  container: '#progress-bar-lc-01',
  width: 226,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 100
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkText: false
});

app.createProgressBar({
  container: '#progress-bar-lc-02',
  width: 226,
  height: 6
});

app.createProgressBar({
  container: '#progress-bar-lc-02',
  width: 226,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 100
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkText: false
});

app.createProgressBar({
  container: '#progress-bar-lc-03',
  width: 226,
  height: 6
});

app.createProgressBar({
  container: '#progress-bar-lc-03',
  width: 226,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 100
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkText: false
});

app.createProgressBar({
  container: '#progress-bar-lc-04',
  width: 226,
  height: 6
});

app.createProgressBar({
  container: '#progress-bar-lc-04',
  width: 226,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 100
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkText: false
});

app.createProgressBar({
  container: '#progress-bar-lc-05',
  width: 226,
  height: 6
});

app.createProgressBar({
  container: '#progress-bar-lc-05',
  width: 226,
  height: 6,
  scale: {
    start: 0,
    end: 100,
    stop: 100
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkText: false
});

app.createProgressBar({
  container: '#rbb-pgb-01',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-01',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 16,
    stop: 5
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-02',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-02',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 16,
    stop: 10
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-03',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-03',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 16,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-04',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-04',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 16,
    stop: 1
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-05',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-05',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 16,
    stop: 0
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-06',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-06',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 9.2
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#rbb-pgb-07',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-07',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 7.4
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#rbb-pgb-08',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-08',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8.6
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#rbb-pgb-09',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-09',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 4.1
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#rbb-pgb-10',
  width: 355,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-10',
  width: 355,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 9.7
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true,
  decimalPoints: 1
});

app.createProgressBar({
  container: '#rbb-pgb-11',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-11',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 10
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-12',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-12',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-13',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-13',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-14',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-14',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 9
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-15',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-15',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-16',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-16',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 3
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-17',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-17',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 5
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-18',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-18',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 4
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-19',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-19',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 2
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-20',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-20',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 9
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-21',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-21',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 9
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-22',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-22',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-23',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-23',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 6
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-24',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-24',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 7
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});

app.createProgressBar({
  container: '#rbb-pgb-25',
  width: 270,
  height: 6
});

app.createProgressBar({
  container: '#rbb-pgb-25',
  width: 270,
  height: 6,
  scale: {
    start: 0,
    end: 10,
    stop: 8
  },
  speed: 30,
  gradient: {
    colors: ['#420ca2', '#00d8ff']
  },
  linkUnits: false,
  linkText: true
});