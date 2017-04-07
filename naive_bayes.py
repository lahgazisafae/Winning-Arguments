from os import walk
import os
from collections import Counter
import math
import re

global test_list
test_list = []

def read_tweets(filepath):
	f = []
	for (dirpath, dirnames, filenames) in walk(filepath):
		f.extend([os.path.join(dirpath,x) for x in filenames])
	training_list = []
	for item in f[:5000]:
		try: 
			file_object = open(item, 'r')
			tweet = file_object.readlines()
			training_list.append(tweet)
		except Exception as e:
			print e 
			continue

	for item in f[101:111]: 
		try: 
			file_object = open(item, 'r')
			tweet = file_object.readlines()
			test_list.append(tweet)
		except Exception as e:
			print e 
			continue
	return training_list

pos_tweets = read_tweets('tweets_train\pos')
neg_tweets = read_tweets('tweets_train\\neg')

POS = Counter()
prob_POS = dict()
NEG = Counter()
prob_NEG = dict()

#train 
def train_pos():
	len_POS = 0
	for doc in pos_tweets: 
		# print doc
		for word in doc[0].split(" "): 
			word = word.strip().lower()
			word = re.sub(r'[^\w\s]','', word)
			#add tweets to POS set
			POS[word]+=1
			len_POS+=1
	# print POS.keys()		
	# print len_POS

	for t in POS.keys():
		prob =  POS[t]*1.0/len_POS
		prob_POS[t] = float(math.log(prob))+1

train_pos()

def train_neg():
	len_NEG = 0
	for doc in neg_tweets: 
		for word in doc[0].split(" "):
			word = word.strip().lower()
			word = re.sub(r'[^\w\s]','', word) 
			#add tweets to POS set
			NEG[word]+=1
			len_NEG+=1

	for t in NEG.keys(): 
		prob =  NEG[t]*1.0/len_NEG
		prob_NEG[t] = float(math.log(prob))+1

train_neg()

def parse_tweet(test_tweet): 
	test_tweet = test_tweet.strip().lower()
	test_tweet = re.sub(r'[^\w\s]','', test_tweet)
	arr = test_tweet.split()
	test_prob_pos = 1
	for i in arr: 
		if i in prob_POS:
			test_prob_pos*=prob_POS[i]
		else: 
			test_prob_pos*=0.01
	test_prob_neg = 1
	for i in arr: 
		if i in prob_NEG:
			test_prob_neg*=prob_NEG[i]
		else: 
			test_prob_neg*=0.01
	if test_prob_pos > test_prob_neg: 
		return "positive"
	else: 
		return "negative"

def find_mean_score(tweet):
	tweet = tweet.strip().lower()
	tweet = re.sub(r'[^\w\s]','', tweet)
	tweet_arr = tweet.split()
	mean_words = open('mean_words.txt')
	data = mean_words.readlines()
	for x in range(len(data)): 
		data[x] = data[x].strip()
	score = 0
	for word in tweet: 
		if word in data: 
			score+=1
	return score/len(tweet_arr)

for x in test_list:
	print x[0], parse_tweet(x[0]), find_mean_score(x[0])


