from flask import Flask, render_template

app = Flask(__name__)

# Lista de películas (puedes cambiar los links)
peliculas = [
    {
        "titulo": "Acción Extrema",
        "url": "https://www.youtube.com/watch?v=DFs7Vnautps&list=RDGMEM0s70dY0AfCwh3LqQ-Bv1xg&index=18"
    },
    {
        "titulo": "Comedia Divertida",
        "url": "https://www.w3schools.com/html/movie.mp4"
    }
    ,
    {
        "titulo":"extrem",
        "url": "/static/videos/0408(1).mp4"
    }


]

@app.route("/")
def inicio():
    return render_template("index.html", peliculas=peliculas)

if __name__ == "__main__":
    app.run(debug=True)


