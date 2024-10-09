class Heap:
    def __init__(self,comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''

        self.comparison_function = comparison_function
        self.heap = init_array[:]  # Create a copy of the input array
        self.size = len(init_array)
        self._build_heap()

    def _build_heap(self):
        # Heapify the array in O(n) time
        for i in range(self.size // 2 - 1, -1, -1):
            self._heapify_down(i)
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        self.heap.append(value)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
    
        if self.size == 0:
            return None
    
        top_value = self.heap[0]
        
        # Only replace the top with the last element if there are still elements left
        if self.size > 1:
            self.heap[0] = self.heap.pop()  # Replace the root with the last element
        else:
            self.heap.pop()  # Just remove the last element if it's the only one

        self.size -= 1
        
        # If there's still an element, heapify down
        if self.size > 0:
            self._heapify_down(0)
        
        return top_value
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        if self.size == 0:
            return None
        return self.heap[0]
    
    # You can add more functions if you want to

    def _heapify_up(self, index):
        '''
        Helper function to maintain heap property when an element is inserted.
        '''
        parent = (index - 1) // 2
        while index > 0 and self.comparison_function(self.heap[index], self.heap[parent]):
            # Swap the current element with its parent
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        '''
        Helper function to maintain heap property after extraction.
        '''
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index

        # Compare with left child
        if left_child < self.size and self.comparison_function(self.heap[left_child], self.heap[smallest]):
            smallest = left_child

        # Compare with right child
        if right_child < self.size and self.comparison_function(self.heap[right_child], self.heap[smallest]):
            smallest = right_child

        # If the current node is not the smallest, swap with the smallest child and recurse
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)