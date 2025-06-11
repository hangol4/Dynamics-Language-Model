import string

def most_common_word(chunk):
    # remove punctuation, convert to lowercase and split the chunk into words
    chunk = chunk.translate(str.maketrans('', '', string.punctuation))
    chunk = chunk.lower()
    words = chunk.split()
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

chunk = "This is a test chunk. This chunk is for testing purposes. Testing is important. love Love LOVE love."
print(most_common_word(chunk))  