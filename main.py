import sys
import re
from rbtree import RedBlackTree
from reservationheap import ReservationHeap

def main(file_name):
    rbt = RedBlackTree()
    rh = ReservationHeap()  # Instance of ReservationHeap to manage reservations
    new_filename = file_name[:-4]
    with open(file_name, 'r') as f, open(new_filename+'_output_file.txt', 'w') as o:
        for line in f:
            args = re.findall(r'\((.*?)\)', line)

            if "InsertBook" in line:
                try:
                    # Split the arguments and unpack the first four
                    split_args = [arg.strip() for arg in args[0].split(',')]
                    bookID, bookName, authorName, availabilityStatus = split_args[:4]
                    
                    # Remove double quotes from availabilityStatus
                    availabilityStatus = availabilityStatus.strip('"')

                    # Check if borrowedBy is provided, else set it to None
                    borrowedBy = split_args[4] if len(split_args) > 4 else None
                    success = rbt.insert_book(int(bookID), bookName, authorName, availabilityStatus, borrowedBy)
                    # o.write(f'InsertBook: {"Success" if success else "Failed"}\n')
                except ValueError as e:
                    o.write(f'InsertBook: Failed - {str(e)}\n')
                    continue


            elif re.match(r"PrintBooks\((.+)\)", line):
                try:
                    # print(f"Debug - args[0]: {args[0]}")  
                    # Extract the book IDs from the argument string, split them, and convert to integers
                    bookID1, bookID2 = (int(x.strip()) for x in args[0].split(','))
                    # Call the function to get books info in the range
                    books_info = rbt.print_books_in_range(bookID1, bookID2)
                    # Write the formatted books info to the output
                    o.write(f'{books_info}\n\n')
                except ValueError as e:
                    # If there's an error, such as not being able to convert to int, write an error message
                    o.write('Error in processing PrintBooks command: ' + str(e) + '\n')
     
            elif re.match(r"PrintBook\((.+)\)", line):
                try:
                    bookID = int(args[0])
                    book_info = rbt.print_book(bookID)
                    o.write(f'{book_info}\n\n')
                except ValueError as e:
                    o.write(f'Error processing PrintBook command: {str(e)}\n')


            elif "BorrowBook" in line:
                patronID, bookID, patronPriority = map(int, args[0].split(','))
                result = rbt.borrow_book(patronID, bookID, patronPriority, rh)
                o.write(f'{result}\n')

            elif "ReturnBook" in line:
                patronID, bookID = map(int, args[0].split(','))
                result = rbt.return_book(patronID, bookID, rh)
                o.write(f'{result}\n')

                
            elif "DeleteBook" in line:
                bookID = int(args[0])
                result = rbt.delete_book(bookID)
                o.write(f'{result}\n\n')

            elif "FindClosestBook" in line:
                targetID = int(args[0])
                closest_books = rbt.find_closest_book(targetID)
                closest_books.reverse()
                if closest_books:
                    for book in closest_books:
                        # book_info = f"BookID: {book.bookID}, BookName: {book.bookName}, AuthorName: {book.authorName}, " \
                        #             f"AvailabilityStatus: {book.availabilityStatus}, BorrowedBy: {book.borrowedBy}"
                        book_info = (
                                        f"BookID = {book.bookID}\n"
                                        f"Title = {book.bookName}\n"
                                        f"Author = {book.authorName}\n"
                                        f"Availability = \"{book.availabilityStatus}\"\n"
                                        f"BorrowedBy = {book.borrowedBy if book.borrowedBy is not None else 'None'}\n"
                                        f"Reservations= {book.reservations}\n"
                                    )
                        o.write(f'{book_info}\n')
                else:
                    o.write('FindClosestBook: No closest book found.\n')


            elif "ColorFlipCount" in line:
                count = rbt.color_flip_count  # Access the attribute directly, without parentheses
                o.write(f'ColorFlipCount: {count}\n')

            elif "Quit" in line:
                o.write('Quit: Terminating the program.\n')
                break

            else:
                o.write('Unrecognized command.\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
    else:
        input_file = sys.argv[1]
        main(input_file)
