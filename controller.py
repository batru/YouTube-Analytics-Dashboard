from main import getSubscribers, get_videos, best_post_time
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv() #load env variables

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

jdbc_url = "jdbc:postgresql://localhost:5432/batru_youtube"

properties = {
    "user": db_user,
    "password": db_password,
    "driver": "org.postgresql.Driver"
}


# Function to clear a table using psycopg2
def clear_table(table_name):
    conn = psycopg2.connect(
        dbname="batru_youtube",
        user=db_user,
        password=db_password,
        host="localhost",
        port=5432
    )
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name}")
    conn.commit()
    cur.close()
    conn.close()

def loadData():
    # load data frame
    subscriber_df = getSubscribers()
    videos_list, best_videos_df = get_videos()
    best_post_time_df = best_post_time(videos_list)

    # push the data frames in postgresql db
    # Write to PostgreSQL
    subscriber_df.write \
    .jdbc(url=jdbc_url, table="subscriber_data", mode='append', properties=properties)

    # Clear and load best post time
    clear_table("best_post_time")
    best_post_time_df.write \
    .jdbc(url=jdbc_url, table="best_post_time", mode='append', properties=properties)

    # Clear and load best performing videos
    clear_table("best_performing_videos")
    best_videos_df.write \
    .jdbc(url=jdbc_url, table="best_performing_videos", mode='append', properties=properties)


loadData() #call the function to execute
