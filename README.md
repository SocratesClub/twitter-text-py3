# twitter-text-py3

twitter-text-py could not be used for python 3, https://github.com/dryan/twitter-text-py/issues/21

I debug the problem, and make this new repo. 

# Install

Python 3 users can install it using the following terminal command:

> pip install git+git://github.com/computational-class/twitter-text-py3.git


# Use

```python
import twitter_text

tweet = '''RT @AnonKitsu: ALERT!!!!!!!!!!COPS ARE KETTLING PROTESTERS IN PARK W HELICOPTERS AND PADDYWAGONS!!!! 
            #OCCUPYWALLSTREET #OWS #OCCUPYNY PLEASE @chengjun @mili http://computational-communication.com 
            http://ccc.nju.edu.cn RT !!HELP!!!!'''

ex = twitter_text.Extractor(tweet)
at_names = ex.extract_mentioned_screen_names()
urls = ex.extract_urls()
hashtags = ex.extract_hashtags()
print(at_names, urls, hashtags)

```
