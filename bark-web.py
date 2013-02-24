from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json,pprint

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	url =  app.config['api_url'] + 'login'
        request_headers = {
            'Content-Type': 'application/json',
            'xhrFields' : {
                'withCredentials': True,
            }
        }
        request_data = {
			'username' : request.form['username'],
    		'password' : request.form['password'],
		}

        response = requests.post(url,data=json.dumps(request_data),headers=request_headers)
        r = response.json()


        if r['status'] != 'OK':
	        error = r['error_detail']
        else:
            session['auth_token'] = r['auth_token']
            flash('You were logged in')
            return redirect(url_for('events'))
    return render_template('login.html', error=error)



@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
	return 'edit'

@app.route('/events/<int:event_id>', methods=['GET'])
def show_event(event_id):
    url =  app.config['api_url'] + 'events/' + event_id
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields': {
            'withCredentials': True,
        }
    }
    request_data = {
		'auth_token' : session['auth_token'],
	}

    response = requests.post(url,data=json.dumps(request_data),headers=request_headers)
    r = response.json()

    if r['status']!= 'OK':
	    error = r['error_detail']
    else:
        event = r['event']
    return render_template('events.html', event=event)
    
@app.route('/events/')
def events():

    return 'events page'


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'aslkdjf;lsakdjf;alksdjf;lkj'
    app.config['api_url'] = 'http://localhost:5000/'
    app.run(port=4444)
