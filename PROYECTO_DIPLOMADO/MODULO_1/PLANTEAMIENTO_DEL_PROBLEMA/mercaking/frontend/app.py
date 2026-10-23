from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"
API_BASE = "http://localhost:8000"


@app.route("/")
def index():
    return render_template("index.html", brand="MercaKing")


@app.route("/login")
def login():
    return render_template("login.html", brand="MercaKing")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", brand="MercaKing", api=API_BASE)


@app.route("/productos")
def productos():
    return render_template("productos.html", brand="MercaKing", api=API_BASE)


@app.route("/inventario")
def inventario():
    return render_template("inventario.html", brand="MercaKing", api=API_BASE)


@app.route("/ventas")
def ventas():
    return render_template("ventas.html", brand="MercaKing", api=API_BASE)


@app.route("/reportes")
def reportes():
    return render_template("reportes.html", brand="MercaKing", api=API_BASE)


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", brand="MercaKing", api=API_BASE)


@app.route("/minimercados")
def minimercados():
    return render_template("minimercados.html", brand="MercaKing", api=API_BASE)


@app.route("/asistente-ia")
def asistente_ia():
    return render_template("asistente_ia.html", brand="MercaKing", api=API_BASE)


@app.route("/superadmin")
def superadmin():
    return render_template("superadmin.html", brand="MercaKing", api=API_BASE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
