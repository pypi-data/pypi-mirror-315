#include "def.h"

#include "tatami/tatami.hpp"

#include "pybind11/pybind11.h"

#include <vector>

MatrixPointer initialize_delayed_bind(pybind11::list inputs, int along) {
    std::vector<MatrixPointer> combined;
    combined.reserve(inputs.size());
    for (size_t i = 0, n = inputs.size(); i < n; ++i) {
        combined.push_back(inputs[i].cast<MatrixPointer>());
    }
    return tatami::make_DelayedBind(std::move(combined), along == 0);
}

void init_delayed_bind(pybind11::module& m) {
    m.def("initialize_delayed_bind", &initialize_delayed_bind);
}
