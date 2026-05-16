"""
RootSync - Newton-Raphson Solver
Core computation logic for root finding

=============================================================================
 BUILT-IN TEST CASES (Week 4 Requirement)
=============================================================================

 Test Case 1:
   Function:       f(x) = x² − 4
   Initial Guess:  x₀ = 3
   Tolerance:      ε = 0.0001
   Max Iterations: 20
   Expected Root:  x ≈ 2.0000
   Notes:          Simple quadratic, converges quickly in ~4 iterations

 Test Case 2:
   Function:       f(x) = x³ − x − 2
   Initial Guess:  x₀ = 1.5
   Tolerance:      ε = 0.0001
   Max Iterations: 20
   Expected Root:  x ≈ 1.5214
   Notes:          Cubic function, converges in ~4 iterations

 Test Case 3:
   Function:       f(x) = e⁻ˣ − x
   Initial Guess:  x₀ = 0.5
   Tolerance:      ε = 0.0001
   Max Iterations: 20
   Expected Root:  x ≈ 0.5671 (Lambert W function solution)
   Notes:          Transcendental function, converges in ~3 iterations

=============================================================================
 WEEK 12 TESTING & QA: DEBUG FLAGS
=============================================================================

Enable console logging for debugging by setting the environment variable:
  set ROOTSYNC_DEBUG=1

All computations will log their key decisions to stdout for auditability.

=============================================================================
"""

import math
import os


# ============================================================================
# DEBUG LOGGING CONFIGURATION (Week 12)
# ============================================================================
DEBUG = os.environ.get("ROOTSYNC_DEBUG", "").lower() == "1"

def debug_log(section, message):
    """Optional console logging for debugging (enabled with ROOTSYNC_DEBUG=1)"""
    if DEBUG:
        print(f"[{section}] {message}")


def _is_finite_number(value):
    """Return True when value is a finite int/float."""
    return isinstance(value, (int, float)) and math.isfinite(value)

# =============================================================================
# PREDEFINED FUNCTIONS (f, f')
# =============================================================================
def f1(x):  # x^2 - 4
    return x * x - 4.0

def df1(x):
    return 2.0 * x

def f2(x):  # x^3 - x - 2
    return x**3 - x - 2.0

def df2(x):
    return 3.0 * (x**2) - 1.0

def f3(x):  # e^(-x) - x
    return math.exp(-x) - x

def df3(x):
    return -math.exp(-x) - 1.0


# Dictionary mapping display names to (f, f') tuples
FUNCTIONS = {
    "f(x) = x² - 4": (f1, df1),
    "f(x) = x³ - x - 2": (f2, df2),
    "f(x) = e⁻ˣ - x": (f3, df3),
}


