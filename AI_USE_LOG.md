# AI Use Log - HydroSense-Kenya

**Student Name:** Bongo Sydney Meshack  
**Course:** ICS 2207 Scientific Computing  
**Project:** HydroSense-Kenya  
## NOTE: SLIGHTLY ZOOM OUT TO VIEW TABLE PROPERLY.
---
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Prompt Used                       | AI Output Summary                             | Accepted? | Modified?             | Validation Method                      |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How would one go about writing a  | Structure provided:                           | Partly    | Yes: Did not use some | I compared my resultant problem        |
| problem statement?                | 1. Context,                                   |           | subsections of the    | statement to another from a real-life  |
|                                   | 2. Specific problem,                          |           | structure.            | case study.                            |
|                                   | 3. Scientific gap,                            |           |                       |                                        |
|                                   | 4. Consequences,                              |           |                       |                                        |
|                                   | 5. Proposed approach,                         |           |                       |                                        |
|                                   | 6. Stakes                                     |           |                       |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Show me how one would create a    | Methods displayed:                            | Partly    | Yes: Modified code to | I checked that the dictionary was      |
| data dictionary.                  | from existing dataset,                        |           | fit my existing one   | created in the processed folder.       |
|                                   | using pandas DataFrames,                      |           | and generate a        |                                        |
|                                   | using Python dictionary,                      |           | dictionary.           |                                        |
|                                   | along with respective codes.                  |           |                       |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How do I restart kernel in VSCode?| - Click restart button,                       | Yes       | None                  | Kernel restarted and was able to run   |
|                                   | - Use Command Palette,                        |           |                       | required libraries well.               |
|                                   | - Kernel Menu                                 |           |                       |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Generate code for loop-based ET   | Provided function `et_loop_based()` using     | Yes       | None                  | Compared output with manual calculation|
| computation. Using formula        | Python for-loops.                             |           |                       | on sample data.                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Generate code for vectorized ET   | Provided function `calculate_et()` using NumPy| Yes       | None                  | Compared execution time and confirmed  |
| computation.                      | vectorization.                                |           |                       | identical results.                     |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to compare loop vs vectorized | Provided timing comparison code with          | Yes       | Added performance     | Verified speedup factor matches        |
| performance?                      | `time.time()` and speedup calculation.        |           | scaling plot.         | expected (50-200x for large data)      |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Demonstrate floating point errors | Showed classic example and explained binary   | Yes       | Added error           | Manually verified `0.1 + 0.2 != 0.3`   |
| with 0.1 + 0.2                    | representation.                               |           | accumulation example. |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to simulate sensor noise      | Provided Gaussian noise addition and error    | Yes       | Added wrong decision  | Ran experiment showing 5% noise → 20%  |
| propagation?                      | metrics calculation.                          |           | percentage metric.    | wrong decisions.                       |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement bisection method for    | Provided complete function with bracketing    | Yes       | Adjusted tolerance to | Tested on f(x) = x²-4,                 |
| root finding.                     | and tolerance.                                |           | 1e-6.                 | found root at 2.0                      |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement Newton-Raphson method.  | Provided function requiring derivative, with  | Yes       | Added error handling  | Tested on f(x) = cos(x)-x,             |
|                                   | quadratic convergence.                        |           | for zero derivative.  | converged in 4 iterations.             |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement secant method.          | Provided function requiring two initial       | Partly    | Modified initial guess| Compared convergence speed against     |
|                                   | guesses, no derivative needed.                |           | range.                | Bisection and Newton.                  |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement numerical               | Provided three difference methods with error  | Yes       | Added soil moisture   | Verified central difference is most    |
| differentiation                   | analysis.                                     |           | rate function.        | accurate O(h².)                        |
| (forward/backward/central.)       |                                               |           |                       |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement Trapezoidal and         | Provided composite rules with error order     | Yes       | Fixed even interval   | Compared with SciPy's trapezoid()      |
| Simpson's integration rules.      | analysis.                                     |           | requirement for       | function, difference < 1e-10.          |
|                                   |                                               |           | Simpson.              |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to solve three-zone water     | Provided Gaussian elimination                 | Partly    | Modified matrix for   | Verified allocations sum to total      |
| allocation using linear systems?  |                                               |           | tomato, kale, maize   | available water.                       |
|                                   |                                               |           | zones.                |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement Euler method for soil   | Provided time-stepping function with drainage | Yes       | Added non-negative    | Compared with Runge-Kutta,             |
| moisture simulation.              | term.                                         |           | moisture constraint.  | max difference ~0.5%.                  |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Implement Runge-Kutta (4th order) | Provided RK4 function with higher accuracy    | Yes       | None                  | RK4 showed smoother transitions than   |
| for soil moisture.                | O(h⁴.)                                        |           |                       | Euler.                                 |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to generate Monte Carlo       | Provided bootstrapping function from          | Yes       | Added n_scenarios     | Verified mean of scenerios approximates|
| rainfall scenarios?               | historical data.                              |           | parameter.            | historic means.                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Fix ModuleNotFoundError: No module| Provided sys.path.append() solution for path  | Yes       | Added project_root    | All imports work correctly after adding|
| named 'src.'                      | issues.                                       |           | detection.            | path fix.                              |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to fix "ValueError: The truth | Changed `max(0, et)` to `np.maximum(0, et)`   | Yes       | Also fixed water_bal  | Array operations now work element-wise |
| value of an array is ambiguous."  | in numerical_methods.py.                      |           | function.             | without error.                         |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to fix IndexError: invalid    | Corrected optimize_irrigation_schedule to     | Yes       | Modified function to  | S_optimized now returns array of length|
| index to scalar variable.         | return array instead of scalar.               |           | initialize S as       | 27.                                    |
|                                   |                                               |           | np.zeros(n_days.)     |                                        |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| Fix KeyError: 'ET' not in index   | Reordered cells to calculate ET before        | Yes       | None                  | ET column now exists before being      |
|                                   | correlation matrix                            |           |                       | referenced.                            |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|
| How to handle mismatched          | Used actual n_days from data instead of       | Yes       | Removed all hardcoded | All arrays now have consistent length  |
| dimensions (27 vs 30 days)?       | hardcoding 30.                                |           | values                | (27.)                                  |
|-----------------------------------|-----------------------------------------------|-----------|-----------------------|----------------------------------------|

---

## Summary of AI Usage

- **Total AI prompts used:** 22
- **Total fully accepted (no modification):** 14
- **Total partially accepted (modified):** 8
- **Total rejected:** 0

**Validation Statement:** All AI-generated code and explanations have been manually reviewed, tested, and validated against project requirements and scientific correctness. The final submission represents my own understanding and work. Comments have also been written to explain the code for further understanding.

