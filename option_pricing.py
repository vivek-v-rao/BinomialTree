import math
from typing import Literal

def crr_binomial_option(
    s0: float,
    k: float,
    r: float,
    q: float,
    sigma: float,
    t: float,
    n_steps: int,
    option_type: Literal["call", "put"] = "call",
    exercise:    Literal["european", "american"] = "european",
) -> float:
    """
    Price a call or put using the CRR binomial tree with continuous dividend yield.
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")

    dt = t / n_steps
    if dt <= 0:
        raise ValueError("T must be positive")

    # CRR up/down factors
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u

    # Risk-neutral probability with continuous dividend yield q
    disc = math.exp(-r * dt)
    growth = math.exp((r - q) * dt)
    p = (growth - d) / (u - d)

    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Risk-neutral probability out of bounds: p={p:.6f}")

    # Terminal stock prices and payoffs
    values = []
    for j in range(n_steps + 1):
        s = s0 * (u ** j) * (d ** (n_steps - j))
        if option_type == "call":
            payoff = max(s - k, 0.0)
        elif option_type == "put":
            payoff = max(k - s, 0.0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        values.append(payoff)

    # Backward induction
    for i in range(n_steps - 1, -1, -1):
        new_values = []
        for j in range(i + 1):
            # continuation value
            cont = disc * (p * values[j + 1] + (1.0 - p) * values[j])

            if exercise == "american":
                # underlying price at node (i, j)
                s = s0 * (u ** j) * (d ** (i - j))
                if option_type == "call":
                    intrinsic = max(s - k, 0.0)
                else:  # put
                    intrinsic = max(k - s, 0.0)
                node_val = max(cont, intrinsic)
            elif exercise == "european":
                node_val = cont
            else:
                raise ValueError("exercise must be 'european' or 'american'")

            new_values.append(node_val)
        values = new_values
    return values[0]

def bs(
    s0: float,
    k: float,
    r: float,
    q: float,
    sigma: float,
    t: float,
    option_type: Literal["call", "put"] = "call",
) -> float:
    """
    Black–Scholes price of a European call or put with continuous dividend yield.
    """
    if t <= 0.0:
        # At expiry: intrinsic value
        if option_type == "call":
            return max(s0 - k, 0.0)
        elif option_type == "put":
            return max(k - s0, 0.0)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    if sigma <= 0.0:
        # Degenerate case: no volatility, option value is discounted intrinsic under forward
        f0 = s0 * math.exp((r - q) * t)
        if option_type == "call":
            payoff = max(f0 - k, 0.0)
        else:
            payoff = max(k - f0, 0.0)
        return math.exp(-r * t) * payoff

    # standard normal CDF
    def norm_cdf(x: float) -> float:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    sqrt_t = math.sqrt(t)
    d1 = (math.log(s0 / k) + (r - q + 0.5 * sigma * sigma) * t) / (sigma * sqrt_t)
    d2 = d1 - sigma * sqrt_t

    if option_type == "call":
        price = (
            s0 * math.exp(-q * t) * norm_cdf(d1)
            - k * math.exp(-r * t) * norm_cdf(d2)
        )
    elif option_type == "put":
        price = (
            k * math.exp(-r * t) * norm_cdf(-d2)
            - s0 * math.exp(-q * t) * norm_cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return price

def crr_binomial_option_bs_smooth(
    s0: float,
    k: float,
    r: float,
    q: float,
    sigma: float,
    t: float,
    n_steps: int,
    option_type: Literal["call", "put"] = "call",
    exercise:    Literal["european", "american"] = "european",
    band: int = 2,
) -> float:
    """
    CRR tree with first-step BS smoothing near the strike (band=2 -> 5 nodes).
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if band < 0:
        raise ValueError("band must be >= 0")

    dt = t / n_steps
    if dt <= 0:
        raise ValueError("T must be positive")

    # CRR up/down and risk-neutral prob with yield q
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    growth = math.exp((r - q) * dt)
    p = (growth - d) / (u - d)
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Risk-neutral probability out of bounds: p={p:.6f}")

    # terminal payoffs at i = n_steps
    values = []
    for j in range(n_steps + 1):
        s = s0 * (u ** j) * (d ** (n_steps - j))
        if option_type == "call":
            values.append(max(s - k, 0.0))
        elif option_type == "put":
            values.append(max(k - s, 0.0))
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    # --- special first backward step: i = n_steps - 1 ---
    i = n_steps - 1
    # stock prices at the penultimate layer
    s_layer = [s0 * (u ** j) * (d ** (i - j)) for j in range(i + 1)]
    # index closest to the strike
    k_idx = min(range(len(s_layer)), key=lambda j: abs(s_layer[j] - k))
    j_lo = max(0, k_idx - band)
    j_hi = min(i, k_idx + band)

    new_values = []
    for j in range(i + 1):
        s = s_layer[j]
        # continuation: BS over dt near the strike, else usual lattice expectation
        if j_lo <= j <= j_hi:
            cont = bs(s, k, r, q, sigma, dt, option_type)
        else:
            cont = disc * (p * values[j + 1] + (1.0 - p) * values[j])

        if exercise == "american":
            intrinsic = (s - k) if option_type == "call" else (k - s)
            intrinsic = max(intrinsic, 0.0)
            node_val = max(cont, intrinsic)
        elif exercise == "european":
            node_val = cont
        else:
            raise ValueError("exercise must be 'european' or 'american'")

        new_values.append(node_val)
    values = new_values  # now sized i+1

    # --- standard backward induction for remaining layers ---
    for i in range(n_steps - 2, -1, -1):
        new_values = []
        for j in range(i + 1):
            cont = disc * (p * values[j + 1] + (1.0 - p) * values[j])
            if exercise == "american":
                s = s0 * (u ** j) * (d ** (i - j))
                intrinsic = (s - k) if option_type == "call" else (k - s)
                intrinsic = max(intrinsic, 0.0)
                node_val = max(cont, intrinsic)
            else:
                node_val = cont
            new_values.append(node_val)
        values = new_values
    return values[0]
