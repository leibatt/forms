from flask import Flask,flash, session, request, render_template, g, redirect, send_file, url_for
import basic_form
import forms
from database import db_session,init_db
app = Flask(__name__)

init_db()

app.secret_key = "4"

forms.show_survey("pre")

@app.route('/reg/', methods=["POST", "GET"])
def main():
    form = basic_form.RegistrationForm()
    return render_template('register.html',form=form)

@app.route('/login/', methods=["POST"])
def register():
    form = basic_form.RegistrationForm(request.form)
    if form.validate():
        print "received username:",form.username.data
        print "received email:",form.email.data
        print "accept rules:",form.accept_rules.data
        flash('Thanks for registering')
        return redirect(url_for('done'))
    return render_template('register.html', form=form)

@app.route('/done/',methods=["POST","GET"])
def done():
    return render_template('done.html')

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.debug = True
    #address = ('', 8080)
    #http_server = WSGIServer(address, app, handler_class=WebSocketHandler)
    #http_server.serve_forever()
    app.run()
