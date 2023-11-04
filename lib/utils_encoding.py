import json
import random
import csv

SAFE_NAMES_FILE = "names_list.csv"
used_words = []

def random_word_from_library():
    """Generate a random word from library."""
    word_list = []
    with open(SAFE_NAMES_FILE, 'r') as f:
        data = csv.reader(f)
        names = [row[0] for row in data]
        while True:
            random_name = random.choice(names)
            if random_name not in used_words:
                break
        used_words.append(random_name)
    return random_name

def create_randomized_dict(input_file):
    """Create a dictionary with unique words from the JSON file as keys and randomized words as values."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    words_list = [item["word"] for item in data]
    randomized_dict = {}

    for word in words_list:
        rand_word = random_word_from_library()
        randomized_dict[word] = rand_word
    
    return randomized_dict

if __name__ == "__main__":
    input_file = input("Enter the path to the JSON file: ")
    result = create_randomized_dict(input_file)
    print(result)