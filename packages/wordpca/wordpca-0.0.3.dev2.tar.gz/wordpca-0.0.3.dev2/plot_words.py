from typing import Optional, List, Dict, Tuple
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from matplotlib.patches import Circle

from pyPLNmodels import PlnPCA, Brute_ZIPln
from utils import calculate_correlation

colors_viridis = sns.color_palette("viridis")
default_markers = ["o", "v", "*", "x", "P", "s"]


def change_word(old_word: str, new_word: str, column_names: List[str]) -> None:
    """
    Change a word in the list of column names.

    Args:
        old_word (str): The word to be replaced.
        new_word (str): The new word to replace the old word.
        column_names (List[str]): The list of column names.
    """
    if old_word in column_names:
        column_names[column_names.index(old_word)] = new_word


def fit_count(
    count_matrix: pd.DataFrame,
    zero_inflation: bool = False,
    log_transform: bool = False,
    supervised: bool = False,
    labels: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """
    Fit a count matrix using PCA or zero-inflated PCA.

    Args:
        count_matrix (pd.DataFrame): The count matrix.
        zero_inflation (bool): Whether to use zero-inflated PCA.
        log_transform (bool): Whether to log-transform the counts.
        supervised (bool): Whether to use supervised learning.
        labels (Optional[np.ndarray]): The labels for supervised learning.

    Returns:
        pd.DataFrame: The fitted count matrix.
    """
    column_names = list(count_matrix.columns)
    if supervised and labels is None:
        raise ValueError("Cannot perform supervised learning without labels")

    if log_transform:
        fitted_count = log_transform_counts(count_matrix)
    else:
        onehot = OneHotEncoder()
        exog = onehot.fit_transform(np.array(labels).reshape(-1, 1)).toarray()
        print("exog", exog)
        if zero_inflation:
            fitted_count = fit_zero_inflated_pca(count_matrix, supervised, exog)
        else:
            fitted_count = fit_standard_pca(count_matrix, supervised, exog)
    return pd.DataFrame(fitted_count, columns=column_names)


def log_transform_counts(count_matrix: pd.DataFrame) -> np.ndarray:
    """
    Log-transform the counts in the count matrix.

    Args:
        count_matrix (pd.DataFrame): The count matrix.

    Returns:
        np.ndarray: The log-transformed counts.
    """
    count_matrix = count_matrix.to_numpy()
    normalized_counts = (
        (count_matrix + 1) / (np.sum(count_matrix, axis=1).reshape(-1, 1) + 1) * 10000
    )
    return np.copy(np.log(normalized_counts))


def fit_zero_inflated_pca(
    count_matrix: pd.DataFrame, supervised: bool, exog: Optional[np.ndarray]
) -> np.ndarray:
    """
    Fit a zero-inflated PCA model to the count matrix.

    Args:
        count_matrix (pd.DataFrame): The count matrix.
        supervised (bool): Whether to use supervised learning.
        exog (Optional[np.ndarray]): The exogenous variables for supervised learning.

    Returns:
        np.ndarray: The transformed count matrix.
    """
    if supervised:
        pca = Brute_ZIPln(count_matrix, exog=exog, add_const=False)
    else:
        pca = Brute_ZIPln(count_matrix)
    pca.fit(nb_max_epoch=10)
    return np.copy(pca.transform())


def fit_standard_pca(
    count_matrix: pd.DataFrame, supervised: bool, exog: Optional[np.ndarray]
) -> np.ndarray:
    """
    Fit a standard PCA model to the count matrix.

    Args:
        count_matrix (pd.DataFrame): The count matrix.
        supervised (bool): Whether to use supervised learning.
        exog (Optional[np.ndarray]): The exogenous variables for supervised learning.

    Returns:
        np.ndarray: The transformed count matrix.
    """
    if supervised:
        pca = PlnPCA(count_matrix, exog=exog, add_const=False)
    else:
        pca = PlnPCA(count_matrix)
    pca.fit()
    return np.copy(pca.transform())


# Disable too-many-arguments and too-many-positional-arguments
# pylint: disable=too-many-arguments, too-many-positional-arguments,too-many-locals
def myplot(
    ax: plt.Axes,
    fig: plt.Figure,
    scores: np.ndarray,
    labels: Optional[np.ndarray],
    uniques: np.ndarray,
    plot_markers: Optional[List[str]],
    fontsize: int,
) -> None:
    """
    Plot the PCA scores.

    Args:
        ax (plt.Axes): The axes to plot on.
        fig (plt.Figure): The figure to plot on.
        scores (np.ndarray): The PCA scores.
        labels (Optional[np.ndarray]): The labels for the data points.
        uniques (np.ndarray): The unique labels.
        plot_markers (Optional[List[str]]): The markers for the data points.
        fontsize (int): The font size for the plot.
    """
    xs = scores[:, 0]
    ys = scores[:, 1]
    scalex = 1.0 / (xs.max() - xs.min())
    scaley = 1.0 / (ys.max() - ys.min())

    if labels is None:
        ax.scatter(xs * scalex, ys * scaley, c="b", label="Data", s=200)
    elif len(np.unique(labels)) == scores.shape[0]:
        colorbar = ax.scatter(
            xs * scalex, ys * scaley, c=labels, cmap="viridis_r", s=200
        )
        cbar = fig.colorbar(
            colorbar, orientation="horizontal", shrink=0.5, ticks=[0, labels[-1]], pad=0
        )
        cbar.ax.xaxis.set_ticks_position("top")
        cbar.ax.xaxis.set_label_position("top")
        cbar.ax.set_xticklabels(["Beginning of chapter", "End of chapter"])
        cbar.ax.tick_params(labelsize=fontsize - 5)
        cbar.ax.set_position([0.15, 3.1, 0.7, 0.03])
    else:
        for i, label in enumerate(uniques):
            indices = np.where(labels == label)
            marker = plot_markers[i] if plot_markers is not None else None
            ax.scatter(
                (xs * scalex)[indices],
                (ys * scaley)[indices],
                c=colors_viridis[i],
                label=label,
                marker=marker,
                s=200,
            )
    ax.grid()


def check_color_bar_needed(
    labels: Optional[np.ndarray], fitted_count_matrix: np.ndarray
) -> Tuple[bool, np.ndarray]:
    """
    Check if a color bar is needed for the plot.

    Args:
        labels (Optional[np.ndarray]): The labels for the data points.
        fitted_count_matrix (np.ndarray): The fitted count matrix.

    Returns:
        Tuple[bool, np.ndarray]: A tuple containing a boolean indicating
        if a color bar is needed and the unique labels.
    """
    uniques = np.unique(labels)
    return len(labels) == fitted_count_matrix.shape[0], uniques


def encode_labels(labels: Optional[np.ndarray]) -> Optional[np.ndarray]:
    """
    Encode the labels using a label encoder.

    Args:
        labels (Optional[np.ndarray]): The labels to encode.

    Returns:
        Optional[np.ndarray]: The encoded labels.
    """
    if labels is not None:
        labelencoder = LabelEncoder()
        return labelencoder.fit_transform(labels)
    return None


def prepare_pca_data(
    fitted_count_matrix: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, PCA]:
    """
    Prepare the PCA data.

    Args:
        fitted_count_matrix (np.ndarray): The fitted count matrix.

    Returns:
        Tuple[np.ndarray, np.ndarray, PCA]: A tuple containing the PCA scores,
        the explained variance ratio, and the PCA model.
    """
    scaler = StandardScaler()
    x_std = scaler.fit_transform(fitted_count_matrix)
    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x_std)
    explained_ratio = pca.explained_variance_ratio_
    return x_pca, explained_ratio, pca


