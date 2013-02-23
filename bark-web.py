from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    	# do the login and save authkey in session cookies
    else:
        # show the login form

@app.route('/event/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event):
    if request.method == 'POST':
    	# save event info
    else:
        # show event edit form

@app.route('/event/<int:event_id>', methods=['GET'])
def show_event(event):
	 # show the event
    



if __name__ == '__main__':
    app.run()
