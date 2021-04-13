module.exports.loadContent = function (config) {
  const me = {};

  const queryItems = function () {
    $.ajax({
      url: config.url,
      success: config.onSuccess,
      error: config.onError
    });
  };

  me.load = function () {
    config.onLoading();
    window.setTimeout(queryItems, config.loadingDelay);
  };

  return me;
};