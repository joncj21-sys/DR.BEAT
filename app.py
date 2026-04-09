from flask import Flask, render_template

app = Flask(__name__)

peliculas = [
    {
        "titulo": "Acción Extrema",
        "url": "https://www.youtube.com/watch?v=DFs7Vnautps",
        "categoria": "Acción"
    },
    {
        "titulo": "Comedia Divertida",
        "url": "https://www.w3schools.com/html/movie.mp4",
        "categoria": "Comedia"
    }
]

@app.route("/")
def inicio():
    return render_template("index.html", peliculas=peliculas)
