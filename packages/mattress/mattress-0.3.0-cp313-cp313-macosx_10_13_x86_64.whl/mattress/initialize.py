from functools import singledispatch
from typing import Any

import numpy
import delayedarray
from biocutils.package_utils import is_package_installed

from .InitializedMatrix import InitializedMatrix
from . import lib_mattress as lib
from ._utils import _sanitize_subset, _contiguify

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def initialize(x: Any) -> InitializedMatrix:
    """Initialize an :py:class:`~mattress.InitializedMatrix.InitializedMatrix`
    from a Python matrix representation. This prepares the matrix for use in
    C++ code that can accept a ``tatami::Matrix`` instance.

    Args:
        x: Any matrix-like object.

    Raises:
        NotImplementedError: if x is not supported.

    Returns:
        A pointer to tatami object.
    """
    raise NotImplementedError(
        f"initialize is not supported for objects of class: {type(x)}"
    )


@initialize.register
def _initialize_pointer(x: InitializedMatrix) -> InitializedMatrix:
    return x  # no-op


@initialize.register
def _initialize_numpy(x: numpy.ndarray) -> InitializedMatrix:
    if len(x.shape) != 2:
        raise ValueError("'x' should be a 2-dimensional array")
    x = _contiguify(x)
    return InitializedMatrix(
        ptr=lib.initialize_dense_matrix(x.shape[0], x.shape[1], x),
        objects=[x]
    )


if is_package_installed("scipy"):
    import scipy.sparse

    @initialize.register
    def _initialize_sparse_csr_array(x: scipy.sparse.csr_array) -> InitializedMatrix:
        dtmp = _contiguify(x.data)
        itmp = _contiguify(x.indices)
        indtmp = x.indptr.astype(numpy.uint64, copy=False, order="A")
        return InitializedMatrix(
            ptr=lib.initialize_compressed_sparse_matrix(x.shape[0], x.shape[1], dtmp, itmp, indtmp, True),
            objects=[dtmp, itmp, indtmp],
        )


    @initialize.register
    def _initialize_sparse_csr_matrix(x: scipy.sparse.csr_matrix) -> InitializedMatrix:
        return _initialize_sparse_csr_array(x)


    @initialize.register
    def _initialize_sparse_csc_array(x: scipy.sparse.csc_array) -> InitializedMatrix:
        dtmp = _contiguify(x.data)
        itmp = _contiguify(x.indices)
        indtmp = x.indptr.astype(numpy.uint64, copy=False, order="A")
        return InitializedMatrix(
            ptr=lib.initialize_compressed_sparse_matrix(x.shape[0], x.shape[1], dtmp, itmp, indtmp, False),
            objects=[dtmp, itmp, indtmp],
        )


    @initialize.register
    def _initialize_sparse_csc_matrix(x: scipy.sparse.csc_matrix) -> InitializedMatrix:
        return _initialize_sparse_csc_array(x)


@initialize.register
def _initialize_delayed_array(x: delayedarray.DelayedArray) -> InitializedMatrix:
    return initialize(x.seed)


@initialize.register
def _initialize_SparseNdarray(x: delayedarray.SparseNdarray) -> InitializedMatrix:
    if x.contents is not None:
        dvecs = []
        ivecs = []
        for y in x.contents:
            if y is None:
                ivecs.append(None)
                dvecs.append(None)
            else:
                ivecs.append(_contiguify(y[0]))
                dvecs.append(_contiguify(y[1]))
    else:
        nc = x.shape[1]
        dvecs = [None] * nc
        ivecs = [None] * nc

    return InitializedMatrix(
        ptr=lib.initialize_fragmented_sparse_matrix(x.shape[0], x.shape[1], dvecs, ivecs, False, x.dtype, x.index_dtype),
        objects=[dvecs, ivecs]
    )


@initialize.register
def _initialize_delayed_unary_isometric_operation_simple(
    x: delayedarray.UnaryIsometricOpSimple,
) -> InitializedMatrix:
    components = initialize(x.seed)
    ptr = lib.initialize_delayed_unary_isometric_operation_simple(
        components.ptr, x.operation.encode("UTF-8")
    )
    return InitializedMatrix(ptr, components.objects)


@initialize.register
def _initialize_delayed_unary_isometric_operation_with_args(
    x: delayedarray.UnaryIsometricOpWithArgs,
) -> InitializedMatrix:
    components = initialize(x.seed)
    obj = components.objects

    if isinstance(x.value, numpy.ndarray):
        contents = x.value.astype(numpy.float64, copy=False, order="A")
        ptr = lib.initialize_delayed_unary_isometric_operation_with_vector(
            components.ptr, x.operation.encode("UTF-8"), x.right, (x.along == 0), contents
        )
        obj.append(contents)
    else:
        ptr = lib.initialize_delayed_unary_isometric_operation_with_scalar(
            components.ptr, x.operation.encode("UTF-8"), x.right, x.value
        )

    return InitializedMatrix(ptr, obj)


@initialize.register
def _initialize_delayed_subset(
    x: delayedarray.Subset,
) -> InitializedMatrix:
    components = initialize(x.seed)

    for dim in range(2):
        current = x.subset[dim]
        noop, current = _sanitize_subset(current, x.shape[dim])
        if not noop:
            ptr = lib.initialize_delayed_subset(
                components.ptr, current, dim == 0
            )
            components = InitializedMatrix(ptr, components.objects + [current])

    return components


@initialize.register
def _initialize_delayed_bind(
    x: delayedarray.Combine,
) -> InitializedMatrix:
    collected = []
    objects = []
    for i, s in enumerate(x.seeds):
        components = initialize(s)
        collected.append(components.ptr)
        objects += components.objects

    ptr = lib.initialize_delayed_bind(collected, x.along)
    return InitializedMatrix(ptr, objects)


@initialize.register
def _initialize_delayed_transpose(
    x: delayedarray.Transpose,
) -> InitializedMatrix:
    components = initialize(x.seed)

    if x.perm == (1, 0):
        ptr = lib.initialize_delayed_transpose(components.ptr)
        components = InitializedMatrix(ptr, components.objects)

    return components


@initialize.register
def _initialize_delayed_binary_isometric_operation(
    x: delayedarray.BinaryIsometricOp,
) -> InitializedMatrix:
    lcomponents = initialize(x.left)
    rcomponents = initialize(x.right)

    ptr = lib.initialize_delayed_binary_isometric_operation(
        lcomponents.ptr, rcomponents.ptr, x.operation.encode("UTF-8")
    )

    return InitializedMatrix(ptr, lcomponents.objects + rcomponents.objects)


@initialize.register
def _initialize_delayed_round(
    x: delayedarray.Round,
) -> InitializedMatrix:
    components = initialize(x.seed)

    if x.decimals != 0:
        raise NotImplementedError(
            "non-zero decimals in 'delayedarray.Round' are not yet supported"
        )

    ptr = lib.initialize_delayed_unary_isometric_operation_simple(
        components.ptr, "round".encode("UTF-8")
    )

    return InitializedMatrix(ptr, components.objects)
