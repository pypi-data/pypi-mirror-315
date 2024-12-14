
"""
Plots utilities for climate indices.
"""

import math
import itertools as it
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr

import matplotlib.pyplot as plt
from matplotlib import colormaps as cmaps

from ..utils import *
from .utils import *

# default Matplotlib settings
plot_img_defaults = { 'robust':True, 'levels':8 }

MATPLOTLIB_COLORBAR_LABEL = '<colorbar>'

# ------------------------------------------------------------------------------
# XY maps

def plot_index_xy_slice(da, contour=False, show=True, close=True, ofile=None, tight=False, **plot_kw):
    """
    Overloading of `plot_index_xy_slices` for 2D input data arrays.

    Examples
    ========
    >>> plots.plot_index_xy_slice( amt_ds['amt'].isel(model=5, time=1), robust=False, levels=100)
    >>> plots.plot_index_xy_slice( amt_ds['amt'].isel(model=5, time=1), contour=True)
    """
    return plot_index_xy_slices(da, contour=contour, show=show, close=close, ofile=ofile, tight=tight, **plot_kw)


#------------------------------------------------------------------------------
def plot_index_xy_slices(da, contour=False, show=True, close=True, ofile=None, tight=False, **plot_kw):
    """
    Plots all  spatial slices of an input climate index, 
    The plot will lay out models in the same ensembles as columns,
    and time-series of a same model as rows.

    If the array is not 2-dimensional and the time and/or model
    dimensions are not found in the array, an error will be throw
    (set `tdim`/`mdim` to `None` to ignore them).

    In order to reduce the size of the plot, make sure to properly
    subset the input index with the `sel`/`[`/`isel`/`loc` indexers, eg.:

    Examples
    ========
    >>> plots.plot_index_xy_slices( amt_ds['amt'].isel(model=[0,4,5], time=0) )
    >>> plots.plot_index_xy_slices( amt_ds['amt'][time=range(1,10,2)] )
    >>> plots.plot_index_xy_slices( amt_ds['amt'].sel(time=slice('2050','2080')) )
    >>> plots.plot_index_xy_slices( amt_ds['amt'].loc[{'time':'2030'}] )

    See Also
    ========
    climdex.analyse.plots.plot_2D()
    """
    # default row/col layout for index:
    row_dim = MODELS_DIM if MODELS_DIM in da.dims else None
    col_dim = TIME_DIM   if TIME_DIM   in da.dims else None

    return plot_2D(da, contour=contour, show=show, close=close, ofile=ofile,
                        row_dim=row_dim, col_dim=col_dim, tight=tight, **plot_kw)


#------------------------------------------------------------------------------
#
def concat_and_plot_2D(das, dim_name:str, dim_labels=None, **kwargs):
    """
    Plots data from multiple input data arrays as 2D maps.
    The method concatenates the input datasets, then
    forwards the plotting to the 'plot_2D()` function.

    Parameters
    ----------
    das : list of DataArray
        The multiple data arrays to be plotted.

    dim_name : str
        The label for the new dimension where the input
        data arrays will be stacked along.

    dim_labels : list of str (optional)
        The labels of each tick in the new dimension, to be associated
        with each element of das, respectively; these labels
        will appear as title of each sub-plot in the facet.

    **kwargs : forwarded to plot_2D().

    Examples
    ========
    >>> concat_and_plot_2D([da_rcp45, da_rcp85], dim_name='scenario', col_wrap=2,
                            dim_labels=['RCP 4.5', 'RCP 8.5'],
                            cbar_kwargs={'location':'bottom'},
                            contour=True, robust=False, tight=True)

    See Also
    ========
    climdex.analyse.plots.plot_2D()
    """
    # - - - - - - - - - -
    if das is None:
        return None

    if len(das) <= 1:
        raise ValueError("Please provide at least 2 different data arrays.")

    if dim_name is None:
        raise ValueError("Provide the name of the dimension along whic to stack the data.")

    for da in das:
        if dim_name in da.dims:
            raise ValueError("'{}' dimension found in one of the input arrays: {}".format(dim, da.dims))
    # - - - - - - - - - -

    # stack data together
    dim = pd.Index(dim_labels, name=dim_name) if dim_labels is not None else dim_name
    concat_da = xr.concat(das, dim=dim)

    if 'plot_labels' not in kwargs:
        kwargs.update({'plot_labels':dim_labels})
    # plot
    return plot_2D(concat_da, col_dim=dim_name, **kwargs)


