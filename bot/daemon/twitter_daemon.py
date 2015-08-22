import tweepy
import os
import logging


class TwitterBot(object):
    """
    Base Twitter Bot class.
    Class provide post_tweet, media_upload, search methods
    """

    def __init__(self):
        """
        Twitter bot instance constructor
        """

        consumer_key = os.environ["consumer_key"]
        consumer_secret = os.environ["consumer_secret"]
        access_token = os.environ["access_token"]
        access_token_secret = os.environ["access_token_secret"]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='bot.log',
                            level=logging.DEBUG)
        logging.info('Bot initializated')
        self.api = tweepy.API(auth)

    def post_tweet(self, message, media=None, *args, **kwargs):
        """
        Post tweet method for twitter bot.
        -----------------------------------------------------------
        https://dev.twitter.com/rest/reference/post/statuses/update
        -----------------------------------------------------------
        media argument -  list of media_ids to associate with the Tweet.
        You may include up to 4 photos or 1 animated GIF or 1 video in a Tweet.
        example:
        bot = TwitterBot()
        bot.post_tweet("Hello, World!", media = ["/home/user/1.jpg", "2.jpg"])
        """

        try:
            logging.info('Try post tweet...')
            if len(message) > 140:
                raise Exception('Tweet message too long! Only 140 characters')
            if media is not None:
                _list = []
                for element in media:
                    _id = self.api.media_upload(element).media_id
                    _list.append(_id)
                logging.info('Tweet with media posted')
                return self.api.update_status(status=message,
                                              media_ids=_list, *args, **kwargs)
            else:
                logging.info('Tweet posted')
                return self.api.update_status(status=message, *args, **kwargs)
        except Exception as e:
            logging.error(e)

    def media_upload(self, filename, *args, **kwargs):
        """
        Upload media method for twitter bot.
        -----------------------------------------------------------
        https://dev.twitter.com/rest/public/uploading-media
        -----------------------------------------------------------
        """
        try:
            return self.api.media_upload(filename, *args, **kwargs)
        except Exception as e:
            logging.error(e)

    def search(self, q, *args, **kwargs):
        """
        Search method for twitter bot
        ----------------------------------------------------------
        https://dev.twitter.com/rest/reference/get/search/tweets
        ----------------------------------------------------------
        """
        try:
            logging.info('Search...')
            return self.api.search(q=q, *args, **kwargs)
        except Exception as e:
            logging.error(e)
