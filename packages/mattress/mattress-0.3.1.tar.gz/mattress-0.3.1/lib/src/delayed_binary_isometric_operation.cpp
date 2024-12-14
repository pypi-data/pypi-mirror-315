#include "mattress.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

template<typename Operation_>
uintptr_t convert(uintptr_t left, uintptr_t right, Operation_ op) {
    auto lbound = mattress::cast(left);
    auto rbound = mattress::cast(right);

    auto tmp = std::make_unique<mattress::BoundMatrix>();
    tmp->ptr = tatami::make_DelayedBinaryIsometricOperation(lbound->ptr, rbound->ptr, std::move(op));

    pybind11::tuple original(2);
    original[0] = lbound->original;
    original[1] = rbound->original;
    tmp->original = std::move(original);
    return mattress::cast(tmp.release());
}

uintptr_t initialize_delayed_binary_isometric_operation(uintptr_t left, uintptr_t right, const std::string& op) {
    if (op == "add") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricAdd());
    } else if (op == "subtract") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricSubtract());
    } else if (op == "multiply") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricMultiply());
    } else if (op == "divide") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricDivide());
    } else if (op == "remainder") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricModulo());
    } else if (op == "floor_divide") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricIntegerDivide());
    } else if (op == "power") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricPower());

    } else if (op == "equal") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricEqual());
    } else if (op == "not_equal") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricNotEqual());
    } else if (op == "greater") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricGreaterThan());
    } else if (op == "greater_equal") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricGreaterThanOrEqual());
    } else if (op == "less") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricLessThan());
    } else if (op == "less_equal") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricLessThanOrEqual());

    } else if (op == "logical_and") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricBooleanAnd());
    } else if (op == "logical_or") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricBooleanOr());
    } else if (op == "logical_xor") {
        return convert(left, right, tatami::make_DelayedBinaryIsometricBooleanXor());
    }

    throw std::runtime_error("unknown binary isometric operation '" + op + "'");
    return 0;
}

void init_delayed_binary_isometric_operation(pybind11::module& m) {
    m.def("initialize_delayed_binary_isometric_operation", &initialize_delayed_binary_isometric_operation);
}
