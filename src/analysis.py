import pandas as pd
import numpy as np
import string
from collections import Counter
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import sys
import dateutil.parser
import isodate
import scipy.stats as stats
import datetime
from matplotlib.gridspec import GridSpec

def pareto_plot(df, 
                x=None, 
                y=None, 
                title=None, 
                number_categories = 10, 
                show_pct_y=False, 
                pct_format='{0:.0%}'):
    
    '''adapted from mostly from https://tylermarrs.com/posts/pareto-plot-with-matplotlib/ except as indicated'''

    import matplotlib.pyplot as plt

    dfplot = df[[x,y]]

    dfsorted = dfplot.sort_values(y, ascending=False)
    
    df_shortened = dfsorted[0:number_categories] #added for when there are too many categories to plot
    df_remaining = dfsorted[number_categories:df.shape[0]]
    
    xlabel = x
    ylabel = y
    tmp = df_shortened.sort_values(y, ascending=False)
    tmp = tmp.append({x : 'Other' , y : df_remaining[y].abs().sum()}
                     , ignore_index=True) #adds in an other category which has the sum of the remainder
    x = tmp[x].values
    y = tmp[y].values
    weights = y / y.sum()
    cumsum = weights.cumsum()

    
    fig, ax1 = plt.subplots(figsize = (6,6)) #figsize adjusted to account for rotated labels
    ax1.bar(x, y)
    ax1.set_xlabel(xlabel)
    ax1.tick_params(axis = 'x', rotation = 90) #rotation for longer category names
    ax1.set_ylabel(ylabel)
    
    ax2 = ax1.twinx()
    #ax2.ylim(0, 1.0)  
    ax2.plot(x, cumsum, '-ro', alpha=0.5)
    ax2.set_ylabel('', color='r')
    ax2.tick_params('y', colors='k', rotation = 'auto')
    ax2.set_ylim([0,1])
    
    
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    # hide y-labels on right side
    if not show_pct_y:
        ax2.set_yticks([])
    
    formatted_weights = [pct_format.format(x) for x in cumsum]
    for i, txt in enumerate(formatted_weights):
        ax2.annotate(txt, (x[i], cumsum[i]), fontweight='heavy')    
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    plt.show();

def sorted_bar_plot(df,x,y):

    dfplot = df[[x, y]]
    dfsorted = dfplot.sort_values(y, ascending=False)

    #dfplot.head()

    xlabel = x
    ylabel = y

    x = dfsorted[x].values
    y = dfsorted[y].values

    fig, ax = plt.subplots(figsize = (12, 6))

    ax.bar(x,y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis = 'x', rotation = 90)

def plot_relationships(df, x, y, title=None, xlim=None, ylim=None):
    '''x vs y scatterplot with an uneccesarily complicated name
    '''
    xlabel = x
    ylabel = y
    
    dfplot = df[[x,y]]
    
    
    x = dfplot[x].values
    y = dfplot[y].values
    
    fig, ax1 = plt.subplots(figsize = (6,6))
    ax1.plot(x, y, 'o')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)

def label_points(x, y, val, ax='ax'):
    '''labels points on a scatterplot
    '''
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))

def plot_with_line_of_fit(df,x,y,title=None):
    '''produces an x vs y scatter plot with a linear line of best fit
    '''
    xlabel = x
    ylabel = y
    
    dfplot = df[[x,y]]
    
    x = dfplot[x].values
    y = dfplot[y].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        x,
        y)

    line = slope*x+intercept


    fig, ax1 = plt.subplots(figsize = (6,4))
    ax1.plot(x, y, 'o')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    ax1.plot(x, line)

def line_of_fit(df, x, y):
    
    dfplot = df[[x,y]]
    
    x = dfplot[x].values
    y = dfplot[y].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    line = slope*x + intercept
    
    return line

def word_count(df, col):
    '''while this is used to make a word count, it really just generates three
    lists of words.
    Index 0 = all words in a list of lists
    Index 1 = all words in a singe, flat list
    Index 2 = unique list of words
    '''
    words = []
    for i in df[col]:
        lowercase = str(i).lower()
        separate = lowercase.split()
        no_punctuation = [''.join(c for c in s if c not in string.punctuation) for s in separate]
        words.append(no_punctuation)   

    flat_words = []
    for sublist in words:
        for item in sublist:
            flat_words.append(item)
    
    unique_words = np.unique(flat_words)
    
    return words, flat_words, unique_words

def make_wordcloud(df, col):
    '''adapted from https://www.datacamp.com/community/tutorials/wordcloud-python
    '''

    # Create stopword list:
    stopwords = set(STOPWORDS)
    #stopwords.update()

    # Generate a word cloud image
    wordcloud = WordCloud(max_font_size=50,
                          max_words=100,
                          stopwords=stopwords,
                          background_color="white").generate(' '.join(word_count(df,col)[1]))

    # Create and generate a word cloud image:
    #wordcloud = WordCloud( background_color="white").generate(' '.join(flat_title_words))

    # Display the generated image:
    fig, ax = plt.subplots(figsize=(10,15))
    
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

