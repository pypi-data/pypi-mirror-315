#ifndef DEF_H
#define DEF_H

#include "tatami/tatami.hpp"
#include <cstdint>
#include <memory>

typedef double MatrixValue;
typedef uint32_t MatrixIndex;
typedef std::shared_ptr<tatami::Matrix<MatrixValue, MatrixIndex> > MatrixPointer;

#endif
