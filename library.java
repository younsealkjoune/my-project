import java.util.Scanner;

class Book {
    private String title;
    private String author;
    private int year;

    
    public Book(String title, String author, int year) {
        this.title = title;
        this.author = author;
        this.year = year;
    }

   
    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public int getYear() {
        return year;
    }

   
    @Override
    public String toString() {
        return "Title: " + title + "\nAuthor: " + author + "\nYear: " + year + "\n";
    }
}

class BookStore {
    private Book[] books;
    private int bookCount;

    
    public BookStore() {
        books = new Book[100]; 
        bookCount = 0;
    }

  
    public void addBook(Book book) {
        if (bookCount < 100) { 
            books[bookCount] = book;
            bookCount++;
            System.out.println("Book added successfully!");
        } else {
            System.out.println("Cannot add the book. The store is full.");
        }
    }

   
    public void searchBook(String title) {
        boolean found = false;
        for (int i = 0; i < bookCount; i++) {
            Book book = books[i];
            if (book.getTitle().equalsIgnoreCase(title)) {
                System.out.println("Book found!");
                System.out.println(book);
                found = true;
                break; 
            }
        }
        if (!found) {
            System.out.println("Book not found.");
        }
    }

    
    public void removeBook(String title) {
        boolean removed = false;
        for (int i = 0; i < bookCount; i++) {
            Book book = books[i];
            if (book.getTitle().equalsIgnoreCase(title)) {
                
                for (int j = i; j < bookCount - 1; j++) {
                    books[j] = books[j + 1];
                }
                bookCount--;
                removed = true;
                System.out.println("Book removed successfully!");
                break; 
            }
        }
        if (!removed) {
            System.out.println("Book not found.");
        }
    }

    
    public void displayBooks() {
        if (bookCount == 0) {
            System.out.println("No books in the store.");
        } else {
            System.out.println("Books in the store:");
            for (int i = 0; i < bookCount; i++) {
                Book book = books[i];
                System.out.println(book);
                System.out.println("--------------------");
            }
        }
    }
}

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        BookStore bookStore = new BookStore();

        System.out.println("Welcome to the Modern Book Store!");

        while (true) {
            System.out.println("1. Add a book");
            System.out.println("2. Search for a book");
            System.out.println("3. Remove a book");
            System.out.println("4. Display all books");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    scanner.nextLine(); 
                    System.out.print("Enter the book title: ");
                    String title = scanner.nextLine();
                    System.out.print("Enter the book author: ");
                    String author = scanner.nextLine();
                    System.out.print("Enter the publication year: ");
                    int year = scanner.nextInt();

                    Book book = new Book(title, author, year);
                    bookStore.addBook(book);
                    break;
                case 2:
                    scanner.nextLine(); 
                    System.out.print("Enter the book title to search: ");
                    String searchTitle = scanner.nextLine();
                    bookStore.searchBook(searchTitle);
                    break;
                case 3:
                    scanner.nextLine(); 
                    System.out.print("Enter the book title to remove: ");
                    String removeTitle = scanner.nextLine();
                    bookStore.removeBook(removeTitle);
                    break;
                case 4:
                    bookStore.displayBooks();
                    break;
                case 5:
                    System.out.println("Thank you for using the Younes's Book Store...");
                    scanner.close();
                    System.exit(0);
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }
}
