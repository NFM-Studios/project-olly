const app = require('../utils/app.core');

app.createTooltip({
  container: '.ew3-wtl-tooltip',
  direction: 'top',
  tooltipSelector: ['xm-tooltip', 'v2'],
  align: 'center',
  offset: 2,
  animation: {
    type: 'translate-out-fade'
  }
});