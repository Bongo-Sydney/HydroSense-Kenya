# AI Use Log - HydroSense-Kenya

**Student Name:** Bongo Sydney Meshack  
**Course:** ICS 2207 Scientific Computing  
**Project:** HydroSense-Kenya  

---

| Prompt Used                       | AI Output Summary                             | Accepted? | Modified? | Validation Method                               |
|-----------------------------------|-----------------------------------------------|-----------|-----------|-------------------------------------------------|
| How would one go about writing a  | Structure provided: 1. Context, 2. Specific problem, 3. Scientific gap, 4. Consequences, 5. Proposed approach, 6. Stakes | 
| problem statement?
Partly | Yes: Did not use some subsections of the structure | I compared my resultant problem statement to another from a real-life case study |
| Show me how one would create a data dictionary | Methods displayed: from existing dataset, using pandas DataFrames, using Python dictionary, along with respective codes | Partly | Yes: Modified code to fit my existing dataset and generate a dictionary | I checked that the dictionary was created in the processed folder |
| How do I restart kernel in VSCode? | - Click restart button, - Use Command Palette, - Kernel Menu | Yes | None | Kernel restarted and was able to run required libraries well |
| Generate code for loop-based ET computation | Provided function `et_loop_based()` using Python for-loops | Yes | None | Compared output with manual calculation on sample data |
| Generate code for vectorized ET computation | Provided function `calculate_et()` using NumPy vectorization | Yes | None | Compared execution time and confirmed identical results |
| How to compare loop vs vectorized performance? | Provided timing comparison code with `time.time()` and speedup calculation | Yes | Added performance scaling plot | Verified speedup factor matches expected (50-200x for large data) |
| Demonstrate floating point errors with 0.1 + 0.2 | Showed classic example and explained binary representation | Yes | Added error accumulation example | Manually verified `0.1 + 0.2 != 0.3` |
| How to simulate sensor noise propagation? | Provided Gaussian noise addition and error metrics calculation | Yes | Added wrong decision percentage metric | Ran experiment showing 5% noise → 20% wrong decisions |
| Implement bisection method for root finding | Provided complete function with bracketing and tolerance | Yes | Adjusted tolerance to 1e-6 | Tested on f(x)=x²-4, found root at 2.0 |
| Implement Newton-Raphson method | Provided function requiring derivative, with quadratic convergence | Yes | Added error handling for zero derivative | Tested on f(x)=cos(x)-x, converged in 4 iterations |
| Implement secant method | Provided function requiring two initial guesses, no derivative needed | Partly | Modified initial guess range | Compared convergence speed against bisection and Newton |
| Implement numerical differentiation (forward/backward/central) | Provided three difference methods with error analysis | Yes | Added soil moisture rate function | Verified central difference is most accurate O(h²) |
| Implement Trapezoidal and Simpson's integration rules | Provided composite rules with error order analysis | Yes | Fixed even interval requirement for Simpson | Compared with SciPy's trapezoid() function, difference < 1e-10 |
| How to solve three-zone water allocation using linear systems? | Provided Gaussian elimination and LU decomposition | Partly | Modified matrix for tomato, kale, maize zones | Verified allocations sum to total available water |
| Implement Euler method for soil moisture simulation | Provided time-stepping function with drainage term | Yes | Added non-negative moisture constraint | Compared with Runge-Kutta, max difference ~0.5% |
| Implement Runge-Kutta (4th order) for soil moisture | Provided RK4 function with higher accuracy O(h⁴) | Yes | None | RK4 showed smoother transitions than Euler |
| How to generate Monte Carlo rainfall scenarios? | Provided bootstrapping function from historical data | Yes | Added n_scenarios parameter | Verified mean of scenarios approximates historical mean |
| Fix ModuleNotFoundError: No module named 'src' | Provided sys.path.append() solution for path issues | Yes | Added project_root detection | All imports work correctly after adding path fix |
| How to fix "ValueError: The truth value of an array is ambiguous" | Changed `max(0, et)` to `np.maximum(0, et)` in numerical_methods.py | Yes | Also fixed water_balance function | Array operations now work element-wise without error |
| How to fix IndexError: invalid index to scalar variable | Corrected optimize_irrigation_schedule to return array instead of scalar | Yes | Modified function to initialize S as np.zeros(n_days) | S_optimized now returns array of length 27 |
| Fix KeyError: 'ET' not in index | Reordered cells to calculate ET before correlation matrix | Yes | None | ET column now exists before being referenced |
| How to handle mismatched dimensions (27 vs 30 days)? | Used actual n_days from data instead of hardcoding 30 | Yes | Removed all hardcoded values | All arrays now have consistent length (27) |

---

## Summary of AI Usage

- **Total AI prompts used:** 22
- **Total fully accepted (no modification):** 14
- **Total partially accepted (modified):** 8
- **Total rejected:** 0

**Validation Statement:** All AI-generated code and explanations have been manually reviewed, tested, and validated against project requirements and scientific correctness. The final submission represents my own understanding and work.

