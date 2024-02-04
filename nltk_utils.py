import nltk
import numpy as np

nltk.download('punkt')  # package with pre-trained tokenizer
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()


# tokenize is to split string into individual words, punctuations and numbers
def tokenize(sentence):
    return nltk.word_tokenize(sentence)


# stemming is to generate root form of the words, find similarity and then chop off the ends of each word
def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]  # stem the tokenized sentence
    bag = np.zeros(len(all_words), dtype=np.float32)  # initializes a NumPy array bag filled with zeros,same length
    # as the no of unique words in all_words
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0  # if word in tokenized sentence present in all words, replace with 1.0
    return bag

# test bag_of_words
# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bag = bag_of_words(sentence, words)
# print(bag)

# test tokenization
# a = "How long does shipping take?"
# print(a)
# a = tokenize(a)
# print(a)

# test stemming
# words = ["Organize", "organizes", "organizing"]
# stemmed_words = [stem(w) for w in words]
# print(stemmed_words)
