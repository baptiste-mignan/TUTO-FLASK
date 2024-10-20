from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import Mapped

user_favoris = db.Table('user_favoris',
    db.Column('user_id', db.String(50), db.ForeignKey('user.username'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key = True)
)


class Author(db.Model):
    """
    Class décrivant la table Author
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __repr__ (self ):
        return "<Author (%d) %s>" % (self.id , self.name)


class Book(db.Model):
    """
    Class décrivant la table Book
    """
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(200))
    img = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref = db.backref("books", lazy="dynamic"))
    def __repr__ (self ):
        return "<Book (%d) %s>" % (self.id , self.title)
    
def get_sample(nb=400):
    return Book.query.limit(nb).all()

def get_all_books():
    return Book.query.all()

def get_author(id):
    return Author.query.filter(Author.id == id)[0]

def get_author_livre(id):
    return Book.query.filter(Book.author_id == id)

def add_author_bd(nom_author):
    if len(list(Author.query.filter(Author.name == nom_author))) == 0:
        author = Author(name=nom_author)
        db.session.add(author)
        db.session.commit()
        return author.id

class User(db.Model , UserMixin):
    username = db.Column(db.String(50), primary_key =True)
    password = db.Column(db.String(64))
    books : Mapped[list["Book"]]= db.relationship(secondary=user_favoris)
    def get_id(self):
        return self.username
    

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)




def add_favoris(user_id, book_id):
    (u, ) = User.query.filter(User.username == user_id)
    (b, ) = Book.query.filter(Book.id == book_id)
    u.books.append(b)
    db.session.commit()

def supp_favoris(user_id, book_id):
    (user, ) = User.query.filter(User.username == user_id)
    (book, ) = Book.query.filter(Book.id == book_id)
    if is_fav(user, book):
        user.books.remove(book)
        db.session.commit()

def get_books_favoris(user_id):
    liste_books = []
    favoris = db.session.query(user_favoris).filter(user_favoris.c.user_id==user_id ).all()
    
    for fav in favoris:
        book = Book.query.get(fav.book_id)  # Récupérer le livre par son ID
        if book:
            liste_books.append(book)
    return liste_books


def is_fav(user, book):
    return len(db.session.query(user_favoris).filter((user_favoris.c.user_id==user.username) & (user_favoris.c.book_id == book.id)).all()) == 1



def search_filter(q, titre, auteur):
    results = get_all_books()
    results2 = []
    if titre:
        for book in results:
            if q in book.title:
                results2.append(book)
    if auteur:
        for book in results:
            if q in book.author.name:
                results2.append(book)
    results = results2    
    return results