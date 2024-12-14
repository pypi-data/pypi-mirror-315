#include "mattress.h"

#include "tatami/tatami.hpp"

#include "pybind11/pybind11.h"

#include <vector>

uintptr_t initialize_delayed_bind(const pybind11::list& inputs, int along) {
    std::vector<std::shared_ptr<tatami::Matrix<mattress::MatrixValue, mattress::MatrixIndex> > > combined;
    combined.reserve(inputs.size());
    pybind11::tuple originals(inputs.size());

    for (size_t i = 0, n = inputs.size(); i < n; ++i) {
        auto bound = mattress::cast(inputs[i].cast<uintptr_t>());
        combined.push_back(bound->ptr);
        originals[i] = bound->original; 
    }

    auto tmp = std::make_unique<mattress::BoundMatrix>();
    tmp->ptr = tatami::make_DelayedBind(std::move(combined), along == 0);
    tmp->original = std::move(originals);
    return mattress::cast(tmp.release());
}

void init_delayed_bind(pybind11::module& m) {
    m.def("initialize_delayed_bind", &initialize_delayed_bind);
}
