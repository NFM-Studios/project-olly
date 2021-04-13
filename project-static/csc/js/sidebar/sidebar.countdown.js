const app = require('../utils/app.core');

/**
 * Countdown auto - restart
 */
const now = new Date(),
      today = {
        day: now.getDate(),
        month: now.getMonth(),
        year: now.getFullYear()
      };

app.createCountdown({
  container: '#sidebar-twitch-countdown-1',
  startDate: new Date(today.year, today.month - 1, today.day),
  targetDate: new Date(today.year, today.month, today.day + 12),
  textOnly: true,
  textCounter: {
    days: false
  }
});

app.createProgressBar({
  container: '#ew1-pgb-cd'
});

const ew1_sd_pgb = app.createProgressBar({
  container: '#ew1-pgb-cd',
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  controlAnimation: true
});

if (ew1_sd_pgb) {
  app.createCountdown({
    container: '#ew1-cd-text',
    startDate: new Date(today.year, today.month - 1, today.day),
    targetDate: new Date(today.year, today.month, today.day + 12),
    textOnly: true,
    onStep: ew1_sd_pgb.render
  });
}