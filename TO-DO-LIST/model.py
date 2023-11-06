# model.py
import sqlite3
import datetime

# class Tache:
#     def __init__(self, tache, description, heure):
#         self.tache = tache
#         self.description = description
#         self.heure = heure
    
#     def get_tache(self):
#         return self.tache
    
#     def get_description(self):
#         return self.description
    
#     def get_heure(self):
#         return self.heure


DATABASE = 'db.sqlite'

def create_todo(title, description):
    # Crée une nouvelle tâche avec le titre, la description et l'heure spécifiés
    added_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (title, description, complete, added_at) VALUES (?, ?, ?, ?)", (title, description, 0, added_at))
    conn.commit()
    conn.close()

def get_todo_list():
    # Récupère la liste complète des tâches
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo")
    todo_list = cursor.fetchall()
    conn.close()
    return todo_list

def update_todo_complete(todo_id, complete):
    # Met à jour l'état de complétude d'une tâche spécifiée par son ID
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE todo SET complete=? WHERE id=?", (complete, todo_id))
    conn.commit()
    conn.close()

def delete_todo(todo_id):
    # Supprime une tâche spécifiée par son ID
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
