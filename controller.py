from manage import User, db, Book, UserBook, app
from flask import Flask, request, jsonify, redirect, url_for
import json


# USER class methods
@app.route("/signup",methods=['GET','POST'])
def user_signup():
    input_data = request.get_json()

    first_name = input_data.get('first_name')
    last_name = input_data.get('last_name')
    admin = User(
        user_name = first_name + " " + last_name,
        email=input_data.get('email'),
        password=input_data.get('password'),
        role=input_data.get('role'),
        initial_balance = input_data.get('initial_balance')
    )
    admin.add()

    return "Signed Up"

@app.route("/listusers")
def list_users():
    users = User.query.all()
    user_list = []

    for user in users:
        print(user.id,user.user_name,user.email,user.role)
        dic_user = {
            "User_id" : user.id,
            "User_name" : user.user_name,
            "Email" : user.email
        }
        user_list.append(dic_user)    
    return jsonify(user_list)   


# BOOK Class Methods
@app.route("/addbook",methods=['GET'])
def add_book():
    input_data = request.get_json()

    author_first_name=input_data.get('author_first_name')
    author_last_name=input_data.get('author_last_name')
    
    entry = Book(
        title = input_data.get('title'),
        author_name = author_first_name + " " + author_last_name,
        price = input_data.get('price'),
        pages = input_data.get('pages')
    )
    entry.add()
    
    return "Book is Added!"


@app.route('/listbooks')
def list_books():
    books = Book.query.all()
    print(books)
    book_list = []

    for book in books:
        print(book.title,book.author_name,book.price,book.pages)

        dic_book = {
            "Title" : book.title,
            "Author" : book.author_name,
            "Price" : book.price,
            "Pages" : book.pages
        }
        book_list.append(dic_book)

    return jsonify(book_list)


# USERBOOK class method
@app.route("/purchasebook",methods=['GET','POST'])
def purchase_book():
    input_data = request.json
    
    existing_user = User.query.get(input_data['user_id'])
    existing_book = Book.query.get(input_data['book_id'])
    print(existing_book.id, existing_book.price, existing_book.title)
    
    if not existing_user:
        print("User signup is needed to buy a book")
        return "User signup is needed to buy a book"

    if not existing_book:
        print("Book is not available")
        return "Book is not available"

    already_existing = UserBook.query.filter_by(user_id=input_data['user_id'],book_id=input_data['book_id']).first()
    
    if already_existing:
        print("You already bought this book")
        return "You already bought this book"

    print(existing_user.initial_balance)
    if existing_book.price > existing_user.initial_balance:
        return "You've insufficient balance to buy a book"

    update_user_balance = existing_user.initial_balance - existing_book.price
    print("User wallet", update_user_balance)

    user_wallet = User.query.filter_by(initial_balance=existing_user.initial_balance).first()
    user_wallet.initial_balance = update_user_balance

    get_author = User.query.filter_by(user_name=existing_book.author_name).first()
    
    author_wallet = User.query.filter_by(initial_balance=get_author.initial_balance).first()

    update_author_balance = author_wallet.initial_balance + existing_book.price
    print("Author wallet", update_author_balance)

    author_wallet.initial_balance = update_author_balance

    user_book = UserBook(user_id=input_data['user_id'],book_id=input_data['book_id'])
    user_book.add()
    return "Book is added."
    

@app.route("/allpurchasebooks")
def list_purchase_books():
    print("\tALL SELLED BOOKS")
    bro_books = UserBook.query.all()
    li_purchase = []

    for row in bro_books:
        user_det = User.query.filter_by(id=row.user_id).first()
        book_det = Book.query.filter_by(id=row.book_id).first()

        dic_purchase = {
            "user_id" : row.user_id,
            "user_name" : user_det.user_name,
            "email" : user_det.email,
            "book_id" : row.book_id,
            "title" : book_det.title,
            "author_name" : book_det.author_name,
            "price" : book_det.price,
            "pages" : book_det.pages
        }
        li_purchase.append(dic_purchase)

    return json.dumps(li_purchase)


app.run(host='0.0.0.0',port=6000,debug=True)
