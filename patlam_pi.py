# -*- coding: utf-8 -*-

import os
import subprocess
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
    render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SOUNDDATA=os.path.join(app.root_path, 'sound'),
    LOGFILE=os.path.join(app.root_path, 'log', 'snmptrapd_receive.log'),
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
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def get_setting(key):
    with app.app_context():
        db = get_db()
        cur = db.execute("SELECT val FROM settings WHERE key = '" + key + "'")
        __setting = cur.fetchone()
        return __setting[0]

def set_volume_fromdb():
    cmd = "amixer -c 0 sset 'PCM' " + get_setting('SoundVolume') + "%"
    os.system(cmd)

def __system(cmd):
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    stdout_data, stderr_data = p.communicate()
    if p.returncode == 0:
        return stdout_data
    else:
        return "Error Occurred"

def __get_system_stat():
    statuses = dict()
    statuses['IP'] = __system("hostname -I")
    statuses['Uptime'] = __system("w | head -1")
    statuses['Snmptrap'] = __system("grep 'snmptrapd' /var/log/daemon.log | tail -5").replace('\n','<br>')

    return statuses

@app.route('/')
def top():
    db = get_db()
    cur = db.execute('select * from settings')
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