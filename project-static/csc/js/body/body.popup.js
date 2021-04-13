const app = require('../utils/app.core');

app.createPopup({
  container: '#popup-login',
  trigger: '.popup-login-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-register',
  trigger: '.popup-register-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-player-builds',
  trigger: '.popup-player-builds-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-advanced-search',
  trigger: '.popup-advanced-search-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-create-topic',
  trigger: '.popup-create-topic-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-quick-reply',
  trigger: '.popup-quick-reply-trigger',
  animation: {
    type: 'translate-out-fade'
  },
  align: 'bottom',
  sticky: true
});

app.createPopup({
  container: '#popup-write-review',
  trigger: '.popup-write-review-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});

app.createPopup({
  container: '#popup-watch-video',
  trigger: '.popup-watch-video-trigger',
  animation: {
    type: 'translate-out-fade'
  }
});