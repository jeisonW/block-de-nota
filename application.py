from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
db = SQL("sqlite:///block.db")

db.execute('''create table if not EXISTS users (id INTEGER, name TEXT NOT NULL,
                password TEXT NOT NULL, PRIMARY KEY(id));''')

db.execute('''CREATE TABLE if not EXISTS block (id_notas INTEGER PRIMARY KEY NOT NULL,
           id_persona INTEGER, nota VARCHAR(20) NOT NULL, FOREIGN KEY(id_persona) REFERENCES users(id))''')

@app.route("/")
def index():
    if not session.get("id"):
        return redirect("/login")
    notas = db.execute("select * from block where id_persona = ?" ,session["id"])
    return render_template("index.html" , notas = notas)


@app.route("/add" , methods = ["POST"])
def addnota():
    if request.method == "POST":
        nota = request.form.get("nota")
        db.execute("INSERT INTO block(id_persona, nota) VALUES(?,?)",session["id"], nota)
        return redirect("/")

@app.route("/delete" , methods=["POST"])
def delete():
    id = request.form.get("id")
    db.execute("delete from block where id_notas = ? " , id)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login" , methods= ["GET" , "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("name"):
            return "error "

        elif not request.form.get("password"):
            return "error "

        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("name"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return "error contraseña"

        session["id"] = rows[0]["id"]

        return redirect("/")
    return render_template("login.html")


@app.route("/registro" , methods= ["GET" , "POST"])
def registro():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        db.execute("insert into users (name , password) values (?,?)" , name , generate_password_hash(password))
        return redirect("login")
    return render_template("register.html")