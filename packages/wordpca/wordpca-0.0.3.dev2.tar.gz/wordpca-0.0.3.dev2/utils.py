import numpy as np


def calculate_correlation(X, pca_transformed):
    """
    Calculate correlations between each variable in X and the first two principal components.

    Parameters
    ----------
    X : np.ndarray
        Input data matrix with shape (n_samples, n_features).
    pca_transformed : np.ndarray
        Data matrix after PCA transformation.

    Returns
    -------
    ccircle : list of tuples
        List of tuples containing correlations with the first and second principal components.
    """
    ccircle = []
    for j in X.T:
        corr1 = np.corrcoef(j, pca_transformed[:, 0])[0, 1]
        corr2 = np.corrcoef(j, pca_transformed[:, 1])[0, 1]
        ccircle.append((corr1, corr2))
    return ccircle
