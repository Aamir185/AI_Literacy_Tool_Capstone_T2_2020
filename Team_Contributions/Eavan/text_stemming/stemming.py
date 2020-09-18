"""
Usage:
    1st) from stemming import lemmatize_sentence
    2nd) lemmatize_sentence(var) # var is a variable stored string

Made by Eavan
"""

from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

if __name__ == '__main__':

    strings_example = """Hello Mr. Smith, how are you doing today?
                         The weather is great, and city is awe some.\n
                         The sky is pinkish-blue. You shouldn't eat cardboard"""
    tokenized_words = word_tokenize(strings_example)

    print(lemmatize_sentence(tokenized_words))