"""
Master Test Runner for Selenium Automation Assignments (1 - 9)
Executes all assignment test suites sequentially, records timings and status,
and displays a summary execution dashboard.

Usage:
    python run_all_assignments.py
"""

import subprocess
import sys
import time

TESTS = [
    ("Assignment 1: Multi-Locator Challenge", [sys.executable, "assignment1_multi_locator.py"]),
    ("Assignment 2: Synchronization & Explicit Waits", [sys.executable, "assignment2_explicit_waits.py"]),
    ("Assignment 3: Dynamic Dropdowns & Checkboxes", [sys.executable, "assignment3_dropdowns_checkboxes.py"]),
    ("Assignment 4: JavaScript Alerts and Confirms", [sys.executable, "assignment4_js_alerts.py"]),
    ("Assignment 5: HTML Web Table Extractor", [sys.executable, "assignment5_table_extractor.py"]),
    ("Assignment 6: Windows, Tabs, and Iframes", [sys.executable, "assignment6.py"]),
    ("Assignment 7: Page Object Model (POM)", [sys.executable, "-m", "pytest", "-v", "assignment7.py"]),
    ("Assignment 8: Data-Driven Automation (DDT)", [sys.executable, "assignment8.py"]),
    ("Assignment 9: PyTest Integration & HTML Report", [sys.executable, "-m", "pytest", "-v", "assignment9.py", "--html=report_a9.html", "--self-contained-html"]),
]


def main():
    print("=" * 75)
    print("STARTING COMPREHENSIVE VALIDATION RUNNER FOR ALL ASSIGNMENTS (1 to 9)")
    print("=" * 75 + "\n")

    results = []
    total_start = time.time()

    for name, cmd in TESTS:
        print(f">>> Running: {name}...")
        t0 = time.time()
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        duration = time.time() - t0
        status = "PASSED" if res.returncode == 0 else "FAILED"
        print(f"    Result: {status} in {duration:.2f}s")
        results.append((name, status, duration, res.stdout))

    total_duration = time.time() - total_start

    print("\n" + "=" * 75)
    print("FINAL EXECUTION SUMMARY DASHBOARD")
    print("=" * 75)
    print(f"{'Assignment Name':<48} | {'Status':<8} | {'Duration':<10}")
    print("-" * 75)
    for name, status, duration, _ in results:
        print(f"{name:<48} | {status:<8} | {duration:6.2f}s")
    print("-" * 75)
    print(f"Total Execution Time: {total_duration:.2f}s")

    all_passed = all(status == "PASSED" for _, status, _, _ in results)
    print(f"Overall Status: {'ALL ASSIGNMENTS PASSED (9/9)' if all_passed else 'SOME ASSIGNMENTS FAILED'}")
    print("=" * 75)

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