video_deets_df = pd.read_csv('../data/video_deets_df.csv')

title_dict = {}
for i in video_deets_df['channelTitle'].unique():
    value = i.lower().split()
    no_punctuation = [''.join(c for c in s if c not in string.punctuation) for s in value]
    title_dict[i] = no_punctuation

flat_title_words = []
for sublist in list(title_dict.values()):
    for item in sublist:
        flat_title_words.append(item)
unique_title_words = list(np.unique(flat_title_words))

def word_count_omit_words(df, col, omit_words = title_dict):
    '''Something in this function doesn't quote work, but the intention was to
    use this, for instance, to make a word cloud of words that are in the video
    title, but NOT in the channel titel.
    '''
    words = []
    for i in df[col]:
        lowercase = str(i).lower()
        separate = lowercase.split()
        no_punctuation = [''.join(c for c in s if c not in string.punctuation) for s in separate]
        for j in no_punctuation:
            if j not in omit_words:
                words.append(no_punctuation)   

    flat_words = []
    for sublist in words:
        for item in sublist:
            flat_words.append(item)
    
    unique_words = np.unique(flat_words)
    
    return words, flat_words, unique_words

def make_wordcloud_omit_words(df, col):
    '''Accompanying function to word_count_omit_words
    adapted from https://www.datacamp.com/community/tutorials/wordcloud-python
    '''

    # Create stopword list:
    stopwords = set(STOPWORDS)
    #stopwords.update()

    # Generate a word cloud image
    wordcloud = WordCloud(max_font_size=50,
                          max_words=100,
                          stopwords=stopwords,
                          background_color="white").generate(' '.join(word_count_omit_words(df,col)[1])
                                                            )

    # Create and generate a word cloud image:
    #wordcloud = WordCloud( background_color="white").generate(' '.join(flat_title_words))

    # Display the generated image:
    fig, ax = plt.subplots(figsize=(10,15))
    
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

def create_sub_df(chan,col):
    video_title_df = video_deets_df[['channelTitle',col,'viewCount']]
    data = video_title_df[video_title_df['channelTitle']==chan]
    data = data[[col,'viewCount']]
    data_dict = {}

    for i, row in data.iterrows():
        data_dict[i] = [row['viewCount'],row[col].lower().split()]
        
    return data, data_dict

def top_videos_per_channel(chan, quant):
    '''Returns the top quant % videos from channel = chan'''
    df = video_deets_df[(video_deets_df.channelTitle == chan) & 
                             (video_deets_df.viewCount > 
                              np.quantile(video_deets_df[video_deets_df.channelTitle == chan].viewCount,
                                          quant))].sort_values(by='viewCount', ascending=False)
    return df

def wordcloud_all_vs_top_words_per_channel(df, chan, col, quant):
    #### from https://www.datacamp.com/community/tutorials/wordcloud-python

    # Create stopword list:
    stopwords = set(STOPWORDS)
    #stopwords.update()

    # Generate a word cloud image
    wordcloud1 = WordCloud(max_font_size=50,
                          max_words=50,
                          stopwords=stopwords,
                          background_color="white").generate(
        ' '.join(word_count(video_deets_df[video_deets_df.channelTitle == chan]
                                       ,col)[1])
                                                            )
    wordcloud2 = WordCloud(max_font_size=50,
                          max_words=50,
                          stopwords=stopwords,
                          background_color="white").generate(
        ' '.join(word_count(video_deets_df[(video_deets_df.channelTitle == chan) & 
                             (video_deets_df.viewCount > 
                              np.quantile(video_deets_df[video_deets_df.channelTitle == chan].viewCount,
                                          quant))].sort_values(by='viewCount', ascending=False)
                                       ,col)[1])
                                                            )

    # Create and generate a word cloud image:
    #wordcloud = WordCloud( background_color="white").generate(' '.join(flat_title_words))

    # Display the generated image:
    fig = plt.figure(figsize=(12,12))#subplots(1,2, figsize=(12,12))
    fig.suptitle("Most Popular Words in {} from {}".format(col, chan), y=.65, fontsize=18)
    gs = fig.add_gridspec(1, 2)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(wordcloud1, interpolation='bilinear')
    ax1.axis("off")
    ax1.set_title('All Videos')
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(wordcloud2, interpolation='bilinear')
    ax2.axis("off")
    ax2.set_title('{}% Most Popular Videos'.format(round((1-quant)*100)))

def channel_hist(chan, mostviews, quant):
    
    data = create_sub_df(chan,'videoTitle')[0].viewCount
    
    fig, ax = plt.subplots()

    N, bins, patches = ax.hist(data,
                               edgecolor='white', 
                               linewidth=1, 
                               bins = 30,
                               range = (0,mostviews))

    for patch, leftside, rightside in zip(patches, bins[:-1], bins[1:]):
        if rightside > np.percentile(data,quant):
            patch.set_facecolor('r')
    
    ax.set_xlabel('Views')
    ax.tick_params(axis = 'x', rotation = 90)
    ax.set_ylabel('Video Count')
    ax.set_title('Distribution of Views for {}'.format(chan))