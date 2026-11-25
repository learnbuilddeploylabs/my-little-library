"""
My Little Library
Author: Rob Merrill / legolicious / Learn.Build.Deploy / slash / /
Version: 1.0.0

A simple command-line library builder to keep track of your books!
"""

###########
# IMPORTS #
###########

import sqlite3

#################
# CONFIGURATION #
#################

# Database file location
DB_FILE = "library.db"

###########
# CLASSES #
###########

class Book:
    """Represents a book in the library"""

    # Initialize a book instance (determines what each book is made of)
    def __init__(self, title, author_first_name, author_last_name, isbn, page_count):
        self.title = title
        self.author_first_name = author_first_name
        self.author_last_name = author_last_name
        self.isbn = isbn
        self.page_count = page_count
   
#############
# FUNCTIONS #
#############

def create_book():
    """Create a new book using book class"""

    print("Enter book details...\n")

    # Prompt user for the book's details
    title = input("Title: ")
    author_first_name = input("Author (First Name): ")
    author_last_name = input("Author (Last Name): ")
    isbn = input("ISBN: ")
    page_count = input("Page Count: ")

    # Variable passes user input to Book class
    book = Book(title, author_first_name, author_last_name, isbn, page_count)
    
    print("\nBook added to your library!")

    # Book object returned for use
    return book

def edit_book(conn, book_id):
    """Edit an existing book"""
    
    while True:
        print()
        editing_menu = "Editing Menu\n"
        print(f'{editing_menu}{'-' * len(editing_menu)}\n')

        print(
                f'{"1":>2} |  Title\n'
                f'{"2":>2} |  Author (First Name)\n'
                f'{"3":>2} |  Author (Last Name)\n'
                f'{"4":>2} |  ISBN\n'
                f'{"5":>2} |  Page Count\n'
                f'{"6":>2} |  Back to main menu...\n'
            )

        select_detail = (input("Which detail would you like to edit?\n"))

        if select_detail == "1":
            column = "title"
            new_value = input("Title: ")
        elif select_detail == "2":
            column = "author_first_name"
            new_value = input("Author (First Name): ")
        elif select_detail == "3":
            column = "author_last_name"
            new_value = input("Author (Last Name): ")
        elif select_detail == "4":
            column = "isbn"
            new_value = input("ISBN: ")
        elif select_detail == "5":
            column = "page_count"
            new_value = input("Page Count: ")
        elif select_detail == "6":
            return
        else:
            print("Invalid choice. Enter 1-5.")
            continue

        update_book(conn, book_id, column, new_value)

def generate_table_header():
    """Return a formatted table header containing book detail categories"""
    header = (
        f'{"ID":<5} | {"Title":<25} | {"Author (Last Name, First Name)":<31} | '
        f'{"ISBN":<15} | {"Pages":<6} |'
    )

    return f"\n{header}\n{'-' * len(header)}"

def generate_table_row(book):
    """Return a formatted table row containing a book's details"""
    
    if book:
        row = (
            f'{book[0]:<5} | {book[1]:<25} | {book[3]:<10} {book[2]:<20} | '
            f'{book[4]:<15} | {book[5]:<6} |'
        )
        return f"\n{row}\n{'-' * len(row)}"
    else:
        return "Book not found."
        
def generate_table(all_books):
    """Return a formatted table with details for all books in the library"""
    
    all_books_list = []

    header = generate_table_header()

    if all_books:
        for book in all_books:
            all_books_list.append(generate_table_row(book))
    else:
        print()
        return "No books found."


    return f"{header}\n{''.join(all_books_list)}"

def confirm_action():
    """Asks user to confirm an action"""
    
    confirm_delete = input("\nAre you sure? (y/n): ").lower()
    
    if confirm_delete == "y":
        return True
    else:
        return False

def main(connection):
    """Main program loop"""
    # pass

    # Allow user to remain in program
    while True:
        main_menu = "\nMain Menu\n"
        print(f'{main_menu}{'-' * len(main_menu)}\n')

        print(
            f'{"1":>2} |  View library\n'
            f'{"2":>2} |  Add a book\n'
            f'{"3":>2} |  Edit a book\n'
            f'{"4":>2} |  Remove a book\n'
            f'{"5":>2} |  Exit\n'
        )

        # Prompt user for selection
        menu_prompt = input("What would you like to do?\nEnter #: ")

        # Displays the library
        if menu_prompt == "1":
            print()
            print(generate_table(get_all_books(connection)))
            print("\n")
        
        # Allow user to add a book
        elif menu_prompt == "2":
            print()
            book = create_book()
            add_book(connection, book)
            print("\n")
        elif menu_prompt == "3":
            book_id = int(input("\nEnter Book ID: "))
            book = get_book(connection, book_id)

            print(generate_table([book]))

            if book and confirm_action():
                edit_book(connection, book_id)
                print("\n")
        elif menu_prompt == "4":
                book_id = int(input("\nEnter Book ID: "))
                book = get_book(connection, book_id)
                
                print(generate_table([book]))
                
                if book and confirm_action():
                    delete_book(connection, book_id)
                    print("\n")
        elif menu_prompt == "5":
                return
        else:
            print()
            print(f"Invalid selection. Please enter 1-5\n")
            

######################
# DATABASE FUNCTIONS #
######################

def init_db(conn):
    """Create the library database if needed"""

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author_first_name TEXT,
            author_last_name TEXT,
            isbn TEXT,
            page_count INTEGER
        )
    """)
    conn.commit()

def add_book(conn, book):
    """Add a book to the library"""

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO library (
            title,
            author_first_name,
            author_last_name,
            isbn,
            page_count
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        book.title,
        book.author_first_name,
        book.author_last_name,
        book.isbn,
        book.page_count
    ))
    conn.commit()

def update_book(conn, book_id, column, new_value):
    """Update a book's details"""

    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE library
        SET {column} = ?
        WHERE id = ?
    """, (new_value, book_id))
    conn.commit()

    print("\nBook detail updated!")

def delete_book(conn, book_id):
    """Delete a book from the library"""

    cursor = conn.cursor()
    cursor.execute("""
        DELETE
        FROM library
        WHERE id = ?
    """, (book_id,))
    conn.commit()

    print("\nBook deleted from library.")

def get_book(conn, book_id):
    """Return database record of a book"""

    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM library
        WHERE id = ?
    """, (book_id,))

    book = cursor.fetchone()
    return book

def get_all_books(conn):
    """Return database records of all books"""

    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM library
    """)

    all_books = cursor.fetchall()
    return all_books
    
##################
# MAIN EXECUTION #
##################

if __name__ == "__main__":
    connection = sqlite3.connect(DB_FILE)

    try:
        init_db(connection)

        # Replace th is with whatever you want to call your librar... or don't!
        print()
        print("MY LITTLE LIBRARY v1.2.0")

        main(connection)
    finally:
        connection.close()