# Disable too-many-arguments and too-many-positional-arguments
# pylint: disable=too-many-arguments, too-many-positional-arguments
def plot_pca_results(
    ax: plt.Axes,
    explained_ratio: np.ndarray,
    corrs: np.ndarray,
    best_words: List[str],
    fontsize: int,
) -> None:
    """
    Plot the PCA results.

    Args:
        ax (plt.Axes): The axes to plot on.
        explained_ratio (np.ndarray): The explained variance ratio.
        corrs (np.ndarray): The correlations.
        best_words (List[str]): The best words.
        fontsize (int): The font size for the plot.
    """
    min_x = np.min(corrs[:, 0]) - 0.2
    max_x = np.max(corrs[:, 0]) + 0.2
    min_y = np.min(corrs[:, 1]) - 0.2
    max_y = np.max(corrs[:, 1]) + 0.2

    for word, corr in zip(best_words, corrs):
        x = corr[0]
        y = corr[1]
        size = abs(x) + abs(y)
        ax.text(x=x, y=y, s=word, fontsize=1.4 * (3.5 + 2 * size) ** 2)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    circle = Circle((0, 0), 1, facecolor="none", edgecolor="k", linewidth=1, alpha=0.5)
    ax.add_patch(circle)
    ax.set_xlabel(
        f"PCA 1 ({(np.round(explained_ratio[0]*100, 3))}%)", fontsize=fontsize
    )
    ax.set_ylabel(
        f"PCA 2 ({(np.round(explained_ratio[1]*100, 3))}%)", fontsize=fontsize
    )
    ax.tick_params(axis="both", which="major", labelsize=fontsize - 5)


# Disable too-many-arguments and too-many-positional-arguments
# pylint: disable=too-many-arguments, too-many-positional-arguments,too-many-locals
def plot_fitted_count(
    fitted_count_matrix: np.ndarray,
    nb_words: int,
    fontsize: int = 20,
    labels: Optional[np.ndarray] = None,
    plot_markers: Optional[List[str]] = None,
    file_extension: str = "png",
    replacement_dict: Optional[Dict[str, str]] = None,
    filename: str = "biplot",
) -> None:
    """
    Plot the fitted count matrix.

    Args:
        fitted_count_matrix (np.ndarray): The fitted count matrix.
        nb_words (int): The number of words to plot.
        fontsize (int): The font size for the plot.
        labels (Optional[np.ndarray]): The labels for the data points.
        plot_markers (Optional[List[str]]): The markers for the data points.
        file_extension (str): The file extension for the saved plot.
        replacement_dict (Optional[Dict[str, str]]): The dictionary for replacing words.
        filename (str): The filename for the saved plot.
    """
    if replacement_dict is None:
        replacement_dict = {}
    uniques = np.unique(labels)

    column_names = list(fitted_count_matrix.columns)
    for key, value in replacement_dict.items():
        change_word(key, value, column_names)

    labels = np.array(labels)
    x_pca, explained_ratio, _ = prepare_pca_data(fitted_count_matrix)
    corrs = np.array(calculate_correlation(fitted_count_matrix.to_numpy(), x_pca))

    best_indices = np.flip(np.argsort(np.sum(fitted_count_matrix, axis=0)))[:nb_words]
    best_words = [column_names[indice] for indice in best_indices]
    corrs = corrs[best_indices]

    fig, ax = plt.subplots(figsize=(20, 20), layout="constrained")
    myplot(
        ax,
        fig,
        x_pca[:, 0:2],
        labels,
        uniques,
        plot_markers,
        fontsize,
    )
    plot_pca_results(ax, explained_ratio, corrs, best_words, fontsize)

    plt.savefig(
        filename + "." + file_extension, format=file_extension, bbox_inches="tight"
    )
