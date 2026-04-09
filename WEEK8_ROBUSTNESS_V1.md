# Week 8 Robustness Output (Version 1)

## Goal

Handle edge cases gracefully and log warnings in the trail.

## Required Outputs Checklist

- [x] Edge case list (minimum 5)
- [x] At least 3 edge-case tests documented
- [x] No crashes; warnings/messages shown in UI
- [x] Trail logs warnings clearly

## Edge Case List

1. Derivative near zero in Newton-Raphson (`|f'(x)| < 1e-12`).
2. Secant denominator near zero (`|f(x_n) - f(x_(n-1))| < 1e-12`).
3. Non-finite numeric inputs (`NaN`, `Infinity`, `-Infinity`).
4. Non-finite values during iteration (intermediate `x`, `f(x)`, or `f'(x)` becomes `NaN/Inf`).
5. Function/derivative evaluation exceptions during iteration.
6. Maximum iterations reached before convergence.
7. Unexpected runtime exceptions in solver/plot phase.

## Edge-Case Test Documentation

### Test EC-1: Derivative Near Zero (Newton-Raphson)
- Setup: Use function `f(x) = x² - 4` with initial guess close to zero (`x0 = 0`) where derivative is near zero.
- Expected behavior: No crash. Solver stops safely with warning that derivative is too small.
- Expected trail evidence: `STOPPING RULE` says safe stop; `WARNINGS` section includes derivative stability warning.

### Test EC-2: Missing x1 for Secant
- Setup: Select `Secant Method`, leave second guess field blank.
- Expected behavior: No crash. Validation fails before solve.
- Expected trail evidence: `VALIDATION` section shows FAIL and message: second guess required.

### Test EC-3: Non-finite Input (`NaN`)
- Setup: Enter `NaN` in `x0`.
- Expected behavior: No crash. Input validator blocks run with finite-number warning.
- Expected trail evidence: `VALIDATION` section shows finite input requirement.

### Test EC-4: Unstable / Non-finite Iteration
- Setup: Use very large starting values that can drive unstable updates.
- Expected behavior: No crash. Solver stops safely when a non-finite value is detected.
- Expected trail evidence: `WARNINGS` section logs non-finite iteration step.

## UI/Trail Robustness Behavior Added

- Solver now catches function/derivative evaluation errors and returns structured warnings.
- Solver detects non-finite values (`NaN/Inf`) in inputs, iteration steps, and residual checks.
- UI catches unexpected computation and plotting exceptions to avoid app crashes.
- Trail includes a dedicated `WARNINGS` section whenever warnings exist.
- Status badge reflects warning state (`Warning` or `Converged (Warnings)`).

## Evidence To Attach

- [ ] Screenshot: Edge-case run #1 (UI + trail)
- [ ] Screenshot: Edge-case run #2 (UI + trail)
- [ ] Screenshot: Edge-case run #3 (UI + trail)

Suggested filenames:
- `edge_case_1_derivative_warning.png`
- `edge_case_2_validation_warning.png`
- `edge_case_3_nonfinite_warning.png`

## Reflection

**Which edge case produced the most bugs and why?**

The non-finite numeric path (`NaN/Inf`) produced the most bugs because these values can bypass basic float parsing and then propagate silently into multiple steps (solver updates, residual checks, and plotting), so they required guards in several layers instead of a single validation check.