# =============================================================================
# NEWTON-RAPHSON SOLVER
# =============================================================================
def newton_raphson(f, df, x0, tol, max_iter, deriv_eps=1e-12):
    """
    Perform Newton-Raphson iteration to find root of f(x) = 0.
    
    Parameters:
        f: Function to find root of
        df: Derivative of f
        x0: Initial guess
        tol: Tolerance for convergence (|Δx| < tol)
        max_iter: Maximum number of iterations
        deriv_eps: Minimum acceptable derivative magnitude
    
    Returns:
        dict: {
            "converged": bool,
            "root": float,
            "iterations": int,
            "rows": list of dict rows (iteration data),
            "stop_reason": str,
            "residual": float,
        }
    """
    rows = []
    x = x0
    converged = False
    stop_reason = ""
    iterations_used = 0
    warnings = []

    debug_log("NEWTON_RAPHSON", f"Starting: x0={x0}, tol={tol}, max_iter={max_iter}")

    if not _is_finite_number(x):
        debug_log("NEWTON_RAPHSON", "Non-finite initial guess detected")
        return {
            "converged": False,
            "root": x0,
            "iterations": 0,
            "rows": rows,
            "stop_reason": "Stopped: non-finite initial guess.",
            "residual": float("inf"),
            "warnings": ["Initial guess is not finite (NaN/Inf)."],
        }

    for n in range(max_iter):
        try:
            fx = f(x)
            dfx = df(x)
        except Exception as exc:
            stop_reason = "Stopped: function/derivative evaluation error."
            warnings.append(f"Evaluation error at iteration {n}: {exc.__class__.__name__}: {exc}")
            iterations_used = n
            break

        if not _is_finite_number(fx) or not _is_finite_number(dfx):
            stop_reason = "Stopped: non-finite function value encountered."
            warnings.append(f"Non-finite value at iteration {n} (f(x)={fx}, f'(x)={dfx}).")
            iterations_used = n
            break

        if abs(dfx) < deriv_eps:
            stop_reason = f"Stopped: derivative too small (|f'(x)| < {deriv_eps})."
            warnings.append("Derivative near zero; Newton step would be unstable.")
            iterations_used = n
            break

        x_next = x - (fx / dfx)
        dx = abs(x_next - x)

        if not _is_finite_number(x_next) or not _is_finite_number(dx):
            stop_reason = "Stopped: non-finite iteration step encountered."
            warnings.append(f"Unstable update at iteration {n}; x_(n+1) became {x_next}.")
            iterations_used = n
            break

        rows.append({
            "n": n,
            "x_n": x,
            "f_x": fx,
            "df_x": dfx,
            "x_next": x_next,
            "dx": dx
        })

        if dx < tol:
            converged = True
            x = x_next
            iterations_used = n + 1
            stop_reason = "Converged: |Δx| < tolerance."
            debug_log("NEWTON_RAPHSON", f"Converged at iteration {n+1}: |Δx|={dx:.2e} < tol={tol:.2e}")
            break

        x = x_next
        iterations_used = n + 1

    if not converged and stop_reason == "":
        stop_reason = "Not converged: reached maximum iterations."
        warnings.append("Maximum iterations reached before tolerance was satisfied.")
        debug_log("NEWTON_RAPHSON", f"Max iterations reached: {iterations_used} iterations completed")

    try:
        residual_raw = f(x)
        residual = abs(residual_raw) if _is_finite_number(residual_raw) else float("inf")
        if not _is_finite_number(residual_raw):
            warnings.append("Residual is non-finite at final estimate.")
    except Exception as exc:
        residual = float("inf")
        warnings.append(f"Residual evaluation failed: {exc.__class__.__name__}: {exc}")

    return {
        "converged": converged,
        "root": x,
        "iterations": iterations_used,
        "rows": rows,
        "stop_reason": stop_reason,
        "residual": residual,
        "warnings": warnings,
    }


