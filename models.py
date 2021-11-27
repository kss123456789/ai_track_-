from sqlalchemy.orm import backref
from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(30), primary_key=True, nullable=False)
    pw = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(30), nullable=False)

    user_review = db.relationship("Review", backref='user')
    user_record = db.relationship("Record", backref='user')

class BookList(db.Model):
    __tablename__ = 'booklist'
    book_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_name = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.String(10), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.Text(), nullable=False)
    stock = db.Column(db.Integer, default=2, nullable=False)
    avg_rating = db.Column(db.Integer, default=0, nullable=False)

    book_review = db.relationship("Review", backref='booklist')
    book_record = db.relationship("Record", backref='booklist')
    
class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('booklist.book_id'), nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('user.id'), nullable=False)
    review = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(21), nullable=False)

class Record(db.Model):
    __tablename__ = 'record'
    record_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.String(30), db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('booklist.book_id'), nullable=False)
    first_date = db.Column(db.String(19), nullable=False)
    last_date = db.Column(db.String(19), nullable=True)