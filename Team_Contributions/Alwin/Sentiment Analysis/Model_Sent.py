from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

import re, string
import pickle

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []
    t = []

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
        t.append(token.lower())

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens, t



if __name__ == "__main__":

    #custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
    custom_tweet = "I ordered just once from TerribleCo, it was a good experince"
    custom_tokens,r = remove_noise(word_tokenize(custom_tweet))
    loaded_model = pickle.load(open("sent_model.sav", 'rb'))
    result = loaded_model.classify(dict([token, True] for token in custom_tokens))
    print(r)
    #print(dict([token, True] for token in custom_tokens))