.. _function:

=========
Functions
=========

All NNabla functions are derived from the :class:`nnabla.function.Function` class.

Function
========

.. automodule:: nnabla.function
.. autoclass:: Function
   :members:

.. _functions:

List of Functions
=================

.. automodule:: nnabla.functions

The :mod:`nnabla.functions` module provides various types of functions listed below.
These functions takes input :class:`nnabla.Variable` (s) as its leading argument(s), followed by options
specific to each function.

Note:
    The functions can also take :obj:`~nnabla.NdArray`s as inputs instead
    of :obj:`~nnabla.Variable`s. It will execute the function operation immediately,
    and returns :obj:`~nnabla.NdArray` (s) as output(s) holding output values of the
    operation. We call this "Imperative Mode" (NdArray + Functions).


Neural Network Layers
---------------------

.. autofunction:: affine
.. autofunction:: convolution
.. autofunction:: deconvolution
.. autofunction:: max_pooling
.. autofunction:: average_pooling
.. autofunction:: sum_pooling
.. autofunction:: unpooling
.. autofunction:: embed


Neural Network Activation
-------------------------

.. autofunction:: sigmoid
.. autofunction:: tanh
.. autofunction:: relu
.. autofunction:: softmax
.. autofunction:: elu
.. autofunction:: crelu
.. autofunction:: celu
.. autofunction:: prelu


Normalization
-------------

.. autofunction:: batch_normalization
.. autofunction:: mean_subtraction


Reduction
---------

.. autofunction:: sum
.. autofunction:: mean
.. autofunction:: max
.. autofunction:: min
.. autofunction:: prod
.. autofunction:: reduce_sum
.. autofunction:: reduce_mean


Arithmetic
----------

.. autofunction:: add2
.. autofunction:: sub2
.. autofunction:: mul2
.. autofunction:: div2
.. autofunction:: pow2
.. autofunction:: add_scalar
.. autofunction:: mul_scalar
.. autofunction:: pow_scalar
.. autofunction:: r_sub_scalar
.. autofunction:: r_div_scalar
.. autofunction:: r_pow_scalar


Logical
-------

.. autofunction:: equal
.. autofunction:: equal_scalar
.. autofunction:: greater
.. autofunction:: greater_equal
.. autofunction:: greater_equal_scalar
.. autofunction:: greater_scalar
.. autofunction:: less
.. autofunction:: less_equal
.. autofunction:: less_equal_scalar
.. autofunction:: less_scalar
.. autofunction:: logical_and
.. autofunction:: logical_and_scalar
.. autofunction:: logical_not
.. autofunction:: logical_or
.. autofunction:: logical_or_scalar
.. autofunction:: logical_xor
.. autofunction:: logical_xor_scalar
.. autofunction:: not_equal
.. autofunction:: not_equal_scalar
.. autofunction:: sign
.. autofunction:: minimum2
.. autofunction:: maximum2
.. autofunction:: minimum_scalar
.. autofunction:: maximum_scalar


Math
----

.. autofunction:: abs
.. autofunction:: exp
.. autofunction:: log
.. autofunction:: identity


Array Manipulation
------------------

.. autofunction:: concatenate
.. autofunction:: split
.. autofunction:: stack
.. autofunction:: slice
.. autofunction:: transpose
.. autofunction:: broadcast
.. autofunction:: flip
.. autofunction:: shift
.. autofunction:: reshape
.. autofunction:: one_hot


Stochasticity
-------------

.. autofunction:: dropout
.. autofunction:: random_crop
.. autofunction:: random_flip
.. autofunction:: random_shift
.. autofunction:: image_augmentation


Loss Functions
--------------

.. autofunction:: sigmoid_cross_entropy
.. autofunction:: binary_cross_entropy
.. autofunction:: softmax_cross_entropy
.. autofunction:: categorical_cross_entropy
.. autofunction:: squared_error
.. autofunction:: huber_loss
.. autofunction:: kl_multinomial


Quantization Neural Network Layers
----------------------------------

.. autofunction:: binary_sigmoid
.. autofunction:: binary_tanh
.. autofunction:: binary_connect_affine
.. autofunction:: binary_connect_convolution
.. autofunction:: binary_weight_affine
.. autofunction:: binary_weight_convolution
		  
   
Unsupported, Special Use
------------------------

.. autofunction:: vat_noise
.. autofunction:: unlink


Validation
----------

.. autofunction:: top_n_error
