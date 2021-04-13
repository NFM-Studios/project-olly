const app = require('../utils/app.core');

/**
 *  SPONSORS SLIDER
 */
app.createSlider({
  sliderContainer: '#footer-sponsor-slider',
  itemsContainer: '.sponsors-slider-items',
  rosterContainer: false,
  autoSlide: false,
  controls: {
    container: '#footer-sponsor-slider-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 6000,
    slideTransition: 1000,
    slideGap: 30
  }
});