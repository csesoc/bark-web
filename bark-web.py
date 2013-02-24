from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json,pprint

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

#Auth
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

@app.route('/logout', methods=['GET'])
def logout():
    url =  app.config['api_url'] + 'logout'
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        }
    }
    request_data = {
        'auth_token' : session['auth_token'],
    }

    response = requests.post(url,data=json.dumps(request_data),headers=request_headers)
    session.pop('auth_token', None)   

    flash('You were logged out')
    return redirect(url_for('login'))


#Events
@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
	return 'edit'

@app.route('/events/<int:event_id>/delete', methods=['GET'])
def delete_event(event_id):
    url =  app.config['api_url'] + 'events/'+ str(event_id)
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.delete(url,headers=request_headers)
    r = response.json()
    if r['status']!= 'OK':
        flash('Not deleted')
    else:
        flash('Deleted')
    return redirect(url_for('events'))

@app.route('/events/<int:event_id>', methods=['GET'])
def show_event(event_id):
    url =  app.config['api_url'] + 'events/'+ str(event_id)
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.get(url,headers=request_headers)
    r = response.json()

    if r['status']!= 'OK':
        error = r['error_detail']
        return render_template('events_not_found.html', error=error)
    else:
        event = r['event']
    return render_template('events_view.html', event=event)
    
@app.route('/events/')
def events():
    url =  app.config['api_url'] + 'events'
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.get(url,headers=request_headers)
    r = response.json()

    events = r['events']
    return render_template('events.html', events=events)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    error = None
    if request.method == 'POST':
        url =  app.config['api_url'] + 'events'
        request_headers = {
            'Content-Type': 'application/json',
            'xhrFields' : {
                'withCredentials': True,
            },
            'auth_token' : session['auth_token'], 
        }
        request_data = {
            'description' : request.form['description'],
            'name'        : request.form['name'],
            'start_time'  : request.form['start_time'],
            'end_time'    : request.form['end_time'],
            'group_id'    : int(request.form['group_id']),

        }

        response = requests.post(url,data=json.dumps(request_data),headers=request_headers)
        r = response.json()


        if r['status'] != 'OK':
            error = r['error_detail']
        else:
            return redirect('/events/' + str(r['event_id']))
    return render_template('events_add.html', error=error)

#Groups


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'aslkdjf;lsakdjf;alksdjf;lkj'
    app.config['api_url'] = 'http://localhost:5000/'
    app.run(port=4444)
