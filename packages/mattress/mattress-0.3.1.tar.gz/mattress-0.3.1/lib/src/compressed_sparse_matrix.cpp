#include "mattress.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <string>
#include <stdexcept>
#include <cstdint>

template<typename Data_, typename Index_>
uintptr_t initialize_compressed_sparse_matrix_raw(
    mattress::MatrixIndex nr,
    mattress::MatrixValue nc,
    const pybind11::array& data,
    const pybind11::array& index,
    const pybind11::array& indptr,
    bool byrow)
{
    size_t expected = (byrow ? nr : nc);
    if (indptr.size() != expected + 1) {
        throw std::runtime_error("unexpected length for the 'indptr' array");
    }
    tatami::ArrayView<uint64_t> pview(check_numpy_array<uint64_t>(indptr), indptr.size());

    size_t nz = pview[pview.size() - 1];
    if (data.size() != nz) {
        throw std::runtime_error("unexpected length for the 'data' array");
    }
    tatami::ArrayView<Data_> dview(check_contiguous_numpy_array<Data_>(data), nz);

    if (data.size() != nz) {
        throw std::runtime_error("unexpected length for the 'data' array");
    }
    tatami::ArrayView<Index_> iview(check_contiguous_numpy_array<Index_>(index), nz);

    auto tmp = std::make_unique<mattress::BoundMatrix>();
    typedef tatami::CompressedSparseMatrix<mattress::MatrixValue, mattress::MatrixIndex, decltype(dview), decltype(iview), decltype(pview)> Spmat;
    tmp->ptr.reset(new Spmat(nr, nc, std::move(dview), std::move(iview), std::move(pview), byrow));

    pybind11::tuple objects(3);
    objects[0] = data;
    objects[1] = index;
    objects[2] = indptr;
    tmp->original = std::move(objects);

    return mattress::cast(tmp.release());
}

template<typename Data_>
uintptr_t initialize_compressed_sparse_matrix_itype(
    mattress::MatrixIndex nr,
    mattress::MatrixValue nc,
    const pybind11::array& data,
    const pybind11::array& index,
    const pybind11::array& indptr,
    bool byrow)
{
    auto dtype = index.dtype();

    if (dtype.is(pybind11::dtype::of<int64_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_,  int64_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int32_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_,  int32_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int16_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_,  int16_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int8_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_,   int8_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint64_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_, uint64_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint32_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_, uint32_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint16_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_, uint16_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint8_t>())) {
        return initialize_compressed_sparse_matrix_raw<Data_,  uint8_t>(nr, nc, data, index, indptr, byrow);
    }

    throw std::runtime_error("unrecognized index type '" + std::string(dtype.kind(), 1) + std::to_string(dtype.itemsize()) + "' for compressed sparse matrix initialization");
    return 0;
}

uintptr_t initialize_compressed_sparse_matrix(
    mattress::MatrixIndex nr,
    mattress::MatrixValue nc,
    const pybind11::array& data,
    const pybind11::array& index,
    const pybind11::array& indptr,
    bool byrow)
{
    auto dtype = data.dtype();

    if (dtype.is(pybind11::dtype::of<double>())) {
        return initialize_compressed_sparse_matrix_itype<  double>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<float>())) {          
        return initialize_compressed_sparse_matrix_itype<   float>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int64_t>())) {
        return initialize_compressed_sparse_matrix_itype< int64_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int32_t>())) {
        return initialize_compressed_sparse_matrix_itype< int32_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int16_t>())) {
        return initialize_compressed_sparse_matrix_itype< int16_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<int8_t>())) {
        return initialize_compressed_sparse_matrix_itype<  int8_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint64_t>())) {
        return initialize_compressed_sparse_matrix_itype<uint64_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint32_t>())) {
        return initialize_compressed_sparse_matrix_itype<uint32_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint16_t>())) {
        return initialize_compressed_sparse_matrix_itype<uint16_t>(nr, nc, data, index, indptr, byrow);
    } else if (dtype.is(pybind11::dtype::of<uint8_t>())) {
        return initialize_compressed_sparse_matrix_itype< uint8_t>(nr, nc, data, index, indptr, byrow);
    }

    throw std::runtime_error("unrecognized data type '" + std::string(dtype.kind(), 1) + std::to_string(dtype.itemsize()) + "' for compressed sparse matrix initialization");
    return 0;
}

void init_compressed_sparse_matrix(pybind11::module& m) {
    m.def("initialize_compressed_sparse_matrix", &initialize_compressed_sparse_matrix);
}
