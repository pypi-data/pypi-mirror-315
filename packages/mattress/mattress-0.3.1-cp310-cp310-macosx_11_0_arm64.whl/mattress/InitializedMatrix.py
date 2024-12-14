import numpy
import delayedarray
from . import lib_mattress as lib
from typing import Tuple, Sequence
from ._utils import _sanitize_subset

__author__ = "ltla, jkanche"
__copyright__ = "ltla, jkanche"
__license__ = "MIT"


def _factorize(group):
    mapping = {}
    indices = numpy.ndarray((len(group),), numpy.uint32)
    levels = []
    for i, x in enumerate(group):
        if x not in mapping:
            mapping[x] = len(levels)
            levels.append(x)
        indices[i] = mapping[x]
    return levels, indices


class InitializedMatrix:
    """Pointer to an initialized ``tatami::matrix``, for use in C++ code.
    Instances of this class should only be created by developers and used
    within package functions; this is done by passing the :py:attr:`~ptr`
    address to C++ and casting it to a ``mattress::BoundMatrix``. All
    ``InitializedMatrix`` instances are expected to be transient within a
    Python session; they should not be serialized, nor should they be visible
    to end users. Each instance will automatically free the C++-allocated
    memory upon garbage collection.
    """

    def __init__(self, ptr: int):
        """
        Args:
            ptr:
                Address of a ``mattress::BoundMatrix`` instance.
        """
        self._ptr = ptr

    def __del__(self):
        """Free the instance at :py:attr:`~ptr`."""
        lib.free_mattress(self._ptr)

    def nrow(self) -> int:
        """Get number of rows.

        Returns:
            Number of rows.
        """
        return self.shape[0];

    def ncol(self) -> int:
        """Get number of columns.

        Returns:
            Number of columns.
        """
        return self.shape[1];

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the matrix, to masquerade as a NumPy-like object."""
        return lib.extract_dim(self._ptr)

    @property
    def ptr(self): 
        """An address to a ``mattress::BoundMatrix`` instance, to be passed
        as a ``uintptr_t`` to C++ for casting."""
        return self._ptr

    @property
    def dtype(self) -> numpy.dtype:
        """Type of the matrix, to masquerade as a NumPy-like object."""
        return numpy.dtype("float64")

    def __array__(self) -> numpy.ndarray:
        """Realize the underlying matrix into a dense NumPy array.

        Returns:
            Contents of the underlying matrix.
        """
        shape = self.shape;
        return _extract_array(self._ptr, (range(shape[0]), range(shape[1])), sparse=False)

    def __DelayedArray_dask__(self) -> numpy.ndarray:
        """Enable the use of the poiners with dask.

        See :py:meth:`~delayedarray.DelayedArray.DelayedArray.__DelayedArray_dask__` for details.

        This is largely a placeholder method for compatibility; it just realizes the underlying matrix into a dense
        array under the hood.

        Returns:
            Contents of the underlying matrix.
        """
        return self.__array___()

    def sparse(self) -> bool:
        """Is the matrix sparse?

        Returns:
            True if matrix is sparse.
        """
        return lib.extract_sparse(self._ptr); 

    def row(self, r: int) -> numpy.ndarray:
        """Access a row from the tatami matrix. This method is primarily intended for troubleshooting and should not be
        used to iterate over the matrix in production code. (Do that in C++ instead.)

        Args:
            r: Row to access.

        Returns:
            Row from the matrix. This is always in double-precision,
            regardless of the underlying representation.
        """
        return lib.extract_row(self._ptr, r)

    def column(self, c: int) -> numpy.ndarray:
        """Access a column from the tatami matrix. This method is primarily intended for troubleshooting and should not
        be used to iterate over the matrix in production code. (Do that in C++ instead.)

        Args:
            c: Column to access.

        Returns:
            Column from the matrix. This is always in double-precision,
            regardless of the underlying representation.
        """
        return lib.extract_column(self._ptr, c)

    def row_sums(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute row sums.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row sums.
        """
        return lib.compute_row_sums(self._ptr, num_threads)

    def column_sums(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute column sums.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column sums.
        """
        return lib.compute_column_sums(self._ptr, num_threads)

    def row_variances(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute row variances.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row variances.
        """
        return lib.compute_row_variances(self._ptr, num_threads)

    def column_variances(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute column variances.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column variances.
        """
        return lib.compute_column_variances(self._ptr, num_threads)

    def row_medians(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute row medians.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row medians.
        """
        return lib.compute_row_medians(self._ptr, num_threads)

    def column_medians(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute column medians.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column medians.
        """
        return lib.compute_column_medians(self._ptr, num_threads)

    def row_mins(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute row minima.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row minima.
        """
        return lib.compute_row_mins(self._ptr, num_threads)

    def column_mins(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute column minima.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column minima.
        """
        return lib.compute_column_mins(self._ptr, num_threads)

    def row_maxs(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute row maxima.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row maxima.
        """
        return lib.compute_row_maxs(self._ptr, num_threads)

    def column_maxs(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to compute column maxima.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column maxima.
        """
        return lib.compute_column_maxs(self._ptr, num_threads)

    def row_ranges(self, num_threads: int = 1) -> Tuple[numpy.ndarray, numpy.ndarray]:
        """Convenience method to compute row ranges.

        Args:
            num_threads: Number of threads.

        Returns:
            Tuple containing the row minima and maxima.
        """
        return lib.compute_row_ranges(self._ptr, num_threads)

    def column_ranges(self, num_threads: int = 1) -> Tuple[numpy.ndarray, numpy.ndarray]:
        """Convenience method to compute column ranges.

        Args:
            num_threads: Number of threads.

        Returns:
            Tuple containing the column minima and maxima.
        """
        return lib.compute_column_ranges(self._ptr, num_threads)

    def row_nan_counts(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to count the number of NaNs on each row.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of row NaN counts.
        """
        return lib.compute_row_nan_counts(self._ptr, num_threads)

    def column_nan_counts(self, num_threads: int = 1) -> numpy.ndarray:
        """Convenience method to count the number of NaNs on each column.

        Args:
            num_threads: Number of threads.

        Returns:
            Array of column NaN counts.
        """
        return lib.compute_column_nan_counts(self._ptr, num_threads)

    def row_medians_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the row-wise median for each group of columns.

        Args:
            group: Sequence of length equal to the number of columns of the matrix,
                containing the group assignment for each column.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each column represents
            a group and contains the row-wise medians for that group, across all rows of the matrix;
            and a list containing the unique levels of ``group`` represented by each column.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.ncol():
            raise ValueError(
                "'group' should have length equal to the number of columns"
            )

        output = lib.compute_row_medians_by_group(self._ptr, ind, num_threads);
        return output, lev

    def column_medians_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the column-wise median for each group of row.

        Args:
            group: Sequence of length equal to the number of row of the matrix,
                containing the group assignment for each row.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each row represents a
            group and contains the column-wise medians for that group, across
            all columns of the matrix; and a list containing the unique levels
            of ``group`` represented by each row.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.nrow():
            raise ValueError("'group' should have length equal to the number of rows")

        output = lib.compute_column_medians_by_group(self._ptr, ind, num_threads)
        return output.T, lev

    def row_sums_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the row-wise sum for each group of columns.

        Args:
            group: Sequence of length equal to the number of columns of the matrix,
                containing the group assignment for each column.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each column represents
            a group and contains the row-wise sums for that group, across all
            rows of the matrix; and a list containing the unique levels of
            ``group`` represented by each column.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.ncol():
            raise ValueError(
                "'group' should have length equal to the number of columns"
            )

        output = lib.compute_row_sums_by_group(self._ptr, ind, num_threads)
        return output, lev

    def column_sums_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the column-wise sum for each group of row.

        Args:
            group: Sequence of length equal to the number of row of the matrix,
                containing the group assignment for each row.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each row represents a
            group and contains the column-wise sums for that group, across all
            columns of the matrix; and a list containing the unique levels of
            ``group`` represented by each row.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.nrow():
            raise ValueError("'group' should have length equal to the number of rows")

        output = lib.compute_column_sums_by_group(self._ptr, ind, num_threads)
        return output.T, lev

    def row_variances_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the row-wise variance for each group of columns.

        Args:
            group: Sequence of length equal to the number of columns of the matrix,
                containing the group assignment for each column.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each column represents
            a group and contains the row-wise variances for that group, across all
            rows of the matrix; and a list containing the unique levels of
            ``group`` represented by each column.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.ncol():
            raise ValueError(
                "'group' should have length equal to the number of columns"
            )

        output = lib.compute_row_variances_by_group(self._ptr, ind, num_threads)
        return output, lev

    def column_variances_by_group(
        self, group: Sequence, num_threads: int = 1
    ) -> Tuple[numpy.ndarray, list]:
        """Convenience method to compute the column-wise variance for each group of row.

        Args:
            group: Sequence of length equal to the number of row of the matrix,
                containing the group assignment for each row.

            num_threads: Number of threads.

        Returns:
            Tuple containing a 2-dimensional array where each row represents a
            group and contains the column-wise variances for that group, across all
            columns of the matrix; and a list containing the unique levels of
            ``group`` represented by each row.
        """
        lev, ind = _factorize(group)
        if len(ind) != self.nrow():
            raise ValueError("'group' should have length equal to the number of rows")

        output = lib.compute_column_variances_by_group(self._ptr, ind, num_threads)
        return output.T, lev



@delayedarray.is_sparse.register
def is_sparse(x: InitializedMatrix):
    """See :py:func:`~delayedarray.is_sparse.is_sparse`."""
    return x.sparse()


def _extract_array(x: InitializedMatrix, subset: Tuple[Sequence[int], ...], sparse: bool): 
    shape = x.shape
    rnoop, rsub = _sanitize_subset(subset[0], shape[0])
    cnoop, csub = _sanitize_subset(subset[1], shape[1])
    if not sparse:
        return lib.extract_dense_subset(x.ptr, rnoop, rsub, cnoop, csub)
    else:
        return lib.extract_sparse_subset(x.ptr, rnoop, rsub, cnoop, csub)


@delayedarray.extract_dense_array.register
def extract_dense_array(x: InitializedMatrix, subset: Tuple[Sequence[int], ...]) -> numpy.ndarray:
    """See :py:func:`~delayedarray.extract_dense_array.extract_dense_array`."""
    return _extract_array(x, subset, False)

@delayedarray.extract_sparse_array.register
def extract_sparse_array(x: InitializedMatrix, subset: Tuple[Sequence[int], ...]) -> delayedarray.SparseNdarray:
    """See :py:func:`~delayedarray.extract_sparse_array.extract_sparse_array`."""
    return _extract_array(x, subset, True)

@delayedarray.is_masked.register
def is_masked(x: InitializedMatrix) -> bool:
    """See :py:func:`~delayedarray.is_masked.is_masked`."""
    return False

@delayedarray.chunk_grid.register
def chunk_grid(x: InitializedMatrix) -> bool:
    """See :py:func:`~delayedarray.chunk_grid.chunk_grid`."""
    return delayedarray.chunk_shape_to_grid((1, 1), x.shape, cost_factor=1)
