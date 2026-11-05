"""
N-Dimensional Geometry Library

Simple, correct implementations of n-dimensional shape calculations.
Originally a CS102 Java project (2014), cleaned up in 2025.

Usage:
    from ndgeometry import Sphere, Cube, Ellipsoid, Simplex

    s = Sphere(dimensions=4, radius=2.0)
    print(s.volume)       # 39.478...
    print(s.surface_area) # 78.956...

Dimensions and accuracy:
    Every shape works in any number of dimensions. The float properties
    (`volume`, `surface_area`, ...) are IEEE doubles: correct to ~1e-15 in low
    dimensions, degrading to roughly n * 1e-16 by dimension n, and they
    saturate to 0.0 / inf outside the double range (~1e-308 .. 1e308) instead
    of raising. `log_volume` is the natural log of the volume and stays finite
    at any dimension. `precise(digits)` evaluates the same formulas with the
    decimal module to any number of significant digits, at any magnitude.

    s = Sphere(1000, 10.0)
    s.volume                 # 3.0798e+114
    s.log_volume             # 263.619...
    s.precise(40)["volume"]  # Decimal('3.0798...E+114'), 40 correct digits
"""

import math
from dataclasses import dataclass
from decimal import MAX_EMAX, MIN_EMIN, Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from typing import Callable, Dict, Tuple


# --- Float helpers -------------------------------------------------------

def _unit_ball_volume(n: int) -> float:
    """Volume of unit n-ball: π^(n/2) / Γ(n/2 + 1)"""
    if n <= 340:  # math.gamma overflows beyond this; log-space is slightly less accurate
        return math.pi ** (n / 2) / math.gamma(n / 2 + 1)
    return _exp(_log_unit_ball_volume(n))


def _log_unit_ball_volume(n: int) -> float:
    """Natural log of the unit n-ball volume; finite for any n."""
    return (n / 2) * math.log(math.pi) - math.lgamma(n / 2 + 1)


def unit_ball_coefficient(n: int) -> Fraction:
    """Exact rational c such that the unit n-ball volume is c · π^(n // 2).

    Even n = 2k: 1 / k!.   Odd n = 2k + 1: 2^(k+1) / (2k+1)!! = 2^(2k+1) k! / n!.
    """
    k = n // 2
    if n % 2 == 0:
        return Fraction(1, math.factorial(k))
    return Fraction(2 ** (2 * k + 1) * math.factorial(k), math.factorial(n))


def _exp(x: float) -> float:
    """exp() that saturates to inf instead of raising OverflowError."""
    try:
        return math.exp(x)
    except OverflowError:
        return math.inf


def _float_or_log(direct: Callable[[], float], log_value: float) -> float:
    """Evaluate direct() in floats; if an intermediate over/underflows, use exp(log_value)."""
    try:
        v = direct()
        if 0 < v < math.inf:
            return v
    except OverflowError:
        pass
    return _exp(log_value)


# --- Arbitrary-precision helpers (decimal module) -------------------------

@lru_cache(maxsize=None)
def _pi(prec: int) -> Decimal:
    """π to `prec` significant digits (Gauss–Legendre AGM: correct digits double per step)."""
    with localcontext() as ctx:
        ctx.prec = prec + 10
        a, b, t, p = Decimal(1), 1 / Decimal(2).sqrt(), Decimal(1) / 4, Decimal(1)
        for _ in range(prec.bit_length() + 1):
            a, b, t, p = (a + b) / 2, (a * b).sqrt(), t - p * ((a - b) / 2) ** 2, 2 * p
        pi = (a + b) ** 2 / (4 * t)
        ctx.prec = prec
        return +pi


def _unit_ball_volume_decimal(n: int, pi: Decimal) -> Decimal:
    """Unit n-ball volume in the current Decimal context, via V_n = V_(n-2) · 2π / n."""
    v = Decimal(2 if n % 2 else 1)  # V_1 = 2 (a segment), V_0 = 1 (a point)
    for m in range(n % 2 + 2, n + 1, 2):
        v = v * 2 * pi / m
    return v


def _D(x) -> Decimal:
    """Input as the decimal number it prints as, so radius=0.1 means exactly 0.1."""
    return Decimal(str(x))


