const app = require('../utils/app.core');

/**
 *  MOBILE MENU TOGGLE
 */
const mobileMenu = document.querySelector('.mobile-menu-wrap'),
      mobileMenuOpen = document.querySelector('.mobile-menu-open'),
      mobileMenuClose = document.querySelector('.mobile-menu-close');

if (mobileMenu && mobileMenuOpen && mobileMenuClose) {
  const overlay = app.createOverlay();

  overlay.element.appendChild(mobileMenu);

  const openMobileMenu = function () {
    mobileMenu.classList.add('open');
    overlay.show();
    overlay.addTrigger({
      event: 'click',
      callback: closeMobileMenu
    });
  };

  const closeMobileMenu = function () {
    mobileMenu.classList.remove('open');
    overlay.hide();
  };

  mobileMenuOpen.addEventListener('click', openMobileMenu);
  mobileMenuClose.addEventListener('click', closeMobileMenu);
  
  /**
   *  MOBILE MENU DROPDOWNS
   */
  $('.pd-dropdown-handler').on('click', function () {
    $(this).parent().toggleClass('active');
    $(this).siblings('.pd-dropdown').slideToggle(600);
  });  
}
