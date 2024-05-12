from flask import Flask, render_template, abort, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

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
