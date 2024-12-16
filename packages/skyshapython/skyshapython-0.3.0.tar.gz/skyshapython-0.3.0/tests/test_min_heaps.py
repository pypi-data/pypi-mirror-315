import pytest
from skyshapython import MinHeap

def test_top_k_smallest():
    """Test extracting the top-k smallest elements."""
    data = [15, 20, 5, 10, 25, 1]
    k = 3

    heap = MinHeap(data)
    top_k = heap.pop(k)
    
    assert top_k == [1, 5, 10]

def test_sorting_ascending_with_pushpop():
    """Test whether sorting in order is possible with pushpop."""
    data = [4, 8, 12, 9, 3, 1, 5]

    heap = MinHeap()
    assert heap.pushpop(data) == [1, 3, 4, 5, 8, 9 ,12]

def test_sorting_ascending_with_popall():
    """Test whether sorting works with feeding values and using popall."""
    data = [4, 8, 12, 9, 3, 1, 5]

    heap = MinHeap(data)
    assert heap.popall() == [1, 3, 4, 5, 8, 9 ,12]

def test_sorting_ascending_with_pop():
    """Test whether sorting works with using pop for a value greater than the contents."""
    data = [4, 8, 12, 9, 3, 1, 5]

    heap = MinHeap(data)
    assert heap.pop(len(heap) + 1) == [1, 3, 4, 5, 8, 9 ,12]

def test_init_with_empty():
    """Test initializing an empty MinHeap."""
    heap = MinHeap()
    assert len(heap) == 0
    assert not heap  # Should evaluate to False when empty

def test_init_with_single_value():
    """Test initializing a MinHeap with a single value."""
    heap = MinHeap(42)
    assert len(heap) == 1
    assert heap.peek() == 42

def test_init_with_list():
    """Test initializing a MinHeap with a list."""
    heap = MinHeap([10, 20, 5])
    assert len(heap) == 3
    assert heap.popall() == [5, 10, 20]

def test_push_and_pop_single():
    """Test pushing and popping a single value."""
    heap = MinHeap()
    heap.push(100)
    assert heap.pop() == 100

def test_pop_partial():
    """Test popping fewer items than the heap contains."""
    heap = MinHeap([10, 20, 5])
    assert heap.pop(2) == [5, 10]
    assert heap.pop() == 20

def test_pop_more_than_available():
    """Test popping more items than the heap contains."""
    heap = MinHeap([10, 20, 5])
    assert heap.pop(5) == [5, 10, 20]  # Should return all items
    assert not heap  # Heap should be empty now

def test_push_multiple():
    """Test pushing multiple values."""
    heap = MinHeap()
    heap.push([10, 20, 30])
    assert len(heap) == 3
    assert heap.pop() == 10

def test_pushpop_single():
    """Test the pushpop operation with a single value."""
    heap = MinHeap([50, 30, 40])
    assert heap.pushpop(20) == 20  # 20 becomes the smallest and is popped
    assert heap.pop() == 30

def test_pushpop_multiple():
    """Test the pushpop operation with multiple values."""
    heap = MinHeap([10, 20])
    assert heap.pushpop([5, 15]) == [5, 10]  # Pushes and pops the 2 smallest
    assert heap.pop() == 15

def test_peek():
    """Test peek operation behavior."""
    heap = MinHeap([15, 10])
    assert heap.peek() == 10

def test_popall():
    """Test popall operation with multiple values."""
    heap = MinHeap([10, 20, 5])
    assert heap.popall() == [5, 10, 20]
    assert not heap  # Heap should now be empty

def test_popall_on_empty():
    """Test popall on an empty heap."""
    heap = MinHeap()
    assert heap.popall() == []  # Should return an empty list

def test_empty_pop():
    """Test pop operation when empty."""
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.pop()

def test_empty_pop_multiple():
    """Test multi-pop operation when empty"""
    heap = MinHeap()
    with pytest.raises(IndexError):
        heap.pop(2)

def test_len_and_bool():
    """Test len() and boolean behavior."""
    heap = MinHeap()
    assert len(heap) == 0
    assert not heap  # Should be False when empty

    heap.push([10, 20, 30])
    assert len(heap) == 3
    assert heap  # Should be True when not empty

def test_large_heap_operations():
    """Stress test with a large number of elements."""
    large_list = list(range(1, 10001))  # 10,000 elements
    heap = MinHeap(large_list)
    assert len(heap) == 10000
    assert heap.pop() == 1
    assert heap.pop(3) == [2, 3, 4]
