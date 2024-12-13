#include "def.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <string>
#include <cstdint>

MatrixPointer initialize_delayed_transpose(MatrixPointer mat) {
    return tatami::make_DelayedTranspose(std::move(mat));
}

void init_delayed_transpose(pybind11::module& m) {
    m.def("initialize_delayed_transpose", &initialize_delayed_transpose);
}
