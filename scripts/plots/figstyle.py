"""Module to set dimensions and style of figures."""

import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib as mpl


def fig_initialize(
    latex=False,
    setsize=False,
    size="preprint",
    fraction=1,
    subplots=(1, 1),
):

    mpl.rcParams["lines.marker"] = ""
    mpl.rcParams["lines.markersize"] = 1.2

    if latex:
        # Set up tex rendering
        plt.rc("text", usetex=True)
        plt.rc(
            "text.latex", preamble=r"\usepackage{amsmath, amsthm, amssymb, amsfonts}"
        )
        mpl.rcParams["font.family"] = "serif"
        mpl.rcParams["font.serif"] = "STIX"
        mpl.rcParams["mathtext.fontset"] = "stix"
    if setsize:
        mpl.rcParams["font.size"] = 10
        mpl.rcParams["axes.linewidth"] = 0.5
        mpl.rcParams["xtick.major.width"] = 0.5
        mpl.rcParams["ytick.major.width"] = 0.5
        mpl.rcParams["lines.linewidth"] = 1
        mpl.rcParams["axes.labelsize"] = 10
        mpl.rcParams["xtick.labelsize"] = 8
        mpl.rcParams["ytick.labelsize"] = 8
        plt.rc("legend", **{"fontsize": 8})
        plt.rc("legend", **{"frameon": False})
        mpl.rcParams["legend.labelspacing"] = 0.25

    # determine fig height and width
    if size == "reprint":
        width_pt = 243
    elif size == "scipy3d":
        width_pt = 320

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5 ** 0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    figdims = (fig_width_in, fig_height_in)

    return figdims
