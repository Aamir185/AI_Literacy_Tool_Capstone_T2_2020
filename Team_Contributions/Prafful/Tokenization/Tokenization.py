import nltk

# Download these modules from nltk package
# nltk.download('punkt')
# nltk.download('wordnet')

#Get the Random tweet which you want to tokenize

Tokenized_Tweet = nltk.word_tokenize("getting the random tweet from tweet account")
print(Tokenized_Tweet)
#Check the Data Type of the Tokentized Tweet
print(type(Tokenized_Tweet))

#convert the list Datatype into String Datatype and Print the output
String_type_Tokenization = ', '.join(map(str, Tokenized_Tweet))
print(String_type_Tokenization)
print(type(String_type_Tokenization))