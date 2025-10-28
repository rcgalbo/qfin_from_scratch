import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Normal
from adabelief_pytorch import AdaBelief
from datetime import datetime
import time


class AdaptiveIVSolver:
    """
    Implied Volatility Solver using Adaptive Gradient Descent (Adam/AdaBelief)
    Based on the research paper methodology
    """

    def __init__(self, risk_free_rate=0.05, optimizer_type="adam"):
        """
        Args:
            risk_free_rate: Risk-free interest rate
            optimizer_type: 'adam' or 'adabelief'
        """
        self.r = risk_free_rate
        self.norm = Normal(0, 1)
        self.optimizer_type = optimizer_type.lower()

    def black_scholes(self, S, K, T, r, sigma, is_call):
        """
        Black-Scholes pricing formula
        All inputs must be PyTorch tensors for autograd
        """
        sqrt_T = torch.sqrt(T + 1e-10)

        d1 = (torch.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T + 1e-10)
        d2 = d1 - sigma * sqrt_T

        call_price = S * self.norm.cdf(d1) - K * torch.exp(-r * T) * self.norm.cdf(d2)
        put_price = K * torch.exp(-r * T) * self.norm.cdf(-d2) - S * self.norm.cdf(-d1)

        return torch.where(is_call, call_price, put_price)

    def solve_batch_iv(
        self,
        market_prices,
        S,
        K,
        T,
        r,
        is_call,
        initial_sigma=0.4,
        learning_rate=0.001,
        beta1=0.9,
        beta2=0.999,
        eps=1e-7,
        max_iterations=2000,
        convergence_threshold=1e-4,
        check_every=10,
    ):
        """
        Solve implied volatility using adaptive gradient descent

        Following the paper's methodology:
        - sigma is the trainable parameter (requires_grad=True)
        - Loss function: h(sigma) = (c_model - c_market)²
        - Optimizer: Adam with paper's hyperparameters
        - Initial guess: sigma0 = 0.4

        Args:
            market_prices: Observed market prices
            S: Underlying prices
            K: Strike prices
            T: Time to expiration
            r: Risk-free rates
            is_call: Boolean tensor for call/put
            initial_sigma: Initial volatility guess (default 0.4 per paper)
            learning_rate: eta = 0.001 (paper default)
            beta1: beta1 = 0.9 (paper default)
            beta2: beta2 = 0.999 (paper default)
            eps: eps = 10⁻⁷ (paper default)
            max_iterations: Maximum optimization steps
            convergence_threshold: |c_j,n - c_j,n-1| < 10^-4
            check_every: Check convergence every N iterations
        """
        n_options = len(market_prices)

        print(f"ADAPTIVE GRADIENT DESCENT IV SOLVER")
        print(f"Options to solve: {n_options}")
        print(f"Optimizer: {self.optimizer_type.upper()}")
        print(f"Initial σ₀: {initial_sigma}")
        print(f"Learning rate η: {learning_rate}")
        print(f"Max iterations: {max_iterations}")
        print(f"Convergence threshold: {convergence_threshold}")

        # Initialize σ as trainable parameter (CRITICAL: requires_grad=True)
        sigma = torch.full(
            (n_options,), initial_sigma, dtype=torch.float32, requires_grad=True
        )

        # Initialize optimizer with paper's hyperparameters
        if self.optimizer_type == "adam":
            optimizer = torch.optim.Adam(
                [sigma], lr=learning_rate, betas=(beta1, beta2), eps=eps
            )
        elif self.optimizer_type == "adabelief":
            optimizer = AdaBelief(
                [sigma], lr=learning_rate, betas=(beta1, beta2), eps=eps
            )
        else:
            raise ValueError(f"Unknown optimizer: {self.optimizer_type}")

        # Track convergence
        converged = torch.zeros(n_options, dtype=torch.bool)
        iterations_taken = torch.zeros(n_options, dtype=torch.int32)
        previous_prices = torch.zeros(n_options)

        start_time = time.time()

        # Optimization loop (Algorithm 1 from paper)
        for iteration in range(max_iterations):

            # Step 1: Zero gradients (clear from previous iteration)
            optimizer.zero_grad()

            # Step 2: Forward pass - calculate model prices
            model_prices = self.black_scholes(S, K, T, r, sigma, is_call)

            # Step 3: Calculate loss function h(sigma) = (c_model - c_market)²
            # Using MSE for batch processing
            loss = torch.mean((model_prices - market_prices) ** 2)

            # Step 4: Backward pass - compute grad_h(sigma) via Automatic Differentiation
            loss.backward()

            # Step 5: Optimizer step - apply Adam update rule (Equation 10 in paper)
            optimizer.step()

            # Clamp sigma to reasonable bounds to prevent numerical issues
            with torch.no_grad():
                sigma.data = torch.clamp(sigma.data, 0.001, 5.0)

            # Check convergence periodically (every check_every iterations)
            if iteration % check_every == 0:
                with torch.no_grad():
                    # Convergence criterion: |c_j,n - c_j,n-1| < threshold
                    price_change = torch.abs(model_prices - previous_prices)
                    newly_converged = (price_change < convergence_threshold) & (
                        ~converged
                    )
                    converged = converged | newly_converged
                    iterations_taken[newly_converged] = iteration
                    previous_prices = model_prices.clone()

                    # Progress update
                    if iteration % 100 == 0:
                        n_converged = converged.sum().item()
                        avg_loss = loss.item()
                        print(
                            f"Iteration {iteration:4d} | Converged: {n_converged:5d}/{n_options} "
                            f"({100*n_converged/n_options:5.1f}%) | Loss: {avg_loss:.2e}"
                        )

                    # Early stopping if all converged
                    if converged.all():
                        elapsed = time.time() - start_time
                        print(
                            f"\nAll options converged in {iteration} iterations ({elapsed:.2f}s)"
                        )
                        break
        else:
            # Max iterations reached
            elapsed = time.time() - start_time
            n_converged = converged.sum().item()
            print(f"\n Reachedmax iterations ({max_iterations})")
            print(
                f"Converged: {n_converged}/{n_options} ({100*n_converged/n_options:.1f}%)"
            )
            print(f"Time elapsed: {elapsed:.2f}s")

        # Calculate final statistics
        with torch.no_grad():
            final_prices = self.black_scholes(S, K, T, r, sigma, is_call)
            pricing_errors = torch.abs(final_prices - market_prices)
            mae = pricing_errors.mean().item()

            print(f"\n{'='*70}")
            print(f"RESULTS SUMMARY")
            print(f"{'='*70}")
            print(f"Convergence Rate (CR): {100*converged.sum().item()/n_options:.2f}%")
            print(
                f"Non-Convergence Rate (NC): {100*(1-converged.sum().item()/n_options):.2f}%"
            )
            print(f"Mean Absolute Error (MAE): {mae:.6f}")
            print(
                f"Average iterations: {iterations_taken[converged].float().mean():.1f}"
            )
            print(f"Total time: {elapsed:.2f}s")
            print(f"Options/second: {n_options/elapsed:.0f}")

        return {
            "sigma": sigma.detach().clone(),
            "converged": converged,
            "iterations": iterations_taken,
            "final_prices": final_prices.detach(),
            "pricing_errors": pricing_errors,
            "mae": mae,
        }


