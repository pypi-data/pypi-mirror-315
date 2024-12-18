"""
File Purpose: indexing xarrays
"""
import numpy as np
import xarray as xr

from .xarray_accessors import pcAccessor, pcArrayAccessor, pcDatasetAccessor
from .xarray_dimensions import (
    is_iterable_dim,
    xarray_ensure_dims, _paramdocs_ensure_dims,
)
from .xarray_misc import xarray_copy_kw
from ..arrays import interprets_fractional_indexing
from ..pytools import format_docstring
from ..sentinels import UNSET
from ...errors import DimensionValueError


''' --------------------- Indexing --------------------- '''

_isel_doc = xr.DataArray.isel.__doc__
if 'Examples\n' in _isel_doc:  # gives docstring with Examples removed
    _isel_doc = _isel_doc[:_isel_doc.index('Examples\n')].rstrip()
if 'Returns\n' in _isel_doc:  # gives docstring with Returns removed
    _isel_doc = _isel_doc[:_isel_doc.index('Returns\n')].rstrip()

@pcAccessor.register('isel')
@format_docstring(isel_doc=_isel_doc, fractional_indexing_doc=interprets_fractional_indexing.__doc__,
                  **_paramdocs_ensure_dims, sub_ntab=1)
def xarray_isel(array, indexers=None, *, promote_dims_if_needed=True,
                drop=False, missing_dims='raise', rounding='round', **indexers_as_kwargs):
    '''array.isel(...) which can also interpret fractional indexes between -1 and 1, and promotes non-dim coords.

    behaves just like xarray.DataArray.isel, but:
        - indexers also allow fractional indexes.
        - if any dim with index provided refers to a non-dimension coordinate, first promote it via swap_dims.
    In particular, for {{cname: index}}:
        - fractional indexes:
            if index is a slice, int, or iterable of ints, use it as is.
            if index contains any values between -1 and 1 (excluding -1, 0, and 1):
                treat that value as a fraction of L=len(array[cname]).
                E.g. 0.25 --> int(L * 0.25);
                    -0.1  --> -int(L * 0.1).
                This is equivalent to interprets_fractional_indexing(index, L)
        - non-dimension coordinates:
            if cname is a non-dimension coordinate, use xarray_promote_dim(array, cname).

    promote_dims_if_needed: {promote_dims_if_needed}
    drop, missing_dims: passed to array.isel; see below for details.
    rounding: passed to interprets_fractional_indexing; see below for details.

    xarray.DataArray.isel docs copied below:
    ----------------------------------------
        {isel_doc}

    interprets_fractional_indexing docs copied below:
    -------------------------------------------------
        {fractional_indexing_doc}
    '''
    if indexers is None:
        indexers = indexers_as_kwargs
    else:
        indexers = {**indexers, **indexers_as_kwargs}
    indexers_input = indexers
    array_input = array  # <-- helps with debugging in case of crash.
    # interpret fractional indexes, and promote coords to dims as necessary.
    indexers = dict()  # <-- not overwriting the originally-input value, this is a new dict.

    kw_ensure_dims = dict(promote_dims_if_needed=promote_dims_if_needed, missing_dims=missing_dims,
                          assert_1d=True,  # because here doesn't implement any way to index 2D+ dims.
                          return_existing_dims=True,  # so we can avoid indexing any missing dims!
                          )
    array, existing_dims = xarray_ensure_dims(array, list(indexers_input.keys()), **kw_ensure_dims)
    for cname in existing_dims:
        index = indexers_input[cname]
        coord = array.coords[cname]
        indexers[cname] = interprets_fractional_indexing(index, L=len(coord), rounding=rounding)
    # call isel
    return array.isel(indexers, drop=drop, missing_dims=missing_dims)

@pcAccessor.register('search')
def xarray_search(array, dim, value):
    '''return first index of value along dim
    (or coord. returns 0, not crash, if scalar coord which matches value.)
    Not efficient for large dims. For large sorted dims, see xarray.DataArray.searchsorted.

    crash with DimensionValueError if value not found in dim.
    '''
    for i, val in enumerate(np.atleast_1d(array.coords[dim].values)):
        if val == value:
            return i
    raise DimensionValueError(f'value={value!r} not found in array[{dim!r}]')

_sel_doc = xr.DataArray.sel.__doc__
if 'Examples\n' in _sel_doc:  # gives docstring with Examples removed
    _sel_doc = _sel_doc[:_sel_doc.index('Examples\n')].rstrip()
if 'Returns\n' in _sel_doc:  # gives docstring with Returns removed
    _sel_doc = _sel_doc[:_sel_doc.index('Returns\n')].rstrip()

