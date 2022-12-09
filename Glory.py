from flask import Flask, render_template, redirect, url_for, request, flash
import numpy as np
import os, cv2

app = Flask(__name__, template_folder='./templates')
app.secret_key=os.urandom(512)

@app.errorhandler(404)
def page_not_found(e):
    flash('404- NO PAGE FOUND!', "dark")
    return redirect(url_for('index'))

@staticmethod
def detect(image):
	img = cv2.imread(image)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3,3), 0)
	edges = cv2.Canny(blurred, 50, 150)
	num_edges = np.sum(edges)
	if np.count_nonzero(edges) > 100000:
		return(True)
	else:
		return(False)

@app.route('/', methods=['GET'])
def index():
   return render_template("index.html")

@app.route('/check_Image', methods=['POST'])
def check():
	image=request.files['Image']
	image.save('./file/{}'.format(image.filename))
	verdict=detect("./file/"+image.filename)
	if verdict==True:
		flash("IMAGE SEEMS LEGIT!", "success")
		return render_template("index.html")
	else:
		flash("IMAGE NOT LEGIT!", "danger")
		return render_template("index.html")

if __name__=='__main__':
	app.run(debug=True)