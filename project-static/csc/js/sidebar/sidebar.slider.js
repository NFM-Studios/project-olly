const app = require('../utils/app.core');

app.createSlider({
  sliderContainer: '#award-slider',
  itemsContainer: '.widget-slider-items',
  rosterContainer: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  },
  controls: {
    container: '#award-slider-controls',
    disabledClass: 'disabled'
  }
});