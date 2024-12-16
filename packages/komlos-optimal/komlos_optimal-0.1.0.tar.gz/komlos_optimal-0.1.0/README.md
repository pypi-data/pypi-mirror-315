# Komlós Optimal

A Python library for computing optimal subsequences inspired by the Komlós conjecture. It is designed to find signs of vectors based on subsequences that minimize variance, providing a fast and scalable alternative to brute force approaches.

---

## Features

- **Optimal Subsequence Algorithm**: Computes signs by identifying subsequences that minimize variance.
- **Performance**: Highly efficient compared to brute force methods, making it scalable for large datasets.
- **Flexibility**: Can process datasets with multiple vectors and high dimensionality.
- **Validation**: Benchmarked and tested against a brute force implementation to ensure correctness.

---

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory and activate your virtual environment.
3. Install the library:
   ```bash
   pip install -e .
   ```

---

## Usage

### Basic Example

```python
from komlos_optimal.core import compute_signs_for_dataset
import numpy as np

# Example dataset
data = np.array([
    [1, 2, 3, -1, -2, -3],
    [4, 5, -6, -7, 8, 9]
])

# Compute exact signs
signs = compute_signs_for_dataset(data)
print("Exact Signs:", signs)
```

### Benchmarking Against Brute Force

Use the following script to validate and benchmark the library against a brute force implementation:

```python
import numpy as np
from komlos_optimal.core import compute_signs_for_dataset

# Brute force implementation
def compute_brute_force_signs(vector):
    best_variance = float('inf')
    best_sign = 0
    for start in range(len(vector)):
        for end in range(start + 1, len(vector) + 1):
            subsequence = vector[start:end]
            variance = np.var(subsequence)
            mean = np.mean(subsequence)
            sign = np.sign(mean)
            if variance < best_variance:
                best_variance = variance
                best_sign = sign
    return best_sign

def compute_brute_force_signs_for_dataset(data):
    return np.array([compute_brute_force_signs(vector) for vector in data])

# Test dataset
data = np.random.randn(10, 100)

# Optimized algorithm
optimized_signs = compute_signs_for_dataset(data)

# Brute force algorithm
brute_force_signs = compute_brute_force_signs_for_dataset(data)

# Validate
if np.array_equal(optimized_signs, brute_force_signs):
    print("Results Match!")
else:
    print("Results Mismatch!")
```

---

## Performance Comparison

### Example Output:

For a dataset of 10 vectors with 100 dimensions:

```plaintext
Optimized Algorithm Time: 0.01 seconds
Brute Force Algorithm Time: 2.13 seconds
Results Match: Yes
```

This demonstrates that the optimized algorithm is significantly faster than brute force while producing identical results.

---

## Tests

Run the tests to ensure the library is working correctly:

1. Install `pytest`:
   ```bash
   pip install pytest
   ```

2. Run all tests:
   ```bash
   pytest
   ```

---

## Requirements

- Python 3.8+
- NumPy

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributions

Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## Author

Developed by **Anthony Olevester**. Feel free to reach out with feedback or questions!

---

Let me know if you want to customize any section further!