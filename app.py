from flask import Flask, render_template

app = Flask(__name__)

peliculas = [
    {
        "titulo": "Acción Extrema",
        "url": "https://www.youtube.com/watch?v=DFs7Vnautps"
    },
    {
        "titulo": "Comedia Divertida",
        "url": "https://www.w3schools.com/html/movie.mp4"
    },
    {
        "titulo": "Extrem",
        "url": "/static/videos/0408(1).mp4"
    }
]

@app.route("/")
def inicio():
    return render_template("index.html", peliculas=peliculas)

# IMPORTANTE PARA RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