def _precise(digits: int, n: int, compute: Callable[[Decimal], Dict[str, Decimal]]) -> Dict[str, Decimal]:
    """Run compute(pi) with guard digits (the loops do ~n roundings), then round to `digits`."""
    if digits < 1:
        raise ValueError("digits must be >= 1")
    with localcontext() as ctx:
        ctx.prec = digits + 5 + len(str(n))
        ctx.Emax, ctx.Emin = MAX_EMAX, MIN_EMIN  # no magnitude limit
        results = compute(_pi(ctx.prec))
        ctx.prec = digits
        return {key: +value for key, value in results.items()}


# --- Shapes ----------------------------------------------------------------

@dataclass
class Sphere:
    """N-dimensional sphere (n-ball boundary and interior)."""
    dimensions: int
    radius: float

    def __post_init__(self):
        if self.dimensions < 1:
            raise ValueError("dimensions must be >= 1")
        if self.radius <= 0:
            raise ValueError("radius must be positive")

    @property
    def volume(self) -> float:
        """N-dimensional volume (hypervolume)."""
        n = self.dimensions
        return _float_or_log(lambda: _unit_ball_volume(n) * self.radius ** n, self.log_volume)

    @property
    def log_volume(self) -> float:
        """Natural log of the volume; finite in any dimension."""
        return _log_unit_ball_volume(self.dimensions) + self.dimensions * math.log(self.radius)

    @property
    def surface_area(self) -> float:
        """(N-1)-dimensional surface area."""
        return self.dimensions * self.volume / self.radius

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    def precise(self, digits: int = 30) -> Dict[str, Decimal]:
        """volume and surface_area correct to `digits` significant digits."""
        n, r = self.dimensions, _D(self.radius)

        def compute(pi):
            volume = _unit_ball_volume_decimal(n, pi) * r ** n
            return {"volume": volume, "surface_area": n * volume / r}
        return _precise(digits, n, compute)

    @property
    def name(self) -> str:
        names = {1: "line segment", 2: "circle", 3: "sphere"}
        return names.get(self.dimensions, f"{self.dimensions}D hypersphere")


@dataclass
class Cube:
    """N-dimensional hypercube."""
    dimensions: int
    side: float

    def __post_init__(self):
        if self.dimensions < 1:
            raise ValueError("dimensions must be >= 1")
        if self.side <= 0:
            raise ValueError("side must be positive")

    @property
    def volume(self) -> float:
        """N-dimensional volume."""
        return _float_or_log(lambda: self.side ** self.dimensions, self.log_volume)

    @property
    def log_volume(self) -> float:
        """Natural log of the volume; finite in any dimension."""
        return self.dimensions * math.log(self.side)

    @property
    def surface_area(self) -> float:
        """(N-1)-dimensional surface area."""
        n = self.dimensions
        return _float_or_log(lambda: 2 * n * self.side ** (n - 1),
                             math.log(2 * n) + (n - 1) * math.log(self.side))

    @property
    def diagonal(self) -> float:
        """Space diagonal length."""
        return self.side * math.sqrt(self.dimensions)

    @property
    def vertices(self) -> int:
        """Number of vertices."""
        return 2 ** self.dimensions

    @property
    def edges(self) -> int:
        """Number of edges."""
        return self.dimensions * 2 ** (self.dimensions - 1)

    def precise(self, digits: int = 30) -> Dict[str, Decimal]:
        """volume, surface_area and diagonal correct to `digits` significant digits."""
        n, s = self.dimensions, _D(self.side)

        def compute(pi):
            return {"volume": s ** n, "surface_area": 2 * n * s ** (n - 1),
                    "diagonal": s * Decimal(n).sqrt()}
        return _precise(digits, n, compute)

    @property
    def name(self) -> str:
        names = {1: "line segment", 2: "square", 3: "cube", 4: "tesseract"}
        return names.get(self.dimensions, f"{self.dimensions}D hypercube")