def prepare_options_data(df):
    """Prepare dataframe for IV calculation"""
    print("\n" + "=" * 70)
    print("DATA PREPARATION")
    print("=" * 70)

    # Convert dates
    df["date"] = pd.to_datetime(df["date"])
    df["expiration"] = pd.to_datetime(df["expiration"])

    # Calculate time to expiration in years
    df["T"] = (df["expiration"] - df["date"]).dt.days / 365.0

    # Calculate mid price
    df["market_price"] = (df["bid"] + df["ask"]) / 2.0

    # Data filtering
    original_count = len(df)
    df = df[df["T"] > 0].copy()
    df = df[df["T"] < 3].copy()
    df = df[df["market_price"] > 0].copy()
    df = df[df["bid"] > 0].copy()
    df = df[df["strike"] > 0].copy()

    removed = original_count - len(df)
    print(f"Original rows: {original_count}")
    print(f"Removed: {removed} ({100*removed/original_count:.1f}%)")
    print(f"Final dataset: {len(df)} options")
    print(f"  Symbols: {df['act_symbol'].nunique()}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Expirations: {df['expiration'].nunique()}")

    return df


def compute_everything_adaptive_gd(
    df,
    underlying_prices=None,
    risk_free_rate=0.05,
    optimizer_type="adam",
    initial_sigma=0.4,
):
    """
    MAIN FUNCTION: Complete pipeline using Adaptive Gradient Descent

    Following the paper's recommendations:
    1. Use Adam optimizer with sigma0 = 0.4
    2. Calculate IV via gradient descent (not Newton-Raphson)
    3. Use automatic differentiation for all Greeks
    4. Process entire dataset in parallel

    Args:
        df: Options dataframe
        underlying_prices: Underlying price mapping (or None to extract from data)
        risk_free_rate: Risk-free rate
        optimizer_type: 'adam' or 'adabelief'
        initial_sigma: Initial volatility guess (0.4 recommended by paper)
    """

    # Prepare data
    df = prepare_options_data(df)

    # Convert to PyTorch tensors
    print("\nConverting to tensors...")
    S = torch.tensor(df["underlying_price"].values, dtype=torch.float32)
    K = torch.tensor(df["strike"].values, dtype=torch.float32)
    T = torch.tensor(df["T"].values, dtype=torch.float32)
    market_price = torch.tensor(df["market_price"].values, dtype=torch.float32)
    r = torch.full_like(S, risk_free_rate)
    is_call = torch.tensor(df["call_put"].values == "C", dtype=torch.bool)

    print(f"✓ Converted {len(df)} options to tensors")

    # Initialize solver
    solver = AdaptiveIVSolver(
        risk_free_rate=risk_free_rate, optimizer_type=optimizer_type
    )

    # Solve for implied volatility using adaptive gradient descent
    iv_results = solver.solve_batch_iv(
        market_prices=market_price,
        S=S,
        K=K,
        T=T,
        r=r,
        is_call=is_call,
        initial_sigma=initial_sigma,  # Paper recommends 0.4
    )

    # Add IV results to dataframe
    df["implied_volatility"] = iv_results["sigma"].numpy()
    df["iv_converged"] = iv_results["converged"].numpy()
    df["iv_iterations"] = iv_results["iterations"].numpy()
    df["bs_price"] = iv_results["final_prices"].numpy()
    df["pricing_error"] = iv_results["pricing_errors"].numpy()
    df["pricing_error_pct"] = 100 * df["pricing_error"] / df["market_price"]

    return df


