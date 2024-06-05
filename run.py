from flask import Flask, render_template, request, redirect, make_response, url_for
from models import db, GuestBookEntry

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Tworzenie tabeli
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("home.html")


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
