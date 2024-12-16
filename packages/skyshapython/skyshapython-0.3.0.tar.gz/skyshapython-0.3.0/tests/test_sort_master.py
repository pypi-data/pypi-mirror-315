import pytest
from skyshapython import SortMaster

@pytest.fixture
def sort_master():
    """Fixture to create an instance of SortMaster for testing."""
    return SortMaster()

def test_bubble_sort(sort_master):
    """Test Bubble Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.bubble_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.bubble_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_selection_sort(sort_master):
    """Test Selection Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.selection_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.selection_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_quick_sort(sort_master):
    """Test Quick Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.quick_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.quick_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_merge_sort(sort_master):
    """Test Merge Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.merge_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.merge_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_insertion_sort(sort_master):
    """Test Insertion Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.insertion_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.insertion_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_heap_sort(sort_master):
    """Test Heap Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.heap_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.heap_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_timsort(sort_master):
    """Test Timsort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.timsort(arr.copy(), reverse=False)
    sorted_desc = sort_master.timsort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_introsort(sort_master):
    """Test IntroSort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.introsort(arr.copy(), reverse=False)
    sorted_desc = sort_master.introsort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_thread_sort(sort_master):
    """Test Thread Sort with both ascending and descending order."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_asc = sort_master.thread_sort(arr.copy(), reverse=False)
    sorted_desc = sort_master.thread_sort(arr.copy(), reverse=True)

    assert sorted_asc == [1, 2, 5, 5, 6, 9]
    assert sorted_desc == [9, 6, 5, 5, 2, 1]

def test_edge_cases(sort_master):
    """Test edge cases like an empty list, single element list, and already sorted list."""
    
    # Empty list
    empty_list = []
    assert sort_master.bubble_sort(empty_list.copy(), reverse=False) == []
    assert sort_master.bubble_sort(empty_list.copy(), reverse=True) == []
    
    # Single element list
    single_element = [42]
    assert sort_master.bubble_sort(single_element.copy(), reverse=False) == [42]
    assert sort_master.bubble_sort(single_element.copy(), reverse=True) == [42]
    
    # Already sorted list
    sorted_list = [1, 2, 3, 4, 5]
    assert sort_master.bubble_sort(sorted_list.copy(), reverse=False) == sorted_list
    assert sort_master.bubble_sort(sorted_list.copy(), reverse=True) == sorted_list[::-1]
    
    # Reverse sorted list
    reverse_sorted_list = [5, 4, 3, 2, 1]
    assert sort_master.bubble_sort(reverse_sorted_list.copy(), reverse=False) == sorted_list
    assert sort_master.bubble_sort(reverse_sorted_list.copy(), reverse=True) == sorted_list[::-1]

def test_bogosort(sort_master):
    """Test Bogosort (this will be very slow, so avoid using on large datasets)."""
    arr = [5, 2, 9, 1, 5, 6]
    sorted_arr = sort_master.bogosort(arr.copy(), reverse=False)
    assert sorted_arr == sorted(arr)

@pytest.mark.parametrize("arr,expected", [
    ([5, 2, 9, 1, 5, 6], [1, 2, 5, 5, 6, 9]),
    ([1, 2, 3], [1, 2, 3]),
    ([3, 2, 1], [1, 2, 3]),
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
])
def test_sort_algorithms(sort_master, arr, expected):
    """Test all algorithms with various test cases using pytest parametrize."""
    assert sort_master.bubble_sort(arr.copy(), reverse=False) == expected
    assert sort_master.selection_sort(arr.copy(), reverse=False) == expected
    assert sort_master.quick_sort(arr.copy(), reverse=False) == expected
    assert sort_master.merge_sort(arr.copy(), reverse=False) == expected
    assert sort_master.insertion_sort(arr.copy(), reverse=False) == expected
    assert sort_master.heap_sort(arr.copy(), reverse=False) == expected
    assert sort_master.timsort(arr.copy(), reverse=False) == expected
    assert sort_master.introsort(arr.copy(), reverse=False) == expected

def test_fastest_sort(sort_master):
    """Test the fastest sort method."""
    arr = [5, 2, 9, 1, 5, 6]
    fastest = sort_master.fastest(arr.copy(), reverse=False)
    assert fastest in ["QuickSort", "MergeSort", "Timsort", "IntroSort"]

@pytest.mark.parametrize("arr,expected", [
    ([2, 1, 3, 2], [1, 2, 2, 3]),
    ([1], [1]),
    ([], []),
])
def test_sleep_sort(sort_master, arr, expected):
    """Test Sleep Sort (be cautious as this might be slow depending on the numbers)."""
    result = sort_master.sleep_sort(arr.copy(), reverse=False)
    assert result == expected