# Changelog

## Version 0.3.0

- Switch to **pybind11** for the Python/C++ interface, with CMake for the build system.
- Updated to use the latest versions of the **tatami** libraries in **assorthead**.
- Renamed `tatamize()` to `initialize()` and `TatamiNumericPointer` to `InitializedMatrix`.
- Added an `initialize()` method for `SparseNdarray` objects from **delayedarray**.

## Version 0.2.0

Compatibility with NumPy 2.0

## Version 0.1 - 0.1.6

Bindings to the mattress package.
