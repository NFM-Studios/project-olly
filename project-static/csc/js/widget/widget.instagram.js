(function () {
  const instaWidgetWrap = document.querySelector('.photo-list');
  
  if (!instaWidgetWrap) return;

  const showLoading = function () {
    const loader = document.createElement('div');
    loader.classList.add('loader', 'red');
    instaWidgetWrap.append(loader);
  };

  const showError = function () {
    instaWidgetWrap.innerHTML = '<p class="loader-error">Couldn\'t load Instagram</p>';
  };

  const createInstagramItem = function (data) {
    const item = ` <!-- PHOTO ITEM WRAP -->
      <a target="_blank" href="${data.link}" class="photo-item-wrap">
        <!-- PHOTO ITEM -->
        <figure class="photo-item liquid">
          <img src="${data.images.thumbnail.url}" alt="${data.id}">
        </figure>
        <!-- /PHOTO ITEM -->

        <!-- PHOTO ITEM OVERLAY -->
        <div class="photo-item-overlay">
          <!-- PLUS CC ICON -->
          <svg class="plus-cc-icon">
            <use xlink:href="#svg-plus-cc"></use>
          </svg>
          <!-- /PLUS CC ICON -->
        </div>
        <!-- /PHOTO ITEM OVERLAY -->
      </a>
      <!-- /PHOTO ITEM WRAP -->`;

    return item;
  };

  const createInstagramItems = function (response) {
    const count = 12;
    response = response.data;
    instaWidgetWrap.innerHTML = '';
    for (let i = 0; i < count; i++) {
      instaWidgetWrap.insertAdjacentHTML('beforeend', createInstagramItem(response[i]));
    }
  };

  const contentLoader = require('../utils/content-loader');
  /**
   *  INSTAGRAM FEED
   */
  // Instagram access token, you need to replace this with your access_token value
  const insta_access_token = 'YOUR_ACCESS_TOKEN',
        instaLoader = contentLoader.loadContent({
          url: `https://api.instagram.com/v1/users/self/media/recent/?access_token=${insta_access_token}`,
          onLoading: showLoading,
          loadingDelay: 1000,
          onSuccess: createInstagramItems,
          onError: showError
        });

  instaLoader.load();
})();