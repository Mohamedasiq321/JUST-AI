const axios = require('axios');
const cheerio = require('cheerio');

async function fetchTweets(keyword) {
  try {
    const url = `https://nitter.net/search?f=tweets&q=${encodeURIComponent(keyword)}&since=&until=&near=`;
    const { data } = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0',
      }
    });

    const $ = cheerio.load(data);
    const tweets = [];

    $('div.timeline-item').each((_, el) => {
      const content = $(el).find('.tweet-content').text().trim();
      if (content) tweets.push(content);
    });

    return tweets.slice(0, 10); // return top 10 tweets
  } catch (err) {
    console.error('Twitter scrape error:', err);
    return [];
  }
}

module.exports = fetchTweets;
