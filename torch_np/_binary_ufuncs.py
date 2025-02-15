from ._decorators import deco_binary_ufunc_from_impl
from ._detail import _ufunc_impl

#
# Functions in this file implement binary ufuncs: wrap two first arguments in
# asarray and delegate to functions from _ufunc_impl.
#
# Functions in _detail/_ufunc_impl.py receive tensors, implement common tasks
# with ufunc args, and delegate heavy lifting to pytorch equivalents.
#

# the list is autogenerated, cf autogen/gen_ufunc_2.py
add = deco_binary_ufunc_from_impl(_ufunc_impl.add)
arctan2 = deco_binary_ufunc_from_impl(_ufunc_impl.arctan2)
bitwise_and = deco_binary_ufunc_from_impl(_ufunc_impl.bitwise_and)
bitwise_or = deco_binary_ufunc_from_impl(_ufunc_impl.bitwise_or)
bitwise_xor = deco_binary_ufunc_from_impl(_ufunc_impl.bitwise_xor)
copysign = deco_binary_ufunc_from_impl(_ufunc_impl.copysign)
divide = deco_binary_ufunc_from_impl(_ufunc_impl.divide)
equal = deco_binary_ufunc_from_impl(_ufunc_impl.equal)
float_power = deco_binary_ufunc_from_impl(_ufunc_impl.float_power)
floor_divide = deco_binary_ufunc_from_impl(_ufunc_impl.floor_divide)
fmax = deco_binary_ufunc_from_impl(_ufunc_impl.fmax)
fmin = deco_binary_ufunc_from_impl(_ufunc_impl.fmin)
fmod = deco_binary_ufunc_from_impl(_ufunc_impl.fmod)
gcd = deco_binary_ufunc_from_impl(_ufunc_impl.gcd)
greater = deco_binary_ufunc_from_impl(_ufunc_impl.greater)
greater_equal = deco_binary_ufunc_from_impl(_ufunc_impl.greater_equal)
heaviside = deco_binary_ufunc_from_impl(_ufunc_impl.heaviside)
hypot = deco_binary_ufunc_from_impl(_ufunc_impl.hypot)
lcm = deco_binary_ufunc_from_impl(_ufunc_impl.lcm)
ldexp = deco_binary_ufunc_from_impl(_ufunc_impl.ldexp)
left_shift = deco_binary_ufunc_from_impl(_ufunc_impl.left_shift)
less = deco_binary_ufunc_from_impl(_ufunc_impl.less)
less_equal = deco_binary_ufunc_from_impl(_ufunc_impl.less_equal)
logaddexp = deco_binary_ufunc_from_impl(_ufunc_impl.logaddexp)
logaddexp2 = deco_binary_ufunc_from_impl(_ufunc_impl.logaddexp2)
logical_and = deco_binary_ufunc_from_impl(_ufunc_impl.logical_and)
logical_or = deco_binary_ufunc_from_impl(_ufunc_impl.logical_or)
logical_xor = deco_binary_ufunc_from_impl(_ufunc_impl.logical_xor)
matmul = deco_binary_ufunc_from_impl(_ufunc_impl.matmul)
maximum = deco_binary_ufunc_from_impl(_ufunc_impl.maximum)
minimum = deco_binary_ufunc_from_impl(_ufunc_impl.minimum)
remainder = deco_binary_ufunc_from_impl(_ufunc_impl.remainder)
multiply = deco_binary_ufunc_from_impl(_ufunc_impl.multiply)
nextafter = deco_binary_ufunc_from_impl(_ufunc_impl.nextafter)
not_equal = deco_binary_ufunc_from_impl(_ufunc_impl.not_equal)
power = deco_binary_ufunc_from_impl(_ufunc_impl.power)
remainder = deco_binary_ufunc_from_impl(_ufunc_impl.remainder)
right_shift = deco_binary_ufunc_from_impl(_ufunc_impl.right_shift)
subtract = deco_binary_ufunc_from_impl(_ufunc_impl.subtract)
divide = deco_binary_ufunc_from_impl(_ufunc_impl.divide)