#------------------------------------------------------------------------------
#
def plot_2D(da, contour=False, show=True, close=True, row_dim=None, col_dim=None,
            plot_labels=None, cmap_name=None, cbar_title=None, bg_color=None, bad=None, vmin=None, vmax=None,
            geometries=None, geom_kw=None, tight=False, axis='on', ofile=None, dpi='figure', **plot_kw):
    """
    Plots 1+ 2D maps an input data array.
    If the input data is 3+D, then row_dim/col_dim shall be used to
    specify along which dimensions should the slices be extracted.

    Parameters
    ----------
    da : DataArray
        The array containing the data to be plotted.

    contour : bool (optional, default False)
        Whether to plot the pixels or the derived (filled) contours.

    show : bool (optional, default True)
        Whether to show the plot on the display or not.

    close : bool (optional, default True)
        Whether to close the Matplotlib call or not before exiting.

    row_dim : str (optional)
        The dimension where to lay out the rows in the facet plot
        ('row' argument in the Matplotlib call).

    col_dim : str (optional)
        The dimension where to lay out the columns in the facet plot
        ('col' argument in the Matplotlib call).

    plot_labels : list of str
        The custom labels for each subplot in the facet
        (otherwise automatically crafted by matplotlib)

    cmap_name : str
        The name of the colormap to be selected from matplotlib.colormaps
        (see list(matplotlib.colormaps); directly use the matplotlib 'cmap'
        argument directly to set a custom colormap.

    cbar_title : str
        The title of the colorbar (on top of object).
        For default labelling use 'cbar_kwargs:label' param.

    bg_color : str
        The background color to be set for all sub-plot.

    bad : numeric
        Value to be set to completely transparent in the plot.

    vmin, vmax : numeric
        Values to be set for the "set_clim" call in the plots: values
        below/over the limits are hidden.

    geometries : GeoDataFrame or GeoSeries
        Vector data to be overlaid on each subplot.

    geom_kw :
        Keyword arguments for the GeoPandas plot call.

    tight : bool (optional, default False)
        Whether to force a tight layout in the plot.

    axis : 'on'/'off'
        De/activates axes labels and ticks from all plots.

    ofile : str or Path (optional, default None)
        The path to the file where to store the plot.

    dpi : float or 'figure'
        DPI argument for the plt.savefig() function to control resolution of image file.
        To be used in conjuntion with "ofile" to trigger storage of plot to file.

    **plot_kw
        Additional arguments that are passed to the `xr.imshow`/`xr.contourf` functions.

    Examples
    ========
    >>> plot_2D( da, col_dim='scenario', col_wrap=2,
                      levels=range(0, 100, 20),
                      cbar_kwargs={'location':'bottom'})
    >>> plot_2D( da, contour=True, col_dim='scenario', col_wrap=2)

    Returns
    -------
    The plot object.
    """
    # - - - - - - - - - -
    if da is None:
        return None

    if da.ndim == 1:
        raise ValueError("Input data array shall be at least 2-dimensional.")

    for dim in row_dim, col_dim:
        if dim is not None and (not dim in da.dims):
            raise ValueError("'{}' dimension not found in the array: {}".format(dim, da.dims))

    if (cmap_name is not None) and (cmap_name not in cmaps):
        raise ValueError("'{}' colormap does not exist in matplotlib. See matplotlib.colormaps.".format(cmap_name))

    if axis not in ['on','off']:
        raise ValueError("Wrong axis param: '{}'. Legal values: {}".format(axis, ['on','off']))

    if geometries is not None:
        if (not isinstance(geometries, gpd.GeoDataFrame) and
            not isinstance(geometries, gpd.GeoSeries)):
            raise ValueError("'geometries' input shall be of type GeoDataFrame or GeoSeries (geopandas).")

    # - - - - - - - - - -

    # apply defaults:
    global plot_img_defaults
    _ = [ plot_kw.setdefault(k,v) for k,v in plot_img_defaults.items() ]

    if cmap_name is not None:
        my_cmap = cmaps.get(cmap_name)
        #my_cmap = cmaps.get_cmap(cmap_name).resampled(14)
        #my_cmap.set_bad('green') # -> nans
        #my_cmap.set_under('green') #-> for robust colorbas
        #my_cmap.set_extremes('lightgreen')
        plot_kw.setdefault('cmap', my_cmap)

    if bad is not None:
       da = da.where(da != bad) # like cmap.set_bad -> nan

    if contour:
        g = da.plot.contourf(row=row_dim, col=col_dim, **plot_kw)
    else:
        g = da.plot.imshow(row=row_dim, col=col_dim, **plot_kw)
    
    if vmin is not None or vmax is not None:
        for im in plt.gca().get_images():
            im.set_clim(vmin=vmin, vmax=vmax)

    for i, ax in enumerate(g.axes.flat):
        #ax.set(adjustable="datalim") # -> causes error when plotting geometries overlay (see below here)
        ax.set(adjustable="box") 
        if plot_labels is not None:
            ax.set_title(plot_labels[i])
        if bg_color is not None:
            ax.set_facecolor(bg_color)
        if geometries is not None:
            geometries.plot(ax=ax, **geom_kw)

    for i, ax in enumerate(g.fig.axes):
        if (cbar_title is not None) and (ax.get_label() == MATPLOTLIB_COLORBAR_LABEL): # cbar_title is not None
            ax.set_title(cbar_title)
        

    if axis == 'off':
        g.set_axis_labels('','')
        #g.set_ticks(0, 0) -> [!] division by zero
        plt.xticks([], [])
        plt.yticks([], [])

    if tight:
        plt.tight_layout()
    if ofile is not None:
        plt.savefig( ofile, dpi=dpi )
    if show:
        plt.show()
    if close:
        plt.close()

    return plt


