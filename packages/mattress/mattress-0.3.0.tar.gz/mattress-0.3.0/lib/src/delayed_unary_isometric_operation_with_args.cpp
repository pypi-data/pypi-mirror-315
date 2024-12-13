#include "def.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami/tatami.hpp"

#include <string>
#include <cstdint>

template<bool right_>
MatrixPointer initialize_delayed_unary_isometric_operation_with_vector_internal(MatrixPointer mat, const std::string& op, bool by_row, const pybind11::array& arg) {
    auto aptr = check_numpy_array<double>(arg);
    size_t expected = by_row ? mat->nrow() : mat->ncol();
    if (expected != arg.size()) {
        throw std::runtime_error("unexpected length of array for isometric unary operation");
    }
    tatami::ArrayView<double> aview(aptr, expected);

    if (op == "add") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricAddVector(std::move(aview), by_row));
    } else if (op == "subtract") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricSubtractVector<right_>(std::move(aview), by_row));
    } else if (op == "multiply") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricMultiplyVector(std::move(aview), by_row));
    } else if (op == "divide") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricDivideVector<right_>(std::move(aview), by_row));
    } else if (op == "remainder") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricModuloVector<right_>(std::move(aview), by_row));
    } else if (op == "floor_divide") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricIntegerDivideVector<right_>(std::move(aview), by_row));
    } else if (op == "power") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricPowerVector<right_>(std::move(aview), by_row));

    } else if (op == "equal") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricEqualVector(std::move(aview), by_row));
    } else if (op == "not_equal") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricNotEqualVector(std::move(aview), by_row));
    } else if ((right_ && op == "greater") || (!right_ && op == "less")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricGreaterThanVector(std::move(aview), by_row));
    } else if ((right_ && op == "greater_equal") || (!right_ && op == "less_equal")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricGreaterThanOrEqualVector(std::move(aview), by_row));
    } else if ((right_ && op == "less") || (!right_ && op == "greater")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricLessThanVector(std::move(aview), by_row));
    } else if ((right_ && op == "less_equal") || (!right_ && op == "greater_equal")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricLessThanOrEqualVector(std::move(aview), by_row));

    } else if (op == "logical_and") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanAndVector(std::move(aview), by_row));
    } else if (op == "logical_or") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanOrVector(std::move(aview), by_row));
    } else if (op == "logical_xor") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanXorVector(std::move(aview), by_row));
    }

    throw std::runtime_error("unknown unary isometric vector operation '" + op + "'");
    return MatrixPointer();
}

MatrixPointer initialize_delayed_unary_isometric_operation_with_vector(MatrixPointer mat, const std::string& op, bool right, bool by_row, const pybind11::array& args) {
    if (right) {
        return initialize_delayed_unary_isometric_operation_with_vector_internal<true>(std::move(mat), op, by_row, args);
    } else {
        return initialize_delayed_unary_isometric_operation_with_vector_internal<false>(std::move(mat), op, by_row, args);
    }
}

template<bool right_>
MatrixPointer initialize_delayed_unary_isometric_operation_with_scalar_internal(MatrixPointer mat, const std::string& op, double arg) {
    if (op == "add") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricAddScalar(arg));
    } else if (op == "subtract") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricSubtractScalar<right_>(arg));
    } else if (op == "multiply") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricMultiplyScalar(arg));
    } else if (op == "divide") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricDivideScalar<right_>(arg));
    } else if (op == "remainder") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricModuloScalar<right_>(arg));
    } else if (op == "floor_divide") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricIntegerDivideScalar<right_>(arg));
    } else if (op == "power") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricPowerScalar<right_>(arg));

    } else if (op == "equal") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricEqualScalar(arg));
    } else if (op == "not_equal") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricNotEqualScalar(arg));
    } else if ((right_ && op == "greater") || (!right_ && op == "less")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricGreaterThanScalar(arg));
    } else if ((right_ && op == "greater_equal") || (!right_ && op == "less_equal")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricGreaterThanOrEqualScalar(arg));
    } else if ((right_ && op == "less") || (!right_ && op == "greater")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricLessThanScalar(arg));
    } else if ((right_ && op == "less_equal") || (!right_ && op == "greater_equal")) {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricLessThanOrEqualScalar(arg));

    } else if (op == "logical_and") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanAndScalar(arg));
    } else if (op == "logical_or") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanOrScalar(arg));
    } else if (op == "logical_xor") {
        return tatami::make_DelayedUnaryIsometricOperation(std::move(mat), tatami::make_DelayedUnaryIsometricBooleanXorScalar(arg));
    }

    throw std::runtime_error("unknown unary isometric scalar operation '" + op + "'");
    return MatrixPointer();
}

MatrixPointer initialize_delayed_unary_isometric_operation_with_scalar(MatrixPointer mat, const std::string& op, bool right, double arg) {
    if (right) {
        return initialize_delayed_unary_isometric_operation_with_scalar_internal<true>(std::move(mat), op, arg);
    } else {
        return initialize_delayed_unary_isometric_operation_with_scalar_internal<false>(std::move(mat), op, arg);
    }
}

void init_delayed_unary_isometric_operation_with_args(pybind11::module& m) {
    m.def("initialize_delayed_unary_isometric_operation_with_vector", &initialize_delayed_unary_isometric_operation_with_vector);
    m.def("initialize_delayed_unary_isometric_operation_with_scalar", &initialize_delayed_unary_isometric_operation_with_scalar);
}