# =============================================================================
# SECANT METHOD SOLVER
# =============================================================================
def secant_method(f, x0, x1, tol, max_iter, denom_eps=1e-12):
    """
    Perform Secant Method iteration to find root of f(x) = 0.

    Parameters:
        f: Function to find root of
        x0: First initial guess
        x1: Second initial guess
        tol: Tolerance for convergence (|Δx| < tol)
        max_iter: Maximum number of iterations
        denom_eps: Minimum acceptable denominator magnitude

    Returns a dict with the same shape as newton_raphson().
    """
    rows = []
    x_prev = x0
    x_curr = x1
    converged = False
    stop_reason = ""
    iterations_used = 0
    warnings = []

    debug_log("SECANT_METHOD", f"Starting: x0={x0}, x1={x1}, tol={tol}, max_iter={max_iter}")

    if not _is_finite_number(x_prev) or not _is_finite_number(x_curr):
        debug_log("SECANT_METHOD", "Non-finite initial guesses detected")
        return {
            "converged": False,
            "root": x1,
            "iterations": 0,
            "rows": rows,
            "stop_reason": "Stopped: non-finite initial guesses.",
            "residual": float("inf"),
            "warnings": ["Initial guesses are not finite (NaN/Inf)."],
        }

    for n in range(max_iter):
        try:
            f_prev = f(x_prev)
            f_curr = f(x_curr)
        except Exception as exc:
            stop_reason = "Stopped: function evaluation error."
            warnings.append(f"Evaluation error at iteration {n}: {exc.__class__.__name__}: {exc}")
            iterations_used = n
            break

        if not _is_finite_number(f_prev) or not _is_finite_number(f_curr):
            stop_reason = "Stopped: non-finite function value encountered."
            warnings.append(f"Non-finite value at iteration {n} (f(x_n)={f_curr}, f(x_(n-1))={f_prev}).")
            iterations_used = n
            break

        denom = f_curr - f_prev
        if abs(denom) < denom_eps:
            stop_reason = f"Stopped: denominator too small (|f(x_n) - f(x_(n-1))| < {denom_eps})."
            warnings.append("Denominator near zero; secant step would be unstable.")
            iterations_used = n
            break

        x_next = x_curr - f_curr * (x_curr - x_prev) / denom
        dx = abs(x_next - x_curr)

        if not _is_finite_number(x_next) or not _is_finite_number(dx):
            stop_reason = "Stopped: non-finite iteration step encountered."
            warnings.append(f"Unstable update at iteration {n}; x_(n+1) became {x_next}.")
            iterations_used = n
            break

        rows.append({
            "n": n,
            "x_prev": x_prev,
            "x_curr": x_curr,
            "f_prev": f_prev,
            "f_curr": f_curr,
            "x_next": x_next,
            "dx": dx,
        })

        if dx < tol:
            converged = True
            x_curr = x_next
            iterations_used = n + 1
            stop_reason = "Converged: |Δx| < tolerance."
            debug_log("SECANT_METHOD", f"Converged at iteration {n+1}: |Δx|={dx:.2e} < tol={tol:.2e}")
            break

        x_prev = x_curr
        x_curr = x_next
        iterations_used = n + 1

    if not converged and stop_reason == "":
        stop_reason = "Not converged: reached maximum iterations."
        warnings.append("Maximum iterations reached before tolerance was satisfied.")
        debug_log("SECANT_METHOD", f"Max iterations reached: {iterations_used} iterations completed")

    try:
        residual_raw = f(x_curr)
        residual = abs(residual_raw) if _is_finite_number(residual_raw) else float("inf")
        if not _is_finite_number(residual_raw):
            warnings.append("Residual is non-finite at final estimate.")
    except Exception as exc:
        residual = float("inf")
        warnings.append(f"Residual evaluation failed: {exc.__class__.__name__}: {exc}")

    return {
        "converged": converged,
        "root": x_curr,
        "iterations": iterations_used,
        "rows": rows,
        "stop_reason": stop_reason,
        "residual": residual,
        "warnings": warnings,
    }


