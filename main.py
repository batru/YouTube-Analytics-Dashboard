from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, date_format
from datetime import date


spark = SparkSession.builder\
        .appName("YoutubeAnalytics")\
        .config("spark.jars", "/mnt/c/Users/batru/Downloads/Work/LUX-DE/De_projects/Youtube_Analytics_Pipeline/jars/postgresql-42.6.0.jar") \
        .master("local[*]")\
        .getOrCreate()




#load env
load_dotenv()

#get api key from  env file
google_api_key = os.getenv('API_KEY')


youtube = build(
    'youtube',
    'v3',
    developerKey =  google_api_key
)


# Question one : How has my channel grown over time?

def getSubscribers():

    # get data from youtube channel
    request = youtube.channels().list(
        part = 'statistics',
        id = 'UCtxD0x6AuNNqdXO9Wp5GHew'

    )

    response = request.execute()
    subscriber_count = response['items'][0]['statistics']['subscriberCount']
    date_at = date.today()
    subscriber_data = [(subscriber_count, date_at)]
    # @todo - add  current datetime
    df = spark.createDataFrame(subscriber_data, ["subscriber_count", "date"])


    return df


    




# Question 2: Which videos perform best by engagement (likes/comments/views)?

def get_videos(youtube = youtube, playlist_id = "UUS-zdr8_cuUGNvOhLKUkjZQ" ):
    next_page = None # get next page data
    videos = [] # store dictionary of video data
    
#loop through all videos
    while True:

        #getting video ids for all the videos
        request = youtube.playlistItems().list( part = 'snippet, contentDetails', playlistId = playlist_id, maxResults = 50, pageToken = next_page)

        response = request.execute()

        
        video_ids = []
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])

        #getting data fro all the videos in our video_id list
        data = youtube.videos().list(part = 'snippet, statistics', id=video_ids)
        res = data.execute()

    
    #extracting  #Video ID, title, views, likes, comment count

        for i in range(len(res['items'])):
            title = res['items'][i]['snippet']['title']
            views_count = int(res['items'][i]['statistics']['viewCount'])
            comment_count = int(res['items'][i]['statistics']['commentCount'])
            like_count = int(res['items'][i]['statistics']['likeCount'])
            published_date = res['items'][i]['snippet']['publishedAt']
            engagement_rate = round((like_count + comment_count) / views_count, 2)

            dict_video = {}

            dict_video["title"] = title
            dict_video["view_count"] = views_count
            dict_video['like_count'] = like_count
            dict_video['comment_count'] = comment_count
            dict_video['engagement_rate'] = engagement_rate
            dict_video['published_date'] = published_date

            videos.append(dict_video)

        #checking if data is available for next page if not break the while loop
        next_page = response.get("nextPageToken")

        if not next_page:
            break

    df = spark.createDataFrame(videos)
    best_df = df.orderBy(col("engagement_rate").desc()).limit(5)

    return videos, best_df

  
# videos = get_videos(youtube, "UUS-zdr8_cuUGNvOhLKUkjZQ")


# def best_videos(videos):
#     df = spark.createDataFrame(videos)
#     best_df = df.orderBy(col("engagement_rate").desc()).limit(5)
    
#     return best_df

# df_videos = best_videos(videos)
# df_videos.show()
    
# # Question 3) What days and times work best for publishing content?

def best_post_time(videos):
    #convert videos into dataframe
    df = spark.createDataFrame(videos)
    
    #extract time and day from publisheAt
    df = df.withColumn("time_day", hour(col('published_date')))
    df= df.withColumn("day_week", date_format('published_date', "E"))


    #engagement
    df = df.withColumn("engagement", df.like_count + df.view_count + df.comment_count)

    #find the average engagement and group by day and hour

    grouped = (df.groupby("day_week", "time_day").avg("engagement").withColumnRenamed("avg(engagement)", "avg_engagement").orderBy(col("avg_engagement").desc()))

 

    return grouped.limit(3)

# grouped_df = best_post_time(videos)
# grouped_df.show()

