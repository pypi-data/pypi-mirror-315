import numpy as np
from komlos_optimal.core import compute_signs_for_dataset, find_optimal_subsequence

def test_find_optimal_subsequence():
    vector = [1, 2, -1, -2, 3, 4]
    indices = find_optimal_subsequence(vector)
    subsequence = [vector[i] for i in indices]
    assert np.var(subsequence) == min(np.var(vector[i:j]) for i in range(len(vector)) for j in range(i + 1, len(vector) + 1))

def test_compute_signs_for_dataset():
    data = np.array([[1, 2, 3, -1, -2, -3], [4, 5, -6, -7, 8, 9]])
    signs = compute_signs_for_dataset(data)
    assert len(signs) == len(data)
    assert all(s in [-1, 0, 1] for s in signs)
