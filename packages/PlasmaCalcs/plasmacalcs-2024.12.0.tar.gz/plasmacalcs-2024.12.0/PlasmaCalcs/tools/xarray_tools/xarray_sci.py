"""
File Purpose: high-level xarray functions. May be especially useful for science.
E.g., gaussian filter, polynomial fit.
"""

import numpy as np
import xarray as xr

from ..imports import ImportFailed
try:
    import scipy.ndimage as scipy_ndimage
except ImportError as err:
    scipy_ndimage = ImportFailed('scipy.ndimage',
            'This module is required for some filtering functions.', err=err)


from .xarray_accessors import pcAccessor, pcArrayAccessor, pcDatasetAccessor
from .xarray_dimensions import (
    xarray_promote_dim, xarray_ensure_dims, _paramdocs_ensure_dims,
    xarray_coarsened,
)
from .xarray_indexing import xarray_isel
from ..os_tools import next_unique_name
from ..pytools import format_docstring
from ..sentinels import UNSET
from ...errors import (
    DimensionalityError, DimensionValueError, DimensionKeyError,
    InputConflictError, InputMissingError,
)
from ...defaults import DEFAULTS


''' --------------------- Mapping --------------------- '''

@pcAccessor.register('map')
@format_docstring(**_paramdocs_ensure_dims)
def xarray_map(array, f, *args_f, axis=None, axes=None,
                     promote_dims_if_needed=True, missing_dims='raise', **kw_f):
    '''func(array, *args_f, **kw_f), but axis/axes can be provided as strings!

    Mainly useful if trying to apply f which expects unlabeled array & int axes inputs.
    E.g. numpy.mean can use axis kwarg as iterable of ints,
        but here can provide axis as a dim name str or list of dim names.
    Probably not super useful for mean, since xarray provides xr.mean,
        but may be useful for other functions e.g. scipy.ndimage.gaussian_filter,
        which might not have an existing equivalent in xarray.

    array: xarray.DataArray or Dataset
        apply f to this array, or each array in this Dataset
    f: callable
        will be called as f(array, *args_f, **kw_f),
        possibly will also be passed a value for axis or axes, if provided here
    axis, axes: None, str, or iterable of strs
        if provided, convert to axes positions in dataarray, and pass to f as int(s).
        Also promotes these coords to dims if necessary.
    promote_dims_if_needed: {promote_dims_if_needed}
    missing_dims: {missing_dims}
    '''
    # if Dataset, just apply this to each array.
    if isinstance(array, xr.Dataset):
        ds = array
        result = ds.copy()
        for name, arr in ds.data_vars.items():
            result[name] = xarray_map(arr, f, *args_f, axis=axis, axes=axes,
                                      promote_dims_if_needed=promote_dims_if_needed,
                                      missing_dims=missing_dims, **kw_f)
        return result
    # bookkeeping on 'axis' & 'axes' inputs:
    if axis is None and axes is None:  # simplest case; will just apply f to entire array.
        coords = None
        kw_ax = dict()
    elif axis is not None:  # and axes is None
        coords = axis
        ax_key = 'axis'
    elif axes is not None:  # and axis is None
        coords = axes
        ax_key = 'axes'
    else:  # both axis and axes were provided
        raise InputConflictError('cannot provide both "axis" and "axes".')
    if coords is not None:
        if isinstance(coords, str):
            coords = [coords]
        # ensure the coords exist:
        array, existing_dims = xarray_ensure_dims(array, coords,
                                                  promote_dims_if_needed=promote_dims_if_needed,
                                                  missing_dims=missing_dims, return_existing_dims=True)
        # convert coords to ax nums:
        ax_nums = array.get_axis_num(existing_dims)
        kw_ax = {ax_key: ax_nums}
    # call f but use xarray.Dataset.map functionality to preserve coords/attrs/etc.
    array_name = array.name
    _data_var_name = next_unique_name('_internal_variable', [*array.coords, *array.dims])
    ds = array.to_dataset(name=_data_var_name)
    ds_result = ds.map(f, args=args_f, **kw_f, **kw_ax)
    result = ds_result[_data_var_name]
    result.name = array_name
    return result


''' --------------------- Gaussian Filter --------------------- '''

