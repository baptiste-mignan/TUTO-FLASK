from .app import db

class Author (db.Model):
    """
    Class décrivant la table Author
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

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
    
def get_sample():
    return Book.query.limit(10).all()

# import yaml, os.path
# 
# Books = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "data.yml")))
# 
# # Pour avoir un id
# i = 0
# for book in Books:
#     book['id'] = i
#     i += 1
# 
# def get_sample():
#     return Books[0:10]