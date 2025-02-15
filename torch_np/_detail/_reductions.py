""" Implementation of reduction operations, to be wrapped into arrays, dtypes etc
in the 'public' layer.

Anything here only deals with torch objects, e.g. "dtype" is a torch.dtype instance etc
"""

import torch

from . import _dtypes_impl, _util

NoValue = None


def _atleast_float(dtype, other_dtype):
    """Return a dtype that is real or complex floating-point.

    For inputs that are boolean or integer dtypes, this returns the default
    float dtype; inputs that are complex get converted to the default complex
    dtype; real floating-point dtypes (`float*`) get passed through unchanged
    """
    if dtype is None:
        dtype = other_dtype
    if not (dtype.is_floating_point or dtype.is_complex):
        return _dtypes_impl.default_float_dtype
    return dtype


def count_nonzero(a, axis=None):
    # XXX: this all should probably be generalized to a sum(a != 0, dtype=bool)
    try:
        return a.count_nonzero(axis)
    except RuntimeError:
        raise ValueError
    return tensor


def argmax(tensor, axis=None):
    axis = _util.allow_only_single_axis(axis)

    if tensor.dtype == torch.bool:
        # RuntimeError: "argmax_cpu" not implemented for 'Bool'
        tensor = tensor.to(torch.uint8)

    tensor = torch.argmax(tensor, axis)
    return tensor


def argmin(tensor, axis=None):
    axis = _util.allow_only_single_axis(axis)

    if tensor.dtype == torch.bool:
        # RuntimeError: "argmin_cpu" not implemented for 'Bool'
        tensor = tensor.to(torch.uint8)

    tensor = torch.argmin(tensor, axis)
    return tensor


def any(tensor, axis=None, *, where=NoValue):
    if where is not NoValue:
        raise NotImplementedError

    axis = _util.allow_only_single_axis(axis)

    if axis is None:
        result = tensor.any()
    else:
        result = tensor.any(axis)
    return result


def all(tensor, axis=None, *, where=NoValue):
    if where is not NoValue:
        raise NotImplementedError

    axis = _util.allow_only_single_axis(axis)

    if axis is None:
        result = tensor.all()
    else:
        result = tensor.all(axis)
    return result


def max(tensor, axis=None, initial=NoValue, where=NoValue):
    if initial is not NoValue or where is not NoValue:
        raise NotImplementedError

    result = tensor.amax(axis)
    return result


def min(tensor, axis=None, initial=NoValue, where=NoValue):
    if initial is not NoValue or where is not NoValue:
        raise NotImplementedError

    result = tensor.amin(axis)
    return result


def ptp(tensor, axis=None):
    result = tensor.amax(axis) - tensor.amin(axis)
    return result


def sum(tensor, axis=None, dtype=None, initial=NoValue, where=NoValue):
    if initial is not NoValue or where is not NoValue:
        raise NotImplementedError

    assert dtype is None or isinstance(dtype, torch.dtype)

    if dtype == torch.bool:
        dtype = _dtypes_impl.default_int_dtype

    if axis is None:
        result = tensor.sum(dtype=dtype)
    else:
        result = tensor.sum(dtype=dtype, dim=axis)

    return result


def prod(tensor, axis=None, dtype=None, initial=NoValue, where=NoValue):
    if initial is not NoValue or where is not NoValue:
        raise NotImplementedError

    axis = _util.allow_only_single_axis(axis)

    if dtype == torch.bool:
        dtype = _dtypes_impl.default_int_dtype

    if axis is None:
        result = tensor.prod(dtype=dtype)
    else:
        result = tensor.prod(dtype=dtype, dim=axis)

    return result


def mean(tensor, axis=None, dtype=None, *, where=NoValue):
    if where is not NoValue:
        raise NotImplementedError

    dtype = _atleast_float(dtype, tensor.dtype)

    is_half = dtype == torch.float16
    if is_half:
        # XXX revisit when the pytorch version has pytorch/pytorch#95166
        dtype = torch.float32

    if axis is None:
        result = tensor.mean(dtype=dtype)
    else:
        result = tensor.mean(dtype=dtype, dim=axis)

    if is_half:
        result = result.to(torch.float16)

    return result