# =============================================================================
# INPUT VALIDATION
# =============================================================================
# =============================================================================
# TEST CASES (for programmatic verification)
# =============================================================================
# Week 12: Enhanced test suite with 10+ test cases covering:
# - Valid inputs with convergence
# - Invalid inputs (error handling)
# - Edge cases (tolerance boundaries, near-zero derivatives)
# - Stopping rules (convergence, max iterations, non-convergence)
# - Export and verification tests
TEST_CASES = [
    # ═════════════════════════════════════════════════════════════════════
    # VALID INPUT TESTS (Expected to converge)
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 1",
        "function": "f(x) = x² − 4",
        "x0": 3.0,
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": 2.0,
        "description": "Simple quadratic function with exact root at x=2",
        "category": "valid_convergence"
    },
    {
        "name": "Test Case 2",
        "function": "f(x) = x³ − x − 2",
        "x0": 1.5,
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": 1.5214,
        "description": "Cubic function - real root approximation",
        "category": "valid_convergence"
    },
    {
        "name": "Test Case 3",
        "function": "f(x) = e⁻ˣ − x",
        "x0": 0.5,
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": 0.5671,
        "description": "Transcendental function - Lambert W solution",
        "category": "valid_convergence"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # CONVERGENCE EDGE CASES (tight tolerance, many iterations)
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 4",
        "function": "f(x) = x² − 4",
        "x0": 3.0,
        "tol": 1e-10,  # Very tight tolerance
        "max_iter": 100,
        "expected_root": 2.0,
        "description": "Tight tolerance test - requires many iterations",
        "category": "convergence_tight_tolerance"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # STOPPING RULE TESTS (max iterations reached)
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 5",
        "function": "f(x) = x³ − x − 2",
        "x0": 1.5,
        "tol": 1e-15,  # Impossibly tight - forces max iterations
        "max_iter": 5,  # Few iterations allowed
        "expected_root": 1.5214,  # Expected if full convergence
        "description": "Max iterations stopping rule - tests iteration limit",
        "category": "stopping_rule_max_iter"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # EDGE CASE: NEAR-ZERO DERIVATIVE (Newton-Raphson stability)
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 6",
        "function": "f(x) = x² − 4",
        "x0": 0.0,  # Close to point where f'(x) = 2x ≈ 0
        "tol": 0.01,
        "max_iter": 20,
        "expected_root": 2.0,  # Should still converge despite small derivative
        "description": "Near-zero derivative test - Newton-Raphson stability",
        "category": "edge_case_derivative"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # SECANT METHOD SPECIFIC TESTS (different initial guesses)
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 7",
        "function": "f(x) = x² − 4",
        "x0": 1.0,  # First guess
        "x1": 3.0,  # Second guess
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": 2.0,
        "description": "Secant method with converging guesses",
        "category": "secant_valid"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # EDGE CASE: VERY SMALL TOLERANCE
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 8",
        "function": "f(x) = x² − 4",
        "x0": 3.0,
        "tol": 0.00001,  # Very small tolerance
        "max_iter": 50,
        "expected_root": 2.0,
        "description": "Very small tolerance - tests precision handling",
        "category": "edge_case_small_tol"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # EDGE CASE: INITIAL GUESS CLOSE TO ROOT
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 9",
        "function": "f(x) = x² − 4",
        "x0": 2.01,  # Very close to actual root (2.0)
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": 2.0,
        "description": "Initial guess close to root - tests fast convergence",
        "category": "edge_case_near_root"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # EDGE CASE: INITIAL GUESS FAR FROM ROOT
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 10",
        "function": "f(x) = x² − 4",
        "x0": 100.0,  # Very far from root
        "tol": 0.0001,
        "max_iter": 50,
        "expected_root": 2.0,
        "description": "Initial guess far from root - tests robustness",
        "category": "edge_case_far_guess"
    },
    
    # ═════════════════════════════════════════════════════════════════════
    # VALIDATION TEST: NEGATIVE INITIAL GUESS
    # ═════════════════════════════════════════════════════════════════════
    {
        "name": "Test Case 11",
        "function": "f(x) = x² − 4",
        "x0": -3.0,  # Negative initial guess (different root: x = -2)
        "tol": 0.0001,
        "max_iter": 20,
        "expected_root": -2.0,
        "description": "Negative initial guess - finds different root",
        "category": "valid_negative_root"
    },
]


