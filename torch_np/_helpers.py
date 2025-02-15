import torch

from . import _dtypes
from ._detail import _util


def cast_and_broadcast(tensors, out, casting):
    """Cast dtypes of arrays to out.dtype and broadcast if needed.

    Parameters
    ----------
    arrays : sequence of arrays
        Each element is broadcast against `out` and typecast to out.dtype
    out : the "output" array
        Not modified.
    casting : str
        One of numpy casting modes

    Returns
    -------
    tensors : tuple of Tensors
        Each tensor is dtype-cast and broadcast agains `out`, as needed

    Notes
    -----
    The `out` arrays broadcasts and dtype-casts `arrays`, but not vice versa.

    """
    if out is None:
        return tensors
    else:
        from ._ndarray import asarray, ndarray

        if not isinstance(out, ndarray):
            raise TypeError("Return arrays must be of ArrayType")

        tensors = _util.cast_and_broadcast(
            tensors, out.dtype.type.torch_dtype, out.shape, casting
        )

    return tuple(tensors)


# ### Return helpers: wrap a single tensor, a tuple of tensors, out= etc ###


def result_or_out(result_tensor, out_array=None, promote_scalar=False):
    """A helper for returns with out= argument.

    If `promote_scalar is True`, then:
        if result_tensor.numel() == 1 and out is zero-dimensional,
            result_tensor is placed into the out array.
    This weirdness is used e.g. in `np.percentile`
    """
    from ._ndarray import asarray, ndarray

    if out_array is not None:
        if not isinstance(out_array, ndarray):
            raise TypeError("Return arrays must be of ArrayType")
        if result_tensor.shape != out_array.shape:
            can_fit = result_tensor.numel() == 1 and out_array.ndim == 0
            if promote_scalar and can_fit:
                result_tensor = result_tensor.squeeze()
            else:
                raise ValueError(
                    f"Bad size of the out array: out.shape = {out_array.shape}"
                    f" while result.shape = {result_tensor.shape}."
                )
        out_tensor = out_array.get()
        out_tensor.copy_(result_tensor)
        return out_array
    else:
        return asarray(result_tensor)


def array_from(tensor, base=None):
    from ._ndarray import ndarray

    base = base if isinstance(base, ndarray) else None
    return ndarray._from_tensor_and_base(tensor, base)  # XXX: nuke .base


def tuple_arrays_from(result):
    from ._ndarray import asarray

    return tuple(asarray(x) for x in result)


# ### Various ways of converting array-likes to tensors ###


def ndarrays_to_tensors(*inputs):
    """Convert all ndarrays from `inputs` to tensors. (other things are intact)"""
    from ._ndarray import asarray, ndarray

    if len(inputs) == 0:
        return ValueError()
    elif len(inputs) == 1:
        input_ = inputs[0]
        if isinstance(input_, ndarray):
            return input_.get()
        elif isinstance(input_, tuple):
            result = []
            for sub_input in input_:
                sub_result = ndarrays_to_tensors(sub_input)
                result.append(sub_result)
            return tuple(result)
        else:
            return input_
    else:
        assert isinstance(inputs, tuple)  # sanity check
        return ndarrays_to_tensors(inputs)


def to_tensors(*inputs):
    """Convert all array_likes from `inputs` to tensors."""
    from ._ndarray import asarray, ndarray

    return tuple(asarray(value).get() for value in inputs)


def to_tensors_or_none(*inputs):
    """Convert all array_likes from `inputs` to tensors. Nones pass through"""
    from ._ndarray import asarray, ndarray

    return tuple(None if value is None else asarray(value).get() for value in inputs)
