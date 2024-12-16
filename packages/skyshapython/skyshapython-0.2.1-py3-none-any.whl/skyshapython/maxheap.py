import heapq

class MaxHeap:
    """
    A simple MaxHeap implementation using Python's built-in heapq library.
    """

    def __init__(self):
        """Use a list to store the heap elements (inverted for max-heap behavior)."""
        self._heap = []

    def push(self, items):
        """
        Adds one or more items to the heap.

        Usage:
            your_max_heap.push(value)
            or
            your_max_heap.push([value1, value2, value3])
        """
        if isinstance(items, list):
            for item in items:
                heapq.heappush(self._heap, -item)
        else:
            heapq.heappush(self._heap, -items)

    def pop(self, num=1):
        """
        Removes and returns the largest item(s) from the heap.

        Usage:
            largest_value = your_max_heap.pop()
            or
            largest_values = your_max_heap.pop(3)  # Pop the top 3 largest items
        """
        if not isinstance(num, int) or num < 1:
            num = 1  # Default to popping 1 item if the input is invalid
        
        if self._heap:
            num = min(num, len(self._heap))  # Ensure we don't pop more than available
            return [-heapq.heappop(self._heap) for _ in range(num)]
        raise IndexError("pop from an empty MaxHeap")

    def pushpop(self, items):
        """
        Adds one or more items to the heap and removes/returns the largest item(s).
        This is more efficient than calling push() followed by pop().

        Usage:
            largest_value = your_max_heap.pushpop(some_value)
            or
            largest_values = your_max_heap.pushpop([value1, value2])
        """
        if isinstance(items, list):
            # Add all items to the heap
            for item in items:
                heapq.heappush(self._heap, -item)
            # Pop the largest item(s)
            return [-heapq.heappop(self._heap) for _ in range(min(len(items), len(self._heap)))]
        else:
            heapq.heappush(self._heap, -items)
            # Pop the largest item
            return -heapq.heappop(self._heap)

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
