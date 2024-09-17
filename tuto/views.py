import yaml.loader
from .app import app
from flask import render_template
import yaml , os.path

@app.route("/")
def home():
    return render_template("home.html", title= "Hello World!",
                           names = ["Pierre", "Paul", "Corinne"],)

 # @app.route("/livres")
 # def livres():
 #     return render_template("livres.html", title= "Mes livres",
 #                            names = ["Pierre", "Paul", "Corinne"],
 #                            livres = yaml.loader(open(os.path.join(os.path.dirname(__file__), "data.yml"))))