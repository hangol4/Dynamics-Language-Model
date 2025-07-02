# Initially tried using this function to visualise embeddings - it would find the most common word as desired, 
# but in the case of Binney and Tremaine sometimes it was LaTex gibberish, so it was not useful.

import string

def most_common_word(chunk):
    # remove punctuation, convert to lowercase and split the chunk into words
    chunk = chunk.translate(str.maketrans('', '', string.punctuation))
    chunk = chunk.lower()
    words = chunk.split()
    # remove stop words
    stop_words = set(['the', 'is', 'in', 'and', 'to', 'a', 'of', 'that', 'it', 'for', 'on', \
                      'with', 'as', 'this', 'by', 'an', 'are', 'was', 'at', 'be', 'from', 'or', 'not', 'but', 'which', 'we'])
    words = [word for word in words if word not in stop_words]
    # keep the data in a dictionary
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    # Find the word with the highest count
    most_common = None
    highest_count = 0
    for word, count in word_count.items():
        if count > highest_count:
            most_common = word
            highest_count = count
    return most_common