def std(tensor, axis=None, dtype=None, ddof=0, *, where=NoValue):
    if where is not NoValue:
        raise NotImplementedError

    dtype = _atleast_float(dtype, tensor.dtype)
    tensor = _util.cast_if_needed(tensor, dtype)
    result = tensor.std(dim=axis, correction=ddof)

    return result


def var(tensor, axis=None, dtype=None, ddof=0, *, where=NoValue):
    if where is not NoValue:
        raise NotImplementedError

    dtype = _atleast_float(dtype, tensor.dtype)
    tensor = _util.cast_if_needed(tensor, dtype)
    result = tensor.var(dim=axis, correction=ddof)

    return result


# cumsum / cumprod are almost reductions:
#   1. no keepdims
#   2. axis=None ravels (cf concatenate)


def cumprod(tensor, axis, dtype=None):
    if dtype == torch.bool:
        dtype = _dtypes_impl.default_int_dtype
    if dtype is None:
        dtype = tensor.dtype

    result = tensor.cumprod(axis=axis, dtype=dtype)

    return result


def cumsum(tensor, axis, dtype=None):
    if dtype == torch.bool:
        dtype = _dtypes_impl.default_int_dtype
    if dtype is None:
        dtype = tensor.dtype

    result = tensor.cumsum(axis=axis, dtype=dtype)

    return result


def average(a_tensor, axis, w_tensor):

    # dtype
    # FIXME: 1. use result_type
    #        2. actually implement multiply w/dtype
    if not a_tensor.dtype.is_floating_point:
        result_dtype = torch.float64
        a_tensor = a_tensor.to(result_dtype)

    result_dtype = _dtypes_impl.result_type_impl([a_tensor.dtype, w_tensor.dtype])

    a_tensor = _util.cast_if_needed(a_tensor, result_dtype)
    w_tensor = _util.cast_if_needed(w_tensor, result_dtype)

    # axis
    if axis is None:
        (a_tensor, w_tensor), axis = _util.axis_none_ravel(
            a_tensor, w_tensor, axis=axis
        )

    # axis & weights
    if a_tensor.shape != w_tensor.shape:
        if axis is None:
            raise TypeError(
                "Axis must be specified when shapes of a and weights " "differ."
            )
        if w_tensor.ndim != 1:
            raise TypeError("1D weights expected when shapes of a and weights differ.")
        if w_tensor.shape[0] != a_tensor.shape[axis]:
            raise ValueError("Length of weights not compatible with specified axis.")

        # setup weight to broadcast along axis
        w_tensor = torch.broadcast_to(
            w_tensor, (a_tensor.ndim - 1) * (1,) + w_tensor.shape
        )
        w_tensor = w_tensor.swapaxes(-1, axis)

    # do the work
    numerator = torch.mul(a_tensor, w_tensor).sum(axis)
    denominator = w_tensor.sum(axis)
    result = numerator / denominator

    return result, denominator


def quantile(a_tensor, q_tensor, axis, method):

    if (0 > q_tensor).any() or (q_tensor > 1).any():
        raise ValueError("Quantiles must be in range [0, 1], got %s" % q_tensor)

    if not a_tensor.dtype.is_floating_point:
        dtype = _dtypes_impl.default_float_dtype
        a_tensor = a_tensor.to(dtype)

    # edge case: torch.quantile only supports float32 and float64
    if a_tensor.dtype == torch.float16:
        a_tensor = a_tensor.to(torch.float32)

    # axis
    if axis is not None:
        axis = _util.normalize_axis_tuple(axis, a_tensor.ndim)
    axis = _util.allow_only_single_axis(axis)

    q_tensor = _util.cast_if_needed(q_tensor, a_tensor.dtype)

    (a_tensor, q_tensor), axis = _util.axis_none_ravel(a_tensor, q_tensor, axis=axis)

    result = torch.quantile(a_tensor, q_tensor, axis=axis, interpolation=method)

    return result
