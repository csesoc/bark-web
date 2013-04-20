from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests, json,pprint
from datetime import datetime
import iso8601

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def format_time(time,format="%A, %d %B %Y %I:%M%p"):
        return iso8601.parse_date(time).strftime(format)
    return dict(format_time=format_time)


@app.route('/')
def index():
    if session.get('auth_token'):
        return redirect(url_for('events'))
    return redirect(url_for('login'))


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

        response = requests.post(url,data=json.dumps(request_data),headers=request_headers, verify=False)
        r = response.json()


        if r['status'] != 'OK':
	        error = r['error_detail']
        else:
            session['auth_token'] = r['auth_token']
            flash('You were logged in')
            return redirect(url_for('index'))
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

    response = requests.post(url,data=json.dumps(request_data),headers=request_headers, verify=False)
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

    response = requests.delete(url,headers=request_headers, verify=False)
    r = response.json()
    if r['status']!= 'OK':
        flash('Not deleted')
    else:
        flash('Deleted')
    return redirect(url_for('events'))

@app.route('/events/<int:event_id>', methods=['GET'])
def show_event(event_id):
    url =  app.config['api_url'] + 'events/'+ str(event_id)+'/swipes'
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.get(url,headers=request_headers, verify=False)
    r = response.json()
    if r['status']!= 'OK':
        error = r['error_detail']
        return render_template('events_not_found.html', error=error)

    else:
        event = r['event']
        swipes = r['swipes']
        count = len(swipes)
    return render_template('events_view.html', event=event,swipes=swipes,count=count)
    
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

    response = requests.get(url,headers=request_headers, verify=False)
    r = response.json()

    events = r['events']
    return render_template('events.html', events=events)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    error = None
    groups= None
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'], 
    }
    
    if request.method == 'POST':
        url =  app.config['api_url'] + 'events'
        st = datetime.strptime(request.form['start_time'],"%d/%m/%Y %I:%M %p")
        et = datetime.strptime(request.form['end_time'],"%d/%m/%Y %I:%M %p")    

        request_data = {
            'description' : request.form['description'],
            'name'        : request.form['name'],
            'start_time'  : st.isoformat(),
            'end_time'    : et.isoformat(),
            'group_id'    : int(request.form['group_id']),

        }

        response = requests.post(url,data=json.dumps(request_data),headers=request_headers, verify=False)
        r = response.json()


        if r['status'] != 'OK':
            error = r['error_detail']
        else:
            return redirect('/events/' + str(r['event_id']))
    
    url =  app.config['api_url'] + 'groups'
    response = requests.get(url,headers=request_headers, verify=False)
    r = response.json()
    groups = r['groups']
    return render_template('events_add.html', error=error, groups=groups)

#Groups
@app.route('/groups/')
def groups():
    url =  app.config['api_url'] + 'groups'
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.get(url,headers=request_headers, verify=False)
    r = response.json()

    groups = r['groups']
    return render_template('groups.html', groups=groups)

@app.route('/groups/<int:group_id>', methods=['GET'])
def show_group(group_id):
    url =  app.config['api_url'] + 'groups/'+ str(group_id)
    request_headers = {
        'Content-Type': 'application/json',
        'xhrFields' : {
            'withCredentials': True,
        },
        'auth_token' : session['auth_token'],
    }

    response = requests.get(url,headers=request_headers, verify=False)
    r = response.json()

    if r['status']!= 'OK':
        error = r['error_detail']
        return render_template('groups_not_found.html', error=error)
    else:
        group = r['group']
    return render_template('groups_view.html', group=group)


@app.route('/groups/add', methods=['GET', 'POST'])
def add_groups():
    error = None
    if request.method == 'POST':
        url =  app.config['api_url'] + 'groups'
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
        }

        response = requests.post(url,data=json.dumps(request_data),headers=request_headers, verify=False)
        r = response.json()


        if r['status'] != 'OK':
            error = r['error_detail']
        else:
            return redirect('/groups/' + str(r['group_id']))
    return render_template('groups_add.html', error=error)

#App
app.config['api_url'] = 'https://api.bark.csesoc.unsw.edu.au/'
app.secret_key = 'aslkdjf;lsakdjf;alksdjf;lkj'

if __name__ == '__main__':
    app.debug = True
    app.run(port=4444)
