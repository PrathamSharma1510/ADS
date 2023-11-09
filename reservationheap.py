import heapq
from time import time

class Reservation:
    def __init__(self, patronID, priorityNumber, timestamp=None):
        self.patronID = patronID
        self.priorityNumber = priorityNumber
        self.timestamp = timestamp if timestamp else time()
    
    def __lt__(self, other):
        if self.priorityNumber == other.priorityNumber:
            return self.timestamp < other.timestamp
        return self.priorityNumber < other.priorityNumber

    def __repr__(self):
        return f"({self.patronID}, {self.priorityNumber}, {self.timestamp})"

class ReservationHeap:
    def __init__(self):
        self.heap = []
        self.max_size = 20
        self.index_map = {}  # Maps patronID to the index in the heap

    def insert(self, reservation):
        if len(self.heap) >= self.max_size:
            raise Exception("Waitlist is full")
        self.index_map[reservation.patronID] = len(self.heap)
        heapq.heappush(self.heap, reservation)

    def extract_min(self):
        if self.heap:
            # When popping, remove the patronID from the index map
            reservation = heapq.heappop(self.heap)
            del self.index_map[reservation.patronID]
            # Rebuild index map for all items since they could have been reordered
            self._rebuild_index_map()
            return reservation
        return None

    def peek(self):
        if self.heap:
            return self.heap[0]
        return None

    def remove(self, patronID):
        index = self.index_map.get(patronID)
        if index is not None:
            # Swap with the last reservation and update the index map
            self.index_map[self.heap[-1].patronID] = index
            self.heap[index] = self.heap[-1]
            self.heap.pop()
            # Rebuild the heap from the new index and remove the patronID from the map
            if index < len(self.heap):
                heapq._siftup(self.heap, index)
                heapq._siftdown(self.heap, 0, index)
            del self.index_map[patronID]
            # Rebuild index map for all items since they could have been reordered
            self._rebuild_index_map()

    def update(self, patronID, newPriorityNumber):
        for reservation in self.heap:
            if reservation.patronID == patronID:
                reservation.priorityNumber = newPriorityNumber
                heapq.heapify(self.heap)
                self._rebuild_index_map()
                break

    def print_heap(self):
        print("Current waitlist:")
        for reservation in self.heap:
            print(reservation)

    def _rebuild_index_map(self):
        self.index_map = {reservation.patronID: i for i, reservation in enumerate(self.heap)}

# Example usage:
# reservation_heap = ReservationHeap()
# reservation_heap.insert(Reservation("Patron1", 1))
# reservation_heap.insert(Reservation("Patron2", 2))
# reservation_heap.print_heap()

# # Remove a reservation
# reservation_heap.remove("Patron1")
# reservation_heap.print_heap()

# # Update a reservation's priority
# reservation_heap.update("Patron2", 1)
# reservation_heap.print_heap()

# # Extract the reservation with the minimum priority
# min_reservation = reservation_heap.extract_min()
# print(f"Extracted reservation: {min_reservation}")
