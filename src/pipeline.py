from googleapiclient.discovery import build
import googleapiclient.errors as HttpError
import oauth2client.tools as argparser
import sys
import json
import pandas as pd
import string
import dateutil.parser
import isodate

# Connect to YouTube API

''' We will need to go to http://developers.google.com , start a project, and
sign up for an API key. This key (or multiple keys) can be stored in a list'''

def make_credentials(api_key_index, api_key_list = api_keys):
    DEVELOPER_KEY = api_key_list[api_key_index]
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 developerKey=DEVELOPER_KEY)

# Search for relevant channels

#### adapted from https://github.com/spnichol/youtube_tutorial/blob/master/youtube_videos.py

def youtube_search(q, max_results=50,order="relevance", token=None,youtube=youtube_creds):

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results

  ).execute()

    
  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      return(nexttok, videos)
  except Exception as e:
      nexttok = "last_page"
      return(nexttok, videos)

def channel_search(keyword, token=None):
    '''This search will return ~650 items'''
    result = youtube_search(keyword, token=token)
    token = result[0]
    videos = result[1]
    for vid in videos:
        search_dict['channelId'].append(vid['snippet']['channelId'])
        search_dict['channelTitle'].append(vid['snippet']['channelTitle'])
    print ("added " + str(len(videos)) + " videos to a total of " + str(len(search_dict['channelId'])))
    return token

def drop_irrelevant_chanels(df,irrelevant_channels):
    '''If the channels returned are *mostly* relevant, this function can be used
    to reduce the list to only relevant channels
    '''
    channels_df = df
    for i in irrelevant_channels:
        channels_df = channels_df[channels_df.channelTitle != i]
    return channels_df

def get_channel_data(channel_id,youtube=youtube_creds):    
    '''returns information on channel in JSON format'''
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    return response

def playlist_by_channel(playlist_id,token=None,youtube=youtube_creds):
    
    request = youtube.playlistItems().list(
        part="contentDetails",
        maxResults=50,
        playlistId=playlist_id,
        pageToken=token
    )
    response = request.execute()
    
    #return response

    videos_ids_per_query = []
    
    for i in range(0,len(response['items'])):
        videos_ids_per_query.append(response['items'][i]['contentDetails']['videoId'])
    try:
      nexttok = response["nextPageToken"]
      return(nexttok, videos_ids_per_query)
    except Exception as e:
      nexttok = "last_page"
      return(nexttok, videos_ids_per_query)

def append_videos_from_playlist(playlist_id, token=None):
    results = playlist_by_channel(playlist_id, token=token)
    token = results[0]
    videos = results[1]
    for vid in videos:
        video_list.append(vid)
    print ("added " + str(len(videos)) + " videos for a total of " + str(len(video_list)))
    return token

def video_details(video_id, youtube=youtube_creds):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    
    return response

