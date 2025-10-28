# Preparation for Citi Quant Dev Interview

## Projects
- Convergence Analyzer w/ python binding
- Option PnL Calculator
- Implied Vol. Calculator - SGD

# Modules:

- Section I (Foundations)
- Section II (Computational Math)
- Section III (C++ Performance)
- Section IV (Statistics/ML)
- Section V (Advanced Topics)

## Module 1.1: The Axiomatic Approach — Proof-Based Mathematics and Abstract Analysis

### [x] Module 1.1.1: Real Analysis Review - Uniform Convergence And Compactness in $\mathbb{R}^n$
Rigorous foundations of uniform convergence, compactness in ℝⁿ, and function space topology. Establishes the analytical toolkit for understanding convergence properties of numerical algorithms and Monte Carlo estimators.

Key Deliverables:

Proof of Heine-Borel theorem
Uniform vs. pointwise convergence characterization
C++17 convergence testing framework with PyBind11 wrapper

### [ ] Module 1.1.2: Introduction to Measure Theory
Axiomatic construction of probability theory via σ-algebras, measurable functions, and Lebesgue integration. This is the critical prerequisite for rigorously defining stochastic integrals and martingale theory.

Key Deliverables:

Construction of Lebesgue measure on ℝ
Proof of Radon-Nikodym theorem (essential for change of measure)
Definition of conditional expectation using measure theory
C++17 implementation of σ-algebra data structure for filtration management
Application: Why Black-Scholes PDE derivation requires measure-theoretic foundations

### [ ] Module 1.1.3: Functional Analysis for Dynamic Modeling
Study of Banach and Hilbert spaces, L^p spaces, operator theory, and their application to simplifying high-dimensional optimal control problems (HJB equations). Provides the abstract framework for treating infinite-dimensional systems.

Key Deliverables:

Proof of Riesz Representation Theorem
Spectral theory for self-adjoint operators
Hilbert space formulation of optimal portfolio problems
Connection to PDE weak solutions and variational methods
Application: Reformulating portfolio optimization as operator equations

### [ ] Module 1.1.4: Proof-Based Mathematics — Axiomatic Derivation of Financial Theorems
Rigorous mathematical proofs of fundamental theorems in financial mathematics, starting from first principles. Emphasizes derivation over memorization.

Key Deliverables:

Proof of First Fundamental Theorem of Asset Pricing (FTAP): No arbitrage ↔ Equivalent Martingale Measure exists
Proof of Second FTAP: Market completeness ↔ Uniqueness of EMM
Derivation of Black-Scholes PDE from no-arbitrage principle
Proof of risk-neutral valuation formula
Application: Understanding when derivative pricing formulas are valid

### [ ] Module 1.1.5: Advanced Linear Algebra — High-Performance Numerical Kernels
Beyond theoretical linear algebra—focuses on cache-efficient, SIMD-optimized implementation of core operations (matrix multiplication, decomposition) using only C++17 Standard Library. Computational backbone of all numerical methods.

Key Deliverables:

Spectral decomposition (eigenvalue problems) theory and implementation
Singular Value Decomposition (SVD) from scratch in C++17
Tensor algebra for multi-dimensional data (volatility surfaces)
Memory layout optimization: row-major vs. column-major impact on performance
SIMD vectorization opportunities in matrix operations
Application: Covariance matrix estimation for portfolio optimization
PyBind11 wrapper for Python integration

## Module 2.1: Numerical Simulation and Monte Carlo Methods

### [ ] Module 2.1.1: Stochastic Differential Equations (SDEs) and Discretization
Rigorous treatment of SDEs, Itô calculus, and numerical discretization schemes. Foundation for simulating asset price paths.

Key Deliverables:

Itô's Lemma derivation and proof
Euler-Maruyama discretization scheme
Milstein higher-order scheme (incorporates Itô correction term)
Strong vs. weak convergence analysis
C++17 path generator implementation
Application: Simulating Geometric Brownian Motion for option pricing

### [ ] Module 2.1.2: Variance Reduction Techniques
Advanced methods to accelerate Monte Carlo convergence beyond O(N^{-1/2}). Critical for real-time pricing under tight latency constraints.

Key Deliverables:

