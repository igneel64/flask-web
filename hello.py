from flask import Flask, request, make_response, redirect, url_for
from flask_script import Manager
app = Flask('flask-web')
manager = Manager(app)

@app.route('/')
def index():
	return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
	user_agent = request.headers.get('User-Agent')
	if(user_agent != 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'):
		return redirect(url_for('index'))
	response = make_response('<h1>Hello, {0}, u are using the correct User-Agent</h1>'.format(name))
	response.set_cookie('user', 'petros')
	return response

if __name__ == '__main__':
	app.run(debug=True, threaded = True)
	manager.run()