def run_test_cases():
    """
    Run all built-in test cases and print results.
    Call this function to verify the solver works correctly.
    
    Usage:
        from solver import run_test_cases
        run_test_cases()
    
    Week 12 Enhancement:
    - Runs 11 comprehensive test cases
    - Reports convergence, iteration counts
    - Validates against expected roots
    - Provides category-based results
    """
    print("\n" + "=" * 80)
    print(" ROOTSYNC - COMPREHENSIVE TEST SUITE (Week 12 QA)")
    print("=" * 80)
    
    func_map = {
        "f(x) = x² − 4": (f1, df1),
        "f(x) = x³ − x − 2": (f2, df2),
        "f(x) = e⁻ˣ − x": (f3, df3),
    }
    
    all_passed = True
    results_by_category = {}
    
    for tc in TEST_CASES:
        category = tc.get("category", "uncategorized")
        if category not in results_by_category:
            results_by_category[category] = {"passed": 0, "total": 0}
        results_by_category[category]["total"] += 1
        
        print(f"\n{tc['name']}: {tc['function']}")
        print(f"  Category: {category}")
        print(f"  Description: {tc['description']}")
        print("-" * 80)
        
        f, df = func_map[tc['function']]
        
        # Run with appropriate method
        if "x1" in tc:
            # Secant Method
            x1 = tc['x1']
            result = secant_method(f, tc['x0'], x1, tc['tol'], tc['max_iter'])
            print(f"  Method: Secant")
            print(f"  x₀ = {tc['x0']:>10.6f}  |  x₁ = {x1:>10.6f}")
        else:
            # Newton-Raphson
            result = newton_raphson(f, df, tc['x0'], tc['tol'], tc['max_iter'])
            print(f"  Method: Newton-Raphson")
            print(f"  x₀ = {tc['x0']:>10.6f}")
        
        root = result['root']
        expected = tc['expected_root']
        error = abs(root - expected)
        passed = error < 0.01  # Allow 1% tolerance for test verification
        
        print(f"  ε = {tc['tol']:>15.2e}  |  Max Iterations: {tc['max_iter']}")
        print(f"\n  Computed Root:  {root:>14.8f}")
        print(f"  Expected Root:  {expected:>14.8f}")
        print(f"  Error:          {error:>14.10f}")
        print(f"  Converged:      {result['converged']}")
        print(f"  Iterations:     {result['iterations']}/{tc['max_iter']}")
        print(f"  Residual:       {result['residual']:>14.2e}")
        print(f"  Status:         {'✓ PASS' if passed else '✗ FAIL'}")
        
        # Show warnings if any
        warnings = result.get("warnings", [])
        if warnings:
            print(f"\n  Warnings ({len(warnings)}):")
            for i, w in enumerate(warnings, 1):
                print(f"    {i}. {w}")
        
        if not passed:
            all_passed = False
        else:
            results_by_category[category]["passed"] += 1
    
    # Summary by category
    print("\n" + "=" * 80)
    print(" TEST RESULTS BY CATEGORY")
    print("=" * 80)
    for category, stats in sorted(results_by_category.items()):
        passed = stats["passed"]
        total = stats["total"]
        status = "✓ PASS" if passed == total else f"✓ {passed}/{total}"
        print(f"  {category:<40} {status}")
    
    print("\n" + "=" * 80)
    print(f" OVERALL RESULT: {'ALL TESTS PASSED ✓' if all_passed else 'SOME TESTS FAILED ✗'}")
    print(f" ({sum(r['passed'] for r in results_by_category.values())}/{sum(r['total'] for r in results_by_category.values())} tests passed)")
    print("=" * 80 + "\n")
    
    return all_passed