Mathematical proof of Antithetic Variates variance reduction
Mathematical proof and implementation of Control Variates
Importance Sampling for rare event simulation (deep OTM options)
Stratified Sampling techniques
C++17 optimized implementation (cache-friendly path storage)
Empirical benchmarking: convergence rate comparison
Application: Pricing path-dependent options (Asian, lookback)

### [ ] Module 2.1.3: Quasi-Monte Carlo (QMC) Methods
Replacing pseudo-random numbers with deterministic low-discrepancy sequences. Achieves O(N^{-1}) or better convergence for smooth high-dimensional integrands.

Key Deliverables:

Theory of low-discrepancy sequences (Sobol, Halton, Faure)
Koksma-Hlawka inequality (QMC error bound)
Implementation of Sobol sequence generator in C++17
Randomized QMC for error estimation
Application: Multi-asset basket option pricing
Performance comparison: MC vs. QMC for high-dimensional problems

### [ ] Module 2.1.4: Advanced Greeks Estimation
Efficient calculation of option sensitivities (Greeks) using pathwise derivative method and likelihood ratio method. Essential for real-time delta hedging.

Key Deliverables:

Pathwise method: mathematical derivation and implementation
Likelihood Ratio Method (LRM) for discontinuous payoffs
Smoothing techniques for digital/barrier options
Finite difference Greeks vs. analytic Greeks
C++17 vectorized Greeks calculation
Application: Real-time delta-gamma hedging systems


## Module 2.2: Partial Differential Equations (PDEs) in Financial Modeling

### [ ] Module 2.2.1: PDE Derivation and Transformation Techniques
Rigorous derivation of fundamental PDEs in finance (Black-Scholes, Fokker-Planck, HJB) and transformation to standard heat equation form.

Key Deliverables:

Black-Scholes PDE derivation via no-arbitrage replication
Feynman-Kac formula connecting PDEs and expectations
Heat equation transformation (dimensionless variables)
Boundary conditions for European/American options
Application: Understanding why option pricing is a diffusion problem

### [ ] Module 2.2.2: Finite Difference Method (FDM) — Explicit, Implicit, Crank-Nicolson
Core numerical PDE solver. Discretizes space and time to solve parabolic PDEs backwards from terminal condition. Focus on stability analysis and tri-diagonal solver optimization.

Key Deliverables:

Von Neumann stability analysis for Explicit/Implicit/CN schemes
CFL condition and timestep restrictions
Tri-diagonal matrix solver (Thomas algorithm) in C++17
Use of constexpr for PDE coefficients (risk-free rate, volatility)
Memory-efficient stencil operations
Application: European option pricing via FDM
Performance: sub-millisecond pricing for production systems

### [ ] Module 2.2.3: Free Boundary Problems — American Options
Handling optimal stopping problems where exercise boundary is unknown a priori. Combines PDE methods with optimization.

Key Deliverables:

Linear Complementarity Problem (LCP) formulation
Projected SOR (Successive Over-Relaxation) solver
Penalty method for free boundaries
Least Squares Monte Carlo (LSM) for high-dimensional cases
Longstaff-Schwartz algorithm implementation
Application: American put option pricing and optimal exercise strategy

### [ ] Module 2.2.4: High-Dimensional Solvers — FFT and Deep Galerkin Methods
Description: Beyond traditional FDM—advanced techniques for curse of dimensionality. FFT methods for Lévy processes and Deep Learning for non-linear high-dimensional PDEs.


Key Deliverables:

Fast Fourier Transform (FFT) pricing via characteristic functions
Carr-Madan formula for European options
COS method (Fourier cosine expansion)
Deep Galerkin Method (DGM): neural network PDE solver
Physics-Informed Neural Networks (PINNs) for HJB equations
GPU acceleration via C++ CUDA integration
Application: Multi-asset options, stochastic volatility models (Heston)

## Module 3.1: Object-Oriented Programming (OOP) in C++ for Financial Modeling

### [ ] Module 3.1.1: OOP Fundamentals — Inheritance, Polymorphism, Encapsulation
Description: Designing robust class hierarchies for financial instruments. Balancing abstraction with performance (runtime vs. compile-time polymorphism).


Key Deliverables:

FinancialInstrument base class design
Virtual functions vs. template-based polymorphism
Derived classes: EuropeanOption, AmericanOption, ExoticOption
Payoff functor pattern for flexibility
Application: Unified pricing interface for heterogeneous portfolios

