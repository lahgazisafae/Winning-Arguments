from os import walk
import os
from collections import Counter
import math
import re

global test_list
test_list = []

def read_tweets(filepath, label):
	f = []
	for (dirpath, dirnames, filenames) in walk(filepath):
		f.extend([os.path.join(dirpath,x) for x in filenames])
	training_list = []
	for item in f[:900]:
		try: 
			file_object = open(item, 'r')
			tweet = file_object.read()
			training_list.append(tweet)
		except Exception as e:
			print e 
			continue

	for item in f[900:920]: 
		try: 
			file_object = open(item, 'r')
			tweet = file_object.readlines()
			test_list.append((label, tweet))
		except Exception as e:
			print e 
			continue
	return training_list

pos_tweets = read_tweets('data\pos', 'positive')
neg_tweets = read_tweets('data\\neg', 'negative')
POS = Counter()
prob_POS = dict()
NEG = Counter()
prob_NEG = dict()

#train 
def train_pos():
	global len_POS
	len_POS = 0
	for doc in pos_tweets: 
		for word in doc[0].split(" "): 
			word = word.strip().lower()
			word = re.sub(r'[^\w\s]','', word)
			#add tweets to POS set
			POS[word]+=1
			len_POS+=1

	for t in POS.keys():
		prob =  (POS[t]+1)*1.0/len_POS
		prob_POS[t] = float(math.log(prob))+1

train_pos()

def train_neg():
	global len_NEG
	len_NEG = 0
	for doc in neg_tweets: 
		for word in doc[0].split(" "):
			word = word.strip().lower()
			word = re.sub(r'[^\w\s]','', word) 
			#add tweets to POS set
			NEG[word]+=1
			len_NEG+=1

	for t in NEG.keys(): 
		prob =  (NEG[t]+1)*1.0/len_NEG
		prob_NEG[t] = float(math.log(prob))

train_neg()

def eval_tweet(test_tweet): 
	test_tweet = test_tweet.strip().lower()
	test_tweet = re.sub(r'[^\w\s]','', test_tweet)
	arr = test_tweet.split()
	test_prob_pos = 0
	for i in arr: 
		if i in prob_POS:
			test_prob_pos+=prob_POS[i]
		else: 
			test_prob_pos+=math.log(1.0/len_POS)
	test_prob_neg = 0
	for i in arr: 
		if i in prob_NEG:
			test_prob_neg+=prob_NEG[i]
		else: 
			test_prob_neg*=math.log(1.0/len_NEG)
	if test_prob_pos > test_prob_neg: 
		return "positive", test_prob_pos - test_prob_neg
	else: 
		return "negative", test_prob_pos - test_prob_neg

accuracy = []
for (actual, x) in test_list:
	label, score = eval_tweet(x[0])
	if label == actual:
		accuracy.append(1)
	else:
		accuracy.append(0)
	print actual, x[0], label, score

print("Accuracy: %1.3f" % (sum(accuracy) / float(len(accuracy))))


