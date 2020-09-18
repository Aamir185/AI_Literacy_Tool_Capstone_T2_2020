from stemming import lemmatize_sentence
from nltk.tokenize import word_tokenize

strings_example = """The process of tokenization takes some time 
                     because it’s not a simple split on white space. 
                     After a few moments of processing, you’ll see the
                     following"""
tokenized_words = word_tokenize(strings_example)

print(lemmatize_sentence(tokenized_words))
