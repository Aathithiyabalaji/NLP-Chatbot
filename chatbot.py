import json
import random
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.data.path.append("./nltk_data")

from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

# Load intents
with open("intents.json", encoding='utf-8') as file:
    data = json.load(file)

from nltk.tokenize import word_tokenize

def tokenize(sentence):
    return word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = [1 if w in sentence_words else 0 for w in words]
    return bag

# Preprocess
all_words = []
xy = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = tokenize(pattern)
        all_words.extend(tokens)
        xy.append((tokens, intent["tag"]))
    tags.append(intent["tag"])

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

def get_intent(user_input):
    patterns = []
    tags_list = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            patterns.append(pattern)
            tags_list.append(intent["tag"])

    # Vectorize
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(patterns + [user_input])
    
    # Calculate cosine similarity
    cos_sim = cosine_similarity(vectors[-1], vectors[:-1])
    
    # Get best match
    index = cos_sim.argmax()
    confidence = cos_sim[0][index]
    print(f"Matched intent: {tags_list[index]} with confidence: {confidence:.2f}")

    
    if confidence > 0.3:  # You can adjust threshold here
        return tags_list[index]
    else:
        return "default"


def get_response(user_input):
    intent = get_intent(user_input)
    for intent_data in data["intents"]:
        if intent_data["tag"] == intent:
            return random.choice(intent_data["responses"])
    return "Sorry, I don't understand that."