@pcAccessor.register('gaussian_filter', aliases=['blur'])
@format_docstring(**_paramdocs_ensure_dims, default_sigma=DEFAULTS.GAUSSIAN_FILTER_SIGMA)
def xarray_gaussian_filter(array, dim=None, sigma=None, *,
                           promote_dims_if_needed=True, missing_dims='raise',
                           **kw_scipy_gaussian_filter):
    '''returns array after applying scipy.ndimage.gaussian_filter to it.

    array: xarray.DataArray or Dataset
        filters this array, or each data_var in a dataset.
    dim: None or str or iterable of strs
        dimensions to filter along.
        if None, filter along all dims.
    sigma: None, number, or iterable of numbers
        standard deviation for Gaussian kernel.
        if iterable, must have same length as dim.
        if None, will use DEFAULTS.GAUSSIAN_FILTER_SIGMA (default: {default_sigma}).
    promote_dims_if_needed: {promote_dims_if_needed}
    missing_dims: {missing_dims}

    additional kwargs go to scipy.ndimage.gaussian_filter.
    '''
    if sigma is None:
        sigma = DEFAULTS.GAUSSIAN_FILTER_SIGMA
    return xarray_map(array, scipy_ndimage.gaussian_filter, sigma, axes=dim,
                      promote_dims_if_needed=promote_dims_if_needed,
                      missing_dims=missing_dims, **kw_scipy_gaussian_filter)


''' --------------------- polyfit --------------------- '''

@pcAccessor.register('polyfit')
@format_docstring(xr_polyfit_docs=xr.DataArray.polyfit.__doc__)
def xarray_polyfit(array, coord, degree, *, stddev=False, full=False, cov=False, **kw_polyfit):
    '''returns array.polyfit(coord, degree, **kw_polyfit), after swapping coord to be a dimension, if needed.
    E.g. for an array with dimension 'snap' and associated non-dimension coordinate 't',
        xarray_polyfit(array, 't', 1) is equivalent to array.swap_dims(dict(snap='t')).polyfit('t', 1).

    stddev: bool
        whether to also return the standard deviations of each coefficient in the fit.
        if True, assign the variable 'polyfit_stddev' = diagonal(polyfit_covariance)**0.5,
            mapping the diagonal (across 'cov_i', 'cov_j') to the dimension 'degree'.
            if cov False when stddev True, do not keep_cov in the result.
        Not compatible with full=True.
    full: bool
        passed into polyfit; see below.
    cov: bool
        passed into polyfit; see below.
        Note: if stddev=True when cov=False, still use cov=True during array.polyfit,
            however then remove polyfit_covariance & polyfit_residuals from result.

    Docs for xr.DataArray.polyfit copied below:
    -------------------------------------------
    {xr_polyfit_docs}
    '''
    array = xarray_promote_dim(array, coord)
    if stddev and full:
        raise InputConflictError('stddev=True incompatible with full=True.')
    cov_input = cov
    if stddev:
        cov = True
    result = array.polyfit(coord, degree, full=full, cov=cov, **kw_polyfit)
    if stddev:
        result = xarray_assign_polyfit_stddev(result, keep_cov=cov_input)
    return result

@pcDatasetAccessor.register
def xarray_assign_polyfit_stddev(dataset, *, keep_cov=True):
    '''assign polyfit stddev to dataset['polyfit_stddev'], treating dataset like a result of polyfit.
    These provide some measure of "goodness of fit"; smaller stddev means better fit.

    Specifically, stddev[k] = (covariance matrix)[k,k]**0.5 for k in range(len(dataset['degree']));
        one might quote +-stddev[k] as the error bar for the coefficient at degree=dataset['degree'][k].

    dataset: xarray.Dataset
        dataset to use for calculating polyfit_stderr and in which to assign the result.
        must contain variable 'polyfit_covariance' and dimension 'degree'.
    keep_cov: bool
        whether to keep the 'polyfit_covariance' and 'polyfit_residuals' vars in the result.

    The original dataset will not be altered; a new dataset will be returned.
    '''
    cov = dataset['polyfit_covariance']
    degree = dataset['degree']
    ndeg = len(degree)
    stddev = [cov.isel(cov_i=k, cov_j=k)**0.5 for k in range(ndeg)]
    stddev = xr.concat(stddev, 'degree').assign_coords({'degree': degree})
    result = dataset.assign(polyfit_stddev=stddev)
    if not keep_cov:
        result = result.drop_vars(['polyfit_covariance', 'polyfit_residuals'])
    return result

