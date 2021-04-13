const app = require('../utils/app.core');

/**
 *  INVENTORY BAG PREVIEW
 */
const inventoryBagTrigger = document.querySelector('.inventory-button'),
      inventoryBagPreview = document.querySelector('.inventory-bag-preview'),
      inventoryBagClose = document.querySelector('.inventory-close-button');

if (inventoryBagPreview && inventoryBagTrigger && inventoryBagClose) {
  let inventoryOpen = false,
      overlay = app.createOverlay();

  overlay.element.appendChild(inventoryBagPreview);

  const openInventory = function () {
    if (inventoryOpen) return;
    inventoryBagPreview.style.transform = `translate(-100%, 0)`;
    inventoryOpen = true;
    overlay.show();
    overlay.addTrigger({
      event: 'click',
      callback: closeInventory
    });
  };

  const closeInventory = function () {
    if (!inventoryOpen) return;
    inventoryBagPreview.style.transform = `translate(0, 0)`;
    inventoryOpen = false;
    overlay.hide();
  };

  inventoryBagTrigger.addEventListener('click', openInventory);
  inventoryBagClose.addEventListener('click', closeInventory);
}