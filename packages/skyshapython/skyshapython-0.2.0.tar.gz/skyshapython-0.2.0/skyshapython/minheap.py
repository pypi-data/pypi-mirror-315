import heapq

class MinHeap:
    """
    A simple MinHeap implementation using Python's built-in heapq library.
    """

    def __init__(self):
        """Use a list to store the heap elements."""
        self._heap = []

    def push(self, items):
        """
        Adds one or more items to the heap.

        Usage:
            your_min_heap.push(value)
            or
            your_min_heap.push([value1, value2, value3])
        """
        if isinstance(items, list):
            for item in items:
                heapq.heappush(self._heap, item)
        else:
            heapq.heappush(self._heap, items)

    def pop(self, num=1):
        """
        Removes and returns the smallest item(s) from the heap.

        Usage:
            smallest_value = your_min_heap.pop()
            or
            smallest_values = your_min_heap.pop(3)  # Pop the top 3 smallest items
        """
        if not isinstance(num, int) or num < 1:
            num = 1  # Default to popping 1 item if the input is invalid
        
        if self._heap:
            num = min(num, len(self._heap))  # Ensure we don't pop more than available
            return [heapq.heappop(self._heap) for _ in range(num)]
        raise IndexError("pop from an empty MinHeap")

    def pushpop(self, items):
        """
        Adds one or more items to the heap and removes/returns the smallest item(s).
        This is more efficient than calling push() followed by pop().

        Usage:
            smallest_value = your_min_heap.pushpop(some_value)
            or
            smallest_values = your_min_heap.pushpop([value1, value2])
        """
        if isinstance(items, list):
            # Add all items to the heap
            for item in items:
                heapq.heappush(self._heap, item)
            # Pop the smallest item(s)
            return [heapq.heappop(self._heap) for _ in range(min(len(items), len(self._heap)))]
        else:
            heapq.heappush(self._heap, items)
            # Pop the smallest item
            return heapq.heappop(self._heap)

    def peek(self):
        """
        Returns the smallest item without removing it.

        Usage:
            smallest_value = your_min_heap.peek()
        """
        if self._heap:
            return self._heap[0]
        raise IndexError("peek from an empty MinHeap")

    def __len__(self):
        """
        Returns the number of elements in the heap.

        Usage:
            len(your_min_heap)
        """
        return len(self._heap)

    def __bool__(self):
        """
        Heap evaluates to True if it contains any elements.

        Usage: 
            if your_min_heap:
            -- OR --
            if not your_min_heap:
        """
        return bool(self._heap)
