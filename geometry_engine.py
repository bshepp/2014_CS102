import math
import os
import re
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np


class JavaBridge:
    """
    Bridge to execute the original Java Sphere and MultiSphere classes
    Falls back to Python implementations if Java is not available
    """

    def __init__(self):
        self.java_dir = os.path.dirname(os.path.abspath(__file__))
        self.java_available = self._check_java_availability()
        if self.java_available:
            self._compile_java_files()

    def _check_java_availability(self) -> bool:
        """Check if Java compiler and runtime are available"""
        try:
            subprocess.run(["javac", "-version"], capture_output=True, check=True)
            subprocess.run(["java", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _compile_java_files(self):
        """Compile the original Java files"""
        java_files = ["Sphere.java", "MultiSphere.java"]
        existing_files = [f for f in java_files if os.path.exists(f)]

        if existing_files:
            try:
                subprocess.run(
                    ["javac"] + existing_files, check=True, capture_output=True
                )
                print("✅ Original Java files compiled successfully!")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Java compilation failed: {e}")
                self.java_available = False

    def run_original_multisphere(self, diameter: float) -> str:
        """
        Execute the original MultiSphere.java with given diameter
        This preserves the exact original CS102 implementation
        """
        if not self.java_available:
            return self._python_multisphere_equivalent(diameter)

        try:
            # Create a temporary input for the Java program
            process = subprocess.Popen(
                ["java", "MultiSphere"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = process.communicate(input=str(diameter))

            if process.returncode == 0:
                return f"🎯 ORIGINAL JAVA OUTPUT:\n{stdout}"
            else:
                return f"Java execution failed: {stderr}"

        except Exception as e:
            return f"Error running Java: {e}"

    def _python_multisphere_equivalent(self, diameter: float) -> str:
        """
        Python equivalent of the original MultiSphere logic
        FIXED VERSION - corrected the original bug!
        """
        # First, show the diameter=1 example (like original MultiSphere)
        unit_radius = 1.0 / 2.0
        unit_volume = (4.0 / 3.0) * math.pi * pow(unit_radius, 3)
        unit_area = 4.0 * math.pi * pow(unit_radius, 2)

        # Then calculate for the user's diameter
        user_radius = diameter / 2.0
        user_volume = (4.0 / 3.0) * math.pi * pow(user_radius, 3)
        user_area = 4.0 * math.pi * pow(user_radius, 2)

        # Format output to match original MultiSphere.java (but FIXED!)
        output = "🐍 PYTHON EQUIVALENT (Java not available, but FIXED!):\n"
        output += (
            f"A sphere with a diameter of 1 has a volume of {unit_volume:.3f}, "
            f"and an area of {unit_area:.3f}.\n\n"
        )
        output += "Please enter the diameter of your sphere.\n"
        output += (
            f"The surface area of a sphere with diameter of {diameter:.3f} "
            f"is {user_area:.3f}.\n\n"
        )
        output += (
            f"The volume of a sphere with diameter of {diameter:.3f} "
            f"is {user_volume:.3f}.\n"
        )

        return output

    def run_original_sphere(self, diameter: float) -> str:
        """
        Execute the original Java sphere program with given diameter
        Tries MultiSphere.java first (has main method),
        then falls back to Python equivalent
        """
        if not self.java_available:
            return self._python_sphere_equivalent(diameter)

        try:
            # First try MultiSphere.java since it has a main method
            process = subprocess.Popen(
                ["java", "MultiSphere"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.java_dir,
            )

            stdout, stderr = process.communicate(input=str(diameter))

            if process.returncode == 0:
                return f"🎯 ORIGINAL JAVA OUTPUT (MultiSphere):\n{stdout}"
            else:
                # If MultiSphere fails, try Sphere.java directly
                process = subprocess.Popen(
                    ["java", "Sphere"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self.java_dir,
                )

                stdout, stderr = process.communicate(input=str(diameter))

                if process.returncode == 0:
                    return f"🎯 ORIGINAL JAVA OUTPUT (Sphere):\n{stdout}"
                else:
                    # If Java execution fails (e.g., no main method),
                    # fall back to Python
                    if (
                        "main method not found" in stderr.lower()
                        or "no main method" in stderr.lower()
                        or "main method" in stderr.lower()
                        or "could not find or load main class" in stderr.lower()
                    ):
                        return self._python_sphere_equivalent(diameter)
                    return f"Java execution failed: {stderr}"

        except Exception:
            # Fall back to Python equivalent on any error
            return self._python_sphere_equivalent(diameter)

    def _python_sphere_equivalent(self, diameter: float) -> str:
        """
        Python equivalent of the original Sphere logic
        Mimics the original CS102 Sphere.java behavior
        """
        radius = diameter / 2.0
        volume = (4.0 / 3.0) * math.pi * pow(radius, 3)
        surface_area = 4.0 * math.pi * pow(radius, 2)

        output = "🐍 PYTHON EQUIVALENT (Java class has no main method):\n"
        output += f"Sphere with diameter {diameter:.3f} has:\n"
        output += f"  Volume: {volume:.3f}\n"
        output += f"  Surface Area: {surface_area:.3f}\n"
        output += f"Original diameter input: {diameter:.3f}\n"

        return output

    def get_original_sphere_properties(self, diameter: float) -> Dict[str, float]:
        """
        Get sphere properties using the original Java logic
        Returns dict with volume and surface area
        """
        radius = diameter / 2.0
        return {
            "diameter": diameter,
            "radius": radius,
            "volume": (4.0 / 3.0) * math.pi * pow(radius, 3),
            "surface_area": 4.0 * math.pi * pow(radius, 2),
        }


class NDShape(ABC):
    """
    Abstract base class for n-dimensional geometric shapes
    Python version of our Java framework
    """

    def __init__(self, dimensions: int, *parameters: float):
        if dimensions < 1:
            raise ValueError("Dimensions must be positive")

        self.dimensions = dimensions
        self.parameters = np.array(parameters)
        self.validate_parameters()

    @abstractmethod
    def validate_parameters(self):
        """Validate shape-specific parameters"""
        pass

    @abstractmethod
    def get_volume(self) -> float:
        """Calculate the n-dimensional volume (hypervolume)"""
        pass

    @abstractmethod
    def get_surface_area(self) -> float:
        """Calculate the (n-1)-dimensional surface area"""
        pass

    @abstractmethod
    def get_shape_type(self) -> str:
        """Get shape type name"""
        pass

    @abstractmethod
    def get_volume_formula(self) -> str:
        """Get mathematical formula for volume"""
        pass

    @abstractmethod
    def get_surface_area_formula(self) -> str:
        """Get mathematical formula for surface area"""
        pass

    @staticmethod
    def gamma(x: float) -> float:
        """Gamma function implementation"""
        return math.gamma(x)

    @staticmethod
    def unit_sphere_volume(n: int) -> float:
        """Calculate n-dimensional unit sphere volume coefficient"""
        if n % 2 == 0:
            # Even dimensions: V_n = π^(n/2) / (n/2)!
            result = math.pow(math.pi, n / 2.0)
            for i in range(1, n // 2 + 1):
                result /= i
            return result
        else:
            # Odd dimensions: V_n = 2^((n+1)/2) * π^((n-1)/2) / (n!!)
            result = math.pow(2, (n + 1) / 2.0) * math.pow(math.pi, (n - 1) / 2.0)
            for i in range(n, 0, -2):
                result /= i
            return result

    def __str__(self) -> str:
        volume = self.get_volume()
        surface = self.get_surface_area()
        return (
            f"{self.get_shape_type()} (dim={self.dimensions}): "
            f"Volume={volume:.6f}, Surface Area={surface:.6f}"
        )


class HyperSphere(NDShape):
    """N-dimensional hypersphere implementation"""

    def __init__(self, dimensions: int, radius: float):
        super().__init__(dimensions, radius)
        self.radius = radius

    def validate_parameters(self):
        if len(self.parameters) != 1:
            raise ValueError("HyperSphere requires exactly one parameter (radius)")
        if self.parameters[0] <= 0:
            raise ValueError("Radius must be positive")

    def get_volume(self) -> float:
        return self.unit_sphere_volume(self.dimensions) * pow(
            self.radius, self.dimensions
        )

    def get_surface_area(self) -> float:
        if self.dimensions == 1:
            return 2  # Two points
        return (
            self.dimensions
            * self.unit_sphere_volume(self.dimensions)
            * pow(self.radius, self.dimensions - 1)
        )

    def get_diameter(self) -> float:
        return 2 * self.radius

    def get_shape_type(self) -> str:
        if self.dimensions == 2:
            return "Circle"
        elif self.dimensions == 3:
            return "Sphere"
        else:
            return f"{self.dimensions}D HyperSphere"

    def get_volume_formula(self) -> str:
        if self.dimensions == 1:
            return "V₁ = 2r"
        if self.dimensions == 2:
            return "V₂ = πr²"
        if self.dimensions == 3:
            return "V₃ = (4/3)πr³"
        if self.dimensions == 4:
            return "V₄ = (π²/2)r⁴"

        if self.dimensions % 2 == 0:
            dim_half = self.dimensions // 2
            return (
                f"V_{self.dimensions} = (π^{dim_half}/{dim_half}!) × "
                f"r^{self.dimensions}"
            )
        else:
            power1 = (self.dimensions + 1) // 2
            power2 = (self.dimensions - 1) // 2
            return (
                f"V_{self.dimensions} = (2^{power1} × π^{power2})"
                f"/(odd factors) × r^{self.dimensions}"
            )

    def get_surface_area_formula(self) -> str:
        if self.dimensions == 1:
            return "S₁ = 2"
        if self.dimensions == 2:
            return "S₂ = 2πr"
        if self.dimensions == 3:
            return "S₃ = 4πr²"
        if self.dimensions == 4:
            return "S₄ = 2π²r³"

        return f"S_{self.dimensions} = {self.dimensions} × V_{self.dimensions} / r"

    def contains_point(self, point: List[float]) -> bool:
        """Check if a point is inside the hypersphere"""
        if len(point) != self.dimensions:
            raise ValueError("Point dimension mismatch")

        # Calculate distance from origin to point
        distance_squared = sum(coord**2 for coord in point)
        distance = math.sqrt(distance_squared)

        return distance <= self.radius


class HyperCube(NDShape):
    """N-dimensional hypercube implementation"""

    def __init__(self, dimensions: int, side_length: float):
        super().__init__(dimensions, side_length)
        self.side_length = side_length

    def validate_parameters(self):
        if len(self.parameters) != 1:
            raise ValueError("HyperCube requires exactly one parameter (side length)")
        if self.parameters[0] <= 0:
            raise ValueError("Side length must be positive")

    def get_volume(self) -> float:
        return pow(self.side_length, self.dimensions)

    def get_surface_area(self) -> float:
        if self.dimensions == 0:
            return 0
        if self.dimensions == 1:
            return 2  # Two endpoints

        # Surface area = 2n × s^(n-1) where n is dimensions, s is side length
        return 2 * self.dimensions * pow(self.side_length, self.dimensions - 1)

    def get_vertex_count(self) -> int:
        """Get the number of vertices in the hypercube"""
        return pow(2, self.dimensions)

    def get_edge_count(self) -> int:
        """Get the number of edges in the hypercube"""
        return self.dimensions * pow(2, self.dimensions - 1)

    def get_face_count(self, k: int) -> int:
        """Get the number of k-dimensional faces"""
        if k < 0 or k > self.dimensions:
            return 0

        # Number of k-faces = C(n,k) * 2^(n-k)
        return self._binomial(self.dimensions, k) * pow(2, self.dimensions - k)

    def _binomial(self, n: int, k: int) -> int:
        """Calculate binomial coefficient C(n,k)"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1

        result = 1
        for i in range(1, k + 1):
            result = result * (n - i + 1) // i
        return result

    def get_diagonal_length(self) -> float:
        """Calculate diagonal length through the hypercube"""
        return self.side_length * math.sqrt(self.dimensions)

    def contains_point(self, point: List[float]) -> bool:
        """Check if a point is inside the hypercube"""
        if len(point) != self.dimensions:
            raise ValueError("Point dimension mismatch")

        for coord in point:
            if coord < 0 or coord > self.side_length:
                return False
        return True

    def get_shape_type(self) -> str:
        if self.dimensions == 2:
            return "Square"
        elif self.dimensions == 3:
            return "Cube"
        else:
            return f"{self.dimensions}D HyperCube"

    def get_volume_formula(self) -> str:
        return f"V_{self.dimensions} = s^{self.dimensions}"

    def get_surface_area_formula(self) -> str:
        if self.dimensions == 1:
            return "S₁ = 2"
        return f"S_{self.dimensions} = 2 × {self.dimensions} × s^{self.dimensions - 1}"

    def get_cross_section(self, distance: float) -> float:
        """Calculate the volume of a cross-section at a given distance"""
        if distance <= 0 or distance >= self.side_length:
            return 0

        if self.dimensions == 1:
            return 1  # Point

        # Cross-section is a (n-1)-dimensional hypercube
        cross_section = HyperCube(self.dimensions - 1, self.side_length)
        return cross_section.get_volume()

    def __str__(self) -> str:
        shape_type = self.get_shape_type()
        volume = self.get_volume()
        surface_area = self.get_surface_area()
        vertices = self.get_vertex_count()
        return (
            f"{shape_type} (dim={self.dimensions}, "
            f"side={self.side_length:.3f}): "
            f"Volume={volume:.6f}, Surface Area={surface_area:.6f}, "
            f"Vertices={vertices}"
        )


class HyperEllipsoid(NDShape):
    """N-dimensional hyperellipsoid implementation"""

    def __init__(self, dimensions: int, *semi_axes: float):
        if len(semi_axes) != dimensions:
            raise ValueError(f"HyperEllipsoid requires exactly {dimensions} semi-axes")
        super().__init__(dimensions, *semi_axes)
        self.semi_axes = np.array(semi_axes)

    def validate_parameters(self):
        if len(self.parameters) != self.dimensions:
            raise ValueError(
                f"HyperEllipsoid requires exactly {self.dimensions} "
                f"parameters (semi-axes)"
            )
        if any(axis <= 0 for axis in self.parameters):
            raise ValueError("Semi-axes must be positive")

    def get_volume(self) -> float:
        """Calculate n-dimensional ellipsoid volume"""
        # V = (π^(n/2) / Γ(n/2 + 1)) * ∏(a_i) for n dimensions
        unit_volume = self.unit_sphere_volume(self.dimensions)
        axes_product = np.prod(self.semi_axes)
        return unit_volume * axes_product

    def get_surface_area(self) -> float:
        """Calculate (n-1)-dimensional surface area"""
        if self.dimensions == 1:
            return 2  # Two endpoints
        elif self.dimensions == 2:
            # Ellipse perimeter approximation (Ramanujan)
            a, b = self.semi_axes[0], self.semi_axes[1]
            h = ((a - b) / (a + b)) ** 2
            return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
        elif self.dimensions == 3:
            # Ellipsoid surface area (approximate for general case)
            a, b, c = self.semi_axes
            if a == b == c:
                # Sphere case
                return 4 * math.pi * a * a
            else:
                # Approximate formula for general ellipsoid
                p = 1.6075
                return (
                    4
                    * math.pi
                    * ((a**p * b**p + a**p * c**p + b**p * c**p) / 3) ** (1 / p)
                )
        else:
            # Higher dimensions: use generalized formula
            # Surface area ≈ n * Volume / (geometric mean of semi-axes)
            geometric_mean = np.power(np.prod(self.semi_axes), 1 / self.dimensions)
            return self.dimensions * self.get_volume() / geometric_mean

    def get_eccentricity(self) -> float:
        """Calculate eccentricity for 2D ellipse"""
        if self.dimensions != 2:
            raise ValueError("Eccentricity is only defined for 2D ellipses")

        a, b = sorted(self.semi_axes, reverse=True)  # a >= b
        return math.sqrt(1 - (b / a) ** 2)

    def get_axis_ratio(self) -> float:
        """Get the ratio of largest to smallest semi-axis"""
        return max(self.semi_axes) / min(self.semi_axes)

    def is_sphere(self, tolerance: float = 1e-10) -> bool:
        """Check if this ellipsoid is actually a sphere"""
        return bool(max(self.semi_axes) - min(self.semi_axes) < tolerance)

    def get_shape_type(self) -> str:
        if self.is_sphere():
            if self.dimensions == 2:
                return "Circle"
            elif self.dimensions == 3:
                return "Sphere"
            else:
                return "HyperSphere"
        else:
            if self.dimensions == 2:
                return "Ellipse"
            elif self.dimensions == 3:
                return "Ellipsoid"
            else:
                return "HyperEllipsoid"

    def get_volume_formula(self) -> str:
        if self.dimensions == 1:
            return "V₁ = 2a"
        elif self.dimensions == 2:
            return "V₂ = π × a × b"
        elif self.dimensions == 3:
            return "V₃ = (4/3)π × a × b × c"
        else:
            dim_half = self.dimensions / 2
            return f"V_{self.dimensions} = (π^{dim_half} / " f"Γ({dim_half} + 1)) × ∏aᵢ"

    def get_surface_area_formula(self) -> str:
        if self.dimensions == 1:
            return "S₁ = 2"
        elif self.dimensions == 2:
            return "S₂ ≈ π(a + b)(1 + 3h/(10 + √(4-3h))), h = ((a-b)/(a+b))²"
        elif self.dimensions == 3:
            return "S₃ ≈ 4π((aᵖbᵖ + aᵖcᵖ + bᵖcᵖ)/3)^(1/p), p ≈ 1.6075"
        else:
            return f"S_{self.dimensions} ≈ n × Volume / (geometric mean of semi-axes)"

    def contains_point(self, point: List[float]) -> bool:
        """Check if a point is inside the ellipsoid"""
        if len(point) != self.dimensions:
            raise ValueError("Point dimension mismatch")

        # Check if ∑(xᵢ/aᵢ)² ≤ 1
        sum_squares = sum(
            (point[i] / self.semi_axes[i]) ** 2 for i in range(self.dimensions)
        )
        return sum_squares <= 1.0

    def get_cross_section(self, axis: int, distance: float) -> float:
        """Calculate cross-sectional area at given distance along specified axis"""
        if axis < 0 or axis >= self.dimensions:
            raise ValueError("Invalid axis index")

        if abs(distance) > self.semi_axes[axis]:
            return 0  # Outside ellipsoid

        if self.dimensions == 1:
            return 1 if abs(distance) <= self.semi_axes[0] else 0

        # Create (n-1)-dimensional ellipsoid cross-section
        cross_axes = []
        for i in range(self.dimensions):
            if i != axis:
                # Scale factor for cross-section
                scale_factor = math.sqrt(1 - (distance / self.semi_axes[axis]) ** 2)
                cross_axes.append(self.semi_axes[i] * scale_factor)

        cross_section = HyperEllipsoid(self.dimensions - 1, *cross_axes)
        return cross_section.get_volume()

    def __str__(self) -> str:
        axes_str = ", ".join(f"{a:.3f}" for a in self.semi_axes)
        shape_type = self.get_shape_type()
        volume = self.get_volume()
        surface_area = self.get_surface_area()
        return (
            f"{shape_type} (dim={self.dimensions}, axes=[{axes_str}]): "
            f"Volume={volume:.6f}, Surface Area={surface_area:.6f}"
        )


class OriginalSphere(HyperSphere):
    """
    Python implementation that exactly mirrors the original Java Sphere class
    Maintains compatibility with original MultiSphere behavior
    """

    def __init__(self, diameter: float):
        super().__init__(3, diameter / 2.0)
        self.diameter = diameter

    def set_diameter(self, new_diameter: float):
        """Mirror the original setDiameter method"""
        if new_diameter < 0:
            raise ValueError("Diameter cannot be negative")
        self.diameter = new_diameter
        self.radius = new_diameter / 2.0
        self.parameters = np.array([self.radius])

    def get_diameter(self) -> float:
        """Mirror the original getDiameter method"""
        return self.diameter

    def get_area(self) -> float:
        """Mirror the original getArea method name"""
        return self.get_surface_area()

    def __str__(self) -> str:
        """Mirror the original toString method exactly"""
        return f"a volume of {self.get_volume():.3f}, and an area of {self.get_area():.3f}."


class Simplex(NDShape):
    """N-dimensional simplex (generalized triangle) implementation"""

    def __init__(self, dimensions: int, side_length: float):
        super().__init__(dimensions, side_length)
        self.side_length = side_length

    def validate_parameters(self):
        if len(self.parameters) != 1:
            raise ValueError("Simplex requires exactly one parameter (side length)")
        if self.parameters[0] < 0:
            raise ValueError("Side length cannot be negative")

    def get_volume(self) -> float:
        """Calculate n-dimensional simplex volume"""
        if self.dimensions == 0:
            return 1  # Point
        elif self.dimensions == 1:
            return self.side_length  # Line segment
        elif self.dimensions == 2:
            return (math.sqrt(3) / 4) * self.side_length**2  # Equilateral triangle
        elif self.dimensions == 3:
            return (math.sqrt(2) / 12) * self.side_length**3  # Regular tetrahedron
        else:
            # General formula: V_n = (√(n+1) / (2^n * n!)) * s^n
            # Where s is the side length
            numerator = math.sqrt(self.dimensions + 1)
            denominator = (2**self.dimensions) * math.factorial(self.dimensions)
            return (numerator / denominator) * (self.side_length**self.dimensions)

    def get_surface_area(self) -> float:
        """Calculate (n-1)-dimensional surface area"""
        if self.dimensions == 0:
            return 0  # Point has no surface
        elif self.dimensions == 1:
            return 2  # Two endpoints
        elif self.dimensions == 2:
            return 3 * self.side_length  # Triangle perimeter
        elif self.dimensions == 3:
            # Tetrahedron: 4 triangular faces
            triangle_area = (math.sqrt(3) / 4) * self.side_length**2
            return 4 * triangle_area
        else:
            # General formula: S_n = (n+1) * V_(n-1) where V_(n-1) is (n-1)-simplex volume
            if self.dimensions == 1:
                return 2
            face_simplex = Simplex(self.dimensions - 1, self.side_length)
            return (self.dimensions + 1) * face_simplex.get_volume()

    def get_vertex_count(self) -> int:
        """Get the number of vertices in the simplex"""
        return self.dimensions + 1

    def get_edge_count(self) -> int:
        """Get the number of edges in the simplex"""
        n = self.dimensions + 1
        return (n * (n - 1)) // 2  # C(n,2) = n choose 2

    def get_face_count(self, k: int) -> int:
        """Get the number of k-dimensional faces"""
        if k < 0 or k > self.dimensions:
            return 0
        if k == self.dimensions:
            return 1  # The simplex itself

        # Number of k-faces = C(n+1, k+1) where n is dimensions
        n = self.dimensions + 1
        return self._binomial(n, k + 1)

    def _binomial(self, n: int, k: int) -> int:
        """Calculate binomial coefficient C(n,k)"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1

        result = 1
        for i in range(1, k + 1):
            result = result * (n - i + 1) // i
        return result

    def get_circumradius(self) -> float:
        """Get the circumradius (radius of circumscribed sphere)"""
        if self.dimensions == 2:
            return self.side_length / math.sqrt(3)
        elif self.dimensions == 3:
            return self.side_length * math.sqrt(6) / 4
        else:
            # General formula: R = s * sqrt(n/(2(n+1)))
            return self.side_length * math.sqrt(
                self.dimensions / (2 * (self.dimensions + 1))
            )

    def get_inradius(self) -> float:
        """Get the inradius (radius of inscribed sphere)"""
        if self.dimensions == 2:
            return self.side_length / (2 * math.sqrt(3))
        elif self.dimensions == 3:
            return self.side_length / (2 * math.sqrt(6))
        else:
            # General formula: r = s * sqrt(1/(2n(n+1)))
            return self.side_length * math.sqrt(
                1 / (2 * self.dimensions * (self.dimensions + 1))
            )

    def get_height(self) -> float:
        """Get the height of the simplex"""
        if self.dimensions == 2:
            return self.side_length * math.sqrt(3) / 2
        elif self.dimensions == 3:
            return self.side_length * math.sqrt(2 / 3)
        else:
            # General formula: h = s * sqrt(2(n+1)/n)
            return self.side_length * math.sqrt(
                2 * (self.dimensions + 1) / self.dimensions
            )

    def get_shape_type(self) -> str:
        if self.dimensions == 0:
            return "Point"
        elif self.dimensions == 1:
            return "Line Segment"
        elif self.dimensions == 2:
            return "Triangle"
        elif self.dimensions == 3:
            return "Tetrahedron"
        else:
            return f"{self.dimensions}D Simplex"

    def get_volume_formula(self) -> str:
        if self.dimensions == 0:
            return "V₀ = 1"
        elif self.dimensions == 1:
            return "V₁ = s"
        elif self.dimensions == 2:
            return "V₂ = (√3/4) × s²"
        elif self.dimensions == 3:
            return "V₃ = (√2/12) × s³"
        else:
            return f"V_{self.dimensions} = (√{self.dimensions+1} / (2^{self.dimensions} × {self.dimensions}!)) × s^{self.dimensions}"

    def get_surface_area_formula(self) -> str:
        if self.dimensions == 0:
            return "S₀ = 0"
        elif self.dimensions == 1:
            return "S₁ = 2"
        elif self.dimensions == 2:
            return "S₂ = 3s"
        elif self.dimensions == 3:
            return "S₃ = √3 × s²"
        else:
            return (
                f"S_{self.dimensions} = ({self.dimensions+1}) × V_{self.dimensions-1}"
            )

    def contains_point(self, point: List[float]) -> bool:
        """Check if a point is inside the simplex (simplified check)"""
        if len(point) != self.dimensions:
            raise ValueError("Point dimension mismatch")

        # For regular simplex centered at origin, this is a simplified check
        # A complete implementation would require barycentric coordinates
        if self.dimensions == 2:
            # Triangle: check if point is within equilateral triangle
            x, y = point[0], point[1]
            # Simple bounds check (approximate)
            return abs(x) <= self.side_length / 2 and abs(y) <= self.get_height() / 2
        elif self.dimensions == 3:
            # Tetrahedron: simplified bounds check
            x, y, z = point[0], point[1], point[2]
            return (
                abs(x) <= self.side_length / 2
                and abs(y) <= self.side_length / 2
                and abs(z) <= self.get_height() / 2
            )
        else:
            # Higher dimensions: use distance from center
            distance = math.sqrt(sum(coord**2 for coord in point))
            return distance <= self.get_circumradius()

    def __str__(self) -> str:
        return f"{self.get_shape_type()} (dim={self.dimensions}, side={self.side_length:.3f}): Volume={self.get_volume():.6f}, Surface Area={self.get_surface_area():.6f}, Vertices={self.get_vertex_count()}"


class HyperPyramid(NDShape):
    """N-dimensional hyperpyramid implementation"""

    def __init__(self, dimensions: int, base_side_length: float, height: float):
        super().__init__(dimensions, base_side_length, height)
        self.base_side_length = base_side_length
        self.height = height

    def validate_parameters(self):
        if len(self.parameters) != 2:
            raise ValueError(
                "HyperPyramid requires exactly two parameters (base_side_length, height)"
            )
        if self.parameters[0] < 0 or self.parameters[1] < 0:
            raise ValueError("Base side length and height cannot be negative")

    def get_volume(self) -> float:
        """Calculate n-dimensional pyramid volume"""
        if self.dimensions == 1:
            return self.base_side_length  # Line segment
        elif self.dimensions == 2:
            # Triangle pyramid (triangle): (1/2) * base * height
            return 0.5 * self.base_side_length * self.height
        elif self.dimensions == 3:
            # Square pyramid: (1/3) * base_area * height
            base_area = self.base_side_length**2
            return (1 / 3) * base_area * self.height
        else:
            # General n-dimensional pyramid: (1/n) * base_volume * height
            # Base is an (n-1)-dimensional hypercube
            base_volume = self.base_side_length ** (self.dimensions - 1)
            return (1 / self.dimensions) * base_volume * self.height

    def get_surface_area(self) -> float:
        """Calculate (n-1)-dimensional surface area"""
        if self.dimensions == 1:
            return 2  # Two endpoints
        elif self.dimensions == 2:
            # Triangle: base + two sides
            base = self.base_side_length
            # Side length using Pythagorean theorem
            side_length = math.sqrt(self.height**2 + (base / 2) ** 2)
            return base + 2 * side_length
        elif self.dimensions == 3:
            # Square pyramid: base + 4 triangular faces
            base_area = self.base_side_length**2
            # Slant height from center of base edge to apex
            slant_height = math.sqrt(self.height**2 + (self.base_side_length / 2) ** 2)
            triangle_area = 0.5 * self.base_side_length * slant_height
            return base_area + 4 * triangle_area
        else:
            # General case: base + lateral faces
            # Base is (n-1)-dimensional hypercube
            base_area = self.base_side_length ** (self.dimensions - 1)

            # Lateral surface area approximation
            # Each lateral face is an (n-1)-dimensional pyramid
            lateral_base = self.base_side_length ** (self.dimensions - 2)
            lateral_height = math.sqrt(
                self.height**2 + (self.base_side_length / 2) ** 2
            )
            lateral_area = lateral_base * lateral_height

            # Number of lateral faces = 2 * (n-1) for hypercube base
            num_lateral_faces = 2 * (self.dimensions - 1)

            return base_area + num_lateral_faces * lateral_area

    def get_base_volume(self) -> float:
        """Get the volume of the base"""
        return self.base_side_length ** (self.dimensions - 1)

    def get_base_surface_area(self) -> float:
        """Get the surface area of the base"""
        if self.dimensions <= 1:
            return 0
        return (
            2 * (self.dimensions - 1) * (self.base_side_length ** (self.dimensions - 2))
        )

    def get_apex_distance(self) -> float:
        """Get distance from base center to apex"""
        return self.height

    def get_slant_height(self) -> float:
        """Get slant height from base edge to apex"""
        return math.sqrt(self.height**2 + (self.base_side_length / 2) ** 2)

    def get_lateral_edge_length(self) -> float:
        """Get length of edges from base vertices to apex"""
        # Distance from base corner to center
        base_diagonal = self.base_side_length * math.sqrt(self.dimensions - 1) / 2
        return math.sqrt(self.height**2 + base_diagonal**2)

    def get_vertex_count(self) -> int:
        """Get the number of vertices"""
        if self.dimensions == 1:
            return 2  # Two endpoints
        else:
            # Base vertices + apex
            base_vertices = 2 ** (self.dimensions - 1)  # Hypercube vertices
            return base_vertices + 1

    def get_edge_count(self) -> int:
        """Get the number of edges"""
        if self.dimensions == 1:
            return 1  # One edge
        elif self.dimensions == 2:
            return 3  # Triangle
        else:
            # Base edges + edges from base vertices to apex
            base_edges = (self.dimensions - 1) * (
                2 ** (self.dimensions - 2)
            )  # Hypercube edges
            apex_edges = 2 ** (self.dimensions - 1)  # From each base vertex to apex
            return base_edges + apex_edges

    def get_face_count(self, k: int) -> int:
        """Get the number of k-dimensional faces"""
        if k < 0 or k > self.dimensions:
            return 0
        if k == self.dimensions:
            return 1  # The pyramid itself
        if k == self.dimensions - 1:
            # Base + lateral faces
            return 1 + 2 * (self.dimensions - 1)

        # For lower dimensions, this is complex - simplified approximation
        if k == 0:
            return self.get_vertex_count()
        elif k == 1:
            return self.get_edge_count()
        else:
            # Approximate based on base hypercube structure
            base_faces = self._binomial(self.dimensions - 1, k) * (
                2 ** (self.dimensions - 1 - k)
            )
            return base_faces + (self.dimensions - 1) * self._binomial(
                self.dimensions - 1, k - 1
            )

    def _binomial(self, n: int, k: int) -> int:
        """Calculate binomial coefficient C(n,k)"""
        if k > n or k < 0:
            return 0
        if k == 0 or k == n:
            return 1

        result = 1
        for i in range(1, k + 1):
            result = result * (n - i + 1) // i
        return result

    def get_shape_type(self) -> str:
        if self.dimensions == 1:
            return "Line Segment"
        elif self.dimensions == 2:
            return "Triangle"
        elif self.dimensions == 3:
            return "Square Pyramid"
        else:
            return f"{self.dimensions}D HyperPyramid"

    def get_volume_formula(self) -> str:
        if self.dimensions == 1:
            return "V₁ = s"
        elif self.dimensions == 2:
            return "V₂ = (1/2) × base × height"
        elif self.dimensions == 3:
            return "V₃ = (1/3) × base² × height"
        else:
            return f"V_{self.dimensions} = (1/{self.dimensions}) × base^{self.dimensions-1} × height"

    def get_surface_area_formula(self) -> str:
        if self.dimensions == 1:
            return "S₁ = 2"
        elif self.dimensions == 2:
            return "S₂ = base + 2 × √(h² + (base/2)²)"
        elif self.dimensions == 3:
            return "S₃ = base² + 4 × (1/2) × base × √(h² + (base/2)²)"
        else:
            return f"S_{self.dimensions} = base^{self.dimensions-1} + {2*(self.dimensions-1)} × lateral_face_area"

    def contains_point(self, point: List[float]) -> bool:
        """Check if a point is inside the pyramid (simplified check)"""
        if len(point) != self.dimensions:
            raise ValueError("Point dimension mismatch")

        # Simplified check: point must be within base bounds and height bounds
        if self.dimensions == 2:
            x, y = point[0], point[1]
            # Check if within triangular bounds (simplified)
            return (
                0 <= x <= self.base_side_length
                and 0 <= y <= self.height
                and x / self.base_side_length + y / self.height <= 1
            )
        elif self.dimensions == 3:
            x, y, z = point[0], point[1], point[2]
            # Check if within square pyramid bounds
            return (
                abs(x) <= self.base_side_length / 2
                and abs(y) <= self.base_side_length / 2
                and 0 <= z <= self.height
                and z / self.height >= max(abs(x), abs(y)) / (self.base_side_length / 2)
            )
        else:
            # Higher dimensions: simplified distance-based check
            base_coords = point[:-1]
            height_coord = point[-1]

            # Check height bounds
            if height_coord < 0 or height_coord > self.height:
                return False

            # Check if within base bounds (scaled by height)
            scale_factor = (self.height - height_coord) / self.height
            max_coord = max(abs(coord) for coord in base_coords)
            return max_coord <= (self.base_side_length / 2) * scale_factor

    def get_cross_section(self, height_level: float) -> float:
        """Calculate cross-sectional area at given height"""
        if height_level < 0 or height_level > self.height:
            return 0

        if self.dimensions == 1:
            return 1 if height_level <= self.height else 0

        # Scale factor based on height
        scale_factor = (self.height - height_level) / self.height
        scaled_side = self.base_side_length * scale_factor

        # Cross-section is an (n-1)-dimensional hypercube
        return scaled_side ** (self.dimensions - 1)

    def __str__(self) -> str:
        return f"{self.get_shape_type()} (dim={self.dimensions}, base={self.base_side_length:.3f}, height={self.height:.3f}): Volume={self.get_volume():.6f}, Surface Area={self.get_surface_area():.6f}, Vertices={self.get_vertex_count()}"


class TilingPattern(ABC):
    """Base class for tiling patterns and tessellations"""

    def __init__(self, dimensions: int, base_shape: NDShape, pattern_type: str):
        self.dimensions = dimensions
        self.base_shape = base_shape
        self.pattern_type = pattern_type
        self.tiles = []
        self.bounds = None

    @abstractmethod
    def generate_pattern(self, bounds: List[tuple], density: float = 1.0) -> List[Dict]:
        """Generate tiling pattern within given bounds"""
        pass

    def get_tile_count(self) -> int:
        """Get total number of tiles in the pattern"""
        return len(self.tiles)

    @abstractmethod
    def get_coverage_efficiency(self) -> float:
        """Calculate space coverage efficiency (0-1)"""
        pass

    def get_pattern_properties(self) -> Dict:
        """Get properties of the tiling pattern"""
        return {
            "dimensions": self.dimensions,
            "pattern_type": self.pattern_type,
            "base_shape": (
                self.base_shape.get_shape_type()
                if self.base_shape
                else self.pattern_type
            ),
            "tile_count": self.get_tile_count(),
            "coverage_efficiency": self.get_coverage_efficiency(),
        }


class RegularTiling(TilingPattern):
    """Regular tiling patterns (same shape, same size, regular arrangement)"""

    def __init__(self, dimensions: int, base_shape: NDShape, spacing: float = None):
        super().__init__(dimensions, base_shape, "regular")
        self.spacing = spacing or self._calculate_optimal_spacing()

    def _calculate_optimal_spacing(self) -> float:
        """Calculate optimal spacing for regular tiling"""
        if isinstance(self.base_shape, HyperCube):
            return self.base_shape.side_length
        elif isinstance(self.base_shape, HyperSphere):
            return 2 * self.base_shape.radius
        elif isinstance(self.base_shape, Simplex):
            return self.base_shape.side_length
        else:
            return 1.0

    def generate_pattern(self, bounds: List[tuple], density: float = 1.0) -> List[Dict]:
        """Generate regular tiling pattern"""
        self.bounds = bounds
        self.tiles = []

        if self.dimensions == 2:
            return self._generate_2d_regular_tiling(bounds, density)
        elif self.dimensions == 3:
            return self._generate_3d_regular_tiling(bounds, density)
        else:
            return self._generate_nd_regular_tiling(bounds, density)

    def _generate_2d_regular_tiling(
        self, bounds: List[tuple], density: float
    ) -> List[Dict]:
        """Generate 2D regular tiling"""
        spacing = self.spacing / density
        tiles = []

        x_min, x_max = bounds[0]
        y_min, y_max = bounds[1]

        if isinstance(self.base_shape, HyperCube):
            # Square tiling
            x = x_min
            while x <= x_max:
                y = y_min
                while y <= y_max:
                    tiles.append(
                        {
                            "position": [x, y],
                            "shape": self.base_shape,
                            "rotation": 0,
                            "scale": density,
                        }
                    )
                    y += spacing
                x += spacing

        elif isinstance(self.base_shape, Simplex) and self.dimensions == 2:
            # Triangular tiling
            spacing_x = spacing
            spacing_y = spacing * math.sqrt(3) / 2

            row = 0
            y = y_min
            while y <= y_max:
                x_offset = (spacing_x / 2) if row % 2 == 1 else 0
                x = x_min + x_offset
                while x <= x_max:
                    tiles.append(
                        {
                            "position": [x, y],
                            "shape": self.base_shape,
                            "rotation": 0 if row % 2 == 0 else 180,
                            "scale": density,
                        }
                    )
                    x += spacing_x
                y += spacing_y
                row += 1

        elif isinstance(self.base_shape, HyperSphere):
            # Hexagonal close packing for circles
            spacing_x = spacing
            spacing_y = spacing * math.sqrt(3) / 2

            row = 0
            y = y_min
            while y <= y_max:
                x_offset = (spacing_x / 2) if row % 2 == 1 else 0
                x = x_min + x_offset
                while x <= x_max:
                    tiles.append(
                        {
                            "position": [x, y],
                            "shape": self.base_shape,
                            "rotation": 0,
                            "scale": density,
                        }
                    )
                    x += spacing_x
                y += spacing_y
                row += 1

        self.tiles = tiles
        return tiles

    def _generate_3d_regular_tiling(
        self, bounds: List[tuple], density: float
    ) -> List[Dict]:
        """Generate 3D regular tiling"""
        spacing = self.spacing / density
        tiles = []

        x_min, x_max = bounds[0]
        y_min, y_max = bounds[1]
        z_min, z_max = bounds[2]

        if isinstance(self.base_shape, HyperCube):
            # Cubic tiling
            x = x_min
            while x <= x_max:
                y = y_min
                while y <= y_max:
                    z = z_min
                    while z <= z_max:
                        tiles.append(
                            {
                                "position": [x, y, z],
                                "shape": self.base_shape,
                                "rotation": [0, 0, 0],
                                "scale": density,
                            }
                        )
                        z += spacing
                    y += spacing
                x += spacing

        elif isinstance(self.base_shape, HyperSphere):
            # Face-centered cubic or hexagonal close packing
            layer = 0
            z = z_min
            while z <= z_max:
                # Alternate between two layer types for optimal packing
                if layer % 2 == 0:
                    # A layer
                    x = x_min
                    while x <= x_max:
                        y = y_min
                        while y <= y_max:
                            tiles.append(
                                {
                                    "position": [x, y, z],
                                    "shape": self.base_shape,
                                    "rotation": [0, 0, 0],
                                    "scale": density,
                                }
                            )
                            y += spacing
                        x += spacing
                else:
                    # B layer (offset)
                    x = x_min + spacing / 2
                    while x <= x_max:
                        y = y_min + spacing / 2
                        while y <= y_max:
                            tiles.append(
                                {
                                    "position": [x, y, z],
                                    "shape": self.base_shape,
                                    "rotation": [0, 0, 0],
                                    "scale": density,
                                }
                            )
                            y += spacing
                        x += spacing

                z += spacing * math.sqrt(2 / 3)  # Optimal z-spacing for FCC
                layer += 1

        self.tiles = tiles
        return tiles

    def _generate_nd_regular_tiling(
        self, bounds: List[tuple], density: float
    ) -> List[Dict]:
        """Generate n-dimensional regular tiling"""
        spacing = self.spacing / density
        tiles = []

        # Generate n-dimensional grid
        def generate_grid_points(dim_index: int, current_position: List[float]) -> None:
            if dim_index >= self.dimensions:
                tiles.append(
                    {
                        "position": current_position.copy(),
                        "shape": self.base_shape,
                        "rotation": [0] * self.dimensions,
                        "scale": density,
                    }
                )
                return

            dim_min, dim_max = bounds[dim_index]
            coord = dim_min
            while coord <= dim_max:
                current_position.append(coord)
                generate_grid_points(dim_index + 1, current_position)
                current_position.pop()
                coord += spacing

        generate_grid_points(0, [])
        self.tiles = tiles
        return tiles

    def get_coverage_efficiency(self) -> float:
        """Calculate coverage efficiency for regular tiling"""
        if not self.tiles or not self.bounds:
            return 0.0

        # Calculate total area/volume of bounds
        total_space = 1.0
        for dim_min, dim_max in self.bounds:
            total_space *= dim_max - dim_min

        # Calculate total area/volume of tiles
        tile_space = self.base_shape.get_volume() * len(self.tiles)

        return min(tile_space / total_space, 1.0) if total_space > 0 else 0.0


class HexagonalTiling(TilingPattern):
    """Hexagonal tiling pattern (2D only)"""

    def __init__(self, side_length: float):
        # Create hexagonal shape using coordinates
        super().__init__(2, None, "hexagonal")
        self.side_length = side_length
        self.hexagon_height = side_length * math.sqrt(3)
        self.hexagon_width = side_length * 2

    def generate_pattern(self, bounds: List[tuple], density: float = 1.0) -> List[Dict]:
        """Generate hexagonal tiling pattern"""
        self.bounds = bounds
        self.tiles = []

        x_min, x_max = bounds[0]
        y_min, y_max = bounds[1]

        spacing_x = self.hexagon_width * 0.75 / density
        spacing_y = self.hexagon_height / density

        row = 0
        y = y_min
        while y <= y_max:
            x_offset = (spacing_x / 2) if row % 2 == 1 else 0
            x = x_min + x_offset
            while x <= x_max:
                self.tiles.append(
                    {
                        "position": [x, y],
                        "shape": "hexagon",
                        "side_length": self.side_length * density,
                        "rotation": 0,
                        "scale": density,
                        "vertices": self._get_hexagon_vertices(
                            x, y, self.side_length * density
                        ),
                    }
                )
                x += spacing_x
            y += spacing_y
            row += 1

        return self.tiles

    def _get_hexagon_vertices(
        self, center_x: float, center_y: float, side_length: float
    ) -> List[List[float]]:
        """Generate vertices of a hexagon centered at given position"""
        vertices = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center_x + side_length * math.cos(angle)
            y = center_y + side_length * math.sin(angle)
            vertices.append([x, y])
        return vertices

    def get_coverage_efficiency(self) -> float:
        """Hexagonal tiling has 100% coverage efficiency"""
        return 1.0


class VoronoiTiling(TilingPattern):
    """Voronoi diagram tiling pattern"""

    def __init__(self, dimensions: int, seed_points: List[List[float]]):
        super().__init__(dimensions, None, "voronoi")
        self.seed_points = seed_points

    def generate_pattern(self, bounds: List[tuple], density: float = 1.0) -> List[Dict]:
        """Generate Voronoi diagram"""
        self.bounds = bounds
        self.tiles = []

        # For each seed point, create a Voronoi cell
        for i, seed in enumerate(self.seed_points):
            cell = {
                "position": seed,
                "seed_index": i,
                "shape": "voronoi_cell",
                "vertices": self._calculate_voronoi_vertices(seed, bounds),
                "scale": density,
            }
            self.tiles.append(cell)

        return self.tiles

    def _calculate_voronoi_vertices(
        self, seed: List[float], bounds: List[tuple]
    ) -> List[List[float]]:
        """Calculate vertices of Voronoi cell (simplified for 2D)"""
        if self.dimensions != 2:
            return []  # Complex calculation for higher dimensions

        vertices = []
        # This is a simplified implementation
        # In practice, you'd use algorithms like Fortune's algorithm
        x_min, x_max = bounds[0]
        y_min, y_max = bounds[1]

        # Create a simple rectangular cell as placeholder
        # Real implementation would calculate exact Voronoi boundaries
        cell_size = 1.0
        vertices = [
            [seed[0] - cell_size, seed[1] - cell_size],
            [seed[0] + cell_size, seed[1] - cell_size],
            [seed[0] + cell_size, seed[1] + cell_size],
            [seed[0] - cell_size, seed[1] + cell_size],
        ]

        return vertices

    def get_coverage_efficiency(self) -> float:
        """Voronoi tiling has 100% coverage efficiency"""
        return 1.0


class TilingAnalyzer:
    """Analyzer for tiling patterns and their properties"""

    def __init__(self, tiling_pattern: TilingPattern):
        self.pattern = tiling_pattern

    def analyze_pattern(self) -> Dict:
        """Comprehensive analysis of tiling pattern"""
        return {
            "basic_properties": self.pattern.get_pattern_properties(),
            "coverage_efficiency": self.pattern.get_coverage_efficiency(),
            "tile_density": self._calculate_tile_density(),
            "symmetry_properties": self._analyze_symmetry(),
            "mathematical_properties": self._analyze_mathematical_properties(),
        }

    def _calculate_tile_density(self) -> float:
        """Calculate number of tiles per unit area/volume"""
        if not self.pattern.bounds:
            return 0.0

        total_space = 1.0
        for dim_min, dim_max in self.pattern.bounds:
            total_space *= dim_max - dim_min

        return len(self.pattern.tiles) / total_space if total_space > 0 else 0.0

    def _analyze_symmetry(self) -> Dict:
        """Analyze symmetry properties of the tiling"""
        return {
            "translation_symmetry": True,  # Regular tilings have translation symmetry
            "rotation_symmetry": self._has_rotation_symmetry(),
            "reflection_symmetry": self._has_reflection_symmetry(),
            "point_symmetry": self._has_point_symmetry(),
        }

    def _has_rotation_symmetry(self) -> bool:
        """Check if pattern has rotational symmetry"""
        if self.pattern.pattern_type == "hexagonal":
            return True
        elif isinstance(self.pattern.base_shape, HyperCube):
            return True
        return False

    def _has_reflection_symmetry(self) -> bool:
        """Check if pattern has reflection symmetry"""
        return True  # Most regular tilings have reflection symmetry

    def _has_point_symmetry(self) -> bool:
        """Check if pattern has point symmetry"""
        return self.pattern.pattern_type in ["regular", "hexagonal"]

    def _analyze_mathematical_properties(self) -> Dict:
        """Analyze mathematical properties"""
        return {
            "is_periodic": True,
            "is_regular": self.pattern.pattern_type == "regular",
            "is_uniform": self.pattern.pattern_type in ["regular", "hexagonal"],
            "coordination_number": self._calculate_coordination_number(),
            "vertex_configuration": self._get_vertex_configuration(),
        }

    def _calculate_coordination_number(self) -> int:
        """Calculate coordination number (number of neighboring tiles)"""
        if self.pattern.pattern_type == "hexagonal":
            return 6
        elif isinstance(self.pattern.base_shape, HyperCube):
            return 2 * self.pattern.dimensions  # Each cube has 2n neighbors
        elif isinstance(self.pattern.base_shape, Simplex):
            return self.pattern.dimensions + 1  # Simplex coordination
        return 4  # Default

    def _get_vertex_configuration(self) -> str:
        """Get vertex configuration notation"""
        if self.pattern.pattern_type == "hexagonal":
            return "6.6.6"  # Three hexagons meet at each vertex
        elif isinstance(self.pattern.base_shape, HyperCube):
            return "4.4.4.4"  # Four squares meet at each vertex
        elif isinstance(self.pattern.base_shape, Simplex):
            return "3.3.3.3.3.3"  # Six triangles meet at each vertex
        return "unknown"


class GeometryAgent:
    """
    Python version of the agentic interface
    Enhanced with the ability to use original Java implementations
    """

    def __init__(self):
        self.java_bridge = JavaBridge()
        self.saved_shapes = {}
        self.shape_counter = 1

    def process_query(self, query: str) -> str:
        """Process natural language geometry queries"""
        query = query.lower().strip()

        try:
            # Special command to run original Java code
            if "original" in query and "java" in query:
                return self._handle_original_java_query(query)

            # Ellipsoid-specific queries (must come before general create)
            if "ellipse" in query or "ellipsoid" in query or "oval" in query:
                return self._handle_ellipsoid_query(query)

            # Simplex-specific queries (must come before general create)
            if "simplex" in query or "triangle" in query or "tetrahedron" in query:
                return self._handle_simplex_query(query)

            # Pyramid-specific queries (must come before general create)
            if "pyramid" in query or "cone" in query:
                return self._handle_pyramid_query(query)

            # Create shape queries (general, after specific shapes)
            if "create" in query or "make" in query:
                return self._handle_create_query(query)

            # Property queries
            if "volume" in query or "area" in query or "surface" in query:
                return self._handle_property_query(query)

            # Comparison queries
            if "compare" in query or "vs" in query or "versus" in query:
                return self._handle_comparison_query(query)

            # Tiling-specific queries
            if (
                "tiling" in query
                or "tessellation" in query
                or "tile" in query
                or "pattern" in query
            ):
                return self._handle_tiling_query(query)

            # Show available commands
            return self._show_help()

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def _handle_original_java_query(self, query: str) -> str:
        """Handle queries that want to use the original Java implementation"""
        diameter = self._extract_parameter(query)
        if diameter == -1:
            diameter = 2.0  # Default diameter

        java_result = self.java_bridge.run_original_multisphere(diameter)

        # Also show Python equivalent for comparison
        python_sphere = OriginalSphere(diameter)
        python_result = f"\n🔄 PYTHON EQUIVALENT:\n{python_sphere}\n"

        return java_result + python_result

    def _handle_create_query(self, query: str) -> str:
        """Handle shape creation queries"""
        dimensions = self._extract_dimensions(query)
        parameter = self._extract_parameter(query)

        if dimensions == -1:
            dimensions = 3
        if parameter == -1:
            return "Please specify a parameter (radius or side length)"

        if "cube" in query or "hypercube" in query:
            shape = HyperCube(dimensions, parameter)
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Side length = {parameter}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n• Diagonal: {shape.get_diagonal_length():.6f}"

            return result
        elif "ellipse" in query or "ellipsoid" in query or "oval" in query:
            # Handle ellipsoid creation with multiple axes
            axes = self._extract_multiple_parameters(query)
            if not axes or len(axes) != dimensions:
                return (
                    f"Please specify {dimensions} semi-axes for {dimensions}D ellipsoid"
                )

            shape = HyperEllipsoid(dimensions, *axes)
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Semi-axes = {axes}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            if shape.is_sphere():
                result += "Special Properties:\n• This is actually a sphere (all axes equal)\n"
            else:
                result += (
                    f"Special Properties:\n• Axis ratio: {shape.get_axis_ratio():.6f}\n"
                )
                if dimensions == 2:
                    result += f"• Eccentricity: {shape.get_eccentricity():.6f}\n"

            return result
        elif "simplex" in query or "triangle" in query or "tetrahedron" in query:
            shape = Simplex(dimensions, parameter)
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Side length = {parameter}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n• Circumradius: {shape.get_circumradius():.6f}\n• Inradius: {shape.get_inradius():.6f}\n• Height: {shape.get_height():.6f}"

            return result
        elif "pyramid" in query or "cone" in query:
            # Handle pyramid creation with base and height
            pyramid_params = self._extract_pyramid_parameters(query)
            if not pyramid_params:
                return "Please specify base side length and height for pyramid (e.g., 'base 2 height 3')"

            base_side, height = pyramid_params
            shape = HyperPyramid(dimensions, base_side, height)
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Base side length = {base_side}\n"
            result += f"Height = {height}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n• Slant height: {shape.get_slant_height():.6f}\n• Lateral edge: {shape.get_lateral_edge_length():.6f}\n• Base volume: {shape.get_base_volume():.6f}"

            return result
        else:
            shape = HyperSphere(dimensions, parameter)
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Radius = {parameter}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}"

            return result

    def _handle_property_query(self, query: str) -> str:
        """Handle property calculation queries"""
        dimensions = self._extract_dimensions(query)
        parameter = self._extract_parameter(query)

        if dimensions == -1:
            dimensions = 3
        if parameter == -1:
            return "Please specify a parameter (radius or side length)"

        if "cube" in query or "hypercube" in query:
            shape = HyperCube(dimensions, parameter)
            result = ""

            if "volume" in query:
                result += f"Volume of {dimensions}D cube: {shape.get_volume():.6f}\n"
                result += f"Formula: {shape.get_volume_formula()}"

            if "area" in query or "surface" in query:
                if result:
                    result += "\n"
                result += f"Surface area of {dimensions}D cube: {shape.get_surface_area():.6f}\n"
                result += f"Formula: {shape.get_surface_area_formula()}"

            if not result:
                result = str(shape)

            return result
        else:
            shape = HyperSphere(dimensions, parameter)
            result = ""

            if "volume" in query:
                result += f"Volume of {dimensions}D sphere: {shape.get_volume():.6f}\n"
                result += f"Formula: {shape.get_volume_formula()}"

            if "area" in query or "surface" in query:
                if result:
                    result += "\n"
                result += f"Surface area of {dimensions}D sphere: {shape.get_surface_area():.6f}\n"
                result += f"Formula: {shape.get_surface_area_formula()}"

            if not result:
                result = str(shape)

            return result

    def _handle_comparison_query(self, query: str) -> str:
        """Handle comparison queries"""
        dimensions = self._extract_dimensions(query)
        parameter = self._extract_parameter(query)

        if dimensions == -1:
            dimensions = 3
        if parameter == -1:
            parameter = 1.0

        sphere = HyperSphere(dimensions, parameter)
        cube = HyperCube(dimensions, parameter)

        sphere_volume = sphere.get_volume()
        cube_volume = cube.get_volume()
        sphere_surface = sphere.get_surface_area()
        cube_surface = cube.get_surface_area()

        return (
            f"Comparison in {dimensions}D (parameter = {parameter}):\n\n"
            + f"SPHERE (radius = {parameter}):\n• Volume: {sphere_volume:.6f}\n• Surface Area: {sphere_surface:.6f}\n• Formula: {sphere.get_volume_formula()}\n\n"
            + f"CUBE (side = {parameter}):\n• Volume: {cube_volume:.6f}\n• Surface Area: {cube_surface:.6f}\n• Formula: {cube.get_volume_formula()}\n• Vertices: {cube.get_vertex_count()}\n• Edges: {cube.get_edge_count()}\n\n"
            + f"RATIOS:\n• Volume ratio (sphere/cube): {sphere_volume/cube_volume:.6f}\n• Surface ratio (sphere/cube): {sphere_surface/cube_surface:.6f}\n\n"
            + f"INSIGHTS:\n• Sphere has {'more' if sphere_volume > cube_volume else 'less'} volume than cube\n• Cube has {cube.get_vertex_count()} vertices vs sphere's continuous surface"
        )

    def _show_help(self) -> str:
        """Show available commands"""
        return """🌌 N-Dimensional Geometry Engine Commands:

🎯 ORIGINAL JAVA INTEGRATION:
• 'original java sphere diameter 4' - Run the original CS102 MultiSphere
• 'original java multisphere' - Execute original Java code

🏗️ CREATING SHAPES:
• 'create a 4D sphere with radius 2'
• 'make a 5-dimensional cube with side 1.5'
• 'create a 6D hypercube side length 2'
• 'create a 3D ellipsoid with axes 1.5 2.0 3.0'
• 'make a 2D ellipse with semi-axes 2 3'
• 'create a 3D tetrahedron with side 2'
• 'make a 4D simplex side length 1.5'
• 'create a 3D pyramid base 2 height 3'
• 'make a 4D hyperpyramid base 2.5 height 4'

📊 CALCULATING PROPERTIES:
• 'volume of 3D sphere radius 2'
• 'surface area of 5D cube side 1'
• 'volume of 4D hypercube side 2.5'
• 'ellipsoid with axes 1 2 3'
• 'area of 2D ellipse semi-axes 2 3'
• 'triangle with side 3'
• 'tetrahedron side 2'
• 'pyramid base 2 height 3'

🔲 TILING PATTERNS:
• 'hexagonal tiling side 1.0 area 10x10'
• 'square tiling with cubes area 5x5'
• 'triangular tiling with simplices bounds 0 8'
• 'voronoi tiling seeds 15 area 12x8'
• 'regular tiling with circles density 1.5'

⚖️ COMPARISONS:
• 'compare sphere vs cube in 4 dimensions'
• 'compare 6D sphere and cube parameter 2'

🔍 SHAPE ANALYSIS:
• 'analyze 7D cube properties'
• 'show geometric properties of 5D sphere'

💡 Now supports spheres, cubes, ellipsoids, simplices, pyramids, and tiling patterns in any dimension!
💡 The original Java Sphere.java and MultiSphere.java are preserved and callable!
"""

    def _extract_dimensions(self, query: str) -> int:
        """Extract dimension number from query"""
        pattern = r"(\d+)\s*d(?:imension)?|\b(\d+)\s*dimensional"
        match = re.search(pattern, query)
        if match:
            return int(match.group(1) or match.group(2))
        return -1

    def _extract_parameter(self, query: str) -> float:
        """Extract parameter (radius/diameter/side) from query"""
        pattern = r"(?:radius|diameter|side|length)\s*(?:of|=|is)?\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:radius|diameter|side|length)"
        match = re.search(pattern, query)
        if match:
            return float(match.group(1) or match.group(2))
        return -1

    def _extract_multiple_parameters(self, query: str) -> List[float]:
        """Extract multiple parameters (for ellipsoid axes) from query"""
        # Look for patterns like "axes 1.5 2.0 3.0" or "semi-axes 1,2,3"
        pattern = r"(?:axes|semi-axes)\s*(?:of|=|is)?\s*([\d.,\s]+)"
        match = re.search(pattern, query)
        if match:
            # Split by comma or space and convert to floats
            axes_str = match.group(1).replace(",", " ")
            return [float(x) for x in axes_str.split() if x.strip()]

        # Fallback: look for sequences of numbers
        pattern = r"\b(\d+(?:\.\d+)?)\b"
        matches = re.findall(pattern, query)
        if len(matches) >= 2:
            return [float(x) for x in matches]

        return []

    def _handle_ellipsoid_query(self, query: str) -> str:
        """Handle ellipsoid-specific queries"""
        dimensions = self._extract_dimensions(query)
        if dimensions == -1:
            dimensions = 3

        # Extract axes parameters
        axes = self._extract_multiple_parameters(query)
        if not axes or len(axes) != dimensions:
            return f"Please specify {dimensions} semi-axes for {dimensions}D ellipsoid (e.g., 'axes 1 2 3')"

        shape = HyperEllipsoid(dimensions, *axes)

        if "create" in query or "make" in query:
            # Create and save the shape
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Semi-axes = {axes}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            if shape.is_sphere():
                result += "Special Properties:\n• This is actually a sphere (all axes equal)\n"
            else:
                result += (
                    f"Special Properties:\n• Axis ratio: {shape.get_axis_ratio():.6f}\n"
                )
                if dimensions == 2:
                    result += f"• Eccentricity: {shape.get_eccentricity():.6f}\n"
            return result
        else:
            # Just show properties without creating
            result = "HyperEllipsoid properties:\n"
            result += f"{shape}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"

            if shape.is_sphere():
                result += "Special Note: This is actually a sphere (all axes equal)\n"
            else:
                result += (
                    f"Special Properties:\n• Axis ratio: {shape.get_axis_ratio():.6f}\n"
                )
                if dimensions == 2:
                    result += f"• Eccentricity: {shape.get_eccentricity():.6f}\n"

            return result

    def _handle_simplex_query(self, query: str) -> str:
        """Handle simplex-specific queries"""
        dimensions = self._extract_dimensions(query)
        parameter = self._extract_parameter(query)

        if dimensions == -1:
            dimensions = 3
        if parameter == -1:
            return "Please specify a side length for the simplex"

        if "create" in query or "make" in query:
            return self._handle_create_query(query)

        # Property queries for simplices
        shape = Simplex(dimensions, parameter)

        result = "Simplex properties:\n"
        result += f"{shape}\n"
        result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
        result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n"
        result += f"• Circumradius: {shape.get_circumradius():.6f}\n• Inradius: {shape.get_inradius():.6f}\n• Height: {shape.get_height():.6f}\n"

        # Face counts
        result += "Face counts:\n"
        for k in range(dimensions + 1):
            faces = shape.get_face_count(k)
            if faces > 0:
                result += f"• {k}-faces: {faces}\n"

        return result

    def _extract_pyramid_parameters(self, query: str) -> tuple:
        """Extract base side length and height from pyramid query"""
        # Look for patterns like "base 2 height 3" or "base 2.5 height 4.0"
        pattern = r"base\s+(\d+(?:\.\d+)?)\s+height\s+(\d+(?:\.\d+)?)"
        match = re.search(pattern, query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # Alternative pattern: "side 2 height 3"
        pattern = r"side\s+(\d+(?:\.\d+)?)\s+height\s+(\d+(?:\.\d+)?)"
        match = re.search(pattern, query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # Look for two numbers in sequence
        pattern = r"\b(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\b"
        match = re.search(pattern, query)
        if match:
            return float(match.group(1)), float(match.group(2))

        return None

    def _handle_pyramid_query(self, query: str) -> str:
        """Handle pyramid-specific queries"""
        dimensions = self._extract_dimensions(query)
        if dimensions == -1:
            dimensions = 3

        # Extract pyramid parameters
        pyramid_params = self._extract_pyramid_parameters(query)
        if not pyramid_params:
            return "Please specify base side length and height for pyramid (e.g., 'base 2 height 3')"

        base_side, height = pyramid_params
        shape = HyperPyramid(dimensions, base_side, height)

        if "create" in query or "make" in query:
            # Create and save the shape
            name = f"shape{self.shape_counter}"
            self.shape_counter += 1
            self.saved_shapes[name] = shape

            result = f"Created {shape.get_shape_type()} '{name}':\n"
            result += f"{shape}\n"
            result += f"Base side = {base_side}, Height = {height}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n"
            result += f"• Slant height: {shape.get_slant_height():.6f}\n• Lateral edge: {shape.get_lateral_edge_length():.6f}\n• Base volume: {shape.get_base_volume():.6f}"
            return result
        else:
            # Just show properties without creating
            result = "HyperPyramid properties:\n"
            result += f"{shape}\n"
            result += f"Formulas:\n• {shape.get_volume_formula()}\n• {shape.get_surface_area_formula()}\n"
            result += f"Geometric Properties:\n• Vertices: {shape.get_vertex_count()}\n• Edges: {shape.get_edge_count()}\n"
            result += f"• Slant height: {shape.get_slant_height():.6f}\n• Lateral edge: {shape.get_lateral_edge_length():.6f}\n• Base volume: {shape.get_base_volume():.6f}\n"

            # Face counts
            result += "Face counts:\n"
            for k in range(dimensions + 1):
                faces = shape.get_face_count(k)
                if faces > 0:
                    result += f"• {k}-faces: {faces}\n"

            return result

    def _handle_tiling_query(self, query: str) -> str:
        """Handle tiling-specific queries"""
        dimensions = self._extract_dimensions(query)
        if dimensions == -1:
            dimensions = 2  # Default to 2D for tiling

        # Extract bounds
        bounds = self._extract_bounds(query)
        if not bounds:
            bounds = [(0, 10)] * dimensions  # Default bounds

        density = self._extract_density(query)
        if density == -1:
            density = 1.0  # Default density

        try:
            if "hexagonal" in query or "hexagon" in query:
                # Create hexagonal tiling
                side_length = self._extract_parameter(query)
                if side_length == -1:
                    side_length = 1.0

                tiling = HexagonalTiling(side_length)
                tiles = tiling.generate_pattern(bounds, density)
                analyzer = TilingAnalyzer(tiling)
                analysis = analyzer.analyze_pattern()

                result = "Hexagonal Tiling Pattern:\n"
                result += f"• Dimensions: {dimensions}D\n"
                result += f"• Side length: {side_length:.3f}\n"
                result += f"• Bounds: {bounds}\n"
                result += f"• Tile count: {len(tiles)}\n"
                result += (
                    f"• Coverage efficiency: {analysis['coverage_efficiency']:.3f}\n"
                )
                result += (
                    f"• Tile density: {analysis['tile_density']:.3f} tiles/unit²\n"
                )
                result += f"• Symmetry: {analysis['symmetry_properties']}\n"
                result += f"• Coordination number: {analysis['mathematical_properties']['coordination_number']}\n"
                result += f"• Vertex configuration: {analysis['mathematical_properties']['vertex_configuration']}\n"

                return result

            elif "voronoi" in query:
                # Create Voronoi tiling
                seed_count = self._extract_seed_count(query)
                if seed_count == -1:
                    seed_count = 10

                # Generate random seed points
                import random

                seeds = []
                for _ in range(seed_count):
                    seed = []
                    for i in range(dimensions):
                        dim_min, dim_max = bounds[i]
                        coord = random.uniform(dim_min, dim_max)
                        seed.append(coord)
                    seeds.append(seed)

                tiling = VoronoiTiling(dimensions, seeds)
                tiles = tiling.generate_pattern(bounds, density)
                analyzer = TilingAnalyzer(tiling)
                analysis = analyzer.analyze_pattern()

                result = "Voronoi Tiling Pattern:\n"
                result += f"• Dimensions: {dimensions}D\n"
                result += f"• Seed points: {seed_count}\n"
                result += f"• Bounds: {bounds}\n"
                result += f"• Tile count: {len(tiles)}\n"
                result += (
                    f"• Coverage efficiency: {analysis['coverage_efficiency']:.3f}\n"
                )
                result += f"• Tile density: {analysis['tile_density']:.3f} tiles/unit\n"
                result += "• Pattern type: Irregular (Voronoi)\n"

                return result

            else:
                # Regular tiling with shapes
                shape = self._determine_base_shape(query)
                if not shape:
                    return "Please specify a base shape for regular tiling (sphere, cube, simplex, etc.)"

                tiling = RegularTiling(dimensions, shape)
                tiles = tiling.generate_pattern(bounds, density)
                analyzer = TilingAnalyzer(tiling)
                analysis = analyzer.analyze_pattern()

                result = "Regular Tiling Pattern:\n"
                result += f"• Base shape: {shape.get_shape_type()}\n"
                result += f"• Dimensions: {dimensions}D\n"
                result += f"• Bounds: {bounds}\n"
                result += f"• Tile count: {len(tiles)}\n"
                result += (
                    f"• Coverage efficiency: {analysis['coverage_efficiency']:.3f}\n"
                )
                result += f"• Tile density: {analysis['tile_density']:.3f} tiles/unit\n"
                result += f"• Spacing: {tiling.spacing:.3f}\n"
                result += f"• Symmetry properties: {analysis['symmetry_properties']}\n"
                result += f"• Mathematical properties: {analysis['mathematical_properties']}\n"

                return result

        except Exception as e:
            return f"Error generating tiling pattern: {str(e)}"

    def _extract_bounds(self, query: str) -> List[tuple]:
        """Extract bounds from query"""
        # Look for patterns like "bounds 0 10" or "area 5x5"
        pattern = r"bounds?\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)"
        match = re.search(pattern, query)
        if match:
            min_val, max_val = float(match.group(1)), float(match.group(2))
            return [(min_val, max_val), (min_val, max_val)]

        # Look for area patterns like "5x5" or "10x8"
        pattern = r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)"
        match = re.search(pattern, query)
        if match:
            width, height = float(match.group(1)), float(match.group(2))
            return [(0, width), (0, height)]

        return None

    def _extract_density(self, query: str) -> float:
        """Extract density from query"""
        pattern = r"density\s+(\d+(?:\.\d+)?)"
        match = re.search(pattern, query)
        if match:
            return float(match.group(1))
        return -1

    def _extract_seed_count(self, query: str) -> int:
        """Extract seed count for Voronoi"""
        pattern = r"(?:seeds?|points?)\s+(\d+)"
        match = re.search(pattern, query)
        if match:
            return int(match.group(1))
        return -1

    def _determine_base_shape(self, query: str) -> NDShape:
        """Determine base shape from query"""
        dimensions = self._extract_dimensions(query)
        if dimensions == -1:
            dimensions = 2

        parameter = self._extract_parameter(query)
        if parameter == -1:
            parameter = 1.0

        if "cube" in query or "square" in query:
            return HyperCube(dimensions, parameter)
        elif "sphere" in query or "circle" in query:
            return HyperSphere(dimensions, parameter)
        elif "simplex" in query or "triangle" in query:
            return Simplex(dimensions, parameter)
        elif "pyramid" in query:
            height = parameter
            return HyperPyramid(dimensions, parameter, height)

        return None


def main():
    """Interactive console for the geometry engine"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           N-DIMENSIONAL GEOMETRY ENGINE (Python)            ║")
    print("║              with Original Java Integration                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    agent = GeometryAgent()

    if agent.java_bridge.java_available:
        print("✅ Java is available - Original CS102 code can be executed!")
    else:
        print("⚠️  Java not found - Using Python equivalents")

    print("\n💡 Try: 'original java sphere diameter 4'")
    print("   Or: 'create a 5D sphere with radius 2'")
    print("   Or: 'volume of 4D sphere radius 1.5'")
    print("\nType 'quit' to exit.")

    while True:
        query = input("\n🌌 Geometry > ").strip()

        if query.lower() in ["quit", "exit"]:
            print("Goodbye! Thanks for exploring n-dimensional geometry!")
            break

        if not query:
            continue

        print("\n" + agent.process_query(query))


if __name__ == "__main__":
    main()
