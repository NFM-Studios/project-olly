const app = require('../utils/app.core');

app.createTooltip({
  container: '.ew1-lineups-tooltip',
  direction: 'top',
  align: 'center',
  offset: -10,
  animation: {
    type: 'translate-out-fade'
  }
});

app.createTooltip({
  container: '.ew2-lineups-tooltip',
  direction: 'top',
  align: 'center',
  offset: -10,
  animation: {
    type: 'translate-out-fade'
  }
});