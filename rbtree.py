from collections import deque
from reservationheap import Reservation
class Node:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None,reservations=None):
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservations = reservations if reservations is not None else []
        self.parent = None
        self.color = 1  # Red = 1, Black = 0
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0, None, None, None)  # Our null leaf nodes will have the bookID set to 0
        self.NIL.color = 0
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL
        self.color_flip_count = 0  # To track color flips

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x


    def insert_book(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None):
        node = Node(bookID, bookName, authorName, availabilityStatus, borrowedBy)
        node.left = self.NIL
        node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if node.bookID < current.bookID:
                current = current.left
            elif node.bookID > current.bookID:
                current = current.right
            else:
                # Duplicate bookID, handle according to your system's requirements
                # This is where you might send an error message or take another action
                return False  # Indicates insertion failure due to duplicate ID

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.bookID < parent.bookID:
            parent.left = node
        else:
            parent.right = node

        self.fix_insert(node)
        return True  # Indicates successful insertion

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def fix_delete(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:  # Case 1
                    self.increment_color_flip_count(s.color, 0)
                    self.increment_color_flip_count(x.parent.color, 1)
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:  # Case 2
                    self.increment_color_flip_count(s.color, 1)
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:  # Case 3
                        self.increment_color_flip_count(s.left.color, 0)
                        self.increment_color_flip_count(s.color, 1)
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
                    # Case 4
                    self.increment_color_flip_count(s.color, x.parent.color)
                    self.increment_color_flip_count(x.parent.color, 0)
                    self.increment_color_flip_count(s.right.color, 0)
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # Symmetric cases for the right child
                s = x.parent.left
                if s.color == 1:  # Symmetric Case 1
                    self.increment_color_flip_count(s.color, 0)
                    self.increment_color_flip_count(x.parent.color, 1)
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == 0 and s.left.color == 0:  # Symmetric Case 2
                    self.increment_color_flip_count(s.color, 1)
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:  # Symmetric Case 3
                        self.increment_color_flip_count(s.right.color, 0)
                        self.increment_color_flip_count(s.color, 1)
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left
                    # Symmetric Case 4
                    self.increment_color_flip_count(s.color, x.parent.color)
                    self.increment_color_flip_count(x.parent.color, 0)
                    self.increment_color_flip_count(s.left.color, 0)
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root

        if x.color == 0:
            self.increment_color_flip_count(x.color, 1)
            x.color = 1


    def fix_insert(self, k):
        while k != self.root and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # Uncle node
                if u.color == 1:  # Uncle is red
                    self.increment_color_flip_count(u.color, 0)
                    self.increment_color_flip_count(k.parent.color, 0)
                    self.increment_color_flip_count(k.parent.parent.color, 1)
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    self.increment_color_flip_count(k.parent.color, 0)
                    self.increment_color_flip_count(k.parent.parent.color, 1)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                # Symmetric to the above case
                u = k.parent.parent.right
                if u.color == 1:  # Uncle is red
                    self.increment_color_flip_count(u.color, 0)
                    self.increment_color_flip_count(k.parent.color, 0)
                    self.increment_color_flip_count(k.parent.parent.color, 1)
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    self.increment_color_flip_count(k.parent.color, 0)
                    self.increment_color_flip_count(k.parent.parent.color, 1)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)

        self.increment_color_flip_count(self.root.color, 0)
        self.root.color = 0  # Always set root color to black







    def borrow_book(self, patronID, bookID, patronPriority, reservationHeap):
        book_node = self.search_book(bookID)
        if book_node is None or book_node == self.NIL:
            return "Book not found."

        # Check if the book is available or already borrowed by the same patron
        if book_node.availabilityStatus.strip('\"').lower() == "yes" and book_node.borrowedBy is None:
            book_node.availabilityStatus = "No"
            book_node.borrowedBy = patronID
            return f"Book {bookID} Borrowed by Patron {patronID}\n"

        if book_node.borrowedBy == patronID:
            return f"Patron {patronID} has already borrowed Book {bookID}.\n"

        # Check if the patron has already reserved the book
        if patronID in book_node.reservations:
            return f"Patron {patronID} has already reserved the book {bookID}.\n"

        try:
            # Insert the new reservation into the heap
            reservation = Reservation(patronID, bookID, patronPriority)
            reservationHeap.insert(reservation)

            # Insert patronID into the reservations list in sorted order
            inserted = False
            for i, res_patronID in enumerate(book_node.reservations):
                res_priority = next((res.priorityNumber for res in reservationHeap.heap if res.patronID == res_patronID), None)
                if res_priority is not None and patronPriority < res_priority:
                    book_node.reservations.insert(i, patronID)
                    inserted = True
                    break
            if not inserted:
                book_node.reservations.append(patronID)

            return f"Book {bookID} Reserved by Patron {patronID}\n"
        except Exception as e:
            return str(e)  # Returns "Waitlist is full" if the exception is raised




    def return_book(self, patronID, bookID, reservationHeap):
        book_node = self.search_book(bookID)
        if book_node is None or book_node == self.NIL:
            return "Book not found."

        if book_node.borrowedBy != patronID:
            return f"Book {bookID} is not borrowed by Patron {patronID}."

        # If there are reservations, check if the next reservation is for this book
        while reservationHeap.heap:
            next_reservation = reservationHeap.peek()  # Check the next reservation without removing it
            if next_reservation.bookID == bookID:
                # This reservation is for the current book, so proceed to allocate it
                reservationHeap.extract_min()  # Now remove the reservation from the heap
                if next_reservation.patronID in book_node.reservations:
                    book_node.reservations.remove(next_reservation.patronID)
                book_node.borrowedBy = next_reservation.patronID
                book_node.availabilityStatus = "No"
                return f"Book {bookID} returned by Patron {patronID}\nBook {bookID} Allotted to Patron {next_reservation.patronID}."
            else:
                # The next reservation is not for this book, so remove it and check the next one
                reservationHeap.extract_min()

        # If we reach here, there are no reservations for this book
        book_node.availabilityStatus = "Yes"
        book_node.borrowedBy = None
        return f"Book {bookID} returned by Patron {patronID}. Now available for borrowing."



    def delete_book(self, bookID):
        z = self.search_book(bookID)
        if z is None or z == self.NIL:
            return "Book not found or already deleted."

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            # Check for color change during transplant and increment if there's a change
            self.increment_color_flip_count(z.color, y.color)
            y.color = z.color

        if y_original_color == 0:
            self.fix_delete(x)

        # Notify patrons with a combined message
        patron_ids = ",".join(str(patronID) for patronID in z.reservations)
        cancellation_message = f"Reservation made by Patron {patron_ids} has been cancelled!" if z.reservations else ""
        return f"Book {bookID} is no longer available. {cancellation_message}"


    def search_book(self, bookID):
        node = self.root
        while node != self.NIL and node.bookID != bookID:
            if bookID < node.bookID:
                node = node.left
            else:
                node = node.right
        return node if node != self.NIL else None

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def print_book(self, bookID):
        node = self.search_book(bookID)
        if node is not None and node != self.NIL:
            # availability = "No" if node.borrowedBy is not None else "Yes"
            book_info = (
                f"BookID = {node.bookID}\n"
                f"Title = {node.bookName}\n"
                f"Author = {node.authorName}\n"
                f"Availability = \"{node.availabilityStatus}\"\n"
                f"BorrowedBy = {node.borrowedBy if node.borrowedBy is not None else 'None'}\n"
                f"Reservations= {node.reservations}"
            )
            return book_info
        else:
            return "BookID not found in the Library"
        
    def find_closest_book(self, targetID):
        closest = None
        min_diff = float('inf')
        ties = []
        
        # Start with the root of the tree
        node = self.root
        
        # Traverse the tree
        while node and node != self.NIL:
            if node.bookID == targetID:
                # If the book ID matches the target ID, it's the closest
                return [node]
            else:
                # Calculate the difference and update closest if necessary
                diff = abs(node.bookID - targetID)
                if diff == min_diff:
                    ties.append(node)  # Add to ties in case of a tie
                elif diff < min_diff:
                    closest = node
                    min_diff = diff
                    ties = [node]  # Reset ties since we found a closer book
                
                # Move to the left or right child based on comparison
                if targetID < node.bookID:
                    node = node.left
                else:
                    node = node.right
        
        # Return the closest book or books in case of a tie
        return ties

      
    

    def print_books_in_range(self, bookID1, bookID2):
        books_info = []
        self._print_books_in_range_helper(self.root, bookID1, bookID2, books_info)
        return '\n\n'.join(books_info)  # Join the book info strings with double newlines between them

    def _print_books_in_range_helper(self, node, bookID1, bookID2, books_info):
        if node is None or node == self.NIL:
            return
        # Ensure left subtree is checked only if it may contain books within the range
        if node.left is not None and node.bookID > bookID1:
            self._print_books_in_range_helper(node.left, bookID1, bookID2, books_info)
        # Add node's book info if within range
        if bookID1 <= node.bookID <= bookID2:
            book_info = (
                f"BookID = {node.bookID}\n"
                f"Title = {node.bookName}\n"
                f"Author = {node.authorName}\n"
                f"Availability = {node.availabilityStatus}\n"
                f"BorrowedBy = {node.borrowedBy if node.borrowedBy is not None else 'None'}\n"
                f"Reservations= {node.reservations}"
            )
            books_info.append(book_info)
        # Ensure right subtree is checked only if it may contain books within the range
        if node.right is not None and node.bookID < bookID2:
            self._print_books_in_range_helper(node.right, bookID1, bookID2, books_info)


    def increment_color_flip_count(self, old_color, new_color):
        if old_color != new_color:
            self.color_flip_count += 1