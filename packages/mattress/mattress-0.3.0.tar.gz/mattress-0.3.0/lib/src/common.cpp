#include "def.h"
#include "utils.h"

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"

#include "tatami_stats/tatami_stats.hpp"

pybind11::tuple extract_dim(const MatrixPointer& mat) {
    pybind11::tuple output(2);
    output[0] = mat->nrow();
    output[1] = mat->ncol();
    return output;
}

bool extract_sparse(const MatrixPointer& mat) {
    return mat->is_sparse();
}

pybind11::array_t<MatrixValue> extract_row(const MatrixPointer& mat, MatrixIndex r) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    auto ext = tatami::consecutive_extractor<false, MatrixValue, MatrixIndex>(mat.get(), true, r, 1);
    auto out = ext->fetch(optr);
    tatami::copy_n(out, output.size(), optr);
    return output;
}

pybind11::array_t<MatrixValue> extract_column(const MatrixPointer& mat, MatrixIndex c) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    auto ext = tatami::consecutive_extractor<false, MatrixValue, MatrixIndex>(mat.get(), false, c, 1);
    auto out = ext->fetch(optr);
    tatami::copy_n(out, output.size(), optr);
    return output;
}

/** Stats **/

pybind11::array_t<MatrixValue> compute_column_sums(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::sums::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::sums::apply(false, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_sums(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::sums::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::sums::apply(true, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_variances(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::variances::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::variances::apply(false, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_variances(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::variances::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::variances::apply(true, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_medians(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::medians::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::medians::apply(false, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_medians(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::medians::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::medians::apply(true, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_mins(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(false, mat.get(), optr, static_cast<MatrixValue*>(NULL), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_mins(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(true, mat.get(), optr, static_cast<MatrixValue*>(NULL), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_maxs(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->ncol());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(false, mat.get(), static_cast<MatrixValue*>(NULL), optr, opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_maxs(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> output(mat->nrow());
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(true, mat.get(), static_cast<MatrixValue*>(NULL), optr, opt);
    return output;
}

pybind11::tuple compute_row_ranges(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> mnout(mat->nrow()), mxout(mat->nrow());
    auto mnptr = static_cast<MatrixValue*>(mnout.request().ptr);
    auto mxptr = static_cast<MatrixValue*>(mxout.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(true, mat.get(), mnptr, mxptr, opt);

    pybind11::tuple output(2);
    output[0] = mnout;
    output[1] = mxout;
    return output;
}

pybind11::tuple compute_column_ranges(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixValue> mnout(mat->ncol()), mxout(mat->ncol());
    auto mnptr = static_cast<MatrixValue*>(mnout.request().ptr);
    auto mxptr = static_cast<MatrixValue*>(mxout.request().ptr);
    tatami_stats::ranges::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::ranges::apply(false, mat.get(), mnptr, mxptr, opt);

    pybind11::tuple output(2);
    output[0] = mnout;
    output[1] = mxout;
    return output;
}

pybind11::array_t<MatrixIndex> compute_row_nan_counts(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixIndex> output(mat->nrow());
    auto optr = static_cast<MatrixIndex*>(output.request().ptr);
    tatami_stats::counts::nan::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::counts::nan::apply(true, mat.get(), optr, opt);
    return output;
}

pybind11::array_t<MatrixIndex> compute_column_nan_counts(const MatrixPointer& mat, int num_threads) {
    pybind11::array_t<MatrixIndex> output(mat->ncol());
    auto optr = static_cast<MatrixIndex*>(output.request().ptr);
    tatami_stats::counts::nan::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::counts::nan::apply(false, mat.get(), optr, opt);
    return output;
}

/** Grouped stats **/

pybind11::array_t<MatrixValue> compute_row_sums_by_group(const MatrixPointer& mat, const pybind11::array& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t ncol = mat->ncol();
    if (grouping.size() != ncol) {
        throw std::runtime_error("'grouping' should have length equal to the number of columns");
    }

    size_t ngroups = tatami_stats::total_groups(gptr, ncol);
    size_t nrow = mat->nrow();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ nrow, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * nrow;
    }

    tatami_stats::grouped_sums::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_sums::apply(true, mat.get(), gptr, ngroups, ptrs.data(), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_sums_by_group(const MatrixPointer& mat, const pybind11::array& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t nrow = mat->nrow();
    if (grouping.size() != nrow) {
        throw std::runtime_error("'grouping' should have length equal to the number of rows");
    }

    size_t ngroups = tatami_stats::total_groups(gptr, nrow);
    size_t ncol = mat->ncol();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ ncol, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * ncol;
    }

    tatami_stats::grouped_sums::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_sums::apply(false, mat.get(), gptr, ngroups, ptrs.data(), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_variances_by_group(const MatrixPointer& mat, const pybind11::array_t<MatrixIndex>& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t ncol = mat->ncol();
    if (grouping.size() != ncol) {
        throw std::runtime_error("'grouping' should have length equal to the number of columns");
    }

    auto group_sizes = tatami_stats::tabulate_groups<MatrixIndex, MatrixIndex>(gptr, ncol);
    size_t ngroups = group_sizes.size();
    size_t nrow = mat->nrow();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ nrow, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * nrow;
    }

    tatami_stats::grouped_variances::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_variances::apply(true, mat.get(), gptr, ngroups, group_sizes.data(), ptrs.data(), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_variances_by_group(const MatrixPointer& mat, const pybind11::array_t<MatrixIndex>& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t nrow = mat->nrow();
    if (grouping.size() != nrow) {
        throw std::runtime_error("'grouping' should have length equal to the number of rows");
    }

    auto group_sizes = tatami_stats::tabulate_groups<MatrixIndex, MatrixIndex>(gptr, nrow);
    size_t ngroups = group_sizes.size();
    size_t ncol = mat->ncol();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ ncol, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * ncol;
    }

    tatami_stats::grouped_variances::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_variances::apply(false, mat.get(), grouping.data(), ngroups, group_sizes.data(), ptrs.data(), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_row_medians_by_group(const MatrixPointer& mat, const pybind11::array_t<MatrixIndex>& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t ncol = mat->ncol();
    if (grouping.size() != ncol) {
        throw std::runtime_error("'grouping' should have length equal to the number of columns");
    }

    auto group_sizes = tatami_stats::tabulate_groups<MatrixIndex, MatrixIndex>(gptr, ncol);
    size_t ngroups = group_sizes.size();
    size_t nrow = mat->nrow();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ nrow, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * nrow;
    }

    tatami_stats::grouped_medians::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_medians::apply(true, mat.get(), gptr, group_sizes, ptrs.data(), opt);
    return output;
}

pybind11::array_t<MatrixValue> compute_column_medians_by_group(const MatrixPointer& mat, const pybind11::array_t<MatrixIndex>& grouping, int num_threads) {
    auto gptr = check_numpy_array<MatrixIndex>(grouping);
    size_t nrow = mat->nrow();
    if (grouping.size() != nrow) {
        throw std::runtime_error("'grouping' should have length equal to the number of rows");
    }

    auto group_sizes = tatami_stats::tabulate_groups<MatrixIndex, MatrixIndex>(gptr, nrow);
    size_t ngroups = group_sizes.size();
    size_t ncol = mat->ncol();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ ncol, ngroups });

    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    std::vector<MatrixValue*> ptrs(ngroups);
    for (size_t g = 0; g < ngroups; ++g) {
        ptrs[g] = optr + g * ncol;
    }

    tatami_stats::grouped_medians::Options opt;
    opt.num_threads = num_threads;
    tatami_stats::grouped_medians::apply(false, mat.get(), gptr, group_sizes, ptrs.data(), opt);
    return output;
}

/** Extraction **/

pybind11::array_t<MatrixValue> extract_dense_subset(MatrixPointer mat, bool row_noop, const pybind11::array& row_sub, bool col_noop, const pybind11::array& col_sub) {
    if (!row_noop) {
        auto rptr = check_numpy_array<MatrixIndex>(row_sub);
        auto tmp = tatami::make_DelayedSubset<0>(std::move(mat), tatami::ArrayView<MatrixIndex>(rptr, row_sub.size()));
        mat.swap(tmp);
    }

    if (!col_noop) {
        auto cptr = check_numpy_array<MatrixIndex>(col_sub);
        auto tmp = tatami::make_DelayedSubset<1>(std::move(mat), tatami::ArrayView<MatrixIndex>(cptr, col_sub.size()));
        mat.swap(tmp);
    }

    size_t NR = mat->nrow(), NC = mat->ncol();
    pybind11::array_t<MatrixValue, pybind11::array::f_style> output({ NR, NC });
    auto optr = static_cast<MatrixValue*>(output.request().ptr);
    tatami::convert_to_dense(mat.get(), false, optr);
    return output;
}

pybind11::object extract_sparse_subset(MatrixPointer mat, bool row_noop, const pybind11::array& row_sub, bool col_noop, const pybind11::array& col_sub) {
    if (!row_noop) {
        auto rptr = check_numpy_array<MatrixIndex>(row_sub);
        auto tmp = tatami::make_DelayedSubset<0>(std::move(mat), tatami::ArrayView<MatrixIndex>(rptr, row_sub.size()));
        mat.swap(tmp);
    }

    if (!col_noop) {
        auto cptr = check_numpy_array<MatrixIndex>(col_sub);
        auto tmp = tatami::make_DelayedSubset<1>(std::move(mat), tatami::ArrayView<MatrixIndex>(cptr, col_sub.size()));
        mat.swap(tmp);
    }

    int NC = mat->ncol();
    int NR = mat->nrow();
    pybind11::list content(NC);

    if (mat->prefer_rows()) {
        std::vector<std::vector<MatrixValue> > vcollection(NC);
        std::vector<std::vector<MatrixIndex> > icollection(NC);

        auto ext = tatami::consecutive_extractor<true, MatrixValue, MatrixIndex>(mat.get(), true, 0, NR);
        std::vector<MatrixValue> vbuffer(NC);
        std::vector<MatrixIndex> ibuffer(NC);

        for (int r = 0; r < NR; ++r) {
            auto info = ext->fetch(vbuffer.data(), ibuffer.data());
            for (int i = 0; i < info.number; ++i) {
                auto c = info.index[i];
                vcollection[c].push_back(info.value[i]);
                icollection[c].push_back(r);
            }
        }

        for (int c = 0; c < NC; ++c) {
            if (vcollection[c].size()) {
                pybind11::list tmp(2);
                tmp[0] = pybind11::array_t<MatrixIndex>(icollection[c].size(), icollection[c].data());
                tmp[1] = pybind11::array_t<MatrixValue>(vcollection[c].size(), vcollection[c].data());
                content[c] = std::move(tmp);
            } else {
                content[c] = pybind11::none();
            }
        }

    } else {
        auto ext = tatami::consecutive_extractor<true, MatrixValue, MatrixIndex>(mat.get(), false, 0, NC);
        std::vector<MatrixValue> vbuffer(NC);
        std::vector<MatrixIndex> ibuffer(NC);

        for (int c = 0; c < NC; ++c) {
            auto info = ext->fetch(vbuffer.data(), ibuffer.data());
            if (info.number) {
                pybind11::list tmp(2);
                tmp[0] = pybind11::array_t<MatrixIndex>(info.number, info.index);
                tmp[1] = pybind11::array_t<MatrixValue>(info.number, info.value);
                content[c] = std::move(tmp);
            } else {
                content[c] = pybind11::none();
            }
        }
    }

    pybind11::tuple shape(2);
    shape[0] = NR;
    shape[1] = NC;
    pybind11::module bu = pybind11::module::import("delayedarray");
    return bu.attr("SparseNdarray")(shape, content, pybind11::dtype("float64"), pybind11::dtype("uint32"), false, false);
}

void init_common(pybind11::module& m) {
    m.def("extract_dim", &extract_dim);
    m.def("extract_sparse", &extract_sparse);

    m.def("extract_row", &extract_row);
    m.def("extract_column", &extract_column);

    m.def("compute_column_sums", &compute_column_sums);
    m.def("compute_row_sums", &compute_row_sums);
    m.def("compute_column_variances", &compute_column_variances);
    m.def("compute_row_variances", &compute_row_variances);
    m.def("compute_column_medians", &compute_column_medians);
    m.def("compute_row_medians", &compute_row_medians);
    m.def("compute_column_mins", &compute_column_mins);
    m.def("compute_row_mins", &compute_row_mins);
    m.def("compute_column_maxs", &compute_column_maxs);
    m.def("compute_row_maxs", &compute_row_maxs);
    m.def("compute_column_ranges", &compute_column_ranges);
    m.def("compute_row_ranges", &compute_row_ranges);
    m.def("compute_column_nan_counts", &compute_column_nan_counts);
    m.def("compute_row_nan_counts", &compute_row_nan_counts);

    m.def("compute_row_sums_by_group", &compute_row_sums_by_group);
    m.def("compute_column_sums_by_group", &compute_column_sums_by_group);
    m.def("compute_row_variances_by_group", &compute_row_variances_by_group);
    m.def("compute_column_variances_by_group", &compute_column_variances_by_group);
    m.def("compute_row_medians_by_group", &compute_row_medians_by_group);
    m.def("compute_column_medians_by_group", &compute_column_medians_by_group);

    m.def("extract_dense_subset", &extract_dense_subset);
    m.def("extract_sparse_subset", &extract_sparse_subset);

    pybind11::class_<tatami::Matrix<MatrixValue, MatrixIndex>, MatrixPointer>(m, "Matrix");
}
