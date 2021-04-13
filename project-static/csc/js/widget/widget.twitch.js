const twitchPlayerContainer = document.querySelector('#streamer-twitch-channel-01');

if (twitchPlayerContainer) setupTwitchWidget();

function setupTwitchWidget() {
  /**
   *  TWITCH VOD
   */
  const options = {
    width: '100%',
    height: 520,
    // video: '387234761',
    channel: 'riotgames',
    autoplay: false,
    theme: 'dark'
  },
  player = new Twitch.Embed('streamer-twitch-channel-01', options);
}
