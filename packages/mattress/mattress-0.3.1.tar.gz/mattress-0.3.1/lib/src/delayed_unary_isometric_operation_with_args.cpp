#include "mattress.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

template<typename Operation_>
uintptr_t convert(const mattress::BoundMatrix* bound, const pybind11::array& arg, Operation_ op) {
    auto tmp = std::make_unique<mattress::BoundMatrix>();
    tmp->ptr = tatami::make_DelayedUnaryIsometricOperation(bound->ptr, std::move(op));
    pybind11::tuple original(2);
    original[0] = bound->original;
    original[1] = arg;
    tmp->original = std::move(original);
    return mattress::cast(tmp.release());
}

template<bool right_>
uintptr_t initialize_delayed_unary_isometric_operation_with_vector_internal(uintptr_t ptr, const std::string& op, bool by_row, const pybind11::array& arg) {
    auto bound = mattress::cast(ptr);
    auto aptr = check_numpy_array<double>(arg);
    size_t expected = by_row ? bound->ptr->nrow() : bound->ptr->ncol();
    if (expected != arg.size()) {
        throw std::runtime_error("unexpected length of array for isometric unary operation");
    }
    tatami::ArrayView<double> aview(aptr, expected);

    if (op == "add") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricAddVector(std::move(aview), by_row));
    } else if (op == "subtract") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricSubtractVector<right_>(std::move(aview), by_row));
    } else if (op == "multiply") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricMultiplyVector(std::move(aview), by_row));
    } else if (op == "divide") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricDivideVector<right_>(std::move(aview), by_row));
    } else if (op == "remainder") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricModuloVector<right_>(std::move(aview), by_row));
    } else if (op == "floor_divide") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricIntegerDivideVector<right_>(std::move(aview), by_row));
    } else if (op == "power") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricPowerVector<right_>(std::move(aview), by_row));

    } else if (op == "equal") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricEqualVector(std::move(aview), by_row));
    } else if (op == "not_equal") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricNotEqualVector(std::move(aview), by_row));
    } else if ((right_ && op == "greater") || (!right_ && op == "less")) {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricGreaterThanVector(std::move(aview), by_row));
    } else if ((right_ && op == "greater_equal") || (!right_ && op == "less_equal")) {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricGreaterThanOrEqualVector(std::move(aview), by_row));
    } else if ((right_ && op == "less") || (!right_ && op == "greater")) {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricLessThanVector(std::move(aview), by_row));
    } else if ((right_ && op == "less_equal") || (!right_ && op == "greater_equal")) {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricLessThanOrEqualVector(std::move(aview), by_row));

    } else if (op == "logical_and") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricBooleanAndVector(std::move(aview), by_row));
    } else if (op == "logical_or") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricBooleanOrVector(std::move(aview), by_row));
    } else if (op == "logical_xor") {
        return convert(bound, arg, tatami::make_DelayedUnaryIsometricBooleanXorVector(std::move(aview), by_row));
    }

    throw std::runtime_error("unknown unary isometric vector operation '" + op + "'");
    return 0;
}

uintptr_t initialize_delayed_unary_isometric_operation_with_vector(uintptr_t ptr, const std::string& op, bool right, bool by_row, const pybind11::array& args) {
    if (right) {
        return initialize_delayed_unary_isometric_operation_with_vector_internal<true>(ptr, op, by_row, args);
    } else {
        return initialize_delayed_unary_isometric_operation_with_vector_internal<false>(ptr, op, by_row, args);
    }
}

template<typename Operation_>
uintptr_t convert(uintptr_t ptr, Operation_ op) {
    auto bound = mattress::cast(ptr);
    auto tmp = std::make_unique<mattress::BoundMatrix>();
    tmp->ptr = tatami::make_DelayedUnaryIsometricOperation(bound->ptr, std::move(op));
    tmp->original = bound->original;
    return mattress::cast(tmp.release());
}

template<bool right_>
uintptr_t initialize_delayed_unary_isometric_operation_with_scalar_internal(uintptr_t ptr, const std::string& op, double arg) {
    if (op == "add") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricAddScalar(arg));
    } else if (op == "subtract") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricSubtractScalar<right_>(arg));
    } else if (op == "multiply") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricMultiplyScalar(arg));
    } else if (op == "divide") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricDivideScalar<right_>(arg));
    } else if (op == "remainder") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricModuloScalar<right_>(arg));
    } else if (op == "floor_divide") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricIntegerDivideScalar<right_>(arg));
    } else if (op == "power") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricPowerScalar<right_>(arg));

    } else if (op == "equal") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricEqualScalar(arg));
    } else if (op == "not_equal") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricNotEqualScalar(arg));
    } else if ((right_ && op == "greater") || (!right_ && op == "less")) {
        return convert(ptr, tatami::make_DelayedUnaryIsometricGreaterThanScalar(arg));
    } else if ((right_ && op == "greater_equal") || (!right_ && op == "less_equal")) {
        return convert(ptr, tatami::make_DelayedUnaryIsometricGreaterThanOrEqualScalar(arg));
    } else if ((right_ && op == "less") || (!right_ && op == "greater")) {
        return convert(ptr, tatami::make_DelayedUnaryIsometricLessThanScalar(arg));
    } else if ((right_ && op == "less_equal") || (!right_ && op == "greater_equal")) {
        return convert(ptr, tatami::make_DelayedUnaryIsometricLessThanOrEqualScalar(arg));

    } else if (op == "logical_and") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricBooleanAndScalar(arg));
    } else if (op == "logical_or") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricBooleanOrScalar(arg));
    } else if (op == "logical_xor") {
        return convert(ptr, tatami::make_DelayedUnaryIsometricBooleanXorScalar(arg));
    }

    throw std::runtime_error("unknown unary isometric scalar operation '" + op + "'");
    return 0;
}

uintptr_t initialize_delayed_unary_isometric_operation_with_scalar(uintptr_t ptr, const std::string& op, bool right, double arg) {
    if (right) {
        return initialize_delayed_unary_isometric_operation_with_scalar_internal<true>(ptr, op, arg);
    } else {
        return initialize_delayed_unary_isometric_operation_with_scalar_internal<false>(ptr, op, arg);
    }
}

void init_delayed_unary_isometric_operation_with_args(pybind11::module& m) {
    m.def("initialize_delayed_unary_isometric_operation_with_vector", &initialize_delayed_unary_isometric_operation_with_vector);
    m.def("initialize_delayed_unary_isometric_operation_with_scalar", &initialize_delayed_unary_isometric_operation_with_scalar);
}