def print_detailed_summary(df):
    """Print detailed statistics following paper's metrics"""
    print("\n" + "=" * 70)
    print("DETAILED PERFORMANCE METRICS")
    print("=" * 70)

    df_conv = df[df["iv_converged"]]

    # Overall Statistics
    print(f"\n{'Overall Performance':-^70}")
    print(f"Total options: {len(df)}")
    print(f"Converged: {len(df_conv)} ({100*len(df_conv)/len(df):.2f}%)")
    print(f"Non-Convergence Rate (NC): {100*(1-len(df_conv)/len(df)):.4f}%")

    # Implied Volatility Statistics
    print(f"\n{'Implied Volatility Distribution':-^70}")
    print(f"Mean IV: {df_conv['implied_volatility'].mean():.6f}")
    print(f"Median IV: {df_conv['implied_volatility'].median():.6f}")
    print(f"Std Dev: {df_conv['implied_volatility'].std():.6f}")
    print(f"Min IV: {df_conv['implied_volatility'].min():.6f}")
    print(f"Max IV: {df_conv['implied_volatility'].max():.6f}")

    # Pricing Accuracy (Paper's MAE metric)
    print(f"\n{'Pricing Accuracy':-^70}")
    print(f"Mean Absolute Error (MAE): {df_conv['pricing_error'].mean():.6f}")
    print(f"RMSE: {np.sqrt((df_conv['pricing_error']**2).mean()):.6f}")
    print(f"Mean % Error: {df_conv['pricing_error_pct'].abs().mean():.4f}%")

    # Convergence Statistics
    print(f"\n{'Convergence Statistics':-^70}")
    print(f"Average iterations: {df_conv['iv_iterations'].mean():.1f}")
    print(f"Median iterations: {df_conv['iv_iterations'].median():.0f}")
    print(f"Max iterations: {df_conv['iv_iterations'].max()}")

    # By Symbol
    print(f"\n{'Performance by Symbol':-^70}")
    for symbol in sorted(df["act_symbol"].unique()):
        symbol_df = df_conv[df_conv["act_symbol"] == symbol]
        if len(symbol_df) > 0:
            print(
                f"{symbol:6s}: {len(symbol_df):5d} options | "
                f"Avg IV: {symbol_df['implied_volatility'].mean():.4f} | "
                f"MAE: {symbol_df['pricing_error'].mean():.6f}"
            )