@pcAccessor.register('coarsened_polyfit')
@format_docstring(xr_polyfit_docs=xr.DataArray.polyfit.__doc__)
def xarray_coarsened_polyfit(array, coord, degree, window_len, *,
                             dim_coarse='window', keep_coord='middle',
                             assign_coarse_coords=True,
                             boundary=UNSET, side=UNSET,
                             stride=UNSET, fill_value=UNSET, keep_attrs=UNSET,
                             **kw_polyfit
                             ):
    '''returns result of coarsening array, then polyfitting along the fine dimension, in each window.
    E.g., make windows of length 10 along 't', then polyfit each window along 't',
    then concat the results from each window, along dim_coarse (default: 'window').

    coord: str
        coordinate to polyfit along.
    degree: int
        degree of polynomial to fit.
    window_len: int or None
        length of window to coarsen over.
        None --> polyfit without coarsening; equivalent to window_len = len(array.coords[coord])
    dim_coarse: str, default 'window'
        name of coarse dimension; the i'th value here corresponds to the i'th window.
    keep_coord: False or str in ('left', 'right', 'middle')
        along the dim_coarse dimension, also provide some of the original coord values.
        'left' --> provide the left-most value in each window.
        'middle' --> provide the middle value in each window.
        'right' --> provide the right-most value in each window.
        False --> don't provide any of the original coord values.
        if not False, result will swap dims such that coord is a dimension instead of dim_coarse.
    assign_coarse_coords: bool or coords
        coords to assign along the dim_coarse dimension.
        True --> use np.arange.
        False --> don't assign coords.
    boundary, side: UNSET or value
        if provided (not UNSET), pass this value to coarsen().
    stride, fill_value, keep_attrs: UNSET or value
        if provided (not UNSET), pass this value to construct().

    additional **kw are passed to polyfit.

    Docs for xr.DataArray.polyfit copied below:
    -------------------------------------------
    {xr_polyfit_docs}
    '''
    # bookkeeping
    if keep_coord not in ('left', 'middle', 'right', False):
        raise InputError(f'invalid keep_coord={keep_coord!r}; expected "left", "middle", "right", or False.')
    # if window_len is None or <1, don't coarsen at all.
    if window_len is None:
        return xarray_polyfit(array, coord, degree, **kw_polyfit)
    # coarsen
    coarsened = xarray_coarsened(array, coord, window_len,
                                dim_coarse=dim_coarse,
                                assign_coarse_coords=assign_coarse_coords,
                                boundary=boundary, side=side,
                                stride=stride, fill_value=fill_value, keep_attrs=keep_attrs)
    # bookkeeping
    n_windows = len(coarsened[dim_coarse])
    if n_windows < 1:
        errmsg = f'coarsened array has n_windows={n_windows} < 1; cannot polyfit.'
        raise DimensionValueError(errmsg)
    # polyfitting
    promoted = []
    for i_window in range(n_windows):
        prom = xarray_promote_dim(coarsened.isel({dim_coarse: i_window}), coord)
        promoted.append(prom)
    polyfits = []
    for arr in promoted:
        pfit = xarray_polyfit(arr, coord, degree, **kw_polyfit)
        polyfits.append(pfit)
    if keep_coord:
        results = []
        for i_window, (arr, prom) in enumerate(zip(polyfits, promoted)):  # i_window just for debugging
            i_keep = {'left': 0, 'middle': 0.5, 'right': -1}[keep_coord]
            # isel from coords[coord] instead of prom, to ensure associated coords are included too,
            #   e.g. t & snap are associated --> this will keep t & snap in the result.
            # if i_keep = 0.5, it is handled by xarray_isel fractional indexing.
            keep = xarray_isel(prom.coords[coord], {coord: i_keep})
            here = arr.assign_coords({coord: keep})
            results.append(here)
    else:
        results = polyfits
    result = xr.concat(results, dim_coarse)
    if keep_coord:
        result = xarray_promote_dim(result, coord)
    return result

