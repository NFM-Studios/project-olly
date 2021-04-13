const app = require('../utils/app.core');

/**
 *  SEARCH POPUP
 */
const searchPopupOpen = document.querySelectorAll('.search-popup-open'),
      searchPopupClose = document.querySelectorAll('.search-popup-close'),
      searchPopup = document.querySelector('.search-popup'),
      searchPopupInput = document.querySelector('.input-line'),
      searchPopupText = document.querySelector('.search-popup-text');

if (searchPopupOpen && searchPopupClose && searchPopup && searchPopupInput && searchPopupText) {
  searchPopup.style.height = `${document.body.offsetHeight}px`;

  const disableScroll = function () {
    document.body.style.overflowY = 'hidden';
  };

  const enableScroll = function () {
    document.body.style.overflowY = 'auto';
  };

  const closeSearchPopupOnKeyPress = function (e) {
    if (e.keyCode === 27) {
      closeSearchPopup();
    }
  };

  const openSearchPopup = function () {
    disableScroll();
    searchPopup.classList.add('open');
    searchPopupInput.classList.add('animate');
    searchPopupText.classList.add('animate');
    setTimeout(function () {
      searchPopupInput.focus();
    }, 500);

    document.addEventListener('keydown', closeSearchPopupOnKeyPress);
  };

  const closeSearchPopup = function () {
    enableScroll();
    searchPopup.classList.remove('open');
    searchPopupInput.value = '';
    searchPopupInput.classList.remove('animate');
    searchPopupText.classList.remove('animate');

    document.removeEventListener('keydown', closeSearchPopupOnKeyPress);
  };

  app.addListener(searchPopupOpen, 'click', openSearchPopup);
  app.addListener(searchPopupClose, 'click', closeSearchPopup);
}
