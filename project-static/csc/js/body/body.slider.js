const app = require('../utils/app.core');

app.createSlider({
  sliderContainer: '#lvideos-slider1',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#lvideos-slider1-controls'
  }
});

app.createSlider({
  sliderContainer: '#postslide-1',
  // reverse: true,
  // autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'vertical',
    transition: 'direct',
    slideDelay: 5000,
    slideTransition: 700
  },
  controls: {
    container: '#postslide-1-controls'
  }
});

app.createSlider({
  sliderContainer: '#gknews-slider1',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#gknews-slider1-controls'
  }
});

app.createSlider({
  sliderContainer: '#esnews-slider1',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#esnews-slider1-controls'
  }
});

app.createSlider({
  sliderContainer: '#lvideos-slider2',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 0,
    slideCount: 1
  },
  controls: {
    container: '#lvideos-slider2-controls'
  }
});

app.createSlider({
  sliderContainer: '#gmnews-slider1',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#gmnews-slider1-controls'
  }
});

app.createSlider({
  sliderContainer: '#ew1-cmrf-slider',
  itemsContainer: '.carousel-match-result-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  },
  controls: {
    container: '#ew1-cmrf-controls',
    disabledClass: 'disabled'
  },
  stopAtEnd: true
});

app.createSlider({
  sliderContainer: '#ew1-cmr-slider',
  itemsContainer: '.carousel-match-result-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000
  },
  controls: {
    container: '#ew1-cmr-controls',
    disabledClass: 'disabled'
  },
  stopAtEnd: true
});

app.createSlider({
  sliderContainer: '#video-info-slider01',
  itemsContainer: '.video-info-slider-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#video-info-slider01-controls'
  }
});

app.createSlider({
  sliderContainer: '#video-slider01',
  itemsContainer: '.video-slider-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1,
    showCount: 2
  },
  controls: {
    container: '#video-info-slider01-controls'
  }
});

app.createSlider({
  sliderContainer: '#st-videos-slider',
  itemsContainer: '.carousel-items',
  rosterContainer: false,
  autoSlide: false,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideGap: 30,
    slideCount: 1
  },
  controls: {
    container: '#st-videos-slider-controls'
  }
});

app.createSlider({
  sliderContainer: '#product-slider-01',
  itemsContainer: '.product-preview-slider-items',
  rosterContainer: '.product-preview-slider-roster',
  autoSlide: true,
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 5000,
    slideTransition: 800
  }
});

app.createSlider({
  sliderContainer: '#shop-banner-slider',
  itemsContainer: '.slider-items',
  rosterContainer: '.shop-banner-slider-roster',
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideCount: 1
  }
});

app.createSlider({
  sliderContainer: '#product-open-slider-01',
  itemsContainer: '.product-slider-items',
  rosterContainer: '.product-slider-roster-items',
  animation: {
    type: 'carousel',
    orientation: 'horizontal',
    transition: 'direct',
    slideDelay: 7000,
    slideTransition: 1000,
    slideCount: 1
  },
  autoSlide: false
});