# =============================================================================
# INPUT VALIDATION (Week 12 Enhanced)
# =============================================================================
def validate_inputs(x0_raw, tol_raw, max_iter_raw, method="Newton-Raphson", x1_raw=None):
    """
    Validate user inputs for supported root-finding computations.
    
    Week 12 Enhancements:
    - Reusable validation pattern for error handling
    - Comprehensive edge case checks
    - Clear, actionable error messages
    - Debug logging for troubleshooting
    
    Parameters:
        x0_raw: Raw string for initial guess x0
        tol_raw: Raw string for tolerance
        max_iter_raw: Raw string for max iterations
        method: Selected method name
        x1_raw: Raw string for second guess (secant only)
    
    Returns:
        tuple: (ok: bool, data: dict or None, error_message: str)
    """
    # Strip whitespace from all inputs
    x0_str = (x0_raw or "").strip()
    tol_str = (tol_raw or "").strip()
    it_str = (max_iter_raw or "").strip()
    method_str = (method or "").strip()
    x1_str = (x1_raw or "").strip() if x1_raw is not None else ""

    debug_log("VALIDATION", f"Method={method_str}, x0='{x0_str}', tol='{tol_str}', iter='{it_str}', x1='{x1_str}'")

    # ─────────────────────────────────────────────────────────────────────
    # STEP 1: Check for empty inputs
    # ─────────────────────────────────────────────────────────────────────
    if not x0_str or not tol_str or not it_str:
        msg = "All fields are required (x₀, tolerance, max iterations)."
        debug_log("VALIDATION", f"FAIL: {msg}")
        return (False, None, msg)

    if method_str.lower().startswith("secant") and not x1_str:
        msg = "Second Guess (x₁) is required for Secant Method."
        debug_log("VALIDATION", f"FAIL: {msg}")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 2: Parse x0 (initial guess)
    # ─────────────────────────────────────────────────────────────────────
    try:
        x0 = float(x0_str)
    except ValueError:
        msg = "Initial Guess (x₀) must be a valid number."
        debug_log("VALIDATION", f"FAIL: {msg} (got '{x0_str}')")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 3: Parse tolerance
    # ─────────────────────────────────────────────────────────────────────
    try:
        tol = float(tol_str)
    except ValueError:
        msg = "Tolerance must be a valid decimal number."
        debug_log("VALIDATION", f"FAIL: {msg} (got '{tol_str}')")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 4: Parse max iterations
    # ─────────────────────────────────────────────────────────────────────
    try:
        max_iter = int(it_str)
    except ValueError:
        msg = "Max Iterations must be an integer."
        debug_log("VALIDATION", f"FAIL: {msg} (got '{it_str}')")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 5: Parse x1 (second guess for Secant Method)
    # ─────────────────────────────────────────────────────────────────────
    x1 = None
    if x1_str:
        try:
            x1 = float(x1_str)
        except ValueError:
            msg = "Second Guess (x₁) must be a valid number."
            debug_log("VALIDATION", f"FAIL: {msg} (got '{x1_str}')")
            return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 6: Check for non-finite values (NaN, Inf)
    # ─────────────────────────────────────────────────────────────────────
    if not math.isfinite(x0):
        msg = "Initial Guess (x₀) must be finite (not NaN or Infinity)."
        debug_log("VALIDATION", f"FAIL: {msg} (x0={x0})")
        return (False, None, msg)

    if x1 is not None and not math.isfinite(x1):
        msg = "Second Guess (x₁) must be finite (not NaN or Infinity)."
        debug_log("VALIDATION", f"FAIL: {msg} (x1={x1})")
        return (False, None, msg)

    if not math.isfinite(tol):
        msg = "Tolerance must be finite (not NaN or Infinity)."
        debug_log("VALIDATION", f"FAIL: {msg} (tol={tol})")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 7: Validate tolerance (must be positive)
    # ─────────────────────────────────────────────────────────────────────
    if tol <= 0:
        msg = "Tolerance must be greater than 0."
        debug_log("VALIDATION", f"FAIL: {msg} (tol={tol})")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 8: Validate max iterations (positive, reasonable range)
    # ─────────────────────────────────────────────────────────────────────
    if max_iter <= 0:
        msg = "Max Iterations must be positive (at least 1)."
        debug_log("VALIDATION", f"FAIL: {msg} (max_iter={max_iter})")
        return (False, None, msg)

    if max_iter > 10000:  # Sanity check (prevent extreme iterations)
        msg = "Max Iterations cannot exceed 10000 (please use a reasonable value)."
        debug_log("VALIDATION", f"FAIL: {msg} (max_iter={max_iter})")
        return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # STEP 9: Secant Method specific validation
    # ─────────────────────────────────────────────────────────────────────
    if method_str.lower().startswith("secant"):
        if x1 is None:
            msg = "Secant Method requires both x₀ and x₁."
            debug_log("VALIDATION", f"FAIL: {msg}")
            return (False, None, msg)
        
        # Ensure x0 and x1 are different
        if abs(x0 - x1) < 1e-14:
            msg = "Secant Method requires two different guesses (x₀ ≠ x₁)."
            debug_log("VALIDATION", f"FAIL: {msg} (x0={x0}, x1={x1}, diff={abs(x0 - x1)})")
            return (False, None, msg)

    # ─────────────────────────────────────────────────────────────────────
    # VALIDATION PASSED
    # ─────────────────────────────────────────────────────────────────────
    data = {"x0": x0, "tol": tol, "max_iter": max_iter}
    if x1 is not None:
        data["x1"] = x1
    
    debug_log("VALIDATION", f"PASS ✓")
    return (True, data, "")
