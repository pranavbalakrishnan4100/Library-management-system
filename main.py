import mysql.connector as mysql

host="localhost"
user="root"
password="4100"


#Connecting to MySQL
try:
    library=mysql.connect(host=host,user=user,password=password,database="library")
    command_handler=library.cursor()
    print("Connected succesfully")
except Exception as e:
    print(e)

def validMemId(mem_id):
    command_handler=library.cursor()
    command_handler.execute("SELECT * FROM members WHERE mem_id=%s",(mem_id,))
    record=command_handler.fetchone()
    if(record==None):
        return False
    else:
        return True

def welcome():
    print("")
    print("Welcome to Library Management System.")
    
    print("1.Issue a book.")
    print("2.Return a book.")
    print("3.Add a new member.")
    print("4.Cancel membership.")
    print("5.Add book.")
    print("6.Remove book.")
    print("7.Search for a book.")
    choice=int(input("What would you like to do?"))

    if(choice==1):
        issueBook()
    elif(choice==2):
        returnBook()
    elif(choice==3):
        addMember()
    elif(choice==4):
        removeMember()
    elif(choice==5):
        addBooks()
    elif (choice==6):
        removeBooks()
    elif(choice==7):
        searchBooks()
    else:
        print("Invalid choice")
        welcome()


def addMember():
    #add a new record to the members table
    command_handler=library.cursor()
    ph=input("Enter phone number:")
    name=input("Enter name:")

    try:
        query_attr=(name,ph)
        command_handler.execute("INSERT INTO members (name, phone) VALUES (%s, %s);",query_attr)
        library.commit()
        print("User added succesfully.")
        command_handler=library.cursor()
        query_attr=(ph,)
        command_handler.execute("SELECT mem_id FROM members WHERE phone=%s;",query_attr)
        record=command_handler.fetchone()
        print("Your membership id is:",record[0])
    except Exception as e:
        print(e)
        print("Error:Unable to add user.")
    welcome()

def removeMember():
    #remove existing record from User table
    command_handler=library.cursor()
    mem_id=input("Enter membership id to be removed:")
    
    try:
        command_handler.execute("SELECT book_issued FROM members WHERE mem_id=%s;",(mem_id,))
        record=command_handler.fetchone()
        if(record==(None,)):
            command_handler=library.cursor()
            command_handler.execute("DELETE FROM members WHERE mem_id=%s;",(mem_id,))
            library.commit()
            print("Deleted succesfully.")
        else:
            print("Member hasnt return book:",record);
    except Exception as e:
        print(e)
        print("Error:Unable to delete.")
    welcome()


def addBooks():
    #add a new record to books table
    command_handler=library.cursor()
    
    title=input("Enter title of the book:")
    isbn=input("Enter ISBN:")
    author=input("Enter author(s) name:")
    publisher=input("Enter publishers name:")
    category=input("Enter category:")
    status="available"
    
    try:
        query_attr=(isbn,title,author,publisher,category,status)
        command_handler.execute("INSERT INTO books (isbn, title, author, publisher, category, status) VALUES (%s, %s, %s, %s, %s, %s);",query_attr)
        library.commit()
        print("Inserted succesfully.")
        command_handler=library.cursor()
        command_handler.execute("SELECT MAX(book_id) FROM books;")
        record=command_handler.fetchone()
        print("BOOK ID IS :",record[0])
        choice=input("Would you like to add another book? [Y/N]:")
        if(choice=='Y'):
            addBooks()
    except Exception as e:
        print(e)
        print("Error:Unable to add new book.")
    welcome()
    

def removeBooks():
    #remove an existing record from books table
    command_handler=library.cursor()
    
    try:
        book_id=input("Enter book id of the book to be deleted:")
        command_handler.execute("DELETE FROM books WHERE book_id=%s;",(book_id,))
        print("Deleted succesfully.")
        library.commit()
        choice=input("Would you like to delete another book? [Y/N]:")
        if(choice=='Y'):
            removeBooks()
    except Exception as e:
        print(e)
        print("Error:Unable to delete.")
    welcome()
  
def issueBook():
    #change book status attribute to issued in books table
    command_handler=library.cursor()
    mem_id=input("Enter membership id:")
    if(validMemId(mem_id)==True):
        book_id=input("Enter book_id of the book to be issued:")

        command_handler.execute("SELECT status FROM books WHERE book_id=%s;",(book_id,))
        record=command_handler.fetchone()
        if(record!=('available',)):
            print("Book not available.")
        else:
            try:
                command_handler=library.cursor()
                command_handler.execute("UPDATE books SET status = %s,issued_to=%s WHERE book_id=%s;",("unavailable",mem_id,book_id));
                library.commit()
                command_handler=library.cursor()
                command_handler.execute("UPDATE members SET book_issued= %s WHERE mem_id=%s;",(book_id,mem_id))
                library.commit()
                print("Book issued.")
            except Exception as e:
                print(e)
    else:
        print("Invalid membership id.")
    welcome()
    
    
def returnBook():
    #change book status attribute to received in books table
    command_handler=library.cursor()
    mem_id=input("Enter membership id:")
    if(validMemId(mem_id)==True):
        book_id=input("Enter book_id of the book to be returned:")
        command_handler.execute("SELECT issued_to FROM books WHERE book_id=%s;",(book_id,))
        record=command_handler.fetchone()
        if(record==(int(mem_id),)):
            try:
                command_handler=library.cursor()
                command_handler.execute("UPDATE books SET status = %s,issued_to=%s WHERE book_id=%s;",("available",None,book_id));
                library.commit()
                command_handler.execute("UPDATE members SET book_issued= %s WHERE mem_id=%s;",(None,mem_id))
                library.commit()
                print("Book returned.")
            except Exception as e:
                print(e)
        else:
            print("Cannot return book.")
    else:
        print("Invalid membership id.")
    welcome()


def searchBooks():
    #Search books database based on various parameters
    isbn=input("Enter isbn:")
    title=input("Enter title:")
    author=input("Enter author:")
    publisher=input("Enter publisher:")
    category=input("Enter category:")

    try:
        command_handler=library.cursor()
        command_handler.execute("SELECT * FROM books WHERE isbn LIKE %s AND title LIKE %s AND author LIKE %s AND publisher LIKE %s AND category LIKE %s",('%'+isbn+'%', '%'+title+'%', '%'+author+'%', '%'+publisher+'%', '%'+category+'%' ))
        records=command_handler.fetchall()
        if(len(records)==0):
            print("No books found,Try again.")
        else:
            for record in records:
                print(record)
                print("")
    except Exception as e:
        print(e)
    welcome()
                            
                                                
###MAIN###

welcome()
