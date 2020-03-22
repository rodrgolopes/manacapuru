import tweepy
import re
import random
import time
import datetime
import os

API_DELAY = 30 * 60  # 30 minutes

class Manacapuru:

    def __init__(self):
        self.api = self.__authorize()
        self.outfile = "manacapuru.txt"

    @staticmethod
    def __authorize():
        consumer_key = "YOUR_CONSUMER_KEY"
        consumer_secret = "YOUR_CONSUMER_SECRET"
        access_token = "YOUR_ACCESS_KEY"
        access_token_secret = "YOUR_ACCESS_SECRET"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api

    def checking_db(self):
        try:
            file = open(self.outfile, 'r')
            if self.get_date("%d-%m-%Y") in file.readline().split('|'): return True
            else: return False
        except: return False
    
    def create_db(self, id):
        if self.checking_db():
            db = open(self.outfile, 'a')
            db.write(';' + id)
        else:
            db = open(self.outfile, 'w')
            db.write(self.get_date("%d-%m-%Y") + '|' + id)
        db.close()

    def load_db(self, id):
        try:
            file = open(self.outfile, 'r')
            return file.readline().split('|')[1].split(';').count(id)
        except: return 0

    def response_text(self):
        text = ['How are you?','How are you doing?','Whats new?','Thats it for now. XOXO!',]
        return text[random.randrange(0, len(text))]

    def screen_cleaning(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def cleaning_plurals(self, sentece):
        replacements = [(r'(as)\b','a'),(r'(oes)\b','ao'),(r'(es)\b','e'),(r'(is)\b','i'),(r'(os)\b','o'),(r'(us)\b','u')]
        for old, new in replacements:
            sentece = re.sub(old, new, sentece, flags=re.I)
        return sentece

    def cleaning_characters(self, sentece):
        replacements = [('á|à|ã|â|ä','a'),('é|è|ê|ë','e'),('í|ì|î|ï','i'),('ó|ò|õ|ô|ö','o'),('ú|ù|û|ü','u'),('ç|ć|č','c'), ('#|\\?|\\!|\\,|\\.|;|:|=','')]
        for old, new in replacements:
            sentece = re.sub(old, new, sentece, flags=re.I)
        return sentece

    def bad_words(self, sentece):
	    sentece = self.cleaning_characters(sentece)
	    sentece = self.cleaning_plurals(sentece)
	    badwords = ['follow','fuck']
	    for word in badwords:
		    if re.search(word, sentece, re.IGNORECASE):
			    return True
	    badwords = ('fuck','bitch','shit','pussy')
	    for word in sentece.split():
		    if word.lower() in badwords:
			    return True
	    return False

    def bad_users(self, users):
	    badusers = ['brancosenulos','fodase_bot','manacapuru_','fucklaligaplay1']
	    if users.lower() in badusers:
		    return True
	    return False

    def bad_caracteres(self, sentece):
	    caracteres = ['#',':',',',';','=']
	    for caracter in caracteres:
		    if sentece.count(caracter) >= 5:
		        return True
	    replacements = [('(@[A-Za-z0-9]+)',''),('(#[A-Za-z0-9_]+)',''),('\s+',' ')]
	    for old, new in replacements:
	        sentece = re.sub(old, new, sentece.strip(), flags=re.I)
	    if sentece.isupper():
	        return True
	    return False

    def get_datetime(self):
        utc = datetime.datetime.utcnow()
        return utc - datetime.timedelta(minutes = 4 * 60)

    def get_date(self, x):
        return self.get_datetime().strftime(x)

    def trends_selection(self):
        trends1 = self.api.trends_place(23424768)
        trends = list([trend['name'] for trend in trends1[0]['trends'] if trend['name'].startswith('#') and re.search('follow', trend['name'], re.IGNORECASE)])
        if trends:
            return trends[0]
        return False
    
    def query_tweets(self, query: str, result_type: str = "", tweet_mode: str = "extended",):
        tweets = [tweet_r for tweet_r in tweepy.Cursor(self.api.search, q=query, include_entities=False, tweet_mode=tweet_mode).items(13)]
        return reversed(tweets)

    def info_tweet(self, id):
        response, tweet = [], self.api.get_status(id)
        try:
            response.append(True) if tweet.favorited else response.append(False)
            response.append(True) if tweet.retweeted else response.append(False)
            return response
        except:
            return [False,False]

    def start_tweets(self):
        self.screen_cleaning()
        terms = ['Manacapuru OR @manacapuru_ -filter:retweets','Manacapuruense OR manacapuruenses -filter:retweets']
        for term in terms:
            print(f'Searching: {term}')
            for tweet in self.query_tweets(term):
                try:
                    if self.get_date("%d-%m-%Y") == tweet.created_at.strftime("%d-%m-%Y") and tweet.favorited == False:
                        tweet_id, tweet_username = tweet.id, tweet.user.screen_name
                        tweet_userid = tweet.user.id
                        tweet_text = tweet.full_text
                        tweet_textclear = re.sub("(@[A-Za-z0-9]+)","",tweet_text).replace('  ',' ')
                        info = self.info_tweet(tweet_id)
                        counts = self.load_db(str(tweet_userid))
                        print(f"\n[@{tweet_username}]{tweet_text}\n",'-'*30)
                        #
                        if (self.bad_words(tweet_text) != True) and (self.bad_users(tweet_username) != True) and (len(tweet_textclear) >= 17) and (self.bad_caracteres(tweet_text) != True) and (info[1] == False) and (info[0] == False) and (counts <= 1):
                            tweet.retweet(), print("[retweet]"), time.sleep(1)
                        if (tweet_username == "rodrgolopes") and (info[0] == False) and (info[1] == False):
                            tweet.retweet(), print("[retweet]"), time.sleep(1)
                        if (info[0] == False) and (self.bad_caracteres(tweet_text) != True) and (counts <= 2):
                            tweet.favorite(), print("[favorite]"), time.sleep(1), self.create_db(str(tweet_userid))
                        if (info[0] == False) and (len(tweet_textclear) <= 16) and (self.bad_words(tweet_text) != True) and (self.bad_users(tweet_username) != True) and (counts == 0):
                            x_status = f"{response_text()}"
                            self.api.update_status(status = x_status, in_reply_to_status_id = tweetId, auto_populate_reply_metadata = True)
                            print(f"TWEET: {x_status}]")
                        print(f"bad_words: {self.bad_words(tweet_text)}, bad_users: {self.bad_users(tweet_username)}, tamanho: {len(tweet_textclear)}, retweet: {info[1]}, favorite: {info[0]}\n",'-'*30)
                        time.sleep(2)
                    #
                except tweepy.TweepError as error:
                    print('\nError: '), print(error.reason)
                except StopIteration:
                    break

if __name__ == "__main__":
    mpu = Manacapuru()
    while True:
        mpu.start_tweets()
        print('aguardando 30 min...'), time.sleep(API_DELAY)