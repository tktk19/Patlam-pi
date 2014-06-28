# -*- coding: utf-8 -*-

import os
import subprocess
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SOUNDDATA=os.path.join(app.root_path, 'sound'),
    DATABASE=os.path.join(app.root_path, 'patlam_pi.db'),
    DEBUG=True,
    SECRET_KEY='De45uw4wuhHUERW232mksdohHUHEFIUI',
    USERNAME='pi',
    PASSWORD='1qazse4'
))
app.config.from_envvar('PATLAM-PI_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def __system(arg0, arg1):
    p = subprocess.Popen([arg0, arg1],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=False)

    return p.stdout.readlines()

def __get_system_stat():
    statuses = dict()
    statuses['IP'] = __system("hostname" , "-I")
    statuses['Uptime'] = __system("w", " | head -1")
    #statuses['Snmptrap'] = __system("grep 'snmptrapd' /var/log/daemon.log", " | tail -5")

    return statuses

@app.route('/')
def top():
    db = get_db()
    cur = db.execute('select * from settings order by id asc')
    settings = cur.fetchall()
    statuses = __get_system_stat()

    return render_template("top.html", settings=settings, statuses=statuses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('top'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('top'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # amixer -c 0 sset 'PCM' 50%
