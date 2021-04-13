const ChartJS = require('chart.js'),
      Overlay = require('./Overlay'),
      app = {};

app.createArc = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Arc');
  if (!document.querySelector(config.container)) return;
  return new XM_Arc(config);
};

app.createCountdown = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Countdown');
  if (!document.querySelector(config.container)) return;
  return new XM_Countdown(config);
};

app.createProgressBar = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_ProgressBar');
  if (!document.querySelector(config.container)) return;
  return new XM_ProgressBar(config);
};

app.createSlider = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Slider');
  if (!document.querySelector(config.sliderContainer)) return;
  return new XM_Slider(config);
};

app.createDropdown = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Dropdown');
  if (!document.querySelector(config.dropdownSelector)) return;
  return new XM_Dropdown(config);
};

app.createLineslide = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Lineslide');
  if (!document.querySelector(config.container)) return;
  return new XM_Lineslide(config);
};

app.createTooltip = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Tooltip');
  if (!document.querySelector(config.container)) return;
  return new XM_Tooltip(config);
};

app.createPopup = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Popup');
  if (!document.querySelector(config.container)) return;
  return new XM_Popup(config);
};

app.createTab = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Tab');
  if (!document.querySelector(config.container)) return;
  return new XM_Tab(config);
};

app.createAccordion = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Accordion');
  if (!document.querySelector(config.triggerSelector)) return;
  return new XM_Accordion(config);
};

app.createCalendar = function (config) {
  if (!config) throw new Error('Must pass a configuration object in order to create an XM_Calendar');
  if (!document.querySelector(config.container)) return;
  return new XM_Calendar(config);
};

app.createChart = function (ctx, config) {
  if (!config) throw new Error('Must pass a configuration object in order to create a ChartJS');
  if (!ctx) return;
  return new ChartJS(ctx, config);
};

app.createOverlay = function () {
  return new Overlay();
};

app.addListener = function (el, event, fn) {
  for (let i = 0; i < el.length; i++) {
    el[i].addEventListener(event, fn);
  }
};

module.exports = app;