#!/usr/bin/env python
# coding: utf-8

# In[86]:


import pickle

def get_file(name):
   
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
pass


# In[87]:


def avg_clusters(clusters):
    tot = 0
    for cluster in clusters:
        tot += len(cluster.nodes())
    ave = tot / len(clusters)

    return ave


# In[88]:


def summary():
    t_file = open('summary.txt','w')
    t_file.write('Number of Twitter users collected:')
    t_file.write('\n \n \n')
    users = get_file('twitter_users')
    t_file.write("There are %d twitter users collected.\n" % (len(users)))
    for user in users:
        t_file.write("%s has %d friends.\n" % (user['screen_name'], len(user['friends_id'])))
    t_file.write('\n')
    tweets = get_file('user_tweets')
    t_file.write('Number of tweets collected: %d \n\n' % (len(tweets)))
    t_file.write('For Sentiment analysis, we took these %d tweets and processed \n \n' % (len(tweets)))
    clusters = get_file('Clusters')
    t_file.write('Number of communities discovered: %d \n' % (len(clusters)))
    t_file.write('We cluster all initial users and their friends in to different communities and exclude users that followed by less than two initial users and outliers.\n Outliers are those points that clustered as singleton.\n')
    avgc = avg_clusters(clusters)
    t_file.write('Average number of users per community: %d\n\n' % (avgc))
    t_file.write('Number of instances per class found:\n \n')
    t_file.write('There are three classes for sentiment analysis.\n')
    classify_tweets = get_file('classify')
    t_file.write('The positive class has %d instances\n' % (len(classify_tweets['positive'])))
    t_file.write('The negative class has %d instances\n' % (len(classify_tweets['negative'])))
    t_file.write('The neutral class has %d instances\n \n \n' % (len(classify_tweets['neutral'])))
    t_file.write('Examples:\n \n')
    t_file.write('Positive class:\n%s\n' % (classify_tweets['positive'][0]).encode("utf-8"))
    t_file.write('Negative class:\n%s\n' % (classify_tweets['negative'][0]))
    t_file.write('Neutral class:\n%s\n' % (classify_tweets['neutral'][0]))
    
    return t_file
pass



    
    


# In[89]:


def main():
    summarize=summary()
    print('Write to summary.txt done.')    


if __name__ == '__main__':
    main()

