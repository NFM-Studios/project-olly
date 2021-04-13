const app = require('../utils/app.core');

/**
 *  SHOP SLIDER
 */
app.createSlider({
  sliderContainer: '#submenu-slider-1',
  itemsContainer: '.submenu-slider-items',
  rosterContainer: '.submenu-slider-options',
  rosterControls: {
    triggerEvent: 'mouseover'
  },
  autoSlide: false,
  lock: false,
  animation: {
    type: 'static',
    orientation: 'vertical',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#submenu-slider-2',
  itemsContainer: '.submenu-slider-items',
  rosterContainer: '.submenu-slider-options',
  rosterControls: {
    triggerEvent: 'mouseover'
  },
  autoSlide: false,
  lock: false,
  animation: {
    type: 'static',
    orientation: 'vertical',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#submenu-ns-news-slider',
  itemsContainer: '.news-section-categories',
  rosterContainer: '.news-section-options',
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'vertical',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  }
});

app.createSlider({
  sliderContainer: '#submenu-gr-slider1',
  itemsContainer: '.news-section-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 3
  },
  controls: {
    container: '#submenu-gr-controls'
  }
});

app.createSlider({
  sliderContainer: '#submenu-gn-slider1',
  itemsContainer: '.news-section-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 3
  },
  controls: {
    container: '#submenu-gn-controls'
  }
});

app.createSlider({
  sliderContainer: '#submenu-gkn-slider1',
  itemsContainer: '.news-section-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 3
  },
  controls: {
    container: '#submenu-gkn-controls'
  }
});

app.createSlider({
  sliderContainer: '#submenu-mn-slider1',
  itemsContainer: '.news-section-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 3
  },
  controls: {
    container: '#submenu-mn-controls'
  }
});

app.createSlider({
  sliderContainer: '#submenu-esn-slider1',
  itemsContainer: '.news-section-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 3
  },
  controls: {
    container: '#submenu-esn-controls'
  }
});