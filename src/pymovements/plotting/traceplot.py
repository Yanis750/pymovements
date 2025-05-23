# Copyright (c) 2022-2025 The pymovements Project Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Provides the traceplot plotting function."""
from __future__ import annotations

import sys

import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.scale
import numpy as np

from pymovements.gaze.gaze_dataframe import GazeDataFrame
from pymovements.plotting._matplotlib import _draw_line_data
from pymovements.plotting._matplotlib import _setup_matplotlib
from pymovements.plotting._matplotlib import LinearSegmentedColormapType

# This is really a dirty workaround to use the Agg backend if runnning pytest.
# This is needed as Windows workers on GitHub fail randomly with other backends.
# Unfortunately the Agg module cannot show plots in jupyter notebooks.
if 'pytest' in sys.modules:  # pragma: no cover
    matplotlib.use('Agg')


def traceplot(
        gaze: GazeDataFrame,
        position_column: str = 'pixel',
        cval: np.ndarray | None = None,  # pragma: no cover
        cmap: matplotlib.colors.Colormap | None = None,
        cmap_norm: matplotlib.colors.Normalize | str | None = None,
        cmap_segmentdata: LinearSegmentedColormapType | None = None,
        cbar_label: str | None = None,
        show_cbar: bool = False,
        padding: float | None = None,
        pad_factor: float | None = 0.05,
        figsize: tuple[int, int] = (15, 5),
        title: str | None = None,
        savepath: str | None = None,
        show: bool = True,
        add_stimulus: bool = False,
        path_to_image_stimulus: str | None = None,
        stimulus_origin: str = 'upper',
) -> None:
    """Plot eye gaze trace from positional data.

    Parameters
    ----------
    gaze: GazeDataFrame
        The GazeDataFrame to plot.
    position_column: str
        The column name of the x and y position data (default: 'pixel')
    cval: np.ndarray | None
        Line color values. (default: None)
    cmap: matplotlib.colors.Colormap | None
        Color map for line color values. (default: None)
    cmap_norm: matplotlib.colors.Normalize | str | None
        Normalization for color values. (default: None)
    cmap_segmentdata: LinearSegmentedColormapType | None
        Color map segmentation to build color map. (default: None)
    cbar_label: str | None
        String label for color bar. (default: None)
    show_cbar: bool
        Shows color bar if True. (default: False)
    padding: float | None
        Absolute padding value.
        If None it is inferred from pad_factor and limits. (default: None)
    pad_factor: float | None
        Relative padding factor to construct padding value if not given. (default: 0.5)
    figsize: tuple[int, int]
        Figure size. (default: (15, 5))
    title: str | None
        Set figure title. (default: None)
    savepath: str | None
        If given, figure will be saved to this path. (default: None)
    show: bool
        If True, figure will be shown. (default: True)
    add_stimulus: bool
        Define whether stimulus should be included. (default: False)
    path_to_image_stimulus: str | None
        Path to image stimulus. (default: None)
    stimulus_origin: str
        Origin of stimulus. (default: 'upper')

    Raises
    ------
    ValueError
        If length of x and y coordinates do not match or if ``cmap_norm`` is unknown.

    """
    # pylint: disable=duplicate-code
    x_signal = gaze.frame[position_column].list.get(0)
    y_signal = gaze.frame[position_column].list.get(1)

    fig, ax, cmap, cmap_norm, cval, show_cbar = _setup_matplotlib(
        x_signal,
        y_signal,
        figsize,
        cmap,
        cmap_norm,
        cmap_segmentdata,
        cval,
        show_cbar,
        add_stimulus,
        path_to_image_stimulus,
        stimulus_origin,
        padding,
        pad_factor,
    )

    line = _draw_line_data(
        x_signal,
        y_signal,
        ax,
        cmap,
        cmap_norm,
        cval,
    )

    if show_cbar:
        # sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=cmap_norm)
        # sm.set_array(cval)
        fig.colorbar(line, label=cbar_label, ax=ax)

    if title:
        ax.set_title(title)

    if savepath is not None:
        fig.savefig(savepath)

    if show:
        plt.show()
    plt.close(fig)
