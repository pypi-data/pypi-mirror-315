#include "def.h"
#include "utils.h"

#include "tatami/tatami.hpp"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <stdexcept>
#include <string>
#include <cstdint>

template<typename Type_>
MatrixPointer initialize_dense_matrix_internal(MatrixIndex nr, MatrixIndex nc, const pybind11::array& buffer) {
    size_t expected = static_cast<size_t>(nr) * static_cast<size_t>(nc);
    if (buffer.size() != expected) {
        throw std::runtime_error("unexpected size for the dense matrix buffer");
    }

    auto flag = buffer.flags();
    bool byrow = false;
    if (flag & pybind11::array::c_style) {
        byrow = true;
    } else if (flag & pybind11::array::f_style) {
        byrow = false;
    } else {
        throw std::runtime_error("numpy array contents should be contiguous");
    }

    auto ptr = get_numpy_array_data<Type_>(buffer);
    tatami::ArrayView<Type_> view(ptr, expected);
    return MatrixPointer(new tatami::DenseMatrix<MatrixValue, MatrixIndex, decltype(view)>(nr, nc, std::move(view), byrow));
}

MatrixPointer initialize_dense_matrix(MatrixIndex nr, MatrixIndex nc, const pybind11::array& buffer) {
    // Don't make any kind of copy of buffer to coerce the type or storage
    // order, as this should be handled by the caller; we don't provide any
    // protection from GC for the arrays referenced by the views. 
    auto dtype = buffer.dtype();

    if (dtype.is(pybind11::dtype::of<double>())) {
        return initialize_dense_matrix_internal<  double>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<float>())) {
        return initialize_dense_matrix_internal<   float>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<int64_t>())) {
        return initialize_dense_matrix_internal< int64_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<int32_t>())) {
        return initialize_dense_matrix_internal< int32_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<int16_t>())) {
        return initialize_dense_matrix_internal< int16_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<int8_t>())) {
        return initialize_dense_matrix_internal<  int8_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<uint64_t>())) {
        return initialize_dense_matrix_internal<uint64_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<uint32_t>())) {
        return initialize_dense_matrix_internal<uint32_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<uint16_t>())) {
        return initialize_dense_matrix_internal<uint16_t>(nr, nc, buffer);
    } else if (dtype.is(pybind11::dtype::of<uint8_t>())) {
        return initialize_dense_matrix_internal< uint8_t>(nr, nc, buffer);
    }

    throw std::runtime_error("unrecognized array type '" + std::string(dtype.kind(), 1) + std::to_string(dtype.itemsize()) + "' for dense matrix initialization");
    return MatrixPointer();
}

void init_dense_matrix(pybind11::module& m) {
    m.def("initialize_dense_matrix", &initialize_dense_matrix);
}
