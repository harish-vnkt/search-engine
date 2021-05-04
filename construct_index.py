import jsonlines, json
import nltk, string, re
from bs4 import BeautifulSoup
import numpy as np, math
import argparse


def initialize_stemmer_stopwords():

    stop_words = list(nltk.corpus.stopwords.words('english'))
    stop_words = set([word.translate(str.maketrans('', '', string.punctuation)) for word in stop_words])
    stemmer = nltk.stem.porter.PorterStemmer()
    return stemmer, stop_words

def preprocess_word(word, stemmer, stop_words):
    """
    Function to convert word to lower-case, remove tags, remove punctuation and number, perform stemming and stop-word removal

    :param word: input word
    :param stemmer: stemmer
    :param stop_words: stop-word list
    :return: preprocessed word or empty string
    """

    # remove tags
    word = re.sub("<.*>", "", word)
    if not word:
        return ""

    word = word.lower()  # convert to lower-case
    # remove punctuation
    new_word = word.translate(str.maketrans('', '', string.punctuation))
    if not new_word:
        return ""
    # remove numbers from the string
    new_word = ''.join([i for i in new_word if not i.isdigit()])
    if not new_word:
        return ""

    # perform stemming and stop-word removal
    if new_word in stop_words:
        return ""
    stemmed_word = stemmer.stem(new_word)
    if stemmed_word in stop_words:
        return ""

    return stemmed_word

def parse_soup(soup_str):

    soup = BeautifulSoup(soup_str, 'html.parser')
    text = soup.get_text()
    return text

def construct_index(path):

    print("Constructing inverted index ..........")
    inv_index = {}  # inverted index for each term
    doc_len = {}  # norm of vectors for each document
    tf_dct = {}  # frequency dictionary for each document

    files = jsonlines.open(path)
    N = 0

    stemmer, stop_words = initialize_stemmer_stopwords()

    for file in files:

        N += 1

        s = parse_soup(file["soup"])
        s = s.strip()
        words = s.split()

        print(file["url"])
        tf_dct[file["url"]] = {}

        for word in words:

            stemmed_word = preprocess_word(word, stemmer, stop_words)
            if not stemmed_word:
                continue

            # add word to frequency dictionary for document
            if stemmed_word not in tf_dct[file["url"]]:
                tf_dct[file["url"]][stemmed_word] = 1
            else:
                tf_dct[file["url"]][stemmed_word] += 1

            # add word to inverted index
            if stemmed_word not in inv_index:
                inv_index[stemmed_word] = {}
                inv_index[stemmed_word][file["url"]] = 1
            else:
                if file["url"] not in inv_index[stemmed_word]:
                    inv_index[stemmed_word][file["url"]] = 1
                else:
                    inv_index[stemmed_word][file["url"]] += 1

        if len(tf_dct[file["url"]]) == 0:
            del tf_dct[file["url"]]

    print("Calculating vector norm for each document ..........")
    # calculate vector norms for each document
    for doc, freq_dct in tf_dct.items():

        max_f = max(freq_dct.values())
        doc_vector = []
        for term, freq in freq_dct.items():
            tf = freq / max_f
            df = len(inv_index[term])
            idf = math.log2(N / df)
            doc_vector.append(tf * idf)

        doc_vector = np.array(doc_vector)
        doc_len[doc] = [np.linalg.norm(doc_vector), max_f]

    with open('inv_index.json', 'w') as fp:
        json.dump(inv_index, fp)

    with open('doc_len.json', 'w') as fp:
        json.dump(doc_len, fp)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="File for constructing the inverted index from the scraped data")
    parser.add_argument("--path", help="Path to jsonlines file containing scraped data", type=str)
    args = parser.parse_args()
    construct_index(args.path)

