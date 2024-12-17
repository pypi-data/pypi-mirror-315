"""Utils for matplotlib.pyplot."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import ndarray

from .arithmetic import (
    almost_factors,
)


def auto_subplot(
    size: int, /, ratio: float = 9 / 16, portrait: bool = False, **subplot_params: Any
) -> tuple[Figure, ndarray[tuple[int], Any]]:
    """
    Automatically creates a subplot grid with an adequate number of rows and columns.

    Args:
        size: The total number of subplots.
        ratio: The threshold aspect ratio between rows and columns.
        portrait: Whether there should be more rows than columns instead of the
            opposite
        **subplot_params: Additional keyword parameters for subplot.

    Returns:
        Tuple containing the figure and the flatten axes.
    """
    # Special case for 2
    large, small = (2, 1) if size == 2 else almost_factors(size, ratio)  # noqa: PLR2004
    rows, cols = (large, small) if portrait else (small, large)

    fig, axes = plt.subplots(rows, cols, **subplot_params)

    # if isinstance(axes, np.ndarray):
    #     axes = axes.flatten()
    axes = axes.flatten()

    # Hide the remaining axes if there are more axes than subplots
    for i in range(size, len(axes)):
        axes[i].set_axis_off()

    return fig, axes
