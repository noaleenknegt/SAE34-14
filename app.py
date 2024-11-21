from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'random token'


@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()