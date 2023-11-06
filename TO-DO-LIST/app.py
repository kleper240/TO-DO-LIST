# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Chemin vers la base de données SQLite
DATABASE = 'db.sqlite'

def create_database():
    # Crée la structure de la base de données si elle n'existe pas déjà
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            complete INTEGER,
            added_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    # Page d'accueil qui affiche la liste des tâches à faire
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo")
    todo_list = cursor.fetchall()
    conn.close()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # Ajoute une nouvelle tâche à la liste
    title = request.form.get("title")
    description = request.form.get("description")
    added_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (title, description, complete, added_at) VALUES (?, ?, ?, ?)", (title, description, 0, added_at))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>", methods=["GET"])
def update(todo_id):
    # Met à jour l'état de complétude d'une tâche
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT complete FROM todo WHERE id=?", (todo_id,))
    result = cursor.fetchone()
    complete = not result[0]

    cursor.execute("UPDATE todo SET complete=? WHERE id=?", (complete, todo_id))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["GET"])
def delete(todo_id):
    # Supprime une tâche de la liste
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
