import json, argparse
from construct_index import initialize_stemmer_stopwords, preprocess_word
import math, numpy as np

def construct_query_response(query, inv_index, doc_len):

    query = query.strip()
    words = query.split()
    stemmer, stop_words = initialize_stemmer_stopwords()
    query_freq_dct = {}
    result = {}
    N = len(doc_len)

    # build frequency dictionary of query
    for word in words:

        stemmed_word = preprocess_word(word, stemmer, stop_words)
        if not stemmed_word:
            continue

        if stemmed_word not in inv_index:
            continue

        if stemmed_word not in query_freq_dct:
            query_freq_dct[stemmed_word] = 1
        else:
            query_freq_dct[stemmed_word] += 1

    # compute max frequency for purpose of normalization
    max_f = max(query_freq_dct.values())
    query_vector = []

    for term, freq in query_freq_dct.items():

        documents = inv_index[term]

        # construct tf-idf vector for query
        query_tf_idf = freq / max_f * math.log2(N / len(documents))
        query_vector.append(query_tf_idf)

    # calculate norm of query vector
    query_vector = np.array(query_vector)
    query_vector_norm = np.linalg.norm(query_vector)

    # accumulate partial cosine similarity for every document
    for i, (term, freq) in enumerate(query_freq_dct.items()):

        documents = inv_index[term]  # documents where term appears
        doc_idf = math.log2(N / len(documents))  # idf of term since it is the same for all the documents
        query_tf_idf = query_vector[i]  # tf-idf of term in query

        # iterate through all the documents in which the term appears
        for doc, doc_freq in documents.items():

            doc_tf_idf = (doc_freq / doc_len[doc][1]) * doc_idf  # calculate tf-idf of term in document
            # add partial cosine similarity to result
            if doc not in result:
                result[doc] = (query_tf_idf * doc_tf_idf) / (query_vector_norm * doc_len[doc][0])
            else:
                result[doc] += (query_tf_idf * doc_tf_idf) / (query_vector_norm * doc_len[doc][0])

    return {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="File for querying the scraped data")
    parser.add_argument("--index_path", help="Path to JSON file containing inverted index", type=str, default="inv_index.json")
    parser.add_argument("--doc_path", help="Path to JSON file containing TF-IDF vector norm for each of the scraped pages", type=str, default="doc_len.json")
    args = parser.parse_args()

    with open(args.index_path, 'r') as f:
        inv_index = json.load(f)
    with open(args.doc_path, 'r') as f:
        doc_len = json.load(f)

    while True:

        query = input("Enter a query to be searched. Enter \"exit\" to exit.")
        if query == "exit":
            print("Exiting ..........")
            break
        else:
            print(construct_query_response(query, inv_index, doc_len))


