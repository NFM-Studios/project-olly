const app = require('../utils/app.core');

/**
 *  LIVE NEWS
 */
app.createLineslide({
  container: '#lineslide-wrap1',
  lineslide: '.live-news-widget-text',
  speed: 1.5,
  startOffset: 100,
  lineslideItems: [
    {
      title: '<a href="post-v1.html" class="link">The "Clash of Eternity" new game was just released: </a>',
      content: 'The new game from the world famous "Eternity Studios" is back with a new adventure game with a lot of classic and puzzle elements',
      separator: '<span class="separator"><span class="separator-bar">/</span><span class="separator-bar">/</span></span>'
    },
    {
      title: '<a href="post-v2.html" class="link">We reviewed the new Magimons game: </a>',
      content: 'Magimons is an incredible take on classic RPGs with a new and fresh approach that includes a mindblowing soundtrack',
      separator: '<span class="separator"><span class="separator-bar">/</span><span class="separator-bar">/</span></span>'
    },
    {
      title: '<a href="post-v3.html" class="link">We reviewed the "Guardians of the Universe" movie: </a>',
      content: 'The latest movie from the franchise has a lot of interesting and fun stuff to look for',
      separator: '<span class="separator"><span class="separator-bar">/</span><span class="separator-bar">/</span></span>'
    },
    {
      title: '<a href="post-v4.html" class="link">Check out some Hearte Bunny original design ideas: </a>',
      content: 'Also, get a sneak peak of the new season looks',
      separator: '<span class="separator"><span class="separator-bar">/</span><span class="separator-bar">/</span></span>'
    },
    {
      title: '<a href="esports-post.html" class="link">Last night the Wolves beat the Rhinos 12-10: </a>',
      content: 'In an intense match, the Lone Wolves came out victorious. Read all about the big night here',
      separator: '<span class="separator"><span class="separator-bar">/</span><span class="separator-bar">/</span></span>'
    }
  ]
});