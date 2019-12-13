#!/usr/bin/env python
# coding: utf-8

# In[41]:


"""
Classify data.
"""
import numpy as np
import pickle
import re


def read_afinn():
    """
    Read afinn document to dict, word to score.
    """
    
    afinn = dict()
    print("Reading Afinn words........")
    with open('AFINN-111.txt', 'r') as val:
        for line in val:
            l = line.strip().split()
            if len(l) == 2:
                afinn[l[0]] = int(l[1])

    print(' %d AFINN words are read.' % (len(afinn)))
    print('for example: %s' %str(list(afinn.items())[:10]))
    return afinn


# In[42]:


def get_tweets(utweet):

    with open(utweet + '.pkl', 'rb') as val:
        print('Fetched the user tweets stored from collect.py')
        return pickle.load(val)


# In[43]:



def tokenize(doc, keep_internal_punct=False):   
 
 if(keep_internal_punct):
     tokens = re.compile("[\w_][^\s]*[\w_]|[\w_]").findall(doc.lower())
 else:
     tokens = re.sub(r'\W+', ' ', doc.lower()).split()
 return np.array(tokens)

positive_tweets = []
negative_tweets = []
neutral_tweets = []
pass


# In[44]:


def sentiment_tweets(utweet, afinn):
    
    score = 0

    twit_word = tokenize(utweet)
    
    for i in twit_word:
        if i in afinn:
            score += afinn[i]
    if score == 0:
        neutral_tweets.append(utweet)
    if score > 0:
        positive_tweets.append(utweet)
    if score < 0:
        negative_tweets.append(utweet)
pass


# In[45]:


def all_sentiment_tweets(tweets, afinn):
    
    for utweet in tweets:
        sentiment_tweets(utweet, afinn)
    print("The sentiment for all the tweets are gathered")
pass


# In[46]:


def classify_tweets(positive_tweets, negative_tweets, neutral_tweets):
    
    classify_tweets = {}
    classify_tweets['positive'] = positive_tweets
    classify_tweets['negative'] = negative_tweets
    classify_tweets['neutral'] = neutral_tweets

    return classify_tweets
pass


# In[47]:


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)
pass


# In[48]:


def main():
    afinn = read_afinn()
    usertweets = get_tweets('user_tweets')
    all_sentiment_tweets(usertweets, afinn)
    print('The number of positive tweets= %d' %(len(positive_tweets)))
    print('The number of negative tweets= %d' %(len(negative_tweets)))
    print('The number of neutral tweets= %d' %(len(neutral_tweets)))
    c= classify_tweets(positive_tweets, negative_tweets, neutral_tweets)
    save_obj(c, 'Classify')
    
    
    
    
if __name__ == '__main__':
    main()

