#include "mattress.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

template<typename Operation_>
uintptr_t convert(uintptr_t ptr, Operation_ op) {
    auto bound = mattress::cast(ptr);
    auto tmp = std::make_unique<mattress::BoundMatrix>();
    tmp->ptr = tatami::make_DelayedUnaryIsometricOperation(bound->ptr, std::move(op));
    tmp->original = bound->original;
    return mattress::cast(tmp.release());
}

uintptr_t initialize_delayed_unary_isometric_operation_simple(uintptr_t ptr, const std::string& op) {
    if (op == "abs") {
        return convert(ptr, tatami::DelayedUnaryIsometricAbs<>());
    } else if (op == "sign") {
        return convert(ptr, tatami::DelayedUnaryIsometricSign<>());

    } else if (op == "log") {
        return convert(ptr, tatami::DelayedUnaryIsometricLog<>());
    } else if (op == "log2") {
        return convert(ptr, tatami::DelayedUnaryIsometricLog(2.0));
    } else if (op == "log10") {
        return convert(ptr, tatami::DelayedUnaryIsometricLog(10.0));
    } else if (op == "log1p") {
        return convert(ptr, tatami::DelayedUnaryIsometricLog1p<>());

    } else if (op == "sqrt") {
        return convert(ptr, tatami::DelayedUnaryIsometricSqrt<>());

    } else if (op == "ceil") {
        return convert(ptr, tatami::DelayedUnaryIsometricCeiling<>());
    } else if (op == "floor") {
        return convert(ptr, tatami::DelayedUnaryIsometricFloor<>());
    } else if (op == "trunc") {
        return convert(ptr, tatami::DelayedUnaryIsometricTrunc<>());
    } else if (op == "round") {
        return convert(ptr, tatami::DelayedUnaryIsometricRound<>());

    } else if (op == "exp") {
        return convert(ptr, tatami::DelayedUnaryIsometricExp<>());
    } else if (op == "expm1") {
        return convert(ptr, tatami::DelayedUnaryIsometricExpm1<>());

    } else if (op == "cos") {
        return convert(ptr, tatami::DelayedUnaryIsometricCos<>());
    } else if (op == "sin") {
        return convert(ptr, tatami::DelayedUnaryIsometricSin<>());
    } else if (op == "tan") {
        return convert(ptr, tatami::DelayedUnaryIsometricTan<>());

    } else if (op == "cosh") {
        return convert(ptr, tatami::DelayedUnaryIsometricCosh<>());
    } else if (op == "sinh") {
        return convert(ptr, tatami::DelayedUnaryIsometricSinh<>());
    } else if (op == "tanh") {
        return convert(ptr, tatami::DelayedUnaryIsometricTanh<>());

    } else if (op == "arccos") {
        return convert(ptr, tatami::DelayedUnaryIsometricAcos<>());
    } else if (op == "arcsin") {
        return convert(ptr, tatami::DelayedUnaryIsometricAsin<>());
    } else if (op == "arctan") {
        return convert(ptr, tatami::DelayedUnaryIsometricAtan<>());

    } else if (op == "arccosh") {
        return convert(ptr, tatami::DelayedUnaryIsometricAcosh<>());
    } else if (op == "arcsinh") {
        return convert(ptr, tatami::DelayedUnaryIsometricAsinh<>());
    } else if (op == "arctanh") {
        return convert(ptr, tatami::DelayedUnaryIsometricAtanh<>());
    }

    throw std::runtime_error("unknown binary isometric operation '" + op + "'");
    return 0;
}

void init_delayed_unary_isometric_operation_simple(pybind11::module& m) {
    m.def("initialize_delayed_unary_isometric_operation_simple", &initialize_delayed_unary_isometric_operation_simple);
}
