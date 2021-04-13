const app = require('../utils/app.core');

app.createDropdown({
  dropdownSelector: '#lang-dropdown',
  dropdownHandler: '#lang-dropdown-trigger',
  offset: {
    top: 54,
    left: -10
  },
  selectable: true,
  options: {
    container: '.widget-option',
    current: '#lang-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#curr-dropdown',
  dropdownHandler: '#curr-dropdown-trigger',
  offset: {
    top: 54,
    left: 40
  },
  selectable: true,
  options: {
    container: '.widget-option',
    current: '#curr-dropdown-option-value'
  },
  breakpoints: {
    960: {
      offset: {
        left: -10
      }
    }
  }
});

app.createDropdown({
  dropdownSelector: '#account-dropdown',
  dropdownHandler: '#account-dropdown-trigger',
  offset: {
    top: 54,
    left: -54
  }
});

app.createDropdown({
  dropdownSelector: '#lang-dropdown-2',
  dropdownHandler: '#lang-dropdown-trigger-2',
  offset: {
    top: 54,
    left: -10
  },
  selectable: true,
  options: {
    container: '.widget-option',
    current: '#lang-dropdown-option-value-2'
  }
});

app.createDropdown({
  dropdownSelector: '#curr-dropdown-2',
  dropdownHandler: '#curr-dropdown-trigger-2',
  offset: {
    top: 54,
    left: 40
  },
  selectable: true,
  options: {
    container: '.widget-option',
    current: '#curr-dropdown-option-value-2'
  },
  breakpoints: {
    960: {
      offset: {
        left: -10
      }
    }
  }
});

app.createDropdown({
  dropdownSelector: '#account-dropdown-2',
  dropdownHandler: '#account-dropdown-trigger-2',
  offset: {
    top: 54,
    right: -10
  }
});