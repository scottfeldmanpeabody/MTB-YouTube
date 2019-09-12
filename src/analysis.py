# mostly from https://tylermarrs.com/posts/pareto-plot-with-matplotlib/ except as indicated

def pareto_plot(df, 
                x=None, 
                y=None, 
                title=None, 
                number_categories = 10, 
                show_pct_y=False, 
                pct_format='{0:.0%}'):
    '''Generates a pareto plot with a specified number of categories and puts
    the remainder of the values into a category called Other
    '''
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
    ax2.tick_params('y', colors='r', rotation = 'auto')
    
    
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

def word_count(df, col):
    '''while this is used to make a word count, it really just generates three
    lists of words.
    Index 0 = all words in a list of lists
    Index 1 = all words in a singe, flat list
    Index 2 = unique list of words
    '''
    words = []
    for i in df[col]:
        lowercase = i.lower()
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
                          background_color="white").generate(' '.join(word_count(df,col)[1])
                                                            )

    # Create and generate a word cloud image:
    #wordcloud = WordCloud( background_color="white").generate(' '.join(flat_title_words))

    # Display the generated image:
    fig, ax = plt.subplots(figsize=(10,15))
    
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

def word_count_omit_words(df, col, omit_words = unique_title_words):
    '''Something in this function doesn't quote work, but the intention was to
    use this, for instance, to make a word cloud of words that are in the video
    title, but NOT in the channel titel.
    '''
    words = []
    for i in df[col]:
        lowercase = i.lower()
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