#------------------------------------------------------------------------------
#
def plot_trend(da, show=True, close=True, xdim=TIME_DIM, perc_dim=MODELS_DIM, scenario_dim=SCENARIO_DIM,
               row_dim=None, col_dim=None, plot_labels=None, hist_threshold=None, moving_avg=None,
               vmin=None, vmax=None, tight=False, ofile=None, dpi='figure', **plot_kw):
    """
    Plots boxplots of input data, grouping by scenarios.
    Input percentiles (min, p05, med, p95, max) are expected to be
    already pre-computed and ready to be plotted.

    Parameters
    ----------
    da : DataArray
        The array containing the data to be plotted.

    show : bool (optional, default True)
        Whether to show the plot on the display or not.

    close : bool (optional, default True)
        Whether to close the Matplotlib call or not before exiting.

    xdim : str (default 'time')
        The name of the dimension for the horizontal axis of the plot.

    perc_dim : str (default 'model')
        The name of the dimension where the percentiles of the data
        are found.

    row_dim : str (optional)
        The dimension where to lay out the rows in the facet plot
        ('row' argument in the Matplotlib call).

    col_dim : str (optional)
        The dimension where to lay out the columns in the facet plot
        ('col' argument in the Matplotlib call).

    plot_labels : list of str
        The custom labels for each subplot in the facet
        (otherwise automatically crafted by matplotlib)

    hist_threshold : str or numeric (optional)
        Value along the xdim which separates historical data (rendered in grey)
        from future projections.

    moving_avg : int (optional)
       Number of time-steps setting the width for a smoothing moving
       average over the data before plotting.

    vmin, vmax : numeric (optional)
        Limit values for the Y axis.

    tight : bool (optional, default False)
        Whether to force a tight layout in the plot.

    ofile : str or Path (optional, default None)
        The path to the file where to store the plot.

    dpi : float or 'figure'
        DPI argument for the plt.savefig() function to control resolution of image file.
        To be used in conjuntion with "ofile" to trigger storage of plot to file.

    **plot_kw
        Additional arguments that are passed to the plotting functions.

    Examples
    ========
    >>> plot_trend( da, col_dim='scenario', ...)
    >>> plot_trend( da, col_dim='scenario', ...)

    Returns
    -------
    The plot object.
    """
    # - - - - - - - - - -
    if da is None:
        return None

    if da.ndim == 1:
        raise ValueError("Input data array shall be at least 2-dimensional.")

    for dim in row_dim, col_dim, xdim, perc_dim, scenario_dim:
        if dim is not None and (not dim in da.dims):
            raise ValueError("'{}' dimension not found in the array: {}".format(dim, da.dims))

    if len(da[perc_dim].values) != 3:
        raise ValueError("Expected 3 ensemble aggregations. Found: {} ({})".format(len(da[perc_dim]), da[perc_dim].values))

    if isinstance(plot_labels, str):
        plot_labels = [plot_labels,]

    if moving_avg is not None and not isinstance(moving_avg, int):
        raise ValueError("Moving average parameter shall be an integer [#time steps].")
    # - - - - - - - - - -

    if hist_threshold is None:
        hist_threshold = da[xdim].values[0]

    # coords
    scenarios   = da[scenario_dim].values
    percentiles = da[perc_dim].values

    # moving average
    if moving_avg is not None:
        da = da.copy(deep=True).dropna(dim=xdim, how="any") # [!] copy not to modify input data
        true_mask = [True,]*da.sizes[xdim]
        for s,p in it.product(scenarios, percentiles):
            slicing = {scenario_dim:s, perc_dim:p}
            # TODO is there a better way?
            np.place(da.sel(slicing).values, true_mask, _moving_avg(da.sel(slicing).values, n=moving_avg))

    # extract arrays of data (split hist/projection for separate rendering)
    xcoords = da[xdim].values
    hist_values = {
           (s,m):da.sel(scenario=s, model=m).where(da[xdim] <= hist_threshold)
           for s in scenarios
           for m in percentiles }
    proj_values = {
           (s,m):da.sel(scenario=s, model=m).where(da[xdim] >= hist_threshold)
           for s in scenarios
           for m in percentiles }

    # 5-50-95 percentiles bands
    fig, axs = plt.subplots(ncols=1, **plot_kw) # allow multiple subplots for different indices?
    axs = [axs,] # FIXME just one plot for now, remove this for faceted plots
    lns = list()
    # TODO assumes 2 scenarios, make more flexible code here
    # TODO multiple indices faceted together
    for i,ax in enumerate(axs):
        # lines
        _ =         ax.plot(xcoords, hist_values[(scenarios[0],percentiles[1])], '-', color='grey',   linewidth=1)
        lns.append( ax.plot(xcoords, hist_values[(scenarios[1],percentiles[1])], '-', color='grey',   linewidth=1)[0] )
        lns.append( ax.plot(xcoords, proj_values[(scenarios[0],percentiles[1])], '-', color='orange', linewidth=1)[0] )
        lns.append( ax.plot(xcoords, proj_values[(scenarios[1],percentiles[1])], '-', color='red',    linewidth=1)[0] )
        # filled confidence
        ax.fill_between(xcoords, da.sel(scenario=scenarios[0], model=percentiles[0]),
                                 da.sel(scenario=scenarios[0], model=percentiles[2]),
                        where=xcoords<=hist_threshold, color='grey', alpha=0.2)
        ax.fill_between(xcoords, da.sel(scenario=scenarios[0], model=percentiles[0]),
                                 da.sel(scenario=scenarios[0], model=percentiles[2]),
                        where=xcoords>=hist_threshold, color='gold', alpha=0.3)
        ax.fill_between(xcoords, da.sel(scenario=scenarios[1], model=percentiles[0]),
                                 da.sel(scenario=scenarios[1], model=percentiles[2]),
                        where=xcoords<=hist_threshold, color='grey', alpha=0.2)
        ax.fill_between(xcoords, da.sel(scenario=scenarios[1], model=percentiles[0]),
                                 da.sel(scenario=scenarios[1], model=percentiles[2]),
                        where=xcoords>=hist_threshold, color='red', alpha=0.2)
        # misc
        ax.set_title(plot_labels[i])
        ax.set_xlim(min(xcoords), max(xcoords))
        ax.set_ylim(vmin, vmax)
        ax.minorticks_on()
        ax.grid(visible=True, which='major', axis='both', linewidth=.5)
        ax.grid(visible=True, which='minor', axis='both', linewidth=.2)

    # for legend:
    bgs = list()
    bgs.append( ax.fill(np.NaN, np.NaN, 'grey', alpha=0.2)[0] )
    bgs.append( ax.fill(np.NaN, np.NaN, 'gold', alpha=0.3)[0] )
    bgs.append( ax.fill(np.NaN, np.NaN, 'red',  alpha=0.2)[0] )

    # LEGEND
    ax.legend(handles=list(zip(bgs, lns)),
                  labels=["Historical", *scenarios],
                  loc='center left', bbox_to_anchor=(1, .5),
                  ncol=1, fancybox=True, shadow=True)

    if tight:
        plt.tight_layout()
    if ofile is not None:
        plt.savefig( ofile, bbox_inches='tight', dpi=dpi )
    if show:
        plt.show()
    if close:
        plt.close()

    return plt


