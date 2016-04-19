#coding:utf-8
from flask import Flask, send_from_directory,render_template, request, redirect, url_for, jsonify, json,session
import time
import random

app = Flask(__name__)


# application start



def config(d,f="output"):
	session["dimension"] = int(d)
	session["output_file"] = f
	return

def init_x():
	d = int(session["dimension"])
	x = [random.uniform(0,1) for i in range(d)]
	session["last_x"] = x
	session["data"] = []
	return

def get_x_message(x_lst):
	s = ''
	for i,x in enumerate(x_lst):
		print i,session["dimension"]
		# if i == session["dimension"]:
		#  	s += "y = " + "{0:.4f}".format(x) + " "
		# else:
		# 	s += "x[" + str(i) + "] = " + "{0:.4f}".format(x) + " "


		s +=  "{0:.4f}".format(x) + " "
	return s


def save(x_lst,y,mode = "a",message=True):
	out = open(session["output_file"], mode)
	for i in x_lst:
		out.write(str(i))
		out.write(" ")

	out.write(str(y) + "\n")
	out.close()
	if message: print "save x,y"



def caluculate(x_lst,y):
	return map(lambda x_i: x_i + random.uniform(0,0.01),x_lst)


@app.route("/test")
def test():
	return render_template("test.html")

@app.route("/config",methods=['POST'])
def re_config():
	d = request.form["setting_dimension"]
	config(d=d)
	print session
	return redirect(url_for("index"))



@app.route("/")
def index():
	print "called index"
	title = "Hello"
	if "dimension" in session:
		d = session["dimension"]
	else:
		d = 3

	config(d,f="output.txt")
	init_x()
	s = get_x_message(session["last_x"])
	f = open(session["output_file"],"w")
	f.close()


	return render_template("index.html",
						   new_x=s+" (initial x)" , title=title)




@app.route("/ypost",methods=['GET', 'POST'])
def post():
	time.sleep(1)
	y = request.json['y']

	#save x,y
	last_x = list(session["last_x"])
	save(last_x, float(y))
	last_x.append(float(y))
	session["data"].append(last_x)

	#make new x
	new_x = caluculate(session["last_x"],y)
	session["last_x"] = new_x
	print session

	return_data = {"new_x": get_x_message(new_x),
				   "result_x":get_x_message(last_x)}
	return jsonify(ResultSet=json.dumps(return_data))



@app.route('/download/<path:filename>')
def download(filename):
	"""donwload file"""
	return send_from_directory('.', filename)



if __name__ == "__main__":
	app.debug = True
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run()