@dataclass
class Ellipsoid:
    """N-dimensional ellipsoid with arbitrary semi-axes."""
    semi_axes: Tuple[float, ...]

    def __post_init__(self):
        if len(self.semi_axes) < 1:
            raise ValueError("need at least one axis")
        if any(a <= 0 for a in self.semi_axes):
            raise ValueError("all semi-axes must be positive")

    @property
    def dimensions(self) -> int:
        return len(self.semi_axes)

    @property
    def volume(self) -> float:
        """N-dimensional volume."""
        return _float_or_log(lambda: _unit_ball_volume(self.dimensions) * math.prod(self.semi_axes),
                             self.log_volume)

    @property
    def log_volume(self) -> float:
        """Natural log of the volume; finite in any dimension."""
        return _log_unit_ball_volume(self.dimensions) + sum(math.log(a) for a in self.semi_axes)

    def precise(self, digits: int = 30) -> Dict[str, Decimal]:
        """volume correct to `digits` significant digits."""
        n = self.dimensions

        def compute(pi):
            return {"volume": _unit_ball_volume_decimal(n, pi) * math.prod(map(_D, self.semi_axes))}
        return _precise(digits, n, compute)

    @property
    def is_sphere(self) -> bool:
        """True if all axes are equal."""
        return len(set(self.semi_axes)) == 1

    @property
    def name(self) -> str:
        if self.is_sphere:
            return Sphere(self.dimensions, self.semi_axes[0]).name
        names = {2: "ellipse", 3: "ellipsoid"}
        return names.get(self.dimensions, f"{self.dimensions}D hyperellipsoid")


@dataclass
class Simplex:
    """N-dimensional regular simplex (equilateral triangle, tetrahedron, etc.)."""
    dimensions: int
    side: float

    def __post_init__(self):
        if self.dimensions < 1:
            raise ValueError("dimensions must be >= 1")
        if self.side <= 0:
            raise ValueError("side must be positive")

    @property
    def volume(self) -> float:
        """N-dimensional volume."""
        n = self.dimensions
        if n > 170:  # n! no longer fits in a float
            return _exp(self.log_volume)
        # V_n = (s^n / n!) * sqrt((n+1) / 2^n)
        return _float_or_log(lambda: (self.side ** n / math.factorial(n)) * math.sqrt((n + 1) / 2 ** n),
                             self.log_volume)

    @property
    def log_volume(self) -> float:
        """Natural log of the volume; finite in any dimension."""
        n = self.dimensions
        return n * math.log(self.side) - math.lgamma(n + 1) + (math.log(n + 1) - n * math.log(2)) / 2

    @property
    def surface_area(self) -> float:
        """(N-1)-dimensional surface area: n+1 facets, each a regular (n-1)-simplex."""
        n = self.dimensions
        return self.volume * n / self.side * math.sqrt(2 * n * (n + 1))

    @property
    def vertices(self) -> int:
        """Number of vertices."""
        return self.dimensions + 1

    @property
    def edges(self) -> int:
        """Number of edges."""
        n = self.dimensions + 1
        return n * (n - 1) // 2

    def precise(self, digits: int = 30) -> Dict[str, Decimal]:
        """volume and surface_area correct to `digits` significant digits."""
        n, s = self.dimensions, _D(self.side)

        def compute(pi):
            factorial = Decimal(1)
            for i in range(2, n + 1):
                factorial *= i
            volume = s ** n / factorial * (Decimal(n + 1) / Decimal(2) ** n).sqrt()
            return {"volume": volume,
                    "surface_area": volume * n / s * Decimal(2 * n * (n + 1)).sqrt()}
        return _precise(digits, n, compute)

    @property
    def name(self) -> str:
        names = {1: "line segment", 2: "triangle", 3: "tetrahedron"}
        return names.get(self.dimensions, f"{self.dimensions}D simplex")


# Quick demo
if __name__ == "__main__":
    print("=== N-Dimensional Geometry ===\n")

    # Show the famous result: unit sphere volume peaks around 5D
    print("Unit sphere volume by dimension:")
    for n in range(1, 12):
        s = Sphere(n, 1.0)
        bar = "#" * int(s.volume * 5)
        print(f"  {n:2d}D: {s.volume:8.4f} {bar}")

    print(f"\n4D sphere (r=2): volume={Sphere(4, 2).volume:.4f}")
    print(f"4D cube (s=2):   volume={Cube(4, 2).volume:.4f}")

    c = unit_ball_coefficient(5)
    print(f"\n5D unit ball, exactly: {c} * pi^2 = {Sphere(5, 1).precise(25)['volume']}")
    big = Sphere(1000, 10.0)
    print(f"1000D sphere (r=10): volume={big.volume:.4e}  log10={big.log_volume / math.log(10):.3f}"
          f"  40 digits={big.precise(40)['volume']}")
