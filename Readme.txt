In this project, I have used TwitterAPI to collect the raw data of twitter users and tweets.
I used these collected data(**collect.py**) to do clustering and classifying(Sentiment analysis).

Overall twitter users selected are 5:
StephenCurry30
KDTrey5
imVkohli
ABdeVilliers17
narendramodi

Over 100 tweets are collected.
**cluster.py** divides the five users and their friends into different communities.
Girvan_Newman algorithm with betweenness of each edge was used in the process.
I also got imVkohli,ABdeVilliers17,narendramodi as a single cluster.
We consider clusters with more than one user.

**classify.py** use afinn method to classify the sentiment(positve, negative or nrutral) of each tweet.
For this, I downloaded a datadet of AFINN words with 2462 words.
Tweets with positive scores are classified as positive tweets, negative scores as negative tweets and zero score as neutral tweets.


**summarize.py** writes the output into summary.txt.

Conclusion:

I wanted to see the connections between NarendraModi, Kohli(Indian Cricketer), ABdeVilliers, StephenCurry30, and KDTrey5.
I discovered that StephenCurry and KDTrey5 has many friends in common. And I was kind of surprised to see NarendraModi 
follows all the other 4 people and infact they do have few friends in common.
I saw that there were more of positive tweets for StephenCurry and very less negative tweets from the 100 tweets I collected.
This shows StephenCurry does have a very good reputation.

