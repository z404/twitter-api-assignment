from dotenv import dotenv_values
import tweepy
import fastapi
from fastapi_utils.tasks import repeat_every
import datetime

config = dotenv_values()
print(config)

auth = tweepy.OAuth1UserHandler(
   config["API_KEY"], config["API_KEY_SECRET"],
   config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"], config["BEARER_TOKEN"]
)
# api = tweepy.API(auth)
client = tweepy.Client(bearer_token=config["BEARER_TOKEN"], consumer_key=config["API_KEY"], consumer_secret=config["API_KEY_SECRET"], access_token=config["ACCESS_TOKEN"], access_token_secret=config["ACCESS_TOKEN_SECRET"])

app = fastapi.FastAPI()

birthdays = []

def post_tweet(tweet: str):
    return client.create_tweet(text=tweet)

@app.get("/add_birthday")
def add_birthday(username: str, birthday: str):
    """
    Add a birthday to database (date in dd-mm-yyyy format)
    """
    birthdays.append({"username": username, "birthday": birthday})
    return {"message": "Birthday added"}

@app.get("/get_birthdays")
def get_birthdays():
    """
    Get all birthdays from database
    """
    return birthdays

# @app.on_event("startup")
# @repeat_every(seconds=20) # 20 SECONDS USED FOR TESTING
# def tweet_birthdays():
#     """
#     Tweet all birthdays from database
#     """
#     tweetid = []
#     for birthday in birthdays:
#         if datetime.datetime.strptime(birthday["birthday"], "%d-%m-%Y").date() == datetime.datetime.now().date():
#             tweetid.append(post_tweet(f"Happy birthday @{birthday['username']}!"))
#     print("TWEETED:",tweetid)

@app.get("/tweet")
def tweet_birthdays():
    """
    Tweet all birthdays from database
    """
    tweetid = []
    for birthday in birthdays:
        if datetime.datetime.strptime(birthday["birthday"], "%d-%m-%Y").date() == datetime.datetime.now().date():
            tweetid.append(post_tweet(f"Happy birthday @{birthday['username']}!"))
    print("TWEETED:",tweetid)

@app.get("/")
def index():
    return {"message": "Hello! Welcome to the birthday bot! Navigate to /docs to see the API documentation."}