import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from plot_words import (
    change_word,
    fit_count,
    log_transform_counts,
    fit_zero_inflated_pca,
    fit_standard_pca,
    check_color_bar_needed,
    encode_labels,
    prepare_pca_data,
)


def test_change_word():
    """
    Test the change_word function.

    This function tests if the change_word function correctly changes a word
    in the list of column names.

    Parameters
    ----------
    None

    """
    column_names = ["word1", "word2", "word3"]
    change_word("word2", "new_word2", column_names)
    assert column_names == ["word1", "new_word2", "word3"]


def test_log_transform_counts():
    """
    Test the log_transform_counts function.

    This function tests if the log_transform_counts function correctly
    transforms the count matrix using log transformation.

    Parameters
    ----------
    None

    """
    count_matrix = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    transformed = log_transform_counts(count_matrix)
    assert transformed.shape == (2, 3)
    assert np.all(transformed >= 0)


def test_fit_count():
    """
    Test the fit_count function.

    This function tests if the fit_count function correctly fits the count
    matrix with supervised labels.

    Parameters
    ----------
    None

    """
    count_matrix = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    labels = np.array([0, 1])
    fitted = fit_count(count_matrix, supervised=True, labels=labels)
    assert isinstance(fitted, pd.DataFrame)
    assert fitted.shape == count_matrix.shape


def test_fit_zero_inflated_pca():
    """
    Test the fit_zero_inflated_pca function.

    This function tests if the fit_zero_inflated_pca function correctly
    transforms the count matrix using zero-inflated PCA.

    Parameters
    ----------
    None

    """
    count_matrix = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    labels = np.array([0, 1])
    exog = LabelEncoder().fit_transform(labels).reshape(-1, 1)
    transformed = fit_zero_inflated_pca(count_matrix, supervised=True, exog=exog)
    assert transformed.shape[0] == count_matrix.shape[0]


def test_fit_standard_pca():
    """
    Test the fit_standard_pca function.

    This function tests if the fit_standard_pca function correctly
    transforms the count matrix using standard PCA.

    Parameters
    ----------
    None

    """
    count_matrix = pd.DataFrame([[1, 2, 3], [4, 5, 6]])
    labels = np.array([0, 1])
    exog = LabelEncoder().fit_transform(labels).reshape(-1, 1)
    transformed = fit_standard_pca(count_matrix, supervised=True, exog=exog)
    assert transformed.shape[0] == count_matrix.shape[0]


def test_check_color_bar_needed():
    """
    Test the check_color_bar_needed function.

    This function tests if the check_color_bar_needed function correctly
    determines if a color bar is needed based on the labels and fitted count matrix.

    Parameters
    ----------
    None

    """
    labels = np.array([0, 1, 2])
    fitted_count_matrix = np.array([[1, 2], [3, 4], [5, 6]])
    result, uniques = check_color_bar_needed(labels, fitted_count_matrix)
    assert result is True
    assert len(uniques) == len(np.unique(labels))


def test_encode_labels():
    """
    Test the encode_labels function.

    This function tests if the encode_labels function correctly
    encodes the labels.

    Parameters
    ----------
    None

    """
    labels = np.array(["a", "b", "a"])
    encoded = encode_labels(labels)
    assert np.array_equal(encoded, np.array([0, 1, 0]))


def test_prepare_pca_data():
    """
    Test the prepare_pca_data function.

    This function tests if the prepare_pca_data function correctly
    prepares the PCA data.

    Parameters
    ----------
    None

    """
    fitted_count_matrix = np.array([[1, 2, 3], [4, 5, 6]])
    pca_data, explained_ratio, _ = prepare_pca_data(fitted_count_matrix)
    assert pca_data.shape[1] == 2
    assert len(explained_ratio) == 2
