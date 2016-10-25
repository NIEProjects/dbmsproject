from flask import Flask, render_template, request, redirect, url_for
from json import loads
import queries

app = Flask('spotify_clone')

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/auth/')
def authpage():
	return render_template('auth.html')

@app.route('/login', methods=['POST'])
def logininfo():
	data = loads(request.data)
	print data
	valid = queries.checkLogin(data['username'],data['password'])
	if valid == True:
		return redirect('/home/'+data['username'])
	else:
		return "Login Failed"

@app.route('/home/<name>/')
def userhome(name):
	print name
	return render_template('userhome.html', name = name)

@app.route('/results/<int:marks>')
def result(marks):
	return render_template('scorecard.html', marks = marks)

if __name__ == '__main__':
	app.run(debug = True)
