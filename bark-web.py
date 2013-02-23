from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	url =  app.config['api_url'] + 'login'
        request_headers = {'Content-Type': 'application/json'}
        request_data = {
			'username' : request.form['username'],
    		'password' : request.form['password'],
		}

		response = requests.post(url,data=json.dumps(request_data),headers=request_headers)

        if response.text['status'] == 'REQUEST_DENIED':
	        error = response.text['error_details']
        else:
            session['auth_token'] = response.text['auth_token']
            flash('You were logged in')
            return redirect(url_for('events'))
    return render_template('login.html', error=error)

@app.route('/events/')
def events():
    return 'events page'

@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event):
	return ''

@app.route('/event/<int:event_id>', methods=['GET'])
def show_event(event):
	return ''
    



if __name__ == '__main__':
	app.DEBUG = True
	app.secret_key = 'aslkdjf;lsakdjf;alksdjf;lkj'
	app.api_url = 'http://localhost:5000/'
    app.run(port=4444)
