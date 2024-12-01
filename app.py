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
    #faire verif trucs clients
    #faire cascade delete et flash
    my_cursor = get_db().cursor()
    rang = {}
    sql = """SELECT * FROM Client"""
    my_cursor.execute(sql)
    clients = my_cursor.fetchall()
    sql = """SELECT * FROM Rang"""
    my_cursor.execute(sql)
    rangs = my_cursor.fetchall()
    for i in rangs:
        rang[i['IdRang']] = i['LibelleRang']
    sql = """SELECT Client.IdCLient, SUM(Achete.Quantite_Achetee) AS TotalAchetee
    FROM Achete RIGHT JOIN Client ON Achete.IdClient = Client.IdClient
        JOIN Rang ON Client.IdRang = Rang.IdRang
    GROUP BY Client.IdCLient;"""
    my_cursor.execute(sql)
    totalAchetee = my_cursor.fetchall()
    TotalDeposee = {}
    sql = """SELECT Client.IdClient, SUM(Depose.Quantite_Deposee) AS TotalDeposee
    FROM Depose RIGHT JOIN Client ON Depose.IdClient = Client.IdClient
        JOIN Rang ON Client.IdRang = Rang.IdRang
    GROUP BY Client.IdClient;"""
    my_cursor.execute(sql)
    totalDeposee = my_cursor.fetchall()
    get_db().commit()
    TotalAchetee = {}
    for i in totalAchetee:
        TotalAchetee[i['IdCLient']] = i['TotalAchetee'] if i['TotalAchetee'] is not None else 0
    for i in totalDeposee:
        TotalDeposee[i['IdClient']]= i['TotalDeposee'] if i['TotalDeposee'] is not None else 0
    return render_template('client/show_client.html', clients=clients, rang=rang, TotalAchetee=TotalAchetee, TotalDeposee=TotalDeposee)

@app.route('/client/add', methods=['GET'])
def add_client():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Rang"""
    my_cursor.execute(sql)
    rangs = my_cursor.fetchall()
    get_db().commit()
    return render_template('client/add_client.html', rangs=rangs)

@app.route('/client/add', methods=['POST'])
def valid_add_client():
    my_cursor = get_db().cursor()
    sql = """INSERT INTO Client (Nom, Prenom, AdresseMail, Telephone, IdRang) VALUES (%s, %s, %s, %s, %s)"""
    my_cursor.execute(sql, (request.form['Nom'], request.form['Prenom'], request.form['AdresseMail'], request.form['Telephone'], request.form['IdRang']))
    get_db().commit()
    return redirect("/client/show")

@app.route('/client/delete', methods=['GET'])
def delete_client():
    my_cursor = get_db().cursor()
    sql = """DELETE FROM Client WHERE IdClient=%s"""
    print(request.args['id'])
    my_cursor.execute(sql, (request.args.get('id')))
    get_db().commit()
    return redirect("/client/show")

@app.route('/client/edit', methods=['GET'])
def edit_client():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Client WHERE IdClient=%s"""
    my_cursor.execute(sql, (request.args.get('id')))
    client = my_cursor.fetchone()
    sql = """SELECT * FROM Rang"""
    my_cursor.execute(sql)
    rangs = my_cursor.fetchall()
    get_db().commit()
    return render_template('client/edit_client.html', client=client, rangs=rangs)

@app.route('/client/edit', methods=['POST'])
def valid_edit_client():
    my_cursor = get_db().cursor()
    Nom = request.form['Nom']
    Prenom = request.form['Prenom']
    IdRang = request.form['IdRang']
    Telephone = request.form['Telephone']
    IdClient = request.form['IdClient']
    if (len(Nom) <= 20 and len(Prenom) <= 20 and len(Telephone) == 10 ):
        sql = """UPDATE Client SET Nom=%s, Prenom=%s, IdRang=%s, Telephone=%s WHERE IdClient=%s"""
        my_cursor.execute(sql, (Nom, Prenom, IdRang, Telephone, IdClient))
        get_db().commit()
    return redirect("/client/show")

@app.route('/reduction/show', methods=['GET'])
def show_reduction():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Reduction"""
    my_cursor.execute(sql)
    reductions = my_cursor.fetchall()
    sql = """SELECT * FROM TypeVetement"""
    my_cursor.execute(sql)
    typeVetements = my_cursor.fetchall()
    sql = """SELECT * FROM Rang"""
    my_cursor.execute(sql)
    rangs = my_cursor.fetchall()
    get_db().commit()
    return render_template('reduction/show_reduction.html', reductions=reductions, typeVetements=typeVetements, rangs=rangs)

@app.route('/reduction/delete', methods=['GET'])
def delete_reduction():
    my_cursor = get_db().cursor()
    sql = """DELETE FROM Reduction WHERE IdTypeVetement=%s AND IdRang=%s"""
    my_cursor.execute(sql, (request.args.get('IdTypeVetement'), request.args.get('IdRang')))
    get_db().commit()
    return redirect("/reduction/show")

@app.route('/reduction/edit', methods=['GET'])
def edit_reduction():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Reduction WHERE IdTypeVetement=%s AND IdRang=%s"""
    my_cursor.execute(sql, (request.args.get('IdTypeVetement'), request.args.get('IdRang')))
    reduction = my_cursor.fetchone()
    get_db().commit()
    return render_template('reduction/edit_reduction.html', reduction=reduction)

