import awesomeapp.main as main

def test_calculate_stats():
    numbers = [1, 2, 3, 4, 5]
    stats = main.calculate_stats(numbers)
    assert stats["mean"] == 3.0
    assert stats["median"] == 3.0
    assert round(stats["std_dev"], 2) == 1.41