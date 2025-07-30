#!/usr/bin/env python3
"""
Special demo to showcase the original Java CS102 code integration
"""

import subprocess

from geometry_engine import GeometryAgent


def demo_original_java_integration():
    """Demo the original Java code integration"""

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              ORIGINAL CS102 JAVA INTEGRATION                ║")
    print("║           Your First Working Code (2014) Lives On!          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    agent = GeometryAgent()

    print("🎯 Testing Original Java MultiSphere.java:")
    print("=" * 50)

    # Test the original Java code directly
    diameters = [1, 2, 3, 4, 5]

    for diameter in diameters:
        print(f"\n⚡ Testing diameter {diameter}:")
        print("-" * 30)

        # Run original Java
        try:
            result = subprocess.run(
                ["java", "MultiSphere"],
                input=str(diameter),
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines:
                    if line.strip():
                        print(f"🌟 Original Java: {line}")
            else:
                print(f"❌ Java error: {result.stderr}")

        except Exception as e:
            print(f"❌ Execution error: {e}")

    print("\n" + "=" * 60)
    print("🤖 Now testing with Agentic Interface:")
    print("=" * 60)

    # Test through the agentic interface
    test_queries = [
        "original java sphere diameter 1",
        "original java sphere diameter 5",
        "create a 3D sphere with radius 2.5",
        "compare original java vs 4D sphere",
        "volume of 10D sphere radius 1",
    ]

    for query in test_queries:
        print(f"\n🌌 Query: '{query}'")
        print("-" * 40)
        response = agent.process_query(query)
        print(response)
        print()

    print(
        "✨ SUCCESS! Your CS102 code is now part of an n-dimensional geometry engine! ✨"
    )


if __name__ == "__main__":
    demo_original_java_integration()
