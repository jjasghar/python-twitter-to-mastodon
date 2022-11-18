import tweepy
import redis
import requests
import logging
import tomli

with open("config.toml", mode="rb") as t:
    config = tomli.load(t)

MASTODON_SERVER = config["mastodon"]["server"]
MASTODON_BOT_TOKEN = config["mastodon"]["bot_token"]
bearer_token = config["twitter"]["bearer_token"]
name = config["twitter"]["name"]
redis_index = config["redis"]["index"]

logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def post_to_mastodon(tweet):
    url = f'https://{MASTODON_SERVER}/api/v1/statuses'
    auth = {'Authorization': f'Bearer {MASTODON_BOT_TOKEN}'}
    params = {'status': f"{tweet}"}

    r = requests.post(url, data=params, headers=auth)
    logging.debug(f"--> successfully posted to {url}")
    if not r.status_code == 200:
        logging.error(f"The error came back with: {r.status_code}, and {r.text}")


redis_client = redis.Redis(host='localhost', port=6379, db=redis_index)

twitter_client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
twitter_user = twitter_client.get_user(username=name).data

# Extract the user id and user name
user_id = twitter_user.id
user_name = twitter_user.name

# Fetch tweets by the user
tweets = twitter_client.get_users_tweets(id=user_id, max_results=5,
                                         tweet_fields=['id', 'text', 'created_at', 'context_annotations'])

for tweet in tweets.data:
    if not redis_client.exists(str(tweet.created_at)):
        redis_client.set(str(tweet.created_at), str(tweet))
        logging.info(f"We found at {tweet.created_at} this {tweet}")
        post_to_mastodon(tweet)
        break
