# GatorLibrary Management System README

## Report Information
- **Name**: Pratham Sharma
- **UFID**: 99812068

## Introduction
The GatorLibrary Book Management System is engineered to maximize efficiency in library book and reservation management. It employs Red-Black Trees for book management and Binary Min-Heaps for reservation management, ensuring optimal performance in library operations.

## Design Overview
### Red-Black Tree for Book Management
- Manages books using a self-balancing binary search tree.
- Ensures O(log n) time complexity for insertions, deletions, and searches.
- Attributes for each book include BookID, BookName, AuthorName, AvailabilityStatus, and BorrowedBy.

### Binary Min-Heap for Reservation Management
- Manages reservations within each book's node, prioritizing based on the patron's priority and reservation time.

## Functionalities
- **Printing book information**: `PrintBook` and `PrintBooks`
- **Adding new books**: `InsertBook`
- **Borrowing and returning books**: `BorrowBook` and `ReturnBook`
- **Deleting books**: `DeleteBook`
- **Finding the closest book by BookID**: `FindClosestBook`
- **Tracking color flips in the Red-Black Tree**: `ColorFlipCount`

## Test Case Breakdown
- Includes scenarios for book insertions, borrowings, and deletions.
- Demonstrates the system's response to various operations like borrowing available books, adding reservations, and managing book returns.

## Code Structure
### Red-Black Tree Class
- Implements the Red-Black Tree with methods for insertion, rotation, deletion, and searching.
  
### Min-Heap Class: ReservationHeap
- Manages book reservations using a Binary Min-Heap, supporting insertion, extraction, and peek operations.

### Node Class
- Represents books in the Red-Black Tree, including attributes for book ID, name, author, availability, borrower, and reservations.

## Running the Program
To run the GatorLibrary Management System:
```shell
make run input_file=input.txt
# or
python3 main.py < input.txt
```
Replace `input.txt` with your file name. The output will be generated in `output_file.txt` in the same directory.

## Unique Features and Considerations
- Explains the difference in color flip count during deletion, highlighting the system's unique approach to deletions and rebalancing.
- Describes scenarios leading to rebalancing and color flips, underscoring the system's efficiency in maintaining tree balance and properties.

This README provides an overview of the GatorLibrary Management System's functionalities, design, and operational instructions, encapsulating the essence of the detailed report for quick reference and understanding.