from flask import Flask, render_template, request, redirect
import psycopg2
from config import DB_CONFIG
from datetime import date

app = Flask(__name__)
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Dummy user (for now)
USER_ID = 1

@app.route('/')
def index():
    cur.execute("SELECT id, name FROM habits WHERE user_id = %s", (USER_ID,))
    habits = cur.fetchall()
    return render_template('index.html', habits=habits)

@app.route('/log/<int:habit_id>')
def log_habit(habit_id):
    cur.execute("INSERT INTO habit_logs (habit_id) VALUES (%s)", (habit_id,))
    cur.execute("UPDATE users SET xp = xp + 10 WHERE id = %s", (USER_ID,))
    
    # Level up logic
    cur.execute("SELECT xp, level FROM users WHERE id = %s", (USER_ID,))
    xp, level = cur.fetchone()
    required = level * 100
    if xp >= required:
        cur.execute("UPDATE users SET level = level + 1 WHERE id = %s", (USER_ID,))
    
    conn.commit()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    cur.execute("SELECT xp, level FROM users WHERE id = %s", (USER_ID,))
    user_data = cur.fetchone()
    return render_template('dashboard.html', xp=user_data[0], level=user_data[1])

if __name__ == '__main__':
    app.run(debug=True)
