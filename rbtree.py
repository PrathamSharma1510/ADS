from collections import deque
from reservationheap import Reservation

# insert_book: This function will insert a new book into the tree, ensuring that book IDs are unique.
# delete_book: This function will delete a book from the tree and handle notifying patrons.
# search_book: This function will search for a book by its ID.
# print_book: This function will print the details of a book given its ID.
# print_books_in_range: This function will print all books within a given range of IDs.
# fix_insert: This will maintain the Red-Black Tree properties after an insertion.
# fix_delete: This will maintain the Red-Black Tree properties after a deletion.
# left_rotate and right_rotate: These functions will perform rotations during insertions and deletions to maintain the Red-Black Tree balance.
# increment_color_flip_count: This would be a new function to count color flips during fix-up operations.

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

    def fix_insert(self, k):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    # Color flip
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.increment_color_flip_count()
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    # Color flip
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.increment_color_flip_count()
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

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
                if s.color == 1:
                    # Color flip
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    self.increment_color_flip_count()
                    s = x.parent.right
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    # Color flip
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    self.increment_color_flip_count()
                    s = x.parent.left
                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        if x.color == 0:
            x.color = 1
            self.increment_color_flip_count()


    def borrow_book(self, patronID, bookID, patronPriority, reservationHeap):
        book_node = self.search_book(bookID)
        if book_node is None or book_node == self.NIL:
            return "Book not found."
        availability_status = book_node.availabilityStatus.strip('\"').lower()
        # If the book is available (not borrowed by anyone), lend it to the patron
        if availability_status == "yes" and book_node.borrowedBy==None:
            book_node.availabilityStatus = "No"# Update the availability status
            book_node.borrowedBy = patronID 
            print(f"After borrowing: BookID: {book_node.bookID}, Availability: {book_node.availabilityStatus}, BorrowedBy: {book_node.borrowedBy}")
            print("hey") # Update with the ID of the patron who borrowed the book
            return f"Book {bookID} Borrowed by Patron {patronID}"

        # If the book is already borrowed by the same patron, return a message
        if book_node.borrowedBy == patronID:
            return f"Patron {patronID} has already borrowed Book {bookID}."

        # If the book is borrowed by another patron, add the current patron to the waitlist
        # but first, check if the patron has already reserved the book
        if any(reservation.patronID == patronID for reservation in reservationHeap.heap):
            return f"Patron {patronID} has already reserved the book {bookID}."

        # If not already reserved, add the patron to the waitlist
        reservation = Reservation(patronID, patronPriority)
        reservation_result = reservationHeap.insert(reservation)
        if reservation_result == "Waitlist is full":
            return "Unable to reserve book; waitlist is full."
        return f"Book {bookID} is not available. Patron {patronID} added to the waitlist."






    def delete_book(self, bookID):
        z = self.search_book(bookID)
        if z is None or z == self.NIL:
            # Book not found, handle this case as needed
            return False

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
            y.color = z.color

        if y_original_color == 0:
            self.fix_delete(x)

        # Notify patrons here if necessary

        return True

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
                if diff < min_diff:
                    closest = node
                    min_diff = diff
                    ties = [node]  # Reset ties since we found a closer book
                elif diff == min_diff:
                    ties.append(node)  # Add to ties in case of a tie
                
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
                f"Title = \"{node.bookName}\"\n"
                f"Author = \"{node.authorName}\"\n"
                f"Availability = \"{('Yes' if node.availabilityStatus == 'Yes' else 'No')}\"\n"
                f"BorrowedBy = {node.borrowedBy if node.borrowedBy is not None else 'None'}\n"
                f"Reservations= {node.reservations}"
            )
            books_info.append(book_info)
        # Ensure right subtree is checked only if it may contain books within the range
        if node.right is not None and node.bookID < bookID2:
            self._print_books_in_range_helper(node.right, bookID1, bookID2, books_info)


    def increment_color_flip_count(self):
        self.color_flip_count += 1