from .app import db

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
    
def get_sample():
    return Book.query.limit(20).all()

def get_author(id):
    return Author.query.filter(Author.id == id)[0]

def get_author_livre(id):
    return Book.query.filter(Book.author_id == id)
