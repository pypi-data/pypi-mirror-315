import pytest
from skyshapython import MaxHeap

def test_top_k_largest():
    """Test extracting the top-k largest elements."""
    data = [15, 20, 5, 10, 25, 1]
    k = 3

    # MinHeap keeps elements sorted by smallest
    heap = MaxHeap(data)
    top_k = heap.pop(k)
    
    assert top_k == [25, 20, 15]

def test_init_with_empty():
    """Test initializing an empty MaxHeap."""
    heap = MaxHeap()
    assert len(heap) == 0
    assert not heap  # Should evaluate to False when empty

def test_init_with_single_value():
    """Test initializing a MaxHeap with a single value."""
    heap = MaxHeap(42)
    assert len(heap) == 1
    assert heap.peek() == 42

def test_init_with_list():
    """Test initializing a MaxHeap with a list."""
    heap = MaxHeap([10, 20, 5])
    assert len(heap) == 3
    assert heap.popall() == [20, 10, 5]

def test_push_and_pop_single():
    """Test pushing and popping a single value."""
    heap = MaxHeap()
    heap.push(100)
    assert heap.pop() == 100

def test_pop_partial():
    """Test popping fewer items than the heap contains."""
    heap = MaxHeap([10, 20, 5])
    assert heap.pop(2) == [20, 10]
    assert heap.pop() == 5

def test_pop_more_than_available():
    """Test popping more items than the heap contains."""
    heap = MaxHeap([10, 20, 5])
    assert heap.pop(5) == [20, 10, 5]  # Should return all items
    assert not heap  # Heap should be empty now

def test_push_multiple():
    """Test pushing multiple values."""
    heap = MaxHeap()
    heap.push([10, 20, 30])
    assert len(heap) == 3
    assert heap.pop() == 30

def test_pushpop_single():
    """Test the pushpop operation with a single value."""
    heap = MaxHeap([50, 30, 40])
    assert heap.pushpop(60) == 60  # 60 becomes the largest and is popped
    assert heap.pop() == 50

def test_pushpop_multiple():
    """Test the pushpop operation with multiple values."""
    heap = MaxHeap([10, 20])
    assert heap.pushpop([30, 40]) == [40, 30]  # Pushes and pops the 2 largest
    assert heap.pop() == 20

def test_peek():
    """Test peek operation behaviour"""
    heap = MaxHeap([15, 10])
    assert heap.peek() == 15

def test_popall():
    """Test popall oeration with multiple values"""
    heap = MaxHeap([10, 20, 5])
    assert heap.popall() == [20, 10, 5]
    assert not heap  # Heap should now be empty

def test_popall_on_empty():
    """Test popall on an empty heap."""
    heap = MaxHeap()
    assert heap.popall() == []  # Should return an empty list

def test_empty_pop():
    """Test pop operation when empty"""
    heap = MaxHeap()
    with pytest.raises(IndexError):
        heap.pop()

def test_len_and_bool():
    """Test len() and boolean behavior."""
    heap = MaxHeap()
    assert len(heap) == 0
    assert not heap  # Should be False when empty

    heap.push([10, 20, 30])
    assert len(heap) == 3
    assert heap  # Should be True when not empty

def test_large_heap_operations():
    """Stress test with a large number of elements."""
    large_list = list(range(1, 10001))  # 10,000 elements
    heap = MaxHeap(large_list)
    assert len(heap) == 10000
    assert heap.pop() == 10000
    assert heap.pop(3) == [9999, 9998, 9997]