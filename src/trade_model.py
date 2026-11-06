"""Three-origin CES import allocation; assumptions are documented in methods.md."""
from dataclasses import dataclass
from math import isclose, isfinite


@dataclass(frozen=True)
class Allocation:
    shares: tuple[float, ...]
    price_index: float
    customs: tuple[float, ...]
    tariff_revenue: float
    real_bundle: float
    compensation: float


def allocate(weights, sigma, tariffs=(0, 0, 0), costs=(1, 1, 1), expenditure=100):
    """Order: Vietnam, China, rest of world. Fixed tariff-inclusive expenditure."""
    if len(weights) != 3 or len(tariffs) != 3 or len(costs) != 3:
        raise ValueError('Exactly three origins required')
    if not all(isfinite(x) for x in (*weights, sigma, *tariffs, *costs, expenditure)):
        raise ValueError('Inputs must be finite')
    if sigma <= 1 or expenditure <= 0 or min(weights) <= 0 or not isclose(sum(weights), 1, abs_tol=1e-10):
        raise ValueError('Positive normalized weights, sigma > 1, expenditure > 0 required')
    if min(tariffs) < 0 or min(costs) <= 0:
        raise ValueError('Nonnegative tariffs and positive cost multipliers required')
    terms = [w * (c * (1+t))**(1-sigma) for w, c, t in zip(weights, costs, tariffs)]
    denom = sum(terms)
    shares = tuple(x / denom for x in terms)
    price = denom**(1/(1-sigma))
    customs = tuple(expenditure*s/(1+t) for s, t in zip(shares, tariffs))
    revenue = sum(v*t for v, t in zip(customs, tariffs))
    return Allocation(shares, price, customs, revenue, expenditure/price, expenditure*(price-1))
