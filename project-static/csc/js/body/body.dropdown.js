const app = require('../utils/app.core');

app.createDropdown({
  dropdownSelector: '#ew1-match-selector-dropdown',
  dropdownHandler: '#ew1-match-selector-dropdown-trigger',
  offset: {
    top: 34,
    left: -10
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#ew1-match-selector-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#ew1-match-selector-dropdown-2',
  dropdownHandler: '#ew1-match-selector-dropdown-trigger-2',
  offset: {
    top: 34,
    left: -10
  },
  absolute: true,
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#ew1-match-selector-dropdown-option-value-2'
  }
});

app.createDropdown({
  dropdownSelector: '#ew1-rounds-dropdown',
  dropdownHandler: '#ew1-rounds-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#ew1-rounds-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#li-dropdown-01',
  dropdownHandler: '#li-dropdown-01-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#li-dropdown-01-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#bi-dropdown-01',
  dropdownHandler: '#bi-dropdown-01-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#bi-dropdown-01-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#bsi-dropdown-01',
  dropdownHandler: '#bsi-dropdown-01-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#bsi-dropdown-01-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#filter-01-dropdown',
  dropdownHandler: '#filter-01-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#filter-01-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#filter-02-dropdown',
  dropdownHandler: '#filter-02-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#filter-02-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#filter-03-dropdown',
  dropdownHandler: '#filter-03-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#filter-03-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#filter-04-dropdown',
  dropdownHandler: '#filter-04-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  selectable: true,
  options: {
    container: '.dp-option',
    current: '#filter-04-dropdown-option-value'
  }
});

app.createDropdown({
  dropdownSelector: '#forums-search-dropdown',
  dropdownHandler: '#forums-search-dropdown-trigger',
  offset: {
    top: 44,
    right: -6
  },
  forceClose: true
});

app.createDropdown({
  dropdownSelector: '#forums-user-dropdown',
  dropdownHandler: '#forums-user-dropdown-trigger',
  offset: {
    top: 44,
    right: -34
  },
  forceClose: true
});

app.createDropdown({
  dropdownSelector: '#filter-05-dropdown',
  dropdownHandler: '#filter-05-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  forceClose: true
});

app.createDropdown({
  dropdownSelector: '#filter-06-dropdown',
  dropdownHandler: '#filter-06-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  forceClose: true
});

app.createDropdown({
  dropdownSelector: '#filter-07-dropdown',
  dropdownHandler: '#filter-07-dropdown-trigger',
  offset: {
    top: 34,
    left: 0
  },
  forceClose: true
});