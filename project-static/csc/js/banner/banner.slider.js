const app = require('../utils/app.core');

app.createSlider({
  sliderContainer: '#banner-slider-1',
  rosterContainer: '.banner-slider-roster',
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 5000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#banner-slider-2',
  rosterContainer: '.banner-slider-preview-roster',
  controls: {
    container: '#sliderb2-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 6000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#banner-slider-2-thumbs',
  itemsContainer: '.banner-slider-preview-roster',
  rosterContainer: false,
  slideOnClick: true,
  loop: true,
  loopOffset: 1,
  controls: {
    container: '#sliderb2-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    slideDelay: 6000,
    slideTransition: 1000,
    slideGap: 146
  }
});

app.createSlider({
  sliderContainer: '#banner-slider-3',
  rosterContainer: false,
  // reverse: true,
  // autoSlide: false,
  controls: {
    container: '#banner-slider-3-controls'
  },
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 8000,
    slideTransition: 1000,
    slideCount: 1
  }
});