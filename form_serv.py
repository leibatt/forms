import uuid
from flask import Flask,flash, session, request, render_template, g, redirect, send_file, url_for
import basic_form
import forms
import models
from database import db_session,init_db
app = Flask(__name__)

init_db()

app.secret_key = "4"

@app.route('/survey/pretest/show/', methods=["POST", "GET"])
def get_pretest():
    if 'user_id' not in session:
	print "got here"
        session['user_id'] = str(uuid.uuid4())
    else:
        print "already user id:",session['user_id']
    user = models.User(session['user_id'])
    db_session.add(user)
    db_session.commit()
    form = forms.generate_survey_instance_form("pre") #basic_form.RegistrationForm()
    return render_template('pretest_survey.html',form=form)

@app.route('/survey/pretest/submit/', methods=["POST"])
def submit_pretest():
    form = forms.generate_survey_instance_form("pre",request.form)
    forms.submit_user_responses(session['user_id'],form)
    return redirect(url_for('done'))

@app.route('/survey/posttest/show/', methods=["POST", "GET"])
def get_posttest():
    form = forms.generate_survey_instance_form("post") #basic_form.RegistrationForm()
    return render_template('posttest_survey.html',form=form)

@app.route('/survey/posttest/submit/', methods=["POST"])
def submit_posttest():
    form = forms.generate_survey_instance_form("post",request.form)
    forms.submit_user_responses(session['user_id'],form)
    return redirect(url_for('done'))

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
