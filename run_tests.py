#!/usr/bin/env python3
"""
Comprehensive Test Runner for N-Dimensional Geometry Engine
Runs all test categories and generates detailed reports
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


class TestRunner:
    """Comprehensive test runner with reporting capabilities."""

    def __init__(self):
        self.start_time = time.time()
        self.results = {}
        self.reports_dir = Path("test-reports")
        self.reports_dir.mkdir(exist_ok=True)

    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str, str]:
        """Run a command and return success status, stdout, stderr."""
        print(f"🔄 Running: {description}")
        print(f"   Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=600  # 10 minutes timeout
            )

            success = result.returncode == 0
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   {status}")

            if not success:
                print(f"   Error: {result.stderr}")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            print("   ⏰ TIMEOUT")
            return False, "", "Command timed out"
        except Exception as e:
            print(f"   💥 EXCEPTION: {e}")
            return False, "", str(e)

    def run_code_quality_checks(self) -> bool:
        """Run code quality checks."""
        print("\n" + "=" * 60)
        print("🔍 CODE QUALITY CHECKS")
        print("=" * 60)

        checks = [
            (
                ["black", "--check", "--diff", "--config", "pyproject.toml", "."],
                "Code formatting (Black)",
            ),
            (
                [
                    "isort",
                    "--check-only",
                    "--diff",
                    "--settings-path",
                    "pyproject.toml",
                    ".",
                ],
                "Import sorting (isort)",
            ),
            (["flake8", "--statistics", "."], "Linting (Flake8)"),
            (
                [
                    "mypy",
                    "--ignore-missing-imports",
                    "--exclude",
                    "mcp-server/deploy/.*",
                    "--exclude",
                    "\\.archive/.*",
                    ".",
                ],
                "Type checking (MyPy)",
            ),
            (
                ["bandit", "-r", ".", "-f", "json", "-o", "test-reports/bandit.json"],
                "Security scanning (Bandit)",
            ),
            (
                ["safety", "check", "--json"],
                "Dependency vulnerabilities (Safety)",
            ),
        ]

        all_passed = True
        for cmd, description in checks:
            try:
                success, stdout, stderr = self.run_command(cmd, description)
                self.results[description] = {
                    "success": success,
                    "stdout": stdout,
                    "stderr": stderr,
                }
                if not success:
                    all_passed = False
            except Exception as e:
                print(f"   ⚠️  Skipping {description}: {e}")
                self.results[description] = {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Skipped: {e}",
                }

        return all_passed

    def run_unit_tests(self) -> bool:
        """Run unit tests."""
        print("\n" + "=" * 60)
        print("🧪 UNIT TESTS")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/test_core.py",
            "-v",
            "--tb=short",
            "--cov=geometry_engine",
            "--cov-report=html:test-reports/coverage-unit",
            "--cov-report=xml:test-reports/coverage-unit.xml",
            "--junit-xml=test-reports/junit-unit.xml",
            "--html=test-reports/report-unit.html",
            "--self-contained-html",
            "-m",
            "unit",
        ]

        success, stdout, stderr = self.run_command(cmd, "Unit Tests")
        self.results["Unit Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_integration_tests(self) -> bool:
        """Run integration tests."""
        print("\n" + "=" * 60)
        print("🌐 INTEGRATION TESTS")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/test_api_integration.py",
            "-v",
            "--tb=short",
            "--cov=web_api",
            "--cov-report=html:test-reports/coverage-integration",
            "--cov-report=xml:test-reports/coverage-integration.xml",
            "--junit-xml=test-reports/junit-integration.xml",
            "--html=test-reports/report-integration.html",
            "--self-contained-html",
            "-m",
            "integration",
        ]

        success, stdout, stderr = self.run_command(cmd, "Integration Tests")
        self.results["Integration Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_performance_tests(self) -> bool:
        """Run performance tests."""
        print("\n" + "=" * 60)
        print("⚡ PERFORMANCE TESTS")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/test_performance.py",
            "-v",
            "--tb=short",
            "--benchmark-only",
            "--benchmark-sort=mean",
            "--benchmark-json=test-reports/benchmark.json",
            "--html=test-reports/report-performance.html",
            "--self-contained-html",
            "-m",
            "performance",
        ]

        success, stdout, stderr = self.run_command(cmd, "Performance Tests")
        self.results["Performance Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_mathematical_tests(self) -> bool:
        """Run mathematical accuracy tests."""
        print("\n" + "=" * 60)
        print("📐 MATHEMATICAL ACCURACY TESTS")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/test_mathematics.py",
            "-v",
            "--tb=short",
            "--junit-xml=test-reports/junit-mathematical.xml",
            "--html=test-reports/report-mathematical.html",
            "--self-contained-html",
            "-m",
            "mathematical",
        ]

        success, stdout, stderr = self.run_command(cmd, "Mathematical Tests")
        self.results["Mathematical Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_tiling_tests(self) -> bool:
        """Run tiling functionality tests."""
        print("\n" + "=" * 60)
        print("🔲 TILING TESTS")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/test_tiling.py",
            "-v",
            "--tb=short",
            "--junit-xml=test-reports/junit-tiling.xml",
            "--html=test-reports/report-tiling.html",
            "--self-contained-html",
            "-m",
            "tiling",
        ]

        success, stdout, stderr = self.run_command(cmd, "Tiling Tests")
        self.results["Tiling Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_comprehensive_tests(self) -> bool:
        """Run all tests together for comprehensive coverage."""
        print("\n" + "=" * 60)
        print("🎯 COMPREHENSIVE TEST SUITE")
        print("=" * 60)

        cmd = [
            "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--cov=.",
            "--cov-report=html:test-reports/coverage-comprehensive",
            "--cov-report=xml:test-reports/coverage-comprehensive.xml",
            "--cov-report=term-missing",
            "--junit-xml=test-reports/junit-comprehensive.xml",
            "--html=test-reports/report-comprehensive.html",
            "--self-contained-html",
            "--durations=10",
        ]

        success, stdout, stderr = self.run_command(cmd, "Comprehensive Test Suite")
        self.results["Comprehensive Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def run_java_tests(self) -> bool:
        """Run Java bridge tests if Java is available."""
        print("\n" + "=" * 60)
        print("☕ JAVA BRIDGE TESTS")
        print("=" * 60)

        # Check if Java is available
        java_check, _, _ = self.run_command(
            ["java", "-version"], "Java availability check"
        )
        if not java_check:
            print("   ⚠️  Java not available, skipping Java tests")
            return True

        # Check if Java files exist
        java_files = ["Sphere.java", "MultiSphere.java"]
        missing_files = [f for f in java_files if not os.path.exists(f)]
        if missing_files:
            print(f"   ⚠️  Missing Java files: {missing_files}, skipping Java tests")
            return True

        # Compile Java files
        compile_success, _, _ = self.run_command(
            ["javac", "Sphere.java", "MultiSphere.java"], "Java compilation"
        )
        if not compile_success:
            print("   ⚠️  Java compilation failed, skipping Java tests")
            return True

        # Run Java-specific tests
        cmd = [
            "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-m",
            "requires_java",
            "--html=test-reports/report-java.html",
            "--self-contained-html",
        ]

        success, stdout, stderr = self.run_command(cmd, "Java Bridge Tests")
        self.results["Java Tests"] = {
            "success": success,
            "stdout": stdout,
            "stderr": stderr,
        }

        return success

    def generate_summary_report(self) -> None:
        """Generate a comprehensive summary report."""
        print("\n" + "=" * 60)
        print("📊 GENERATING SUMMARY REPORT")
        print("=" * 60)

        end_time = time.time()
        total_time = end_time - self.start_time

        # Count results
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r["success"])
        failed_tests = total_tests - passed_tests

        # Generate summary
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_time": f"{total_time:.2f} seconds",
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (
                f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            ),
            "results": self.results,
        }

        # Save JSON report
        with open("test-reports/summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        # Generate HTML report
        html_report = self.generate_html_summary(summary)
        with open("test-reports/summary.html", "w") as f:
            f.write(html_report)

        # Print summary
        print("📊 Test Summary:")
        print(f"   Total Time: {total_time:.2f} seconds")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests*100):.1f}%")

        print("\n📁 Reports saved to: test-reports/")
        print("   📄 Summary: test-reports/summary.html")
        print("   📊 Coverage: test-reports/coverage-comprehensive/index.html")
        print("   🧪 Test Results: test-reports/report-comprehensive.html")

        return summary

    def generate_html_summary(self, summary: Dict) -> str:
        """Generate HTML summary report."""

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Summary Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
                .summary {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
                .success {{ color: green; }}
                .failure {{ color: red; }}
                .results {{ margin: 20px 0; }}
                .test-result {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ddd; }}
                .test-result.pass {{ border-left-color: green; background: #f0fff0; }}
                .test-result.fail {{ border-left-color: red; background: #fff0f0; }}
                .footer {{ margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧪 N-Dimensional Geometry Engine Test Results</h1>
                <p>Generated on {summary["timestamp"]}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Test Summary</h2>
                <p><strong>Total Time:</strong> {summary["total_time"]}</p>
                <p><strong>Total Tests:</strong> {summary["total_tests"]}</p>
                <p><strong>Passed:</strong> <span class="success">{summary["passed_tests"]}</span></p>
                <p><strong>Failed:</strong> <span class="failure">{summary["failed_tests"]}</span></p>
                <p><strong>Success Rate:</strong> <span style="color: {status_color};">{summary["success_rate"]}</span></p>
            </div>
            
            <div class="results">
                <h2>🔍 Detailed Results</h2>
        """

        for test_name, result in summary["results"].items():
            status = "PASSED" if result["success"] else "FAILED"
            status_icon = "✅" if result["success"] else "❌"
            error_section = f'<p><strong>Error:</strong> {result["stderr"]}</p>' if result["stderr"] else ''
            
            html += f"""
                <div class="test-result">
                    <h3>{status_icon} {test_name}</h3>
                    <p><strong>Status:</strong> {status}</p>
                    {error_section}
                </div>
            """

        html += """
            </div>
            
            <div class="footer">
                <h2>📁 Report Files</h2>
                <ul>
                    <li><a href="coverage-comprehensive/index.html">📊 Coverage Report</a></li>
                    <li><a href="report-comprehensive.html">🧪 Detailed Test Report</a></li>
                    <li><a href="benchmark.json">⚡ Performance Benchmarks</a></li>
                    <li><a href="summary.json">📄 JSON Summary</a></li>
                </ul>
            </div>
        </body>
        </html>
        """

        return html

    def run_all_tests(self) -> bool:
        """Run all test categories."""
        print("🚀 Starting Comprehensive Test Suite")
        print("🕐 Start time:", time.strftime("%Y-%m-%d %H:%M:%S"))

        # Run all test categories
        test_categories = [
            ("Code Quality", self.run_code_quality_checks),
            ("Unit Tests", self.run_unit_tests),
            ("Integration Tests", self.run_integration_tests),
            ("Performance Tests", self.run_performance_tests),
            ("Mathematical Tests", self.run_mathematical_tests),
            ("Tiling Tests", self.run_tiling_tests),
            ("Java Tests", self.run_java_tests),
            ("Comprehensive Tests", self.run_comprehensive_tests),
        ]

        all_passed = True
        for category_name, test_func in test_categories:
            try:
                success = test_func()
                if not success:
                    all_passed = False
            except Exception as e:
                print(f"💥 Error in {category_name}: {e}")
                all_passed = False

        # Generate summary report
        self.generate_summary_report()

        # Final status
        if all_passed:
            print("\n🎉 ALL TESTS PASSED! 🚀")
            print("The N-Dimensional Geometry Engine is ready for production!")
        else:
            print("\n❌ Some tests failed. Please check the reports.")

        return all_passed


def main():
    """Main function to run tests."""
    runner = TestRunner()

    # Parse command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()

        if test_type == "quality":
            success = runner.run_code_quality_checks()
        elif test_type == "unit":
            success = runner.run_unit_tests()
        elif test_type == "integration":
            success = runner.run_integration_tests()
        elif test_type == "performance":
            success = runner.run_performance_tests()
        elif test_type == "mathematical":
            success = runner.run_mathematical_tests()
        elif test_type == "tiling":
            success = runner.run_tiling_tests()
        elif test_type == "java":
            success = runner.run_java_tests()
        elif test_type == "comprehensive":
            success = runner.run_comprehensive_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print(
                "Available options: quality, unit, integration, performance, mathematical, tiling, java, comprehensive"
            )
            sys.exit(1)
    else:
        success = runner.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
