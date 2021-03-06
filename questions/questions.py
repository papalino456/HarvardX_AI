from typing import Tuple
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding="utf-8") as file:
            files[filename] = file.read()
    
    return files
    


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    doc = []
    for word in words:
        if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation:
            doc.append(word)
    return doc


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # nDocs = number of docs
    # Wd = number of docs with a given word 
    # idfs of a word = ln(nDocs)/dW

    idfs = {}
    words = set()
    nDocs = len(documents)
    
    for File in documents:
        words.update(set(documents[File]))

    for word in words:
        Wd = sum(word in documents[filename] for filename in documents)
        idf = math.log(nDocs / Wd)
        idfs[word] = idf
    
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = []
    for filename in files:
        tf_idf = 0
        for i in query:
            tf_idf = tf_idf + idfs[i] * files[filename].count(i)
        tf_idfs.append((filename, tf_idf))
        
    tf_idfs.sort(key=lambda x: x[1], reverse=True)

    filenames = [x[0] for x in tf_idfs[:n]]

    return filenames


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    result = []
    for sentence in sentences:
        idf = 0
        total_words_found = 0
        for word in query:
            if word in sentences[sentence]:
                total_words_found += 1
                idf += idfs[word]
        density = float(total_words_found) / len(sentences[sentence])
        result.append((sentence, idf, density))
    result.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return [x[0] for x in result[:n]]



if __name__ == "__main__":
    main()
