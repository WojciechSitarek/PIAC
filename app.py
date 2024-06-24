from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os

app = Flask(__name__)

# Konfiguracja sekretu aplikacji
app.secret_key = secrets.token_hex(16)

# Konfiguracja SQLAlchemy dla bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model wpisu do księgi gości
class GuestBookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

# Tworzenie tabeli w bazie danych
with app.app_context():
    db.create_all()

# Konfiguracja Flask-Dance GitHub OAuth
github_blueprint = make_github_blueprint(
    client_id="Ov23li4czesvxYaQjQs1",
    client_secret="f6056817263c76eaa38cf2307cd6617d3cb08645"
)
app.register_blueprint(github_blueprint, url_prefix='/login')

# Ustawienie zmiennej środowiskowej dla Flask-Dance
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/')
def home():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            github_name = account_info_json['login']
        else:
            github_name = 'Unknown'

    return render_template("home.html", github_name=github_name)

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        nick = request.form['nick']
        text = request.form['text']

        new_entry = GuestBookEntry(nick=nick, text=text)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/guestbook')
        except:
            return "Wystąpił błąd podczas dodawania wpisu."

    entries = GuestBookEntry.query.order_by(GuestBookEntry.date_added.desc()).all()
    return render_template('guestbook.html', entries=entries)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = GuestBookEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.nick = request.form['nick']
        entry.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/guestbook')
        except:
            return "Wystąpił błąd podczas edycji wpisu."
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = GuestBookEntry.query.get_or_404(id)
    try:
        db.session.delete(entry)
        db.session.commit()
        return redirect('/guestbook')
    except:
        return "Wystąpił błąd podczas usuwania wpisu."

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.route('/error_internal')
def error_internal():
    return render_template('template.html', name='ERROR 500'), 500

@app.route('/error_forbidden')
def error_forbidden():
    response = make_response(render_template('template.html', name='ERROR 403'), 403)
    response.headers['X-Something'] = 'A value'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
