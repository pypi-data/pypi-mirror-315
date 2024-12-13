#include "def.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <string>
#include <stdexcept>

template<typename Data_, typename Index_>
MatrixPointer initialize_fragmented_sparse_matrix_raw(MatrixIndex nr, MatrixValue nc, const pybind11::list& data, const pybind11::list& indices, bool byrow) {
    MatrixIndex nvec = byrow ? nr : nc;
    std::vector<tatami::ArrayView<Data_> > data_vec;
    data_vec.reserve(nvec);
    std::vector<tatami::ArrayView<Index_> > idx_vec;
    idx_vec.reserve(nvec);

    for (MatrixIndex i = 0; i < nvec; ++i) {
        auto curdata = data[i];
        if (pybind11::isinstance<pybind11::none>(curdata)) {
            data_vec.emplace_back(static_cast<Data_*>(NULL), 0);
            idx_vec.emplace_back(static_cast<Index_*>(NULL), 0);
            continue;
        }

        // This better not involve any copies.
        auto castdata = curdata.cast<pybind11::array>();
        auto curidx = indices[i];
        auto castidx = curidx.cast<pybind11::array>();

        if (castdata.size() != castidx.size()) {
            throw std::runtime_error("mismatching lengths for the index/data vectors");
        }
        data_vec.emplace_back(check_numpy_array<Data_>(castdata), castdata.size());
        idx_vec.emplace_back(check_numpy_array<Index_>(castidx), castidx.size());
    }

    return MatrixPointer(new tatami::FragmentedSparseMatrix<MatrixValue, MatrixIndex, decltype(data_vec), decltype(idx_vec)>(nr, nc, std::move(data_vec), std::move(idx_vec), byrow, false));
}

template<typename Data_>
MatrixPointer initialize_fragmented_sparse_matrix_itype(MatrixIndex nr, MatrixValue nc, const pybind11::list& data, const pybind11::list& indices, bool byrow, const pybind11::dtype& index_type) {
    if (index_type.is(pybind11::dtype::of<int64_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, int64_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<int32_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, int32_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<int16_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, int16_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<int8_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, int8_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<uint64_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, uint64_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<uint32_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, uint32_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<uint16_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, uint16_t>(nr, nc, data, indices, byrow);
    } else if (index_type.is(pybind11::dtype::of<uint8_t>())) {
        return initialize_fragmented_sparse_matrix_raw<Data_, uint8_t>(nr, nc, data, indices, byrow);
    }

    throw std::runtime_error("unrecognized index type '" + std::string(index_type.kind(), 1) + std::to_string(index_type.itemsize()) + "' for fragmented sparse matrix initialization");
    return MatrixPointer();
}

MatrixPointer initialize_fragmented_sparse_matrix(MatrixIndex nr, MatrixValue nc, const pybind11::list& data, const pybind11::list& indices, bool byrow, const pybind11::dtype& data_type, const pybind11::dtype& index_type) {
    if (data_type.is(pybind11::dtype::of<double>())) {
        return initialize_fragmented_sparse_matrix_itype<double>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<float>())) {
        return initialize_fragmented_sparse_matrix_itype<float>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<int64_t>())) {
        return initialize_fragmented_sparse_matrix_itype<int64_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<int32_t>())) {
        return initialize_fragmented_sparse_matrix_itype<int32_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<int16_t>())) {
        return initialize_fragmented_sparse_matrix_itype<int16_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<int8_t>())) {
        return initialize_fragmented_sparse_matrix_itype<int8_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<uint64_t>())) {
        return initialize_fragmented_sparse_matrix_itype<uint64_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<uint32_t>())) {
        return initialize_fragmented_sparse_matrix_itype<uint32_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<uint16_t>())) {
        return initialize_fragmented_sparse_matrix_itype<uint16_t>(nr, nc, data, indices, byrow, index_type);
    } else if (data_type.is(pybind11::dtype::of<uint8_t>())) {
        return initialize_fragmented_sparse_matrix_itype<uint8_t>(nr, nc, data, indices, byrow, index_type);
    }

    throw std::runtime_error("unrecognized data type '" + std::string(data_type.kind(), 1) + std::to_string(data_type.itemsize()) + "' for fragmented sparse matrix initialization");
    return MatrixPointer();
}

void init_fragmented_sparse_matrix(pybind11::module& m) {
    m.def("initialize_fragmented_sparse_matrix", &initialize_fragmented_sparse_matrix);
}
