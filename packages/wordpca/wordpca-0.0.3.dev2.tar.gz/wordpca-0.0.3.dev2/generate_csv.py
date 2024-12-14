from typing import List, Union, Tuple

import numpy as np
import pandas as pd

from tobow import line_to_bow


def _concat(line1, line2):
    return pd.concat([line1, line2], axis=0, join="outer")


def split(file_lines: List[str], n_samples: int) -> List[str]:
    """
    Splits the file lines into chunks based on the number of samples.

    Parameters
    ----------
    file_lines : list of str
        The lines of the file to be split.
    n_samples : int
        The number of samples to split the file into.

    Returns
    -------
    list of str
        The joined chunks of file lines.
    """
    nb_lines = len(file_lines)
    n = calculate_chunk_size(nb_lines, n_samples)
    chunks = create_chunks(file_lines, n)
    filtered_chunks = filter_chunks(chunks)
    return join_chunks(filtered_chunks)


def calculate_chunk_size(nb_lines: int, n_samples: int) -> int:
    """
    Calculates the size of each chunk based on the number of lines and samples.

    Parameters
    ----------
    nb_lines : int
        The number of lines in the file.
    n_samples : int
        The number of samples to split the file into.

    Returns
    -------
    int
        The size of each chunk.
    """
    return int(nb_lines // n_samples) + ((nb_lines % n_samples) > 0)


def create_chunks(file_list: List[str], chunk_size: int) -> List[List[str]]:
    """
    Creates chunks of the file list based on the chunk size.

    Parameters
    ----------
    file_list : list of str
        The list of lines from the file.
    chunk_size : int
        The size of each chunk.

    Returns
    -------
    list of list of str
        The chunks of file lines.
    """
    return [file_list[i : i + chunk_size] for i in range(0, len(file_list), chunk_size)]


def filter_chunks(chunks: List[List[str]]) -> List[List[str]]:
    """
    Filters out short lines from each chunk.

    Parameters
    ----------
    chunks : list of list of str
        The chunks of file lines.

    Returns
    -------
    list of list of str
        The filtered chunks with short lines removed.
    """
    return [[line for line in chunk if len(line) > 1] for chunk in chunks]


def join_chunks(chunks: List[List[str]]) -> List[str]:
    """
    Joins the lines in each chunk into a single string.

    Parameters
    ----------
    chunks : list of list of str
        The chunks of file lines.

    Returns
    -------
    list of str
        The joined chunks of file lines.
    """
    return [",".join(chunk) for chunk in chunks]


def get_file_lines(file_path):
    """
    Read the content of a file and split it into lines.

    Parameters
    ----------
    file_path : str
        The path to the file.

    Returns
    -------
    list
        A list of lines from the file.
    """
    with open(file_path, "r", encoding="utf-8") as myfile:
        content = myfile.read()
    file_lines = content.replace("\n", " ").split(".")
    return file_lines


def process_file(
    filename: str, n_samples: int, language_stop_words: str
) -> pd.DataFrame:
    """
    Processes a single file and returns the count matrix.

    Parameters
    ----------
    filename : str
        The name of the file to process.
    n_samples : int
        The number of samples to split the file into.
    language_stop_words: str
        The language that will be used for the stop words. If None, no stop words will be used.

    Returns
    -------
    pd.DataFrame
        The count matrix for the file.
    """
    file_lines = get_file_lines(filename)
    text_chunks = split(file_lines, n_samples)

    count_matrix = pd.DataFrame()
    for text_chunk in text_chunks:
        if len(text_chunk) > 5:
            count_line = line_to_bow(text_chunk, language_stop_words)
            count_matrix = _concat(count_matrix, count_line)
    return count_matrix


def get_count_matrix(
    raw_filenames: Union[str, List[str]],
    n_samples: int,
    language_stop_words: str = "english",
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, List[str]]]:
    """
    Generates a count matrix from one or more files.

    Parameters
    ----------
    raw_filenames : str or list of str
        The name of the file or a list of filenames to process.
    n_samples : int
        The number of samples to split each file into.
    language_stop_words: str
        The language that will be used for the stop words. If None, no stop words will be used.
        Only "english" and "french" can be used right now.

    Returns
    -------
    pd.DataFrame
        The combined count matrix from all files.
    list of str, optional
        The list of filenames for each sample
    """
    if isinstance(raw_filenames, str):
        raw_filenames = [raw_filenames]

    count_matrix = pd.DataFrame()
    labels = []
    for filename in raw_filenames:
        processed_file = process_file(filename, n_samples, language_stop_words)
        count_matrix = pd.concat(
            [count_matrix, processed_file],
            ignore_index=True,
        )
        labels = labels + [filename] * processed_file.shape[0]
    if len(np.unique(labels)) == 1:
        labels = np.arange(count_matrix.shape[0])

    count_matrix = count_matrix.fillna(0)
    return count_matrix, labels
