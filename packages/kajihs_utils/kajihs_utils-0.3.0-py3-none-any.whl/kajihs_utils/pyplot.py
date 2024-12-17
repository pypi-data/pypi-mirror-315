"""Utils for matplotlib.pyplot."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import ndarray

from .arithmetic import (
    almost_factors,
)


def auto_subplot(
    size: int, /, ratio: float = 9 / 16, **subplot_params: Any
) -> tuple[Figure, ndarray[tuple[int], Any]]:
    """
    Automatically creates a subplot grid with an adequate number of rows and columns.

    Args:
        size: The total number of subplots.
        ratio: The threshold aspect ratio between rows and columns.
        **subplot_params: Additional keyword parameters for subplot.

    Returns:
        Tuple containing the figure and the flatten axes.
    """
    rows, cols = almost_factors(size, ratio)

    fig, axes = plt.subplots(rows, cols, **subplot_params)

    # if isinstance(axes, np.ndarray):
    #     axes = axes.flatten()
    axes = axes.flatten()

    return fig, axes
