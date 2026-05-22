"""
N-Dimensional Geometry Library

Simple, correct implementations of n-dimensional shape calculations.
Originally a CS102 Java project (2014), cleaned up in 2025.

Usage:
    from ndgeometry import Sphere, Cube, Ellipsoid, Simplex
    
    s = Sphere(dimensions=4, radius=2.0)
    print(s.volume)       # 39.478...
    print(s.surface_area) # 78.956...
"""

import math
from dataclasses import dataclass
from typing import Tuple


def _unit_ball_volume(n: int) -> float:
    """Volume of unit n-ball: π^(n/2) / Γ(n/2 + 1)"""
    return math.pi ** (n / 2) / math.gamma(n / 2 + 1)


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
        return _unit_ball_volume(self.dimensions) * self.radius ** self.dimensions
    
    @property
    def surface_area(self) -> float:
        """(N-1)-dimensional surface area."""
        return self.dimensions * self.volume / self.radius

    @property
    def diameter(self) -> float:
        return 2 * self.radius
    
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
        return self.side ** self.dimensions
    
    @property
    def surface_area(self) -> float:
        """(N-1)-dimensional surface area."""
        return 2 * self.dimensions * self.side ** (self.dimensions - 1)
    
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
        axes_product = math.prod(self.semi_axes)
        return _unit_ball_volume(self.dimensions) * axes_product
    
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
        # V_n = (s^n / n!) * sqrt((n+1) / 2^n)
        return (self.side**n / math.factorial(n)) * math.sqrt((n + 1) / 2**n)
    
    @property
    def vertices(self) -> int:
        """Number of vertices."""
        return self.dimensions + 1
    
    @property
    def edges(self) -> int:
        """Number of edges."""
        n = self.dimensions + 1
        return n * (n - 1) // 2
    
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

