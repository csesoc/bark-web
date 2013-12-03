# Use this when developing on a local environment
#app.config['api_url'] = 'http://127.0.0.1:5000/'

#Use this when deploying to the CSESoc server
app.config['api_url'] = 'https://api.bark.csesoc.unsw.edu.au/'

app.secret_key = 'aslkdjf;lsakdjf;alksdjf;lkj'

if __name__ == '__main__':
	app.debug = True
	app.run(port=4444)