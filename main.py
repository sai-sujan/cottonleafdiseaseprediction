import os

from flask import Flask, render_template, request, url_for, jsonify
from werkzeug.utils import redirect
from decode import decodeImage
from model_cat import image_recog_cat

app = Flask(__name__)


@app.route('/cat', methods=['GET', 'POST'])
def cat():
	if request.method == 'POST':
			f = request.files['file']
			f.save(f'./data/cat/{f.filename}')
			cat_data = image_recog_cat(f'./data/cat/{f.filename}')
			return redirect(url_for("success", filename=f.filename, data={'cat_data': cat_data}))
	return render_template('cat.html')


@app.route('/success/<filename>/<data>', methods=['GET', 'POST'])
def success(filename=None, data=None):
	if filename and data:
		return render_template('success.html', name=filename, data=data)
	return render_template('success.html')




@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == "POST":
		if request.form.get("cat"):
			return redirect(url_for('cat'))

	return render_template('upload.html')


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == "POST":
		if request.form.get("upload"):
			return redirect(url_for('upload'))
	return render_template('index.html')


@app.route('/cat/predict', methods=['POST','GET'])
def catPredict():
	image = request.json['image']
	decodeImage(image)
	cat_data = image_recog_cat('data.jpg')
	return jsonify({'output':cat_data})







if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	# app.run(debug=True)