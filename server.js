const express = require('express');
const axios = require('axios');
const app = express();

const port = process.env.PORT || 3000;

app.get('/', async (req, res) => {
  try {
    const response = await axios.get('https://api.twitch.tv/helix/streams?first=5');
    const streams = response.data.data;
    res.json(streams);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching Twitch streams');
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
