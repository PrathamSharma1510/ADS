from time import time

class Reservation:
    def __init__(self, patronID, bookID, priorityNumber, timestamp=None):
        self.patronID = patronID
        self.bookID = bookID
        self.priorityNumber = priorityNumber
        self.timestamp = timestamp if timestamp is not None else time()

    def __lt__(self, other):
        if self.priorityNumber == other.priorityNumber:
            return self.timestamp < other.timestamp
        return self.priorityNumber < other.priorityNumber

    def __repr__(self):
        return f"({self.patronID}, {self.bookID}, {self.priorityNumber}, {self.timestamp})"

class WaitlistFullException(Exception):
    """Exception raised when the waitlist is full."""
    pass

class ReservationHeap:
    def __init__(self):
        self.heap = []
        self.max_size = 20

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index] < self.heap[parent]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def _heapify_down(self, index):
        length = len(self.heap)
        while index * 2 + 1 < length:
            smallest = index
            left = index * 2 + 1
            right = index * 2 + 2

            if self.heap[left] < self.heap[smallest]:
                smallest = left

            if right < length and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def insert(self, reservation):
        if len(self.heap) >= self.max_size:
            raise WaitlistFullException("Waitlist is full")
        self.heap.append(reservation)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        smallest = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)
        return smallest

    def peek(self):
        return self.heap[0] if self.heap else None

    def print_heap(self):
        for reservation in self.heap:
            print(reservation)


