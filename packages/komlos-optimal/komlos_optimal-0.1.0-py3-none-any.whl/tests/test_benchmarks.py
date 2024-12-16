from komlos_optimal.benchmarks import benchmark_algorithms

def test_benchmark_algorithms():
    try:
        benchmark_algorithms(1, 10, 10)
        assert True  # If no exception is raised
    except Exception as e:
        pytest.fail(f"Benchmarking failed: {e}")
