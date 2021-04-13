const app = require('../utils/app.core');

app.createAccordion({
  triggerSelector: '.accordion-trigger',
  contentSelector: '.accordion-content'
});

app.createAccordion({
  triggerSelector: '.payment-method-trigger',
  contentSelector: '.payment-method-content',
  linkTriggers: true,
  triggerOpens: true
});

app.createAccordion({
  triggerSelector: '.faq-item-trigger',
  contentSelector: '.faq-item-content',
  animation: {
    speed: .6
  }
});