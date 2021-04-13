const app = require('../utils/app.core');

app.createSlider({
  sliderContainer: '#po-slideshow1',
  rosterContainer: false,
  controls: {
    container: '#po-slideshow1-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 5000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#po-slideshow1-1',
  itemsContainer: '.slider-roster',
  rosterContainer: false,
  controls: {
    container: '#po-slideshow1-controls'
  },
  animation: {
    type: 'fade',
    orientation: 'horizontal',
    slideDelay: 5000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#po-slideshow2',
  controls: {
    container: '#po-slideshow2-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 8000,
    slideTransition: 1000
  }
});