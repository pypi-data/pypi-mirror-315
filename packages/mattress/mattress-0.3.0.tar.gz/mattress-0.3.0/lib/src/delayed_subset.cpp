#include "def.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include <string>
#include <cstdint>

MatrixPointer initialize_delayed_subset(MatrixPointer mat, const pybind11::array& subset, bool byrow) {
    auto sptr = check_numpy_array<MatrixIndex>(subset);
    return tatami::make_DelayedSubset(std::move(mat), tatami::ArrayView<MatrixIndex>(sptr, subset.size()), byrow);
}

void init_delayed_subset(pybind11::module& m) {
    m.def("initialize_delayed_subset", &initialize_delayed_subset);
}
