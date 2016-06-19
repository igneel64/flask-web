from flask import Flask, request, make_response, redirect, url_for, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
app = Flask('flask-web')
manager = Manager(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	if(request.headers.get('User-Agent') != 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'):
		return redirect(url_for('index'))
	return render_template('user.html', name = name)

if __name__ == '__main__':
	manager.run()
