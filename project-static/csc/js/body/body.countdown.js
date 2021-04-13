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

/**
 * Countdown
 */
app.createCountdown({
  container: '#countdown-arc',
  startDate: new Date(today.year, today.month, today.day - 1),
  targetDate: new Date(today.year, today.month, today.day + 4),
  global: {
    underlineConfig: {
      width: 66,
      height: 66,
      lineWidth: 6
    },
    arcConfig: {
      width: 66,
      height: 66,
      lineWidth: 6,
      pad: true
    }
  }
});

app.createProgressBar({
  width: 140,
  container: '#ew1-match-cd-pgb'
});

const ew1_match_pgb = app.createProgressBar({
  width: 140,
  container: '#ew1-match-cd-pgb',
  gradient: {
    colors: ['#713fcb', '#00e3d0']
  },
  controlAnimation: true
});

if (ew1_match_pgb) {
  app.createCountdown({
    container: '#ew1-match-cd-text',
    startDate: new Date(today.year, today.month - 1, today.day),
    targetDate: new Date(today.year, today.month, today.day + 13),
    textOnly: true,
    onStep: ew1_match_pgb.render
  });
}