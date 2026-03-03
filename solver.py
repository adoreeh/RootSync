"""
RootSync - Newton-Raphson Solver
Core computation logic for root finding
"""

import math

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

    for n in range(max_iter):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < deriv_eps:
            stop_reason = f"Stopped: derivative too small (|f'(x)| < {deriv_eps})."
            iterations_used = n
            break

        x_next = x - (fx / dfx)
        dx = abs(x_next - x)

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
            break

        x = x_next
        iterations_used = n + 1

    if not converged and stop_reason == "":
        stop_reason = "Not converged: reached maximum iterations."

    residual = abs(f(x))

    return {
        "converged": converged,
        "root": x,
        "iterations": iterations_used,
        "rows": rows,
        "stop_reason": stop_reason,
        "residual": residual,
    }


# =============================================================================
# INPUT VALIDATION
# =============================================================================
def validate_inputs(x0_raw, tol_raw, max_iter_raw):
    """
    Validate user inputs for Newton-Raphson computation.
    
    Parameters:
        x0_raw: Raw string for initial guess
        tol_raw: Raw string for tolerance
        max_iter_raw: Raw string for max iterations
    
    Returns:
        tuple: (ok: bool, data: dict or None, error_message: str)
    """
    x0_str = x0_raw.strip()
    tol_str = tol_raw.strip()
    it_str = max_iter_raw.strip()

    if not x0_str or not tol_str or not it_str:
        return (False, None, "All fields are required (x₀, tolerance, max iterations).")

    try:
        x0 = float(x0_str)
    except ValueError:
        return (False, None, "Initial Guess (x₀) must be a valid number.")

    try:
        tol = float(tol_str)
    except ValueError:
        return (False, None, "Tolerance must be a valid decimal number.")

    try:
        max_iter = int(it_str)
    except ValueError:
        return (False, None, "Max Iterations must be an integer.")

    if tol <= 0:
        return (False, None, "Tolerance must be greater than 0.")
    
    if max_iter <= 0 or max_iter > 1000:
        return (False, None, "Max Iterations must be between 1 and 1000.")

    return (True, {"x0": x0, "tol": tol, "max_iter": max_iter}, "")
