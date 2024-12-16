import time
import random
import threading
import concurrent.futures

class SortMaster:
    """Class to perform different sorting algorithms"""
    
    def __init__(self):
        """Initialize with no specific values / flags."""
        pass
    
    def bubble_sort(self, arr, reverse=False):
        """
        Bubble Sort: Repeatedly steps through the list, compares adjacent items, and swaps them 
        if they are in the wrong order. This process is repeated until the list is sorted.
        
        Time Complexity: O(n^2) in the worst case, where n is the number of elements in the list.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if (arr[j] > arr[j+1] and not reverse) or (arr[j] < arr[j+1] and reverse):
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def selection_sort(self, arr, reverse=False):
        """
        Selection Sort: Divides the input list into a sorted and unsorted region. Repeatedly selects
        the smallest (or largest) element from the unsorted region and swaps it with the first unsorted 
        element to expand the sorted region.

        Time Complexity: O(n^2), where n is the number of elements in the list.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        n = len(arr)
        for i in range(n):
            extreme_idx = i
            for j in range(i+1, n):
                if (arr[j] < arr[extreme_idx] and not reverse) or (arr[j] > arr[extreme_idx] and reverse):
                    extreme_idx = j
            arr[i], arr[extreme_idx] = arr[extreme_idx], arr[i]
        return arr

    def quick_sort(self, arr, reverse=False):
        """
        Quick Sort: Divides the list into two partitions based on a pivot. Elements smaller than the 
        pivot go to one partition, and elements greater than the pivot go to another. The partitioning 
        is done recursively.

        Time Complexity: O(n log n) on average, but can degrade to O(n^2) if the pivot is poorly chosen.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if (x < pivot and not reverse) or (x > pivot and reverse)]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if (x > pivot and not reverse) or (x < pivot and reverse)]
        return self.quick_sort(left, reverse) + middle + self.quick_sort(right, reverse)

    def merge_sort(self, arr, reverse=False):
        """
        Merge Sort: Divides the list into two halves, sorts each half recursively, and merges the two 
        sorted halves back together.

        Time Complexity: O(n log n), where n is the number of elements in the list.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        left_half = self.merge_sort(left_half, reverse)
        right_half = self.merge_sort(right_half, reverse)
        return self._merge(left_half, right_half, reverse)

    def _merge(self, left, right, reverse):
        """
        Helper function for merge sort: Merges two sorted lists into one sorted list.
        
        :param left: First sorted list.
        :param right: Second sorted list.
        :param reverse: If True, merges the lists in descending order. Default is False (ascending).
        :return: Merged sorted list.
        """
        result = []
        left_index, right_index = 0, 0
        while left_index < len(left) and right_index < len(right):
            if (left[left_index] < right[right_index] and not reverse) or (left[left_index] > right[right_index] and reverse):
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        result += left[left_index:]
        result += right[right_index:]
        return result

    def insertion_sort(self, arr, reverse=False):
        """
        Insertion Sort: Builds the sorted list one item at a time by repeatedly picking the next 
        element from the unsorted region and inserting it into its correct position in the sorted region.
        
        Time Complexity: O(n^2), where n is the number of elements in the list.

        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((key < arr[j] and not reverse) or (key > arr[j] and reverse)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def heap_sort(self, arr, reverse=False):
        """
        Heap Sort: Converts the list into a binary heap, and then repeatedly extracts the root element 
        (the largest or smallest) and rebuilds the heap until the list is sorted.

        Time Complexity: O(n log n), where n is the number of elements in the list.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        n = len(arr)

        # Build a max heap
        for i in range(n//2 - 1, -1, -1):
            self._heapify(arr, n, i, reverse)

        # One by one extract elements
        for i in range(n-1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self._heapify(arr, i, 0, reverse)
        return arr

    def _heapify(self, arr, n, i, reverse):
        """
        Helper function for heap sort: Ensures the heap property is maintained.

        :param arr: The list being sorted.
        :param n: Size of the heap.
        :param i: Index of the element being heapified.
        :param reverse: If True, heapifies for descending order. Default is False (ascending).
        :return: None
        """
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((arr[left] > arr[largest] and not reverse) or (arr[left] < arr[largest] and reverse)):
            largest = left
        if right < n and ((arr[right] > arr[largest] and not reverse) or (arr[right] < arr[largest] and reverse)):
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest, reverse)
    
    def timsort(self, arr, reverse=False):
        """
        Timsort: A hybrid sorting algorithm combining Merge Sort and Insertion Sort.
        Timsort is adaptive and performs well on real-world data. It divides the input into small "runs" (subarrays)
        and uses Insertion Sort to sort them, then merges the sorted runs using Merge Sort.
        
        Time Complexity: O(n log n) in the worst case, O(n) in the best case for partially sorted arrays.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        min_run = 32  # Minimum size for a "run" in Timsort

        def _tim_insertion_sort(arr, left, right, reverse):
            """Helper function to perform Insertion Sort on a subarray."""
            for i in range(left + 1, right + 1):
                key = arr[i]
                j = i - 1
                while j >= left and ((key < arr[j] and not reverse) or (key > arr[j] and reverse)):
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key

        def _tim_merge(arr, left, mid, right, reverse):
            """Helper function to merge two sorted halves of the array."""
            left_copy = arr[left:mid + 1]
            right_copy = arr[mid + 1:right + 1]
            i = j = 0
            k = left
            while i < len(left_copy) and j < len(right_copy):
                if (left_copy[i] < right_copy[j] and not reverse) or (left_copy[i] > right_copy[j] and reverse):
                    arr[k] = left_copy[i]
                    i += 1
                else:
                    arr[k] = right_copy[j]
                    j += 1
                k += 1
            while i < len(left_copy):
                arr[k] = left_copy[i]
                i += 1
                k += 1
            while j < len(right_copy):
                arr[k] = right_copy[j]
                j += 1
                k += 1

        # Step 1: Sort small subarrays using Insertion Sort
        n = len(arr)
        for start in range(0, n, min_run):
            end = min(start + min_run - 1, n - 1)
            _tim_insertion_sort(arr, start, end, reverse)

        # Step 2: Merge the subarrays using Merge Sort
        size = min_run
        while size < n:
            for start in range(0, n, 2 * size):
                mid = min(n - 1, start + size - 1)
                end = min(start + 2 * size - 1, n - 1)
                if mid < end:
                    _tim_merge(arr, start, mid, end, reverse)
            size *= 2

        return arr

    def introsort(self, arr, reverse=False):
        """
        IntroSort: Hybrid sorting algorithm that starts with QuickSort and switches to HeapSort
        when the recursion depth exceeds a certain limit. This ensures O(n log n) worst-case performance.

        QuickSort works well for average cases but can degrade to O(n^2) in the worst case. To avoid this, 
        IntroSort switches to HeapSort when the recursion depth exceeds a limit based on the number of elements 
        in the array.

        Time Complexity: O(n log n) in the worst case, with the switch to HeapSort preventing O(n^2) in QuickSort.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: Sorted list.
        """
        def _introsort_util(arr, depth_limit, reverse):
            """Helper function to perform the IntroSort."""
            if len(arr) <= 1:
                return arr
            if depth_limit == 0:
                return self.heap_sort(arr, reverse)  # Switch to heap sort when recursion depth limit is reached
            
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if (x < pivot and not reverse) or (x > pivot and reverse)]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if (x > pivot and not reverse) or (x < pivot and reverse)]

            return _introsort_util(left, depth_limit - 1, reverse) + middle + _introsort_util(right, depth_limit - 1, reverse)

        # Calculate the depth limit (2 * log(n)), where n is the number of elements
        depth_limit = 2 * (len(arr).bit_length())
        return _introsort_util(arr, depth_limit, reverse)


    def fastest(self, arr, reverse=False, display=False):
        """
        Runs multiple sorting algorithms in parallel and returns the name of the fastest sorting algorithm.

        This method runs the QuickSort, MergeSort, Timsort, and IntroSort algorithms concurrently in separate threads.
        It waits for the first algorithm to finish and identifies it as the fastest. Optionally, it displays the
        sorted result along with the name of the fastest algorithm.

        Time Complexity: Depends on the individual sorting algorithms, but typically O(n log n) for most.
        
        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :param display: If True, displays the name of the fastest algorithm and its sorted result. Default is False.
        :return: The name of the fastest sorting algorithm.
        """
        event = threading.Event()
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            algorithms = [
                ("QuickSort", "quick_sort"),
                ("MergeSort", "merge_sort"),
                ("Timsort", "timsort"),
                ("IntroSort", "introsort")
            ]

            for algorithm_name, algorithm in algorithms:
                futures.append(executor.submit(self._run_sorting_algorithm, algorithm_name, algorithm, arr, reverse, event, result))

            # Wait for the first algorithm to finish
            event.wait()

        # Return the name of the fastest algorithm
        fastest_algorithm = result[0][0]

        # Optionally display the result
        if display:
            print(f"First algorithm to finish: {fastest_algorithm}")
            print(f"Sorted result: {result[0][1]}")
        
        return fastest_algorithm
    
    def sleep_sort(self, arr, reverse=False):
        """Sleep Sort: A sorting algorithm that uses the system's sleep function to sort numbers.
        
        Each number in the array is treated as a separate thread, where each thread "sleeps" for a 
        time proportional to the number's value. Once each thread finishes sleeping, the numbers 
        are added to a result list in sorted order, as lower values finish sleeping first.

        Time Complexity: O(n), but highly impractical due to reliance on system timing and threads.
        
        :param arr: List of numbers to be sorted.
        :return: The sorted list.
        """
        def _sleep_and_append(num, result_list):
            """Helper function: Makes a thread sleep for a time proportional to the number's value."""
            time.sleep(num)
            result_list.append(num)

        result = []  # Initialize an empty list to store sorted numbers

        threads = []
        for num in arr:
            thread = threading.Thread(target=_sleep_and_append, args=(num, result))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return result[::-1] if reverse else result

    def bogosort(self, arr, reverse=False):
        """Bogosort: A notoriously inefficient sorting algorithm that randomly shuffles the list 
        until it happens to be sorted. It relies on the randomness to eventually find a sorted permutation.
        
        Time Complexity: O((n+1)!) in the worst case, making it extremely impractical for sorting.
        
        :param arr: List of numbers to be sorted.
        :return: The sorted list.
        """
        def _is_sorted(arr):
            """Helper function: Checks if the array is sorted."""
            if reverse:
                return all(arr[i] >= arr[i+1] for i in range(len(arr)-1))  # Check for descending order
            else:
                return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))  # Check for ascending order

        while not _is_sorted(arr):
            random.shuffle(arr)
        return arr

    def thread_sort(self, arr, reverse=False):
        """
        Runs multiple sorting algorithms in parallel and returns the result of the fastest algorithm.

        This method runs the QuickSort, MergeSort, Timsort, and IntroSort algorithms concurrently in separate threads.
        It waits for the first algorithm to finish and returns the sorted array from that algorithm.

        Time Complexity: Depends on the individual sorting algorithms, but typically O(n log n) for most.

        :param arr: List of elements to be sorted.
        :param reverse: If True, sorts the list in descending order. Default is False (ascending).
        :return: The sorted list from the fastest algorithm.
        """
        event = threading.Event()
        result = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            algorithms = [
                ("QuickSort", "quick_sort"),
                ("MergeSort", "merge_sort"),
                ("Timsort", "timsort"),
                ("IntroSort", "introsort")
            ]

            for algorithm_name, algorithm in algorithms:
                futures.append(executor.submit(self._run_sorting_algorithm, algorithm_name, algorithm, arr, reverse, event, result))

            # Wait for the first algorithm to finish
            event.wait()

        # Return the sorted array from the fastest algorithm
        return result[0][1]

    def _run_sorting_algorithm(self, algorithm_name, algorithm, arr, reverse, event, result):
        """
        Helper function that runs a sorting algorithm in a separate thread.

        This method is intended to be used within threads to execute the sorting algorithms.
        It runs the specified sorting algorithm on a copy of the input list and stores the result
        once the algorithm completes. It also signals the event once the first algorithm finishes.

        :param algorithm_name: The name of the algorithm being run.
        :param algorithm: The method name of the sorting algorithm to be executed.
        :param arr: The list of elements to be sorted.
        :param reverse: If True, sorts the list in descending order.
        :param event: A threading event used to signal when the first algorithm finishes.
        :param result: A list to store the algorithm name and sorted result.
        """
        try:
            # Execute the sorting algorithm and obtain the sorted array
            sorted_arr = getattr(self, algorithm)(arr.copy(), reverse)

            # If no algorithm has finished yet, mark this one as complete
            if not event.is_set():
                event.set()  # Set the event flag to signal completion
                result.append((algorithm_name, sorted_arr))  # Store the result (algorithm name and sorted array)

        except Exception as e:
            print(f"Error while running {algorithm_name}: {e}")