#------------------------------------------------------------------------------
#
def plot_boxplots(da, show=True, close=True, xdim=TIME_DIM, perc_dim=MODELS_DIM, scenario_dim=SCENARIO_DIM,
                  index_dim=None, plot_labels=None, ax_labels=None, vmin=None, vmax=None,
                  col_wrap=None, tight=False, aspect='auto', ofile=None, dpi='figure', **plot_kw):
    """
    Plots 1+ 2D time projections an input data array.
    If the input data is 2+D, then row_dim/col_dim shall be used to
    specify along which dimensions should subdatasets be extracted.

    Parameters
    ----------
    da : DataArray
        The array containing the data to be plotted.

    show : bool (optional, default True)
        Whether to show the plot on the display or not.

    close : bool (optional, default True)
        Whether to close the Matplotlib call or not before exiting.

    xdim : str (default 'time')
        The name of the dimension for the horizontal axis of the plot.

    perc_dim : str (default 'model')
        The name of the dimension where the 5/50/95th percentiles of the data
        are found.

    index_dim : str (optional)
        The dimension that discriminates the subplots in the facet
        (1 subplot = 1 climate index).

    hist_threshold : str or numeric (optional)
        Value along the xdim which separates historical data (rendered in grey)
        from future projections.

    plot_labels : list of str
        The custom labels for each subplot in the facet
        (otherwise automatically crafted by matplotlib)

    ax_labels : list of str
        X and X labels to be applied to each subfigure.

    ncols : int
        Number of columns for faceted plots.

    vmin, vmax : numeric (optional)
        Limit values for the Y axis.

    col_wrap : bool
        Number of columns in faceted plots.

    tight : bool (optional, default False)
        Whether to force a tight layout in the plot.

    ofile : str or Path (optional, default None)
        The path to the file where to store the plot.

    dpi : float or 'figure'
        DPI argument for the plt.savefig() function to control resolution of image file.
        To be used in conjuntion with "ofile" to trigger storage of plot to file.

    **plot_kw
        Additional arguments that are passed to the plotting functions.

    Examples
    ========
    >>> plot_trend( da, col_dim='scenario', col_wrap=2)
    >>> plot_trend( da, contour=True, col_dim='scenario', col_wrap=2)

    Returns
    -------
    The plot object.
    """
    # - - - - - - - - - -
    if da is None:
        return None

    if da.ndim == 1:
        raise ValueError("Input data array shall be at least 2-dimensional.")

    for dim in index_dim, xdim, perc_dim, scenario_dim:
        if dim is not None and (not dim in da.dims):
            raise ValueError("'{}' dimension not found in the array: {}".format(dim, da.dims))

    if len(da[perc_dim].values) != 5:
        raise ValueError("Expected 5 ensemble aggregations. Found: {} ({})".format(len(da[perc_dim]), da[perc_dim].values))

    if len(da[scenario_dim].values) != 2:
        raise ValueError("3+ scenarios boxplots grouping still not implemented. Found: {} ".format(da[scenario_dim].values))

    if isinstance(plot_labels, str):
        plot_labels = [plot_labels,]

    if ax_labels is None:
        ax_labels = [None,]*2
    elif isinstance(ax_labels, str) or len(ax_labels) != 2:
        raise ValueError("'ax_labels' argument shall be a 2-elements array (x and y labels). Found: {}".format(ax_labels))
    # - - - - - - - - - -

    # extract arrays of data (split hist/projection for separate rendering)
    indices     = da[index_dim].values if index_dim else [0,]
    scenarios   = da[scenario_dim].values
    percentiles = da[perc_dim].values
    xcoords     = da[xdim].values

    # manually group/pair the boxplots
    xlocations  = range(len(xcoords))
    width       = .3
    #symbol      = 'r+'
    colors  = dict() #TODO dynamic positioning and width for 3+ scenarios groups
    colors[scenarios[0]] = 'gold' # TODO let user choose the colors
    colors[scenarios[1]] = 'sandybrown' #

    # offset the positions per group:
    positions = dict() # TODO dynamic positioning and width for 3+ scenarios groups
    positions[scenarios[0]] = [x-(width/2) for x in xlocations]
    positions[scenarios[1]] = [x+(width/2) for x in xlocations]

    # plot defaults
    bxpstats_defaults = { 'fliers':[] }
    bxp_defaults = {
        'vert':True, 
        'manage_ticks':False, 
        'widths':width,
        'patch_artist':True,
        'showfliers':False,
        'medianprops': dict(color="k", linewidth=2, alpha=0.7)
    }

    n_plots  = len(indices)
    col_wrap = min(col_wrap, n_plots) if col_wrap else 1
    nrows    = math.ceil(n_plots / col_wrap)
    #print(n_plots, ':', nrows, 'x', col_wrap)

    fig, axs = plt.subplots(nrows=nrows, ncols=col_wrap, **plot_kw)
    if n_plots == 1:
        axs = [axs,] 
    boxes = list()
    # TODO assumes 2 scenarios, make more flexible code here
    for i,ax in enumerate(axs):
        # reshape data for Axes.bxs:
        for s in scenarios:
            slicing = {scenario_dim:s }
            if index_dim is not None:
                slicing.update({index_dim:indices[i]})
            bxpstats = [ {
                'label' : f'{x}/{s}',
                'whislo': da.sel({**slicing, xdim:x}).values[0],
                'q1'    : da.sel({**slicing, xdim:x}).values[1],
                'med'   : da.sel({**slicing, xdim:x}).values[2],
                'q3'    : da.sel({**slicing, xdim:x}).values[3],
                'whishi': da.sel({**slicing, xdim:x}).values[4],
                **bxpstats_defaults
            } for x in xcoords ]
            #
            box = ax.bxp(bxpstats, positions=positions[s], **bxp_defaults)
            boxes.append(box['boxes'][0])
            for patch in box['boxes']:
                patch.set_facecolor(colors[s])
        # global plot params:
        ax.set_title(plot_labels[i])
        ax.set_ylim(vmin, vmax)
        ax.minorticks_on()
        ax.yaxis.grid(True, linewidth=1, linestyle='dotted')
        ax.set_axisbelow(True)
        ax.set_xticks(xlocations)
        ax.set_xticklabels( xcoords, rotation=0 )
        ax.set_aspect( aspect )
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
     
    # LEGEND
    fig.legend(handles=boxes, labels=list(scenarios),
              loc='lower center', bbox_to_anchor=(.5, -.05),
              ncol=len(scenarios),
              fancybox=True, shadow=True)

    if tight:
        plt.tight_layout()
    if ofile is not None:
        plt.savefig( ofile, bbox_inches='tight', dpi=dpi )
    if show:
        plt.show()
    if close:
        plt.close()

    return plt



#------------------------------------------------------------------------------
#
def _moving_avg(a, n):
    """Computes the moving average of size n over a given input array (NAs are ignored)."""
    # prepend/append half-window to have output same size of input
    #a = [*a[:int(n/2)], *a, *a[-(int(n/2)+(n%2)):]] #pre/ap-pend half window
    #a = [*a[:(n - 1)], *a]                  # prepend first (n-1) elements
    #a = [*[a[0],]*(n-1), *a]                # prepend first element (n-1) times
    a = [*[np.mean(a[:(n - 1)]),]*(n-1), *a] # prepend mean of first (n-1)
    # moving window
    #ret = np.nancumsum(a)
    ret = np.cumsum(a)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


