#ifndef RTATAMI_H
#define RTATAMI_H

#include "pybind11/pybind11.h"
#include "tatami/tatami.hpp"
#include <memory>

namespace mattress {

/**
 * Type of the matrix value.
 */
typedef double MatrixValue;

/**
 * Type of the matrix index.
 */
typedef uint32_t MatrixIndex;

/**
 * @brief Pointer to a **tatami** matrix.
 *
 * The `tatami::Matrix` is allowed to hold views on Python-owned data, to avoid copies when moving from Python to C++.
 * However, if garbage collection occurs on the Python-owned data, the use of that data in C++ becomes invalid.
 * To avoid this, we hold the original Python objects to protect them from the garbage collector until this object is also destroyed.
 */
struct BoundMatrix {
    /**
     * Pointer to a `tatami::Matrix`.
     */
    std::shared_ptr<tatami::Matrix<MatrixValue, MatrixIndex> > ptr;

    /**
     * Python object containing the data referenced by `ptr`.
     */
    pybind11::object original;
};

/**
 * @param ptr A stored pointer.
 * @return Pointer to a `BoundMatrix`.
 */
inline BoundMatrix* cast(uintptr_t ptr) {
    return static_cast<BoundMatrix*>(reinterpret_cast<void*>(ptr));
}

/**
 * @param ptr Pointer to a `BoundMatrix`.
 * @return A stored pointer.
 */
inline uintptr_t cast(const BoundMatrix* ptr) {
    return reinterpret_cast<uintptr_t>(static_cast<void*>(const_cast<BoundMatrix*>(ptr)));
}

}

#endif
