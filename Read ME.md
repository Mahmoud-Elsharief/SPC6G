# SPC6G Project

## Overview
This project implements calculations and simulations for SPC6G vehicular communication protocols. The code is organized into modular files for easier maintenance and reuse.

## Project Structure
```
SPC6G_Project/
├── main.py               # Entry point for the project
├── calculations.py       # Contains mathematical calculation functions
├── visualization.py      # (Optional) Contains plotting functions
├── constants.py          # Defines constants and global variables
└── README.md             # Describes the project
```

## Getting Started
1. Clone the repository to your local machine.
2. Install Python 3.8 or later.
3. Run the project:
   ```bash
   python main.py
   ```

## Files Description
### `main.py`
- This is the entry point for the project. It demonstrates how to use the calculation functions.

### `calculations.py`
- Contains the following functions:
  - `calculate_d_int`: Calculates interference distance based on signal parameters.
  - `calculate_RU`: Computes resource utilization for given conditions.
  - `calculate_u_dik`: Evaluates utility for resource allocation.

### `constants.py`
- Stores default values for constants used across the project.

### (Optional) `visualization.py`
- You can add custom visualization functions to analyze results graphically.

## Example Output
When running `main.py`, you will see:
- Interference distance
- Resource utilization
- Utility calculation

## Dependencies
- Python 3.8+
- NumPy
- Matplotlib (optional for visualization)

## Future Enhancements
- Add simulations for dynamic resource allocation.
- Implement visualizations for better understanding of results.

## License
This project is open-source under the MIT License.

