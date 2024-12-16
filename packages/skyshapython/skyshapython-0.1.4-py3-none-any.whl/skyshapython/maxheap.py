import heapq

class MaxHeap:
    """
    A simple MaxHeap implementation using Python's built-in heapq library.
    """

    def __init__(self):
        """Use a list to store the heap elements (inverted for max-heap behavior)."""
        self._heap = []

    def push(self, item):
        """
        Adds an item to the heap.

        Usage:
            your_max_heap.push(value)
        """
        heapq.heappush(self._heap, -item)

    def pop(self):
        """
        Removes and returns the largest item from the heap.

        Usage:
            your_max_heap.pop()
        """
        if self._heap:
            return -heapq.heappop(self._heap)
        raise IndexError("pop from an empty MaxHeap")

    def pushpop(self, item):
        """
        Adds an item to the heap and removes/returns the largest item.
        This is more efficient than calling push() followed by pop().

        Usage:
            largest_value = your_max_heap.pushpop(some_value)
        """
        if self._heap:
            return -heapq.heappushpop(self._heap, -item)
        # If the heap is empty, the new item becomes the only element
        # and is immediately popped.
        return item

    def peek(self):
        """
        Returns the largest item without removing it.

        Usage:
            your_max_heap.peek()
        """
        if self._heap:
            return -self._heap[0]
        raise IndexError("peek from an empty MaxHeap")

    def __len__(self):
        """
        Returns the number of elements in the heap.
        
        Usage:
            len(your_max_heap)
        """
        return len(self._heap)

    def __bool__(self):
        """
        Heap evaluates to True if it contains any elements.
        
        Usage: 
            if your_max_heap:
            -- OR--
            if not your_max_heap:
        """
        return bool(self._heap)
