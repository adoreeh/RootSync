# RootSync Test Plan v1

## Scope

This plan validates the midterm version of the RootSync desktop app for Newton-Raphson and Secant root-finding workflows, UI trail visibility, and About/Help documentation requirements.

## Environment

- OS: Windows
- Python: 3.10+
- Dependency: matplotlib
- Run command: `python main.py`

## Test Cases

1. Valid Newton-Raphson run (quadratic)
- Input: Method `Newton-Raphson`, Function `f(x) = x² - 4`, `x0 = 3`, `tol = 0.0001`, `max_iter = 20`
- Expected: Converged status, root near `2.0000`, trail shows iteration table and final answer, graph shows points and root marker.

2. Valid Newton-Raphson run (transcendental)
- Input: Method `Newton-Raphson`, Function `f(x) = e⁻ˣ - x`, `x0 = 0.5`, `tol = 0.0001`, `max_iter = 20`
- Expected: Converged status, root near `0.5671`, verification section reports small residual.

3. Valid Secant run
- Input: Method `Secant Method`, Function `f(x) = x³ - x - 2`, `x0 = 1.0`, `x1 = 2.0`, `tol = 0.0001`, `max_iter = 20`
- Expected: Converged status, trail uses secant columns (`x_(n-1)`, `x_n`, `x_{n+1}`), graph includes both initial guesses.

4. Input validation failure (missing second guess)
- Input: Method `Secant Method`, leave `x1` empty, fill other fields.
- Expected: Validation fails with message that second guess is required; no computation rows are generated.

5. Input validation failure (non-numeric x0)
- Input: `x0 = abc`, valid tolerance and iterations.
- Expected: Validation fails with clear numeric-input error; status badge shows error state.

6. Input validation failure (invalid tolerance)
- Input: `tol = 0` (or negative), valid numeric `x0`, `max_iter`.
- Expected: Validation fails with tolerance must be greater than zero.

7. About/Help content check
- Action: Open About/Help via header button or `F1`.
- Expected: Dialog shows project name, version, members field, usage guidance, and screenshot guidance.

8. Trail visibility check for evidence
- Action: Run two successful test cases, keep trail panel visible.
- Expected: Screenshots can capture the steps table and final answer sections clearly.

## Pass Criteria

- At least 5 of the above tests are executed.
- All required-output tests (1, 3, 7, 8 and one validation test) pass.
- Evidence screenshots are captured for About/Help and at least two valid runs with trail visible.
