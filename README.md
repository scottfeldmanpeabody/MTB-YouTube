# MTB-YouTube: What leads to more views?

## Background

I'm fascinated with YouTube and how it works. Not only the content of the videos themselves, but the "inside baseball" story of how and why channels become popular. Quite neatly juxtaposing YouTube with my love of cycling is the subject of mountain bike (MTB) videos on YouTube. 

An anecdote to get started: The most popular MTB YouTube channel is Fabio Wibmer, with 2.7M+ subscribers. Unsuprisingly, Fabio is a pro, is sponsored by Red Bull, and makes videos with huge production costs that involve things like jumping out of helicopters and riding his bike down ski resorts:

![alt text](https://i.ytimg.com/vi/1CR0QmCaMTs/maxresdefault.jpg)
[Fabio Wibmer - Tabio Wibmer - Fabiolous Escape 2](https://www.youtube.com/watch?v=1CR0QmCaMTs)

The *second* most popular MTB channel is "Seth's Bike Hacks," with 1.5M+ subscribers. In contrast to Fabio, Seth did not start his channel as a pro, but simply as some dude from Ft. Lauderdale who figures out ways to stop frayed cables and how to run away from gnats effectively. Despite his humble video begginings, Seth has been on top of MTB YouTube for awhile now and regularly gets over 1M views per video. Somehow, he grew with channel without being in a hotbed of mountain biking like Colorado or Utah, not Florida. Is his success all intrinsic to the quality of his videos or does he know something about how to position his videos to gain maximum views?

![10 Bike Hacks that will Blow Your Mind! 🚴🏼 Sorta](https://i.ytimg.com/vi/PrtDD7VHe3g/maxresdefault.jpg)
[10 Bike Hacks that will Blow Your Mind! 🚴🏼 Sorta](https://www.youtube.com/watch?v=PrtDD7VHe3g)

## Data

YouTube provides an [API](https://developers.google.com/youtube/v3/) for developers to access it's data. It's mostly very well [documented](https://developers.google.com/youtube/v3/docs/) with a coder builder for multiple languages, including Python (used here). Developers can sign up for projects and get an API Key to access publically available data. There's also a function for OAuth 2.0 authorization which can be used to access private information on specific channels given login credentials. Only the publically available data was used here.

### Data Pipeline
1. Channels associated with mountain biking were searched for using the API search function
2. Specific channels were hand-picked from the resulting list due to items of interest (see the motivation above, I'm less interested in GoPro vidoes that happen to be about mountain biking than I am in creators dedicated to the subject)
3. Aggregate channel data was pulled from YouTube's API. This includes things like subscriber count and total views. Importantly, it also includes the "uploads" playlist, which allowed me to access all the videos from a particular channel
4. Information on the individual videos associated with the channels identified above was pulled including descriptions and runtimes, as well as statics such as views and likes.

Due to quota limitations from Youtube, a modest 23 channels were pulled with iformation from a total of 7850 videos.

Though the dataset was almost entirely complete, some cleanup had to be done. Data types had to be defined, ISO8601 datetimes needed to be converted to something useable, and a couple missing values had to be dealt with (in this case they were excluded). In addition to the raw numbers provided by YouTube, some additional variables were calculated such as the views per video and the number of days since video upload.

## Exploratory Data Analysis

### Channel Data

First, the channels with the top views, subscribers, and number of video uploads were identified.
![channelView Pareto Plot](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/pareto_channelViews.png)

![subscriber Pareto Plot](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/pareto_subscriberCount.png)

![uploads Pareto Plot](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/pareto_videoCount.png)

Views are what drives a channel's revenue from YouTube, so the relationships between views and other factors was plotted. In the following charts, all channels in the sample group were plotted on the left with a smaller scale plotted on the right so that specific channels can be distinguished:

![views by subcribers](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/channelViews_by_subscriberCount.png)

In the plot on the left, there seems to be a roughtly linear relationship between subscribers and views (orange line). This relationship is strengthened if Fabio Wibmer is eliminated (green line). My subspicion is that Fabio has "transcended" the genre of mountain biking with a number of viral videos which has earned him extra subscribers, but those subscribers don't necessarily result in more views.

![views per subcriber](https://github.com/scottfeldmanpeabody/MTB-YouTube-EDA/blob/master/images/viewsPerSubscriber.png)

Indeed, when looking at the metric of #views / #subscribers, there is a variation of over 2.5 times of the channels studied. Interestingly, it's some of the smaller channels that are higher in this metric.

![views by videos](https://github.com/scottfeldmanpeabody/MTB-YouTube-EDA/blob/master/images/channelViews_by_videoCount.png)

When looking at views vs. videos uploaded, there may be two clusters that emerge: those that have higher views per subscriber (e.g Fabio Wibmer, Seth's Bike Hacks, IFHT) and those that have fewer (e.g. Global Mountain Bike Network, Sam Pilgrim). Zooming in to the smaller channels (chart on the right), a magnified view of this apparent phenomenon is seen. Are there other factors that can identify these two camps?

![views by videos](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/viewsPerVideo.png)

Viewing this as a bar plot of the quotient #views / #videos, one can see a large variation in the number of views per video uploaded. Some of the most popular channels have the highest value, but, notably, Global Mountain Bike Network has very few. Perhaps this channels strategy of near-daily uploads might be better spent on making fewer, higher quality videos? In contrast, IFHT has by far the highest views per video. This channel is known for their high production value.

### Video Popularity

Again, the focus here is channel views, not subscribers, because views leads to income. Subcribers may drive views (and vice versa), but ultimately, creators don't get paid based on subscribers.

![histogram of views](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/hist_views_per_video.png)

Several variables were explored to see if they could explain video views. Ultimately, it looked like the pattern of views by these variables simply followed the distribution of the variables themselves. Shown below, is the relationship between the video views and word counts in the video title and video description.

![views vs. word counts](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/video_views_vs_word_counts.png)

Thought there does seem to be a patter to the scatter plots on the left, they seem to just follow the distribution of the word counts shown in the histograms on the right.

Likewise, there doesn't seem to be a relationship between video duration and number of views:

![views vs. video duration](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/video_views_vs_duration.png)

While there are a lot of popular videos around 10 minutes (red line), there are just plain a lot of videos that are made of a length of about 10 minutes. Incidentally, I believe this is the length that YouTube starts allowing mid-roll ads, potentially leading to higer income for that creator.

A priori, one might suspect that videos that have been out longer tend to have more views. After all, they've had more time to get those views. However, this seems to not be the case:

![views vs. time released](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/video_views_vs_days_since_released.png)

Note: the dropoff at ~1300 days is probably due to when many of the channels selected for this analysis were started.

Zooming in on this data, there seems to be a flat distribution of views vs. days since the video has been released, indicating that most views come soon after release, and also that, in general, creators shouldn't count on an overwhelming increase in income over time once they've built up a large catalog.

### Word Analysis

There is a clear trend on words that in video titles...

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloud_all_video_titles.png)

...and descriptions...

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloud_all_descriptions.png)

There's a very high overlap with the channel title itself!

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloud_all_channel_titles.png)

Finally, a comparison was done between the title words from all videos and the title words from the videos in the top 5% popularity for that channel. First the two word clouds for each channel are plotted, followed by a histogram of the views per video. In these histograms the top 5% most popular videos are colored red.

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloud_BKXC.png)

![histogram](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/histBKXC.png)

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloudSYDandMACKY.png)

![histogram](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/histSYDandMACKY.png)

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloud_SethsBikeHacks.png)

![histogram](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/histSethsBikeHacks.png)

![wordcloud](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/wordcloudGMBN.png)

![histogram](https://github.com/scottfeldmanpeabody/MTB-YouTube/blob/master/images/histGMBN.png)

One thing that stands out about the distributions is that they all have a steep rise on the left side with a long tail to the right. The scale is cut off, but most of them have one or two viral videos with close to a million views or more.

As for the word clouds, there may be more specificity (e.g. riding locations) to the words in the top 5% bucket, but probably because those are pointing to specific videos, not because those words are popular. The only thing obviously systematic is no reference to Global Mountain Bike Network's weekly "Dirt Shed Show" in the top 5% videos. Apparently these weekly shows do not go viral.

## Further Work

None of the features studied clearly resulted in more views beyond popular channels are popular channels. The advice here to aspiring YouTubers would be to focus on exciting content.

There are many places one could go with this work to try to identify what helps make videos popular other than the content iteself. Some ideas:
* NLP on video titles and descriptions to see if one can pull out predictors of specific words (if any) that lead to higher views. Include whether using ALL CAPS and or lots of exclamation points!!!! nets more views. What about question marks???
* Explore the relationships between views and engagement (likes, dislikes, comments)
* Use of image analysis to pull out features of thumbnails (faces, first person view of the handlebars, trail features)
* Look at how subcribers and views have grown with time. Is it specific videos that cause the bumps? To do this retrospectively would require access to individual channels accounts.
