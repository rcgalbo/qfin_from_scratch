// convergence_bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include "convergence_analyzer.hpp"

namespace py = pybind11;
using namespace quant::analysis;

PYBIND11_MODULE(convergence_cpp, m) {
    m.doc() = "High-performance convergence analysis for quantitative finance";
    
    py::class_<ConvergenceAnalyzer>(m, "ConvergenceAnalyzer")
        .def(py::init<Real, Real, size_t>(),
             py::arg("domain_start"),
             py::arg("domain_end"),
             py::arg("num_points") = 1000,
             "Initialize convergence analyzer with domain discretization")
        
        .def("test_uniform_convergence",
             &ConvergenceAnalyzer::test_uniform_convergence,
             py::arg("f_n"),
             py::arg("limit_fn"),
             py::arg("epsilon") = ConvergenceAnalyzer::DEFAULT_EPSILON,
             py::arg("max_n") = ConvergenceAnalyzer::DEFAULT_MAX_N,
             "Test uniform convergence of function sequence")
        
        .def("compute_sup_norm",
             &ConvergenceAnalyzer::compute_sup_norm,
             "Compute supremum norm over domain")
        
        .def("test_compactness",
             &ConvergenceAnalyzer::test_compactness,
             "Test if point set is compact (bounded)")
        
        .def("benchmark_nanoseconds",
             &ConvergenceAnalyzer::benchmark_nanoseconds<std::function<void()>>,
             "Benchmark execution time in nanoseconds");
}
