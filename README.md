# MTB-YouTube

## Background

I'm fascinated with YouTube and how it works. Not only the content of the videos themselves, but the "inside baseball" story of how and why channels become popular. Quite neatly juxtaposing YouTube with my love of cycling is the subject of mountain bike (MTB) videos on YouTube. 

An anecdote to get started: The most popular MTB YouTube channel is Fabio Wibmer, with 2.7M+ subscribers. Unsuprisingly, Fabio is a pro, is sponsored by Red Bull, and makes videos with huge production costs that involve things like riding his bike down a ski resort:

![alt text](https://i.ytimg.com/vi/1CR0QmCaMTs/maxresdefault.jpg)
[Fabio Wibmer - Tabio Wibmer - Fabiolous Escape 2](https://www.youtube.com/watch?v=1CR0QmCaMTs)

The *second* most popular MTB channel is "Seth's Bike Hacks," with 1.5M+ subscribers. In contrast to Fabio, Seth did not start his channel as a pro, but simply as some dude from Ft. Lauderdale. Seth has been on top of MTB YouTube for awhile now and regularly gets over 1M views per video. Somehow, he grew with channel without being in a hotbed of mountain biking like Colorado or Utah, not Florida. Is his success all intrinsic to the quality of his videos or does he know something about how to position his videos to gain maximum views?

![alt text](https://i.ytimg.com/vi/PrtDD7VHe3g/maxresdefault.jpg)
[10 Bike Hacks that will Blow Your Mind! 🚴🏼 Sorta](https://www.youtube.com/watch?v=PrtDD7VHe3g)

## Data

YouTube provides an [API](https://developers.google.com/youtube/v3/) for developers to access it's data. It's mostly very well [documented](https://developers.google.com/youtube/v3/docs/) with a coder builder for multiple languages, including Python (used here). Developers can sign up for projects and get an API Key to access publically available data. There's also a function for OAuth 2.0 authorization which can be used to access private information on specific channels given login credentials. Only the publically available data was used here.

### Data Pipeline
1. Channels associated with mountain biking were searched for using the API search function
2. Specific channels were hand-picked from the resulting list due to items of interest (see the motivation above, I'm less interested in GoPro vidoes that happen to be about mountain biking than I am in creators dedicated to the subject)
3. Aggregate channel data was pulled from YouTube's API. This includes things like subscriber count and total views. Importantly, it also includes the "uploads" playlist, which allowed me to access all the videos from a particular channel
4. Information on the individual videos associated with the channels identified above was pulled including descriptions and runtimes, as well as statics such as views and likes.


