# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Holding mint APIs"""
from mindspore._c_expression import _clamp_instance
from mindspore._c_expression import _div_instance
from mindspore._c_expression import _fmod_instance
from mindspore._c_expression import _remainder_instance
from mindspore._c_expression import _repeat_interleave_instance

def clamp(*args, **kwargs):
    r"""
    clamp(input, min=None, max=None) -> Tensor

    Clamps tensor values between the specified minimum value and maximum value.

    Limits the value of :math:`input` to a range, whose lower limit is `min` and upper limit is `max` .

    .. math::

        out_i= \left\{
        \begin{array}{align}
            max & \text{ if } input_i\ge max \\
            input_i & \text{ if } min \lt input_i \lt max \\
            min & \text{ if } input_i \le min \\
        \end{array}\right.

    Note:
        - `min` and `max` cannot be None at the same time;
        - When `min` is None and `max` is not None, the elements in Tensor larger than `max` will become `max`;
        - When `min` is not None and `max` is None, the elements in Tensor smaller than `min` will become `min`;
        - If `min` is greater than `max`, the value of all elements in Tensor will be set to `max`;
        - The data type of `input`, `min` and `max` should support implicit type conversion and cannot be bool type.

    Args:
        min (Union(Tensor, float, int), optional): The minimum value. Default: ``None`` .
        max (Union(Tensor, float, int), optional): The maximum value. Default: ``None`` .

    Returns:
        Tensor, a clipped Tensor.
        The data type and shape are the same as input.

    Raises:
        ValueError: If both `min` and `max` are None.
        TypeError: If the type of `input` is not Tensor.
        TypeError: If the type of `min` is not in None, Tensor, float or int.
        TypeError: If the type of `max` is not in None, Tensor, float or int.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> # case 1: the data type of input is Tensor
        >>> import mindspore
        >>> from mindspore import Tensor, mint
        >>> import numpy as np
        >>> min_value = Tensor(5, mindspore.float32)
        >>> max_value = Tensor(20, mindspore.float32)
        >>> input = Tensor(np.array([[1., 25., 5., 7.], [4., 11., 6., 21.]]), mindspore.float32)
        >>> output = mint.clamp(input, min_value, max_value)
        >>> print(output)
        [[ 5. 20.  5.  7.]
         [ 5. 11.  6. 20.]]
        >>> # case 2: the data type of input is number
        >>> import mindspore
        >>> from mindspore import Tensor, mint
        >>> import numpy as np
        >>> min_value = 5
        >>> max_value = 20
        >>> input = Tensor(np.array([[1., 25., 5., 7.], [4., 11., 6., 21.]]), mindspore.float32)
        >>> output = mint.clamp(input, min_value, max_value)
        >>> print(output)
        [[ 5. 20.  5.  7.]
         [ 5. 11.  6. 20.]]
    """
    return _clamp_instance(*args, **kwargs)


def clip(*args, **kwargs):
    r"""
    clip(input, min=None, max=None) -> Tensor

    Alias for :func:`mindspore.mint.clamp`.
    """
    return _clamp_instance(*args, **kwargs)


def div(*args, **kwargs):
    r"""
    div(input, other, *, rounding_mode=None) -> Tensor

    Divides the first input tensor by the second input tensor in floating-point type element-wise.

    .. math::

        out_{i} = input_{i} / other_{i}

    Note:
        - When the two inputs have different shapes, they must be able to broadcast to a common shape.
        - The two inputs can not be bool type at the same time,
          [True, Tensor(True, bool\_), Tensor(np.array([True]), bool\_)] are all considered bool type.
        - The two inputs comply with the implicit type conversion rules to make the data types
          consistent.

    Args:
        input (Union[Tensor, Number, bool]): The first input is a Number or
            a bool or a tensor whose data type is number or bool.
        other (Union[Tensor, Number, bool]): The second input is a Number or
            a bool when the first input is a tensor or a tensor whose data type is Number or bool.

    Keyword Args:
        rounding_mode (str, optional): Type of rounding applied to the result. Default: ``None`` .
            Three types are defined as,

            - None: Default behavior, which is the same as true division in Python or `true_divide` in NumPy.

            - "floor": Rounds the division of the inputs down, which is the same as floor division in Python
              or `floor_divide` in NumPy.

            - "trunc": Rounds the division of the inputs towards zero, which is the same as C-style integer division.

    Returns:
        Tensor, the shape is the same as the one after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `input` and `other` is not one of the following: Tensor, Number, bool.
        ValueError: If `rounding_mode` value is not None, "floor" or "trunc".

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> x = Tensor(np.array([1.0, 2.0, 3.0]), mindspore.float32)
        >>> y = Tensor(np.array([4.0, 5.0, 6.0]), mindspore.float32)
        >>> output = mint.div(x, y)
        >>> print(output)
        [0.25 0.4 0.5]
    """
    return _div_instance(*args, **kwargs)


