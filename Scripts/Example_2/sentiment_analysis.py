from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import twitter_samples
from random import randint
import re, string, os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []
    lemmatized_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        lemmatized_tokens.append(token.lower())
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens, lemmatized_tokens

def getRandomTweet():
    # Get a random tweet
    tweets = twitter_samples.strings('tweets.20150430-223406.json')
    return tweets[randint(0,len(tweets))]
    
def getSentiment(custom_tokens):
     # Load saved model for detecting sentiment
    saved_model = os.path.join(BASE_DIR, "Example_2\\sent_model.sav")
    loaded_model = pickle.load(open(saved_model, 'rb'))
    # run sentiment analysis
    result = loaded_model.classify(dict([token, True] for token in custom_tokens))
    return result
