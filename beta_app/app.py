from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
							confirm_login, fresh_login_required)
from json import loads
import queries

class User(UserMixin):
    def __init__(self, name, id, auth=True, active=True):
        self.name = name
        self.id = id
        self.active = active
        
    def is_active(self):
        return self.active

	def is_authenticated(self):
		return True

	def getUsername(self):
		return self.name

app = Flask('nanna_radio')
app.secret_key = 'c60d4c1e51543f9ec97a6900c03221a63f4f84585791f52693c656135d7fb0ed'
app.config.from_object(__name__)
login_manager = LoginManager()

login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."

@login_manager.user_loader
def load_user(email):
	users = queries.getUsers()

	if email not in users.keys():
		return
	
	user = User(email,users[email])	
	
	return user

@login_manager.request_loader
def request_loader(request):
	users = queries.getUsers()
	email = request.form.get('email')
	if email not in users.keys():
		return

	user = User(email,users[email])

	return user

login_manager.init_app(app)

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/auth/')
def authpage():
	return render_template('auth.html')

@app.route('/login', methods=['GET','POST'])
def login():
	print "Within /login"
	if request.method == 'POST':
		data={'username':request.form['username'],'password':request.form['password']}
		print data
		valid = queries.checkLogin(data['username'],data['password'])
		user = load_user(data['username'])

		if valid == True:		
			if(login_user(user)):
				flash("Login Successful")
				print "Login Successful"			
				return render_template('userhome.html')			

		else:
			return "Login Failed"
	else:
		return redirect(url_for("homepage"))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Logged Out")
	return redirect(url_for("homepage"))

@app.route('/userhome')
@login_required
def userhome():	
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

if __name__ == '__main__':
	app.run(debug = True)
