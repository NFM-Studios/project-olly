module.exports = Overlay;

function Overlay () {
  if (typeof Overlay.instance === 'undefined') {
    Overlay.instance = this;
  
    this.show = () => {
      this.element.classList.add('open');
    };

    this.hide = () => {
      this.element.classList.remove('open');
    };

    this.addTrigger = (config) => {
      const callback = () => {
        config.callback();
        this.hide();
        this.element.removeEventListener(config.event, callback);
      };

      this.element.addEventListener(config.event, function (e) {
        if (e.target === this) {
          callback();
        }
      });
    };

    (function init () {
      Overlay.instance.element = document.createElement('div');
      Overlay.instance.element.classList.add('window-overlay');
      Overlay.instance.element.addEventListener('click', function (e) {
        if (e.target === this) {
          Overlay.instance.hide();
        }
      });
      document.body.appendChild(Overlay.instance.element);
    })();
  }

  return Overlay.instance;
}