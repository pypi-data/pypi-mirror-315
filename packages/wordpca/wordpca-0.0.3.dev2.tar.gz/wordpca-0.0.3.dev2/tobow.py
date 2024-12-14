from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from nltk.stem.snowball import EnglishStemmer, FrenchStemmer
from stopwords import french_stop_words  # Correct import statement


def get_stop_words(custom_stop_words=None, language="english"):
    """
    Get the combined list of stop words.

    Parameters
    ----------
    custom_stop_words : list, optional
        A list of custom stop words to use. If None, an empty list is used.
    language : str, optional
        The language for the default stop words. Default is 'english'.

    Returns
    -------
    set
        A set of stop words.
    """
    if custom_stop_words is None:
        custom_stop_words = []

    if language == "french":
        default_stop_words = french_stop_words
    elif language == "english":
        vectorizer = CountVectorizer(stop_words="english")
        default_stop_words = vectorizer.get_stop_words()
    else:
        default_stop_words = []

    combined_stop_words = set(custom_stop_words).union(default_stop_words)
    return combined_stop_words


def stemmed_words(doc, stop_words=None, language="english"):
    """
    Stem the words in a document, excluding stop words.

    Parameters
    ----------
    doc : str
        The document to process.
    stop_words : list, optional
        A list of custom stop words to use. If None, an empty list is used.
    language : str, optional
        The language for the default stop words. Default is 'english'.

    Returns
    -------
    list
        A list of stemmed words from the document.
    """
    stop_words_set = get_stop_words(stop_words, language)
    vectorizer = CountVectorizer()
    analyzer = vectorizer.build_analyzer()

    if language == "french":
        stemmer = FrenchStemmer()
    else:
        stemmer = EnglishStemmer()

    words = analyzer(doc)
    return [stemmer.stem(word) for word in words if word not in stop_words_set]


def read_file(file_path):
    """
    Read the content of a file.

    Parameters
    ----------
    file_path : str
        The path to the file.

    Returns
    -------
    str
        The content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as myfile:
        return myfile.read()


def file_to_bow(file_path, language="english"):
    """
    Convert the content of a file to a bag-of-words DataFrame.

    Parameters
    ----------
    file_path : str
        The path to the file.
    language : str, optional
        The language for the default stop words. Default is 'english'.

    Returns
    -------
    pd.DataFrame
        A DataFrame representing the bag-of-words of the file content.
    """
    text_data = read_file(file_path)
    return line_to_bow(text_data, language)


def line_to_bow(line, language="english"):
    """
    Convert a line of text to a bag-of-words DataFrame.

    Parameters
    ----------
    line : str
        The line of text to process.
    language : str, optional
        The language for the default stop words. Default is 'english'.

    Returns
    -------
    pd.DataFrame
        A DataFrame representing the bag-of-words of the line.
    """
    vectorizer = CountVectorizer(
        analyzer=lambda doc: stemmed_words(doc, language=language)
    )
    count_line = vectorizer.fit_transform([line])
    count_vect_df = pd.DataFrame(
        count_line.todense(), columns=vectorizer.get_feature_names_out()
    )
    return count_vect_df
