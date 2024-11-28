from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'random token'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql.iut-bm.univ-fcomte.fr",
            user="nleenkne",
            password="mdp",
            database="BDD_nleenkne_sae",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/client/show', methods=['GET'])
def show_client():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Client"""
    my_cursor.execute(sql)
    clients = my_cursor.fetchall()
    get_db().commit()
    return render_template('show_client.html', clients=clients)


@app.route('/client/delete', methods=['GET'])
def delete_client():
    my_cursor = get_db().cursor()
    sql = """DELETE FROM Client WHERE IdClient=%s"""
    print(request.args['id'])
    my_cursor.execute(sql, (request.args['id']))
    get_db().commit()
    return redirect("/client/show")

@app.route('/client/add', methods=['GET'])
def edit_client():


@app.route('/reduction', methods=['GET'])
def show_reduction():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Reduction"""
    my_cursor.execute(sql)
    reductions = my_cursor.fetchall()
    return render_template('show_reduction.html', reductions=reductions)

@app.route('/collecte', methods=['GET'])
def show_collecte():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Collecte"""
    my_cursor.execute(sql)
    collectes = my_cursor.fetchall()
    return render_template('show_collecte.html', collectes=collectes)

@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()