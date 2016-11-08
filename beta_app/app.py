from flask import Flask, request, render_template, redirect, url_for, flash, session
from json import loads
import queries

def login_user(user_tup):
	print "login_user"
	if user_tup == None:
		return False
		
	(user_id,username) = user_tup
	tok = queries.createToken(user_id)
	if tok:
		session['token'] = tok
		session['user_id'] = user_id
		session['username'] = username

		print "Login Successful"
		return True

	print "Login Failed"
	return False

def is_loggedin(user_id):
	user_dict = queries.getLoggedinUsers()
	print user_dict
	if session['user_id'] in user_dict.keys():
		if session['token'] == user_dict[user_id]:
			return True
	return False


app = Flask('nanna_radio',static_url_path = '')
app.secret_key = 'c60d4c1e51543f9ec97a6900c03221a63f4f84585791f52693c656135d7fb0ed'
app.config.from_object(__name__)

@app.route('/')
def homepage():
	print session
	return render_template('index.html')

@app.route('/auth/')
def authpage():
	return render_template('auth.html')

@app.route('/login', methods=['GET','POST'])
def login():
	print "login"
	if request.method == 'POST':
		print request.form		
		data={'username':request.form['username'],'password':request.form['password']}
		print data
		valid = queries.checkLogin(data['username'],data['password'])
		
		r = login_user(valid)

		return redirect(url_for('homepage'))
	else:
		return render_template('index.html')

@app.route('/logout')
def logout():	
	if not is_loggedin(session['user_id']):
		return redirect(url_for("homepage"))
		
	res = queries.logoutUser(session['user_id'],session['token'])
	session['user_id'] = 0
	session['token'] = ''
	session['username'] = ''

	print "Logout Successful"

	# flash("Logged Out")
	return redirect(url_for("homepage"))

@app.route('/userhome')
def userhome():	
	if not is_loggedin(session['user_id']):
		return
	print session
	return render_template('userhome.html')

@app.route('/signupDB', methods=['POST'])
def register():
	data = loads(request.data)
	print data
	if "city" in data.keys():
		pass
	else:
		data["city"]=None
	if "state" in data.keys():
		pass
	else:
		data["state"]=None

	res = queries.insertProfile(data['user'], data['first'], data['last'], data['dob'], data['city'], data['state'], data['passwd'])
	if res == True:
		return "Registration Successful"
	else:
		return "Registration Failed"

@app.route('/registration')
def signup():
	return render_template('signup.html')

@app.route('/results/<int:marks>')
def result(marks):
	return render_template('scorecard.html', marks = marks)

@app.route('/radio')
def radioplayer():
	return render_template('radio.html')
@app.route('/radio/getsongs', methods=['POST'])
def songlist():
	data = {"title1":"Test Song 1","title2" : "Happy Birthday","title3":"We shall Overcome", "link1": "/media/preview.mp3", "link2": "/media/happybday.mp3","link3" : "/media/weshallovercome.mp3"}
	return render_template('audio.html', data=data)

# @app.route('/media/<songname>')
# def play():
# 	pass

if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True)
