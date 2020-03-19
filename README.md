![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)

# Twitter Bot Manacapuru

A Python bot that automates some actions on Twitter, such as retweeting and favoriting tweets.

The current working twitter bot can be found at <https://twitter.com/manacapuru_>

## Requirements:

* Tweepy Library


## Setup

Install tweepy by running pip instal tweepy in your terminal

``` sh
$ pip install tweepy
```


## Running instructions

Head over to <https://apps.twitter.com> and get your **access keys**

Change the twitter API credentials in **manacapuru.py** file

``` python
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_key = 'YOUR_ACCESS_KEY'
access_secret = 'YOUR_ACCESS_SECRET'
```

Run **manacapuru.py**

``` sh
$ python manacapuru.py
```

## References

* [Tweepy Documentation](http://docs.tweepy.org/en/v3.5.0/index.html)