if __name__ == "__main__":

    api_keys = ['''''']

    youtube_creds = make_credentials(0)

    '''the first step is to return channels associated with the topic we are 
    interested in.'''

    search_dict = {'channelId':[],
                'channelTitle':[]}

    token = channel_search("mtb")
    while token != "last_page":
        token = channel_search("mtb", token=token)

    '''The search will not return all the information we're looking for. In order to
    do that, we'll need to use a different API call. In this case, we're looking 
    for information on specific channels and all the videos from those channels. 
    Accordingly, the next step is to generate a list of channels associated with 
    the videos. Since there can be duplicates in the channel list (i.e. more than 
    one video was found for some channels), we'll first drop the duplicates and
    then can inspect the remainder for relvance.
    '''

    df_channel_list = pd.DataFrame.from_dict(search_dict)
    df_unique_channels = df_channel_list.drop_duplicates()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_unique_channels)

    df_relevant_channels = df_unique_channels #does not drop any channels
    
    '''Uncomment below to drop channels'''
    #df_relevant_channels = drop_irrelevant_chanels(df_unique_channels,
    #['''channel name 1, channel name 2, ...'''])

    '''Alternately, if there are far more channels returned than relevant 
    channels, we can just select the channels we are interested in. This is fed 
    into the search function from before in order to obtain a the channelId's 
    which will be used to get additional information on the channels. 
    
    Uncomment below to select specific channels'''

    #relevant_channel_list = ['''channel name 1, channel name 2, ...''']

    #df_relevant_channels = df_unique_channels[df_unique_channels['channelTitle']
    #                                        .isin(relevant_channel_list)]

    # Channel Information

    channel_dict = {'channelID':[],
                    'channelTitle':[],
                    'channelDescription':[],
                    'channelCommentCount':[],
                    'hiddenSubscriberCount':[],
                    'subscriberCount':[],
                    'videoCount':[],
                    'channelViewCount':[],
                    'uploads':[],
                }

    '''gather channel information and format resulting df'''

    for chan in df_relevant_channels.channelId:
        new_channel = get_channel_data(chan)
        new_channel = new_channel['items'][0]
        channel_dict['channelID'].append(new_channel['id'])
        channel_dict['channelTitle'].append(new_channel['snippet']['title'])
        channel_dict['channelDescription'].append(new_channel['snippet']['description'])
        channel_dict['channelCommentCount'].append(new_channel['statistics']['commentCount'])
        channel_dict['hiddenSubscriberCount'].append(new_channel['statistics']['hiddenSubscriberCount'])
        channel_dict['subscriberCount'].append(new_channel['statistics']['subscriberCount'])
        channel_dict['videoCount'].append(new_channel['statistics']['videoCount'])
        channel_dict['channelViewCount'].append(new_channel['statistics']['viewCount'])
        channel_dict['uploads'].append(new_channel['contentDetails']['relatedPlaylists']['uploads'])

    df_channels = pd.DataFrame.from_dict(channel_dict)
    df_channels = df_channels.astype({'channelViewCount': 'int32'})
    df_channels = df_channels.astype({'videoCount': 'int32'})
    df_channels = df_channels.astype({'channelCommentCount': 'int32'})
    df_channels = df_channels.astype({'hiddenSubscriberCount': 'int32'})
    df_channels = df_channels.astype({'subscriberCount': 'int32'})

   '''highViews later used for labeling plots without crowding'''
    df_channels['highViews'] = df_channels.apply(lambda row: row.channelTitle 
                                                if row.channelViewCount > 100000000 
                                                else '',
                                                axis =1)

    '''save file for safe keeping (especially important if we reach  our of API quota)'''

    df_channels.to_csv('data/channel_data.csv')

    # Get all videos from relevant channels

    video_list = []

    for channel_upload_id in df_channels["uploads"]:
        token = append_videos_from_playlist(channel_upload_id)
        while token != "last_page":
            token = append_videos_from_playlist(channel_upload_id, token=token)

    '''save our list of videos'''

    videos_df = pd.DataFrame(video_list)
    videos_df.to_csv('data/video_list.csv')

    # Video Details

    youtube_creds = make_credentials('''Index''')

    video_deets_dict = {'videoID':[],
                        'channelId':[],
                        'categoryId':[],
                        'channelTitle':[],
                        'videoTitle':[],
                        'videoDescription':[],
                        #'tags':[],
                        'publishedAt':[],
                        'commentCount':[],
                        'dislikeCount':[],
                        'likeCount':[],
                        'favoriteCount':[],
                        'viewCount':[],
                        'caption':[],
                        'definition':[],
                        'duration':[],
                        'licensedContent':[],
                        'projection':[],
                        'liveBroadcastContent':[]
                        }

    progress = 0 # can be used as a counter in case the API call needs to be restarted
    for vid in video_list:
        this_video = video_details(vid)
        this_video = this_video['items'][0]
        video_deets_dict['videoID'].append(this_video['id'])
        video_deets_dict['channelId'].append(this_video['snippet']['channelId'])
        video_deets_dict['categoryId'].append(this_video['snippet']['categoryId'])
        video_deets_dict['channelTitle'].append(this_video['snippet']['channelTitle'])
        video_deets_dict['videoTitle'].append(this_video['snippet']['title'])
        video_deets_dict['videoDescription'].append(this_video['snippet']['description'])
        #video_deets_dict['tags'].append(this_video['snippet']['tags'])
        video_deets_dict['publishedAt'].append(this_video['snippet']['publishedAt'])
        video_deets_dict['commentCount'].append(this_video['statistics']['commentCount'])
        video_deets_dict['dislikeCount'].append(this_video['statistics']['dislikeCount'])
        video_deets_dict['likeCount'].append(this_video['statistics']['likeCount'])
        video_deets_dict['favoriteCount'].append(this_video['statistics']['favoriteCount'])
        video_deets_dict['viewCount'].append(this_video['statistics']['viewCount'])
        video_deets_dict['caption'].append(this_video['contentDetails']['caption'])
        video_deets_dict['definition'].append(this_video['contentDetails']['definition'])
        video_deets_dict['duration'].append(this_video['contentDetails']['duration'])
        video_deets_dict['licensedContent'].append(this_video['contentDetails']['licensedContent'])
        video_deets_dict['projection'].append(this_video['contentDetails']['projection'])
        video_deets_dict['liveBroadcastContent'].append(this_video['snippet']['liveBroadcastContent'])
        progress += 1
        if progress % 100 == 0:
            print(progress)

    ''' orient='index' and then taking the transpose 
    was necessary for the pandas df conversion'''

    video_deets_df = pd.DataFrame.from_dict(video_deets_dict,orient='index').transpose()
    video_deets_df = video_deets_df.transpose()
    video_deets_df = video_deets_df.dropna()

    '''formating'''

    video_deets_df['publishedAt'] = pd.to_datetime(video_deets_df['publishedAt'])
    video_deets_df = video_deets_df.astype({'commentCount': 'int32'})
    video_deets_df = video_deets_df.astype({'dislikeCount': 'int32'})
    video_deets_df = video_deets_df.astype({'likeCount': 'int32'})
    video_deets_df = video_deets_df.astype({'favoriteCount': 'int32'})
    video_deets_df = video_deets_df.astype({'viewCount': 'int32'})
    video_deets_df = video_deets_df.astype({'caption': 'bool'})
    video_deets_df = video_deets_df.astype({'licensedContent': 'bool'})
    video_deets_df = video_deets_df.astype({'liveBroadcastContent': 'bool'})
    video_deets_df['durationSeconds'] = video_deets_df.apply(
        lambda row: isodate.parse_duration(row.duration).total_seconds(), axis=1)

    '''additional, engineered variables'''
    
    video_deets_df = video_deets_df.dropna()
    
    video_deets_df['durationSeconds'] = video_deets_df.apply(
        lambda row: isodate.parse_duration(row.duration).total_seconds(), axis=1)

    video_deets_df['wordsInVideoTitle'] = video_deets_df.apply(lambda row: 
                                                            len(row.videoTitle.split()),
                                                            axis =1)

    video_deets_df['wordsInVideoDescription'] = video_deets_df.apply(lambda row: 
                                                                    len(row.videoDescription.split()), 
                                                                    axis =1)

    video_deets_df['daysSinceVideoReleased'] = video_deets_df.apply(
        lambda row: (datetime.datetime.utcnow().replace(tzinfo=None) - 
                    row.publishedAt.replace(tzinfo=None)).days, axis =1)

    video_deets_df.to_csv('data/video_deets_df.csv')