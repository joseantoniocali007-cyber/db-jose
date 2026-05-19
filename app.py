import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATABASE_URL = os.getenv("postgresql://db_render_jose_user:b93nb6HSzEHA0FtdSYwECYPtKJ5zvUT1@dpg-d823lodckfvc73evclm0-a.oregon-postgres.render.com/db_render_jose")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, nombre, email FROM usuarios ORDER BY id;')
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route('/add', methods=['POST'])
def add_user():
    nombre = request.form['nombre']
    email = request.form['email']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO usuarios (nombre, email) VALUES (%s, %s)',
        (nombre, email)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