### [ ] Module 3.1.2: Design Patterns for Quantitative Systems
Description: Classic software engineering patterns applied to finance. Emphasizes maintainability and extensibility without sacrificing performance.

Key Deliverables:

Factory Pattern: Creating instruments from market data
Strategy Pattern: Selecting numerical methods (FDM vs. MC) dynamically
Observer Pattern: Market data feed handler → pricing engine propagation
Singleton Pattern: Configuration management
Template Method Pattern: Pricing workflow with customizable steps
Application: Production-grade pricing library architecture

### [ ] Module 3.1.3: Building the Financial Instrument Hierarchy
Description: Complete implementation of a type-safe, extensible instrument class system with compile-time optimization where possible.


Key Deliverables:

Class diagram: options, futures, swaps, bonds
Curiously Recurring Template Pattern (CRTP) for compile-time polymorphism
Type traits and SFINAE for compile-time dispatch
Move semantics and perfect forwarding for zero-copy construction
Application: Multi-asset portfolio with heterogeneous instruments

## Module 3.2: C++ Architecture and Optimization for HFT (C++17 Mandate)

### [ ] Module 3.2.1: Compile-Time Optimization — constexpr and Template Metaprogramming
Description: Shifting computation from runtime to compile-time. Essential for nanosecond-level latency requirements.

Key Deliverables:

constexpr functions for mathematical constants and PDE coefficients
Template metaprogramming for loop unrolling
if constexpr for compile-time branching
Type-level computation (compile-time factorial, Fibonacci)
Application: Pre-computed Greeks tables, compile-time matrix sizes
Benchmarking: runtime vs. compile-time performance comparison

### [ ] Module 3.2.2: Memory Management and Cache Optimization
Description: Understanding CPU cache hierarchy (L1/L2/L3) and designing data structures for cache locality. Deterministic memory allocation for HFT.


Key Deliverables:

Memory arenas and pool allocators (eliminate heap fragmentation)
Stack allocation preference (std::array vs. std::vector)
Cache line alignment (alignas specifier)
False sharing prevention in multi-threaded code
Data-oriented design (SoA vs. AoS layout)
Profiling tools: perf, valgrind --tool=cachegrind
Application: Tick data circular buffer for market data handler

### [ ] Module 3.2.3: Concurrency and Lock-Free Programming
Description: Multi-threaded systems for parallel pricing and order execution. Lock-free data structures using C++11 atomics to avoid mutex contention.


Key Deliverables:

Thread pools with task queues
std::atomic operations and memory ordering
Lock-free ring buffer (SPSC/MPMC)
Thread affinity (pinning threads to CPU cores)
Memory barriers and acquire-release semantics
Application: Parallel Monte Carlo path generation
Benchmarking: speedup analysis (Amdahl's Law)

### [ ] Module 3.2.4: The LMAX Disruptor Pattern for High-Throughput Messaging
Description: Industry-standard architecture for passing messages between HFT system components (Feed Handler → Signal Engine → OMS) with minimal latency.


Key Deliverables:

Ring buffer mechanics and sequence barriers
Wait strategies (busy spin vs. yielding)
Event processors and dependency chains
C++17 implementation of core Disruptor concepts
Application: Market data → signal → order flow pipeline
Throughput: 6M+ messages/second target

Module 3.3.1: The Accelerator Module Principle
Description: Design philosophy: Python for research/backtesting, C++ for production. Creating seamless bridges between high-level analysis and low-level execution.
Key Deliverables:

When to use Python vs. C++ (workflow decision tree)
Profiling Python code to identify bottlenecks
Extracting hot paths for C++ re-implementation
API design for mixed-language systems

## Module 3.3: Python Interoperability — Wrapping Low-Latency C++ Kernels

### [ ] Module 3.3.1: The Accelerator Module Principle
Description: Design philosophy: Python for research/backtesting, C++ for production. Creating seamless bridges between high-level analysis and low-level execution.

Key Deliverables:

When to use Python vs. C++ (workflow decision tree)
Profiling Python code to identify bottlenecks
Extracting hot paths for C++ re-implementation
API design for mixed-language systems

### [ ] Module 3.3.2: PyBind11 — Header-Only C++ Bindings
Description: Practical guide to exposing C++ classes and functions to Python with minimal overhead. Preferred over Boost.Python for simplicity and binary size.


Key Deliverables:

Basic type conversion (scalars, strings, vectors)
Binding C++ classes with constructors and methods
Exposing STL containers (std::vector → Python list)
NumPy array integration (zero-copy views)
Handling C++ exceptions in Python
CMake build system integration
Application: Every numerical module wrapped for Python access

### [ ] Module 3.3.3: Performance Benchmarking — Python vs. C++
Description: Rigorous methodology for measuring and comparing performance across language boundaries.

Key Deliverables:

Timing C++ code (steady_clock vs. rdtsc)
Python timeit module for reliable benchmarking
Overhead analysis of Python-C++ calls
When wrapping provides 10×, 100×, 1000× speedups
Case study: Monte Carlo pricer speedup analysis


## Module 4.1: Time Series Analysis in Finance

### [ ] Module 4.1.1: Non-Stationary Processes — Unit Roots, Cointegration, ECM
Description: Beyond ARMA models—handling non-stationary financial time series. Critical for pairs trading and statistical arbitrage.

Key Deliverables:

Augmented Dickey-Fuller (ADF) test for unit roots
Engle-Granger two-step cointegration procedure
Johansen cointegration test (multivariate)
Error Correction Models (ECM) for mean reversion
Structural Vector Autoregression (SVAR)
C++17 implementation of ADF test
Application: Identifying cointegrated asset pairs


### [ ] Module 4.1.2: Volatility Models — GARCH and Stochastic Volatility
Description: Modeling time-varying volatility (volatility clustering). Essential for risk forecasting and VaR calculation.

Key Deliverables:

ARCH model derivation
GARCH(p,q) model specification and estimation
Maximum Likelihood Estimation (MLE) for GARCH parameters
Stochastic Volatility (SV) models (Heston, SABR)
C++17 GARCH optimizer (quasi-Newton methods)
Application: Forecasting realized volatility for option pricing

### [ ] Module 4.1.3: State-Space Models and Kalman Filtering
Description: Optimal recursive estimation of hidden states from noisy observations. Bayesian filtering framework.

Key Deliverables:

State-space representation (observation + transition equations)
Kalman Filter derivation (prediction + update steps)
Kalman Smoother (backward pass)
Extended Kalman Filter (EKF) for non-linear systems
Unscented Kalman Filter (UKF) via sigma points
C++17 implementation (matrix-free formulation for speed)
Application: Estimating true price from noisy tick data

## Module 4.2: Markov and Hidden Markov Models (HMMs)

### [ ] Module 4.2.1: Foundations — Markov Property and Transition Matrices
Description: Discrete-state continuous-time and discrete-time Markov chains. Foundation for regime-switching models.


Key Deliverables:

Markov property (memorylessness)
Chapman-Kolmogorov equations
Stationary distributions and ergodicity
Absorbing states and transient behavior
Application: Credit rating transitions

### [ ] Module 4.2.2: Core HMM Algorithms — Forward-Backward and Viterbi
Description: The three fundamental HMM problems: evaluation, decoding, learning. Efficient dynamic programming solutions.


Key Deliverables:

Forward algorithm (filtering): P(observations | model)
Backward algorithm: marginal state probabilities
Viterbi algorithm: most likely state sequence
Baum-Welch (EM) for parameter learning
Linear-memory implementations (O(T) space instead of O(T²))
C++17 log-space arithmetic (numerical stability)
Application: Market regime identification (bull/bear/volatile)


### [ ] Module 4.2.3: Advanced HMMs — Time-Varying Parameters and High-Frequency Applications
Description: Extending HMMs to handle non-stationary regimes. Critical for adaptive trading systems.


Key Deliverables:

Adaptive HMMs with time-varying transition matrices
Zero-delay HMMs for real-time inference
Recursive parameter estimation (online learning)
Multivariate HMMs for FX rate modeling
Application: Long-memory effects in volatility (|returns|)
Application: High-frequency regime detection

## Module 4.3: Advanced Bayesian Statistics

### [ ] Module 4.3.1: Foundations — Bayesian Inference and Conjugate Priors
Description: Bayesian paradigm for uncertainty quantification. Prior → Likelihood → Posterior framework.


Key Deliverables:

Bayes' theorem and sequential updating
Conjugate prior families (Beta-Binomial, Normal-Normal, Gamma-Poisson)
Posterior predictive distributions
Bayesian point estimates (MAP, posterior mean, posterior median)
Credible intervals vs. confidence intervals
Application: Bayesian portfolio allocation with parameter uncertainty

### [ ] Module 4.3.2: Computational Bayesian Methods — MCMC and Diagnostics
Description: Sampling from complex posterior distributions when closed-form solutions don't exist.


Key Deliverables:

Metropolis-Hastings algorithm (random walk, independence sampler)
Gibbs Sampler for conditional distributions
Hamiltonian Monte Carlo (HMC) for high-dimensional posteriors
Convergence diagnostics (Gelman-Rubin R^\hat{R}
R^, effective sample size)

Thinning and burn-in strategies
C++17 MCMC sampler with parallel chains
Application: Bayesian inference for GARCH parameters

### [ ] Module 4.3.3: Bayesian Non-Parametrics — Dirichlet Process Mixtures
Description: Frontier topic: Infinite-capacity models that adapt complexity to data. Model-free approach to volatility and Greeks.


Key Deliverables:

Dirichlet Process (DP) definition and stick-breaking construction
Chinese Restaurant Process (CRP) metaphor
Dirichlet Process Mixture Models (DPM) for clustering
Posterior inference via MCMC (Neal's Algorithm 8)
Application: Time-varying volatility without parametric assumptions
Application: Model-free Greeks estimation from option prices (avoids model risk)
Research frontier: When to use BNP vs. parametric models

## Module 5.1: Applied Graph Theory for Portfolio Optimization

### [ ] Module 5.1.1: Graph Representation of Financial Networks
Description: Modeling correlation structure as a graph. Vertices = assets, edges = correlations above threshold.


Key Deliverables:

Adjacency matrix and weighted graph construction
Threshold selection (correlation cutoff)
Graph visualization techniques
Application: Visualizing market structure during crises

### [ ] Module 5.1.2: Graph Algorithms — Cliques and Independent Sets
Description: Finding highly correlated clusters (cliques) vs. diversified sets (independent sets). Directly applicable to portfolio construction.


Key Deliverables:

Maximal clique problem (NP-hard, but tractable for financial networks)
Bron-Kerbosch algorithm for maximal cliques
Maximal independent set problem
Greedy approximation algorithms
C++17 graph algorithm library (from scratch)
Application: Diversification via independent sets

### [ ] Module 5.1.3: Empirical Portfolio Optimization via Graph Structure
Description: Novel approach: Using graph topology to maximize Sharpe ratio.
Key Deliverables:

Brute-force correlation threshold optimization (0.0 to 1.0)
Sharpe ratio maximization via independent vertex sets
Empirical finding: optimal threshold ≈ 0.6 for many markets
Comparison to Markowitz mean-variance optimization
Computational complexity analysis
Application: Robust portfolio construction with minimal correlation

## Module 5.2: Knot Theory and Topological Data Analysis (TDA)

### [ ] Module 5.2.1: Introduction to Topology and Invariants
Description: Topological concepts applied to financial data. Focus on properties preserved under continuous deformations.

Key Deliverables:

Topological spaces and continuous maps
Homotopy and homology theory (intuitive)
Persistent homology: multi-scale structure detection
Betti numbers (connected components, holes, voids)
Application: Detecting topological features in volatility surfaces

Module 5.2.2: Knot Data Analysis (KDA) and Gauss Link Integral
Description: Frontier research: Quantitative knot theory for structural analysis of complex datasets.
Key Deliverables:

Knot invariants (crossing number, Alexander polynomial)
Multiscale Gauss Link Integral (mGLI) for 3D point clouds
Topological signatures as features
Application: Protein-ligand binding (transferable to market data)

### [ ] Module 5.2.3: TDA Applications in Finance — Market Interconnectedness
Description: Speculative/research module: Applying TDA to understand systemic risk and regime changes.

Key Deliverables:

Embedding time series in topological spaces (Takens' theorem)
Persistent homology of correlation matrices
Detecting topological phase transitions (regime shifts)
Early warning signals for market instability
Research questions: Can topological invariants predict crashes?
Literature review: Current state of TDA in finance
