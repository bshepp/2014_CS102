#!/usr/bin/env python3
"""
Test script to demonstrate the geometry engine capabilities
"""

from geometry_engine import GeometryAgent, HyperSphere, OriginalSphere


def test_original_sphere():
    """Test the original sphere implementation"""
    print("🎯 Testing Original Sphere (CS102 logic):")
    print("=" * 50)

    # Test with diameter 1 (like original MultiSphere)
    sphere = OriginalSphere(1.0)
    print(f"A sphere with diameter 1 has {sphere}")

    # Test with diameter 2.5
    sphere.set_diameter(2.5)
    print(f"After setting diameter to 2.5:")
    print(f"  Diameter: {sphere.get_diameter()}")
    print(f"  Volume: {sphere.get_volume():.3f}")
    print(f"  Surface Area: {sphere.get_area():.3f}")
    print()


def test_hypersphere():
    """Test n-dimensional hypersphere"""
    print("🌌 Testing N-Dimensional HyperSphere:")
    print("=" * 50)

    dimensions = [1, 2, 3, 4, 5, 10]
    radius = 1.0

    for dim in dimensions:
        sphere = HyperSphere(dim, radius)
        print(
            f"{dim}D: Volume = {sphere.get_volume():.6f}, Surface = {sphere.get_surface_area():.6f}"
        )
    print()


def test_agent_queries():
    """Test the agentic interface"""
    print("🤖 Testing Agentic Interface:")
    print("=" * 50)

    agent = GeometryAgent()

    test_queries = [
        "create a 3D sphere with radius 2",
        "volume of 4D sphere radius 1.5",
        "create a 5D sphere with radius 1",
        "surface area of 2D sphere radius 3",
    ]

    for query in test_queries:
        print(f"Query: {query}")
        print(f"Response: {agent.process_query(query)}")
        print("-" * 30)


def test_java_integration():
    """Test Java integration if available"""
    print("☕ Testing Java Integration:")
    print("=" * 50)

    agent = GeometryAgent()

    if agent.java_bridge.java_available:
        result = agent.process_query("original java sphere diameter 4")
        print(result)
    else:
        print("Java not available - showing Python equivalent:")
        result = agent.process_query("original java sphere diameter 4")
        print(result)
    print()


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              GEOMETRY ENGINE TEST SUITE                     ║")
    print("║         From CS102 (2014) to N-Dimensional Future          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    test_original_sphere()
    test_hypersphere()
    test_agent_queries()
    test_java_integration()

    print("✨ All tests completed! Your CS102 code lives on in glory! ✨")
