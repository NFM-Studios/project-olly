const parseDate = function (dateText) {
  const targetDate = new Date(dateText),
        todayDate = new Date(),
        diffDate = (todayDate.getTime() - targetDate.getTime()) / 1000,
        daysLeft = window.parseInt(diffDate / 86400),
        hoursLeft = window.parseInt(diffDate / 3600) % 24,
        minutesLeft = window.parseInt(diffDate / 60) % 60,
        secondsLeft = window.parseInt(diffDate) % 60;

  let measure, time;

  if (daysLeft > 0) {
    measure = 'days';
    time = daysLeft;
  } else if (hoursLeft > 0) {
    measure = 'hours';
    time = hoursLeft;
  } else if (minutesLeft > 0) {
    measure = 'minutes';
    time = minutesLeft;
  } else if (secondsLeft > 0) {
    measure = 'seconds';
    time = secondsLeft;
  }

  return `${time} ${measure} ago`;
};

const parseText = function (text) {
  const hashtag = /(#\w*)/ig,
        atTag = /(@(\w*))/ig,
        link = /((http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?)/ig;

  text = text.replace(link, '<a href="$1" class="highlighted">$1</a>');
  text = text.replace(hashtag, '<span class="highlighted">$1</span>');
  text = text.replace(atTag, '<a href="https://twitter.com/$2" class="highlighted">$1</a>');

  return text;
};

const tweetsContainer = document.querySelectorAll('.tweets-preview-widget');

const showLoading = function () {
  tweetsContainer.forEach( (e) => {
    const loader = document.createElement('div');
    loader.classList.add('loader', 'blue');
    e.append(loader);
  });
};

const showError = function () {
  tweetsContainer.forEach( (e) => {
    e.innerHTML = '<p class="loader-error">Couldn\'t load Twitter</p>';
  });
};

const createTweetItem = function (container, data) {
  const tweetItem = document.createElement('div');
  tweetItem.classList.add('tweets-preview-widget-item');

  if (container.classList.contains('v2')) {
    tweetItem.innerHTML += `<p class="tweets-prevew-widget-item-user">@${data.user.screen_name}</p>
    <img class="tweets-preview-widget-item-profile-img" src="${data.user.profile_image_url}" alt="profile-img">`;
  } else {
    tweetItem.innerHTML += `<!-- BUBBLE ORNAMENT -->
    <a href="#" class="bubble-ornament twt">
      <!-- TWITTER ICON -->
      <svg class="twitter-icon">
        <use xlink:href="#svg-twitter"></use>
      </svg>
      <!-- /TWITTER ICON -->
    </a>
    <!-- /BUBBLE ORNAMENT -->`;
  }

  tweetItem.innerHTML += `<p class="tweets-preview-widget-item-text">${parseText(data.text)}</p>
  <p class="tweets-preview-widget-item-timestamp">${parseDate(data.created_at)}</p>`;
  
  return tweetItem;
};

const createTweetItems = function (response) {
  tweetsContainer.forEach( (e) => {
    e.innerHTML = '';
  });
  
  response.forEach(function (el) {
    tweetsContainer.forEach( (e) => {
      e.append(
        createTweetItem(e, el)
      );
    });
  });
};

const contentLoader = require('../utils/content-loader'),
      count = 3;
/**
 *  TWITTER FEED
 */
const tweetsLoader = contentLoader.loadContent({
        url: `http://localhost:3003/tweets_last/${count}`,
        onLoading: showLoading,
        loadingDelay: 1000,
        onSuccess: createTweetItems,
        onError: showError
      });

tweetsLoader.load();