def divide(*args, **kwargs):
    r"""
    divide(input, other, *, rounding_mode=None) -> Tensor

    Alias for :func:`mindspore.mint.div` .

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    return _div_instance(*args, **kwargs)


def fmod(*args, **kwargs):
    r"""
    fmod(input, other) -> Tensor

    Computes the floating-point remainder of the division operation input/other.

    .. math::

        out = input - n * other

    Where :math:`n` is :math:`input/other` with its fractional part truncated.
    The returned value has the same sign as `input` and is less than `other` in magnitude.

    .. warning:
        This is an experimental API that is subject to change or deletion.

    Args:
        input (Tensor): the dividend.
        other (Union[Tensor, Number]): the divisor.

    Returns:
        Tensor, the shape is the same as the one after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `input` is not a Tensor.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> input = Tensor(np.array([-4., -3.5, 0, 3.5, 4]), mindspore.float32)
        >>> output = mint.fmod(input, 2.5)
        >>> print(output)
        [-1.5 -1.   0.   1.   1.5]
    """
    return _fmod_instance(*args, **kwargs)


def remainder(*args, **kwargs):
    r"""
    remainder(input, other) -> Tensor

    Computes the remainder of `input` divided by `other` element-wise. The result has the same sign as the divisor and
    its absolute value is less than that of `other`.

    Supports broadcasting to a common shape and implicit type promotion.

    .. math::

        remainder(input, other) = input - input.div(other, rounding\_mode="floor") * other

    Note:
        Complex inputs are not supported. At least one input need to be tensor, but not both are bool tensors.

    Args:
        input (Union[Tensor, numbers.Number, bool]): The dividend is a numbers.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore/mindspore.dtype.html>`_.
        other (Union[Tensor, numbers.Number, bool]): The divisor is a numbers.Number or
            a bool or a tensor whose data type is number or bool\_ when the dividend is a tensor.
            When the dividend is Scalar, the divisor must be a Tensor whose data type is number or bool\_.

    Returns:
        Tensor, with dtype promoted and shape broadcasted.

    Raises:
        TypeError: If `input` and `other` are not of types: (tensor, tensor), (tensor, number), (tensor, bool),
            (number, tensor) or (bool, tensor).
        ValueError: If `input` and `other` are not broadcastable.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> x = Tensor(np.array([-4.0, 5.0, 6.0]).astype(np.float32))
        >>> y = Tensor(np.array([3.0, 2.0, 3.0]).astype(np.float64))
        >>> output = mint.remainder(x, y)
        >>> print(output)
        [2.  1.  0.]
    """
    return _remainder_instance(*args, **kwargs)


def repeat_interleave(*args, **kwargs):
    r"""
    repeat_interleave(input, repeats, dim=None, output_size=None) -> Tensor

    Repeat elements of a tensor along an axis, like `numpy.repeat`.

    .. warning::
        Only support on Atlas A2 training series.

    Args:
        input (Tensor): The tensor to repeat values for. Must be of types: float16,
            float32, int8, uint8, int16, int32, or int64.
        repeats (Union[int, tuple, list, Tensor]): The number of times to repeat, must be positive.
        dim (int, optional): The dim along which to repeat, Default: ``None``. If dims is None,
            the input Tensor will be flattened and the output will alse be flattened.
        output_size (int, optional): Total output size for the given axis (e.g. sum of repeats),
            Default: ``None``.

    Returns:
        One tensor with values repeated along the specified dim. If input has shape
        :math:`(s1, s2, ..., sn)` and dim is i, the output will have shape :math:`(s1, s2, ...,
        si * repeats, ..., sn)`. The output type will be the same as the type of `input`.

    Supported Platforms:
        ``Ascend``

    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> input = Tensor(np.array([[0, 1, 2], [3, 4, 5]]), mindspore.int32)
        >>> output = mint.repeat_interleave_ext(input, repeats=2, dim=0)
        >>> print(output)
        [[0 1 2]
         [0 1 2]
         [3 4 5]
         [3 4 5]]
    """
    return _repeat_interleave_instance(*args, **kwargs)

__all__ = [
    "clamp",
    "clip",
    "div",
    "divide",
    "fmod",
    "remainder",
    "repeat_interleave",
]
