#!/usr/bin/env python
# coding: utf-8

# In[10]:


"""
Collect data.
"""

from collections import Counter
import configparser
import sys
import time
from TwitterAPI import TwitterAPI
import pickle
import csv
import collections



consumer_key = 'Zxz922DhUyi3Oaa2dypnWebsg'
consumer_secret = 'iiztDsqZikfG8e9myZjjVR9Xf26SMyaPBUPgOVIgvzG1rZmxCI'
access_token = '1058787616823349249-O9aHDBdcV9hXqepSVIOiqE2xkx47js'
access_token_secret = 'TobdikFmLla1114bxWwhvnlzEt6d3OCib1rchpt8YkZ6q'



# In[11]:


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
pass


# In[12]:


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
   ['sundarpichai',
 'StephenCurry30',
 'KDTrey5',
 'imVkohli',
 'ABdeVilliers17',
 'narendramodi']
    """
    ###TODO
    #pass
    file = open(filename, "r")
    names = []
    for line in file:
        names.append(line.strip())
    return names
pass


# In[13]:


read_screen_names('users.txt')


# In[14]:


def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)
            pass


# In[15]:


def get_data_user(twitter, screen_names):
    """
    Retrieve the Twitter user objects for each screen_name.
    
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (screen_name, id, friends_id)

    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """

    data_user = []
    for name in screen_names:
        request = robust_request(twitter, 'users/lookup', {'screen_name': name}, max_tries=5)
        user = [val for val in request]
        friends = []
        request = robust_request(twitter, 'friends/ids', {'screen_name': name, 'count': 5000}, max_tries=5)
        friends = sorted([str(val) for val in request])
        fr = {'screen_name': user[0]['screen_name'],
             'id': str(user[0]['id']),
             'friends_id': friends}
        data_user.append(fr)
   
    return data_user
pass


# In[16]:


def get_tweets(twitter, screen_name, num_tweets):
    """
    Retrieve tweets of the user.

    params:
        twiiter......The TwitterAPI object.
        screen_name..The user to collect tweets from.
        num_tweets...The number of tweets to collect.
    returns:
        A list of strings, one per tweet.
    """

    request = robust_request(twitter, 'search/tweets', {'q': screen_name, 'count': num_tweets})
    tweets = [a['text'] for a in request]

    return tweets
pass


# In[17]:


def save_obj(obj, name):
    """
    store, list of dicts
    """
    
    with open(name + '.pkl', 'wb') as objec:
        pickle.dump(obj, objec)
        
    #with open(name + '.csv', 'rb') as f:
    #data = list(csv.reader(f))
pass


# In[18]:


def main():
    twitter = get_twitter()
    screen_names = read_screen_names('users.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    #users = sorted(get_users(twitter, screen_names)
    data_user = sorted(get_data_user(twitter, screen_names), key=lambda x: x['screen_name'])
    save_obj(data_user, 'twitter_users')
    print("Twitter users information saved....")
    tweets = get_tweets(twitter, screen_names[0], 100)
    save_obj(tweets, 'user_tweets')
    print("%d tweets saved." % (len(tweets)))


if __name__ == '__main__':
    main()
    

