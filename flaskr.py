import os
import pymongo
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

def connect_db():
    """Connects to the specific database."""
    connection = pymongo.MongoClient('127.0.0.1',27017)
    db = connection.entries
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.schema', mode=)

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    extries = [dict(title=row[0], text=row[1] for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)')
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['usernaem'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
