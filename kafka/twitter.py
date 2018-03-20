import os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')


class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages('twitter', data.encode('utf-8'))
        return True

    def on_error(self, status):
        print (status)


kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(languages=["en"], track=['basketball', 'nba', 'ncaa'])
