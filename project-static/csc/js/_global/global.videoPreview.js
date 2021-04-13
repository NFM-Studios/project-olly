(function () {
  const videoPreviews = document.querySelectorAll('.post-preview-video-wrap');
  if (!videoPreviews.length) return;

  const showVid = function () {
    // hide overlay
    this.querySelector('.post-preview-overlay').style.visibility = 'hidden';
    // hide img
    this.querySelector('.post-preview-img').style.visibility = 'hidden';
    // show video
    this.querySelector('.post-preview-video-wrap').style.visibility = 'visible';

    this.removeEventListener('click', showVid);
  };

  videoPreviews.forEach( (el) => {
    el.parentElement.addEventListener('click', showVid);
  });
})();