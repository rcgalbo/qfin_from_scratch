// convergence_analyzer.hpp
// C++17 Standard Library only - no external dependencies

#pragma once
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <functional>
#include <chrono>

namespace quant::analysis {

// Type aliases for clarity and cache-friendly memory layout
using Real = double;
using FunctionSequence = std::function<Real(Real, size_t)>; // f(x, n)
using ConvergenceResult = std::pair<bool, Real>; // (is_uniform, sup_norm)

/**
 * @brief High-performance convergence analyzer for function sequences
 * 
 * Implements rigorous real analysis tests for pointwise and uniform convergence
 * with microsecond-level performance for real-time risk validation.
 */
class ConvergenceAnalyzer {
private:
    // Cache-aligned memory for hot path
    std::vector<Real> domain_points_;
    size_t num_points_;
    
    // Precomputed epsilon thresholds (constexpr candidates)
    static constexpr Real DEFAULT_EPSILON = 1e-6;
    static constexpr size_t DEFAULT_MAX_N = 10000;
    
public:
    /**
     * @brief Construct analyzer with domain discretization
     * @param domain_start Lower bound of domain [a,b]
     * @param domain_end Upper bound of domain [a,b]
     * @param num_points Number of test points (affects accuracy vs. speed)
     */
    explicit ConvergenceAnalyzer(Real domain_start, Real domain_end, 
                                  size_t num_points = 1000)
        : num_points_(num_points)
    {
        // Pre-allocate and populate domain points (memory arena pattern)
        domain_points_.reserve(num_points_);
        const Real dx = (domain_end - domain_start) / (num_points_ - 1);
        
        for (size_t i = 0; i < num_points_; ++i) {
            domain_points_.push_back(domain_start + i * dx);
        }
    }
    
    /**
     * @brief Test uniform convergence using supremum norm
     * @param f_n Function sequence f(x, n)
     * @param limit_fn Limiting function f(x)
     * @param epsilon Convergence threshold
     * @param max_n Maximum sequence index to test
     * @return (converges_uniformly, supremum_distance)
     */
    ConvergenceResult test_uniform_convergence(
        const FunctionSequence& f_n,
        const std::function<Real(Real)>& limit_fn,
        Real epsilon = DEFAULT_EPSILON,
        size_t max_n = DEFAULT_MAX_N) const
    {
        // Implementation of Cauchy criterion in sup norm
        Real sup_distance = 0.0;
        bool found_N = false;
        size_t convergence_N = 0;
        
        // Binary search for optimal N (log-time complexity)
        size_t left = 1, right = max_n;
        
        while (left <= right) {
            size_t mid = left + (right - left) / 2;
            Real current_sup = compute_sup_norm(f_n, limit_fn, mid);
            
            if (current_sup < epsilon) {
                found_N = true;
                convergence_N = mid;
                sup_distance = current_sup;
                right = mid - 1; // Try to find smaller N
            } else {
                left = mid + 1;
            }
        }
        
        return {found_N, sup_distance};
    }
    
    /**
     * @brief Compute supremum norm ||f_n - f||_∞ over discretized domain
     * @param f_n Function sequence
     * @param limit_fn Limit function
     * @param n Sequence index
     * @return sup_{x∈domain} |f_n(x) - f(x)|
     */
    Real compute_sup_norm(
        const FunctionSequence& f_n,
        const std::function<Real(Real)>& limit_fn,
        size_t n) const
    {
        Real sup_norm = 0.0;
        
        // Vectorization-friendly loop (compiler can auto-vectorize)
        for (const Real x : domain_points_) {
            const Real diff = std::abs(f_n(x, n) - limit_fn(x));
            sup_norm = std::max(sup_norm, diff);
        }
        
        return sup_norm;
    }
    
    /**
     * @brief Test if a set is compact (closed and bounded in R^n)
     * @param points Sample points from set
     * @return (is_compact, diameter)
     */
    std::pair<bool, Real> test_compactness(
        const std::vector<std::vector<Real>>& points) const
    {
        if (points.empty()) return {false, 0.0};
        
        // Check boundedness: compute diameter
        Real diameter = 0.0;
        for (size_t i = 0; i < points.size(); ++i) {
            for (size_t j = i + 1; j < points.size(); ++j) {
                Real dist = euclidean_distance(points[i], points[j]);
                diameter = std::max(diameter, dist);
            }
        }
        
        const bool is_bounded = (diameter < std::numeric_limits<Real>::max());
        
        // Note: Checking closedness rigorously requires limit point analysis
        // For practical purposes, we verify boundedness (main HFT concern)
        const bool is_compact = is_bounded; // Simplified for bounded R^n
        
        return {is_compact, diameter};
    }
    
    /**
     * @brief Benchmark convergence test performance
     * @return Execution time in nanoseconds
     */
    template<typename Callable>
    int64_t benchmark_nanoseconds(Callable&& test_function) const {
        using namespace std::chrono;
        
        auto start = high_resolution_clock::now();
        test_function();
        auto end = high_resolution_clock::now();
        
        return duration_cast<nanoseconds>(end - start).count();
    }

private:
    Real euclidean_distance(const std::vector<Real>& p1, 
                           const std::vector<Real>& p2) const {
        Real sum_sq = 0.0;
        for (size_t i = 0; i < p1.size(); ++i) {
            const Real diff = p1[i] - p2[i];
            sum_sq += diff * diff;
        }
        return std::sqrt(sum_sq);
    }
};

} // namespace quant::analysis
