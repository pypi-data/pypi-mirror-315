#include "def.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

MatrixPointer initialize_delayed_binary_isometric_operation(MatrixPointer left, MatrixPointer right, const std::string& op) {
    if (op == "add") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricAdd()));
    } else if (op == "subtract") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricSubtract()));
    } else if (op == "multiply") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricMultiply()));
    } else if (op == "divide") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricDivide()));
    } else if (op == "remainder") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricModulo()));
    } else if (op == "floor_divide") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricIntegerDivide()));
    } else if (op == "power") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricPower()));

    } else if (op == "equal") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricEqual()));
    } else if (op == "not_equal") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricNotEqual()));
    } else if (op == "greater") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricGreaterThan()));
    } else if (op == "greater_equal") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricGreaterThanOrEqual()));
    } else if (op == "less") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricLessThan()));
    } else if (op == "less_equal") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricLessThanOrEqual()));

    } else if (op == "logical_and") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricBooleanAnd()));
    } else if (op == "logical_or") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricBooleanOr()));
    } else if (op == "logical_xor") {
        return (tatami::make_DelayedBinaryIsometricOperation(std::move(left), std::move(right), tatami::make_DelayedBinaryIsometricBooleanXor()));
    }

    throw std::runtime_error("unknown binary isometric operation '" + op + "'");
    return MatrixPointer();
}

void init_delayed_binary_isometric_operation(pybind11::module& m) {
    m.def("initialize_delayed_binary_isometric_operation", &initialize_delayed_binary_isometric_operation);
}
