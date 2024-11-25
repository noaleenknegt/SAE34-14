from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'random token'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql",
            user="nleenkne",
            password="mdp",
            database="BDD_nleenkne",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/client', methods=['GET'])
def show_client():
    return render_template('client.html')

@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()