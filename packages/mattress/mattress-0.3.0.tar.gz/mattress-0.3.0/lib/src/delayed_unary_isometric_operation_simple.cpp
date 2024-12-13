#include "def.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

MatrixPointer initialize_delayed_unary_isometric_operation_simple(MatrixPointer ptr, const std::string& op) {
    if (op == "abs") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAbs<>());
    } else if (op == "sign") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricSign<>());

    } else if (op == "log") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricLog<>());
    } else if (op == "log2") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricLog(2.0));
    } else if (op == "log10") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricLog(10.0));
    } else if (op == "log1p") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricLog1p<>());

    } else if (op == "sqrt") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricSqrt<>());

    } else if (op == "ceil") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricCeiling<>());
    } else if (op == "floor") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricFloor<>());
    } else if (op == "trunc") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricTrunc<>());
    } else if (op == "round") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricRound<>());

    } else if (op == "exp") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricExp<>());
    } else if (op == "expm1") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricExpm1<>());

    } else if (op == "cos") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricCos<>());
    } else if (op == "sin") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricSin<>());
    } else if (op == "tan") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricTan<>());

    } else if (op == "cosh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricCosh<>());
    } else if (op == "sinh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricSinh<>());
    } else if (op == "tanh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricTanh<>());

    } else if (op == "arccos") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAcos<>());
    } else if (op == "arcsin") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAsin<>());
    } else if (op == "arctan") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAtan<>());

    } else if (op == "arccosh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAcosh<>());
    } else if (op == "arcsinh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAsinh<>());
    } else if (op == "arctanh") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(ptr), tatami::DelayedUnaryIsometricAtanh<>());
    }

    throw std::runtime_error("unknown binary isometric operation '" + op + "'");
    return MatrixPointer();
}

void init_delayed_unary_isometric_operation_simple(pybind11::module& m) {
    m.def("initialize_delayed_unary_isometric_operation_simple", &initialize_delayed_unary_isometric_operation_simple);
}
