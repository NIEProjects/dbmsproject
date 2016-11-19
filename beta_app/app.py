from flask import Flask, request, render_template, redirect, url_for, flash, session
from json import loads,dumps
from random import shuffle
import queries

def login_user(user_tup):
	print "login_user"
	if user_tup == None:
		return False
		
	(user_id,username,first) = user_tup
	tok = queries.createToken(user_id)
	if tok:
		session['token'] = tok
		session['user_id'] = user_id
		session['username'] = username
		session['first'] = first

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
	quotes = queries.getQuotes()
	return render_template('index.html',quotes=quotes)

# The below catch all function requires static_url_path = '' to be removed
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
# 	print "Catch all path requested = ",path
# 	return render_template('index.html')

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
		return redirect(url_for('homepage'))

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
		return redirect(url_for('homepage'))
	print session
	return render_template('userhome.html')

@app.route('/profile')
def profile():
	if not is_loggedin(session['user_id']):
		return redirect(url_for('homepage'))
	(data,fav) = queries.getProfile(session['user_id'])
	print data,fav	
	return render_template('profile.html',profile_data=data,favourites=fav,json_fav=dumps(fav.keys()))

@app.route('/updateProfile', methods=['POST'])
def updateProfile():
	if not is_loggedin(session['user_id']):
		return render_template(url_for('homepage'))
	data = loads(request.data)
	print data
	print "updateProfile"
	try:
		queries.updateProfile(session['user_id'],data)
		res = '<p id="resultSuccess">Update Successful</p>'
	except Exception as e:
		print "Error in updateProfile route : ",e
		res = '<p id="resultFailure">Update Profile Failed</p>'
	finally:
		return res

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

@app.route('/registration',methods=['GET','POST'])
def signup():	
	states = queries.getStates()
	if request.method == 'POST':
		data = loads(request.data)
		thisState = data['state']
		cities = queries.getCities(thisState)
		return dumps(cities)

	return render_template('signup.html',states=states)

@app.route('/results/<int:marks>')
def result(marks):
	return render_template('scorecard.html', marks = marks)

@app.route('/updatePlaylist',methods=['POST'])
def updatePlaylist():
	data = loads(request.data)
	print "data : ",data['song_id'],data['action']
	queries.updatePlaylist(session['user_id'],data['song_id'],data['action'])
	return "Done"	
#@app.route('/radio',defaults={'val':5})
@app.route('/radio',methods=['GET'])
def radioplayer():
	try:
		if not is_loggedin(session['user_id']):
			return redirect(url_for("homepage"))		
	except:
		return redirect(url_for("homepage"))	
	try:
		val = int(request.args.get('val'))
	except:
		val = 0
	
	(songs_data,songsCount) = queries.getSongs(val,val+10)
	return render_template('radio.html', songs=songs_data, songs_count=songsCount)

@app.route('/discover',methods=['GET','POST'])
def discoverview():
	try:
		if not is_loggedin(session['user_id']):
			return redirect(url_for("homepage"))		
	except:
		return redirect(url_for("homepage"))	
	if request.method == 'POST':
		song_name = request.data
		print "song name = ",song_name
		queries.updatePopularity(song_name)

	try:
		val = int(request.args.get('val'))
	except:
		val = 0
	
	(songs_data,songsCount) = queries.getSongs(val,val+10)
	print songs_data
	# shuffle(songs_data)
	return render_template('discover.html', songs=songs_data, songs_count=songsCount)

@app.route('/browse',methods=['GET','POST'])
def browseview():
	try:
		if not is_loggedin(session['user_id']):
			return redirect(url_for("homepage"))		
	except:
		return redirect(url_for("homepage"))		
	if request.method == 'POST':
		data = request.form
		print "Search : ",data['search']
		results = queries.search(data['search'])		
		print results
		return render_template('browse.html',results=results)		
	return render_template('browse.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True)
