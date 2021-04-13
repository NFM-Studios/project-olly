const app = require('../utils/app.core');
const currentYear = (new Date()).getFullYear(),
      currentMonth = (new Date()).getMonth();

app.createCalendar({
  container: '#calendar-01',
  events: {
    [new Date(currentYear, currentMonth, 14)]: [
      {
        name: 'Funtendo Online Event',
        info: 'some event info',
        type: 'blue'
      },
      {
        name: 'Fighter X Release!',
        info: 'some other event info',
        type: 'green'
      }
    ],
    [new Date(currentYear, currentMonth, 26)]: [
      {
        name: 'League of Heroes Semifinals',
        info: 'some event info',
        type: 'violet'
      }
    ],
    [new Date(currentYear, currentMonth-1, 30)]: [
      {
        name: 'League of Heroes Semifinals',
        info: 'some event info',
        type: 'violet'
      }
    ]
  },
  linksTo: 'event.html'
});