@pcAccessor.register('sel')
@format_docstring(sel_doc=_sel_doc, **_paramdocs_ensure_dims)
def xarray_sel(array, indexers=None, *, promote_dims_if_needed=True,
               method=None, tolerance=None, drop=False, **indexers_as_kwargs):
    '''array.sel(...) but prioritize general applicability over efficiency:
        - promote non-dimension coordinate dims first if applicable
        - (if coord.dtype is object) check coord equality,
            e.g. 0==Fluid('e', 0)=='e', so could use Fluid('e', 0), 'e', or 0 in sel.
            - can also use list, tuple, or 1D non-string iterable,
                e.g. ['e', 3, 'Fe+'] to get multiple fluids.
            - can also use slice,
                e.g. slice('e', 'Fe+', 2) to get every other fluid,
                starting from 'e', stopping before the first 'Fe+' match.

    Assumes all indexing is for 1D dims. For indexing 2D+ dims, use xarray methods directly.

    promote_dims_if_needed: {promote_dims_if_needed}
    method: None or str
        method to use for inexact matches, for non-object dtype coords.

    xarray.DataArray.sel docs copied below:
    ----------------------------------------
        {sel_doc}
    '''
    if indexers is None:
        indexers = indexers_as_kwargs
    else:
        indexers = {**indexers, **indexers_as_kwargs}
    indexers_input = indexers
    sel_indexers = dict()  # indexing to delegate to xarray.sel
    obj_indexers = dict()  # indexing to handle here
    array_input = array  # <-- helps with debugging in case of crash.
    kw_ensure_dims = dict(promote_dims_if_needed=promote_dims_if_needed, missing_dims='raise',
                          assert_1d=True,  # because here doesn't implement any way to index 2D+ dims.
                          return_existing_dims=True,  # so we can avoid indexing any missing dims!
                          )
    array, existing_dims = xarray_ensure_dims(array, list(indexers_input.keys()), **kw_ensure_dims)
    for cname in existing_dims:
        if array[cname].dtype == object:
            obj_indexers[cname] = indexers_input[cname]
        else:
            sel_indexers[cname] = indexers_input[cname]
    # handle obj_indexers first.
    obj_isels = {}
    if len(obj_indexers) > 0:
        if method is not None:
            raise TypeError(f'cannot use method {method!r} with object dtype coords {list(obj_indexers)}.')
        for cname, index in obj_indexers.items():
            if is_iterable_dim(index):
                isel_here = []
                for ival in index:
                    isel_here.append(xarray_search(array, cname, ival))
                obj_isels[cname] = isel_here
            elif isinstance(index, slice):
                start, stop, step = index.start, index.stop, index.step
                istart, istop = None, None
                if start is not None:
                    istart = xarray_search(array, cname, start)
                if stop is not None:
                    istop = xarray_search(array, cname, stop)
                obj_isels[cname] = slice(istart, istop, step)
            else:  # index is a single value for a dim
                obj_isels[cname] = xarray_search(array, cname, index)
    array = array.isel(obj_isels, drop=drop)
    # handle sel_indexers
    return array.sel(sel_indexers, method=method, tolerance=tolerance, drop=drop)



''' --------------------- Custom where --------------------- '''

@pcAccessor.register('where')
def xarray_where(array, cond, other=UNSET, *, drop=False, skip_if_no_matching_dims=True):
    '''like xarray's builtin where, but return array unchanged if it has no dims matching cond.

    array: xarray.DataArray or xarray.Dataset
        array to apply condition to.
    cond: xarray.DataArray, xarray.Dataset, or callable
        Locations at which to preserve array's values. Must have dtype=bool.
        callable --> replace with cond(array).
    other: UNSET, scalar, DataArray, Dataset, or callable, optional
        Value to use for locations in array where cond is False.
        By default, these locations are filled with NA.
        callable --> replace with other(array).
        UNSET --> do not pass this arg to xarray.where()
    drop: bool, default: False
        If True, coordinate labels that only correspond to False values of
        the condition are dropped from the result.
    skip_if_no_matching_dims: bool, default: True
        If True, return array unchanged if it has no dims matching cond.
                if Dataset, keep data_vars unchanged if they have no dims matching cond.
        If False, return array.where(cond, other=other, drop=drop) directly.
    '''
    kw_where = dict(drop=drop) if other is UNSET else dict(other=other, drop=drop)
    if skip_if_no_matching_dims:  # custom processing here
        if callable(cond):
            cond = cond(array)
        if not any(d in array.coords for d in cond.dims):
            return array
        if isinstance(array, xr.Dataset):
            ds = array
            ds0 = ds  # ds before changing ds var.
            # hit data_vars with any dims matching cond, then append remaining vars.
            to_where = []
            to_skip = []
            for var, val in ds.data_vars.items():
                if any(d in val.coords for d in cond.dims):
                    to_where.append(var)
                else:
                    to_skip.append(var)
            if len(to_where) == 0:
                assert False, 'coding error, should have been handled above.'
            ds = ds[to_where].where(cond, **kw_where)
            if len(to_skip) > 0:
                ds = ds.assign(ds0[to_skip])
            return ds
    # else:
    return array.where(cond, **kw_where)
