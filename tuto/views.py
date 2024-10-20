from .app import app, db
from flask import render_template, url_for , redirect
from .models import get_sample, get_author, get_author_livre, add_author_bd, User ,add_favoris, get_books_favoris, supp_favoris, is_fav, Book, get_all_books, get_genres_book, get_books_genre, get_book_id, Genre, book_genre, get_genres, get_noms_genres, search_filter
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required
from flask import request

@app.route("/")
def home():
    def auteur(livre):
        return get_author(livre.author_id).name
    books = sorted(get_sample(20) , key=auteur)
    
    return render_template("home.html", title="My Books !", books=books)

@app.route("/detail/<id>")
def detail(id):
    books = get_all_books()
    book = books[int(id)-1]
    favoris = None
    genres=get_genres_book(book)
    if isinstance(current_user, User):
        favoris = is_fav(current_user, book)
    return render_template("detail.html", book=book, author_name=get_author(book.author_id).name, author_id=book.author_id, favoris=favoris, genres=genres)

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template("edit-author.html", author =a, form=f)

@app.route("/save/author/", methods =("POST" ,))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)  
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('one_author', id=a.id))
    a = get_author(int(f.id.data))
    return render_template("edit-author.html", author =a, form=f)

@app.route("/one_author/<id>")
def one_author(id):
    author = get_author(id)
    books = get_author_livre(id)
    return render_template("one_author.html", name_author=author.name, books=books, author_id = id)

@app.route("/add/author/")
def add_author():
    f = AuthorForm(id=None, name=None)
    return render_template("add-author.html", form=f)

@app.route("/save/add/author/", methods = ("POST", ))
def save_add_author():
    f = AuthorForm()
    if f.validate_on_submit():
        id = add_author_bd(f.name.data)
        return redirect(url_for('one_author', id = id))
    return render_template("add-author.html")

class LoginForm ( FlaskForm ):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods =("GET","POST" ,))
def login ():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template("login.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/detail/add/<book_id>", methods =("GET","POST" ,))
@login_required
def add_favoris_route(book_id):
    add_favoris(current_user.get_id(), book_id)
    return detail(book_id)

@app.route("/detail/sup/<book_id>", methods =("GET","POST" ,))
@login_required
def supp_favoris_route(book_id):
    supp_favoris(current_user.get_id(), book_id)
    return detail(book_id)

@app.route("/favoris")
@login_required
def favoris_view():
    user = current_user
    id_user = user.get_id()
    user_favoris = get_books_favoris(id_user)
    return render_template("favoris.html", books=user_favoris)





@app.route("/search", methods=('GET',))
def search():
    q = request.args.get("search")
    titre = request.args.get("titre")
    auteur = request.args.get("auteur")
    prix = request.args.get("prix")
    erreur = ''
    results = search_filter(q, titre, auteur, prix)
    if results == []:
        results = get_all_books()
        erreur = "Aucun livre ne correspond"    
    return render_template("search_results.html", results=results, title="My Books", erreur=erreur)

@app.route("/genre/<genre_name>")
def genre(genre_name):
    return render_template("home.html", title=genre_name, books=get_books_genre(genre_name))

class GenreForm(FlaskForm):
    id = HiddenField('id')
    genre = StringField('Genre', validators = [DataRequired()])

@app.route("/add/genre/<int:book_id>", methods=('GET', 'POST',))
def add_genre(book_id):
    return render_template("add_genre.html", book=get_book_id(book_id), form=GenreForm(id=book_id))

@app.route("/save/genre/", methods =("POST" ,))
def save_genre():
    book = None
    f = GenreForm()
    if f.validate_on_submit():
        book = get_book_id(int(f.id.data))
        if f.genre.data not in get_noms_genres():
            genre = Genre(nom_genre=f.genre.data)
            db.session.add(genre)
            db.session.commit()
        else:
            genre = db.session.query(Genre).filter(Genre.nom_genre==f.genre.data).all()[0]
        book.genres.append(genre)
        genre.books.append(book)
        db.session.add(genre)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('detail', id=book.id))
    book = get_book_id(int(f.id.data))
    return render_template("add_genre.html", book=book, form=f)