@app.route('/reduction/edit', methods=['POST'])
def valid_edit_reduction():
    my_cursor = get_db().cursor()
    sql = """UPDATE Reduction SET PourcentageReduction=%s WHERE IdTypeVetement=%s AND IdRang=%s"""
    my_cursor.execute(sql, (request.form['PourcentageReduction'], request.form['IdTypeVetement'], request.form['IdRang']))
    get_db().commit()
    return redirect("/reduction/show")

@app.route('/reduction/add', methods=['GET'])
def add_reduction():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM TypeVetement"""
    my_cursor.execute(sql)
    typeVetements = my_cursor.fetchall()
    sql = """SELECT * FROM Rang"""
    my_cursor.execute(sql)
    rangs = my_cursor.fetchall()
    get_db().commit()
    return render_template('reduction/add_reduction.html', typeVetements=typeVetements, rangs=rangs)

@app.route('/reduction/add', methods=['POST'])
def valid_add_reduction():
    my_cursor = get_db().cursor()
    sql = """INSERT INTO Reduction (IdTypeVetement, IdRang, PourcentageReduction) VALUES (%s, %s, %s)"""
    my_cursor.execute(sql, (request.form['IdTypeVetement'], request.form['IdRang'], request.form['PourcentageReduction']))
    get_db().commit()
    return redirect("/reduction/show")

@app.route('/collecte/show', methods=['GET'])
def show_collecte():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Collecte"""
    my_cursor.execute(sql)
    collectes = my_cursor.fetchall()
    collecte = my_cursor.fetchone()
    sql = """SELECT * FROM TypeVetement"""
    my_cursor.execute(sql)
    typeVetement = my_cursor.fetchall()
    sql = """SELECT * FROM Benne"""
    my_cursor.execute(sql)
    benne = my_cursor.fetchall()
    get_db().commit()
    return render_template('collecte/show_collecte.html', collectes=collectes, typeVetement=typeVetement, benne=benne)

@app.route('/collecte/delete', methods=['GET'])
def delete_collecte():
    my_cursor = get_db().cursor()
    sql = """DELETE FROM Collecte WHERE IdTypeVetement=%s AND IdBenne=%s AND JJ_MM_AAAA=%s"""
    my_cursor.execute(sql, (request.args.get('IdTypeVetement'), request.args.get('IdBenne'), request.args.get('JJ_MM_AAAA')))
    get_db().commit()
    return redirect("/collecte/show")

@app.route('/collecte/edit', methods=['GET'])
def edit_collecte():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM Collecte WHERE IdTypeVetement=%s AND IdBenne=%s AND JJ_MM_AAAA=%s"""
    args = (request.args.get('IdTypeVetement'), request.args.get('IdBenne'), request.args.get('JJ_MM_AAAA'))
    my_cursor.execute(sql, (request.args.get('IdTypeVetement'), request.args.get('IdBenne'), request.args.get('JJ_MM_AAAA')))
    collecte = my_cursor.fetchone()
    print(collecte)
    sql = """SELECT * FROM TypeVetement"""
    my_cursor.execute(sql)
    typeVetements = my_cursor.fetchall()
    sql = """SELECT * FROM Benne"""
    my_cursor.execute(sql)
    bennes = my_cursor.fetchall()
    get_db().commit()
    return render_template('collecte/edit_collecte.html', collecte=collecte, typeVetements=typeVetements, bennes=bennes, args=args)

@app.route('/collecte/edit', methods=['POST'])
def valid_edit_collecte():
    my_cursor = get_db().cursor()
    sql = """UPDATE Collecte SET Quantite_Collectee=%s WHERE IdTypeVetement=%s AND IdBenne=%s AND JJ_MM_AAAA=%s"""
    my_cursor.execute(sql, (request.form['Quantite_Collectee'], request.form['IdTypeVetement'], request.form['IdBenne'], request.form['JJ_MM_AAAA']))
    get_db().commit()
    return redirect("/collecte/show")

@app.route('/collecte/add', methods=['GET'])
def add_collecte():
    my_cursor = get_db().cursor()
    sql = """SELECT * FROM TypeVetement"""
    my_cursor.execute(sql)
    typeVetements = my_cursor.fetchall()
    sql = """SELECT * FROM Benne"""
    my_cursor.execute(sql)
    bennes = my_cursor.fetchall()
    get_db().commit()
    return render_template('collecte/add_collecte.html', typeVetements=typeVetements, bennes=bennes)

@app.route('/collecte/add', methods=['POST'])
def valid_add_collecte():
    my_cursor = get_db().cursor()
    sql = """INSERT INTO Collecte (IdTypeVetement, IdBenne, JJ_MM_AAAA, Quantite_Collectee) VALUES (%s, %s, %s, %s)"""
    my_cursor.execute(sql, (request.form['IdTypeVetement'], request.form['IdBenne'], request.form['JJ_MM_AAAA'], request.form['Quantite_Collectee']))
    get_db().commit()
    return redirect("/collecte/show")
@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()