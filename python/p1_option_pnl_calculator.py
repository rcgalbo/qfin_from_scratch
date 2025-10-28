import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple
from scipy.stats import norm


@dataclass
class Position:
    symbol: str  # "AAPL", "TSLA", etc.
    option_type: str  # "call" or "put"
    K: float  # Strike price
    T: int  #  trading days until expiration
    quantity: int  # number of contracts
    sigma: float  # implied volatilty as a decimal
    purchase_price: float  # the price the options were purchased for
    price_moves: List[Tuple[float, int]]  # Tuple(S: Price Update, Days Elapsed)

    def __post_init__(self):
        self.T_YEARS = self.T / 252


class Option:
    """
    A class to calculate option prices using the Black-Scholes formula.
    Arguments:
    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate
    sigma: Volatility
    """

    def __init__(
        self,
        Positions: List[Position],
        initial_stock_price: float,
        r: float,  # risk free rate
    ):
        self.Positions = Positions
        self.initial_stock_price = initial_stock_price
        self.r = r
        self.op = pd.DataFrame(
            columns=["symbol", "elapsed", "S", "price", "pnl"]
        )  # DataFrame for option prices

    def __post_init__(self):
        self.op.set_index(["symbol", "elapsed"])

    def d1(self, S: float, K: float, T: int, r, sigma) -> float:
        """Calculate d1 for Black-Scholes formula"""
        return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    def d2(self, d1, T, sigma) -> float:
        """Calculate d2 from d1"""
        return d1 - sigma * np.sqrt(T)

    def call_price(
        self, S: float, K: float, T: int, r: float, d1: float, d2: float
    ) -> float:
        """Calculate call option price using Black-Scholes formula"""
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    def put_price(
        self, K: float, T: float, S: float, r: float, d1: float, d2: float
    ) -> float:
        """Calculate put option price using Black-Scholes formula"""
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    def calculate_pnl(
        self, current_value: float, purchase_price: float, quantity: int
    ) -> float:
        """
        Calculate PnL for a specific option
        """
        total_purchase_price = purchase_price * quantity
        total_current_price = current_value * quantity
        return total_current_price - total_purchase_price
    
    def price_options(self):
        """
        Calculate option prices for all positions and store in self.op"""
        for p in self.Positions:
            for S, elapsed in p.price_moves:
                d1 = self.d1(S, p.K, p.T_YEARS, self.r, p.sigma)
                d2 = self.d2(d1, p.T_YEARS, p.sigma)
                cp = self.call_price(S, p.K, p.T_YEARS, self.r, d1, d2)
                pp = self.put_price(p.K, p.T_YEARS, S, self.r, d1, d2)
                if p.option_type == "call":
                    new_row = {
                        "symbol": p.symbol,
                        "elapsed": elapsed,
                        "purchase_price": p.purchase_price,
                        "S": S,
                        "price": cp,
                        "pnl": self.calculate_pnl(
                            current_value=cp,
                            purchase_price=p.purchase_price,
                            quantity=p.quantity
                        )
                    }
                    self.op = pd.concat(
                        [self.op, pd.DataFrame([new_row])], ignore_index=True
                    )
                if p.option_type == "put":
                    new_row = {
                        "symbol": p.symbol,
                        "elapsed": elapsed,
                        "purchase_price": p.purchase_price,
                        "S": S,
                        "price": pp,
                        "pnl": self.calculate_pnl(
                            current_value=pp,
                            purchase_price=p.purchase_price,
                            quantity=p.quantity
                        ),
                    }
                    self.op = pd.concat(
                        [self.op, pd.DataFrame([new_row])], ignore_index=True
                    )
                




if __name__ == "__main__":
    pos = [
        Position(
            symbol="AAPL",
            option_type="call",
            K=100,
            T=20,
            quantity=1,
            sigma=0.5,
            purchase_price=5,
            price_moves=[(120, 1), (150, 5), (180, 10), (200, 15), (250, 20)],
        ),
        Position(
            symbol="TSLA",
            option_type="call",
            K=100,
            T=20,
            quantity=1,
            sigma=0.5,
            purchase_price=20,
            price_moves=[(80, 1), (120, 10), (150, 15), (200, 20),  (250, 25)],
        ),
    ]
    opt = Option(pos, initial_stock_price=100, r=0.05)
    opt.price_options()
    print(opt.op)
