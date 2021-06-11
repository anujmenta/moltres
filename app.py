from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, send_file
from flask import send_from_directory

import requests, time, json
import pandas as pd
import re
import os
import collections
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'csv', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'bill_examples'
app.config['XML_FOLDER'] = 'xml_files'
app.config['CSV_FOLDER'] = 'csv_files'
app.config['OUTPUT_FOLDER'] = 'reports'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def page_to_csv(purifieddict, category, region, usagetype, defaultxpos):
	csv_appender = []
	for key in purifieddict:
		lin = sorted(purifieddict[key], key=lambda x: float(x[2]))
		if len(lin)==2:
			if float(lin[0][2])==defaultxpos[0]:
				category = lin[0][0]
			elif float(lin[0][2])==defaultxpos[1]:
				region = lin[0][0]
			elif float(lin[0][2])==defaultxpos[2]:
				usagetype = lin[0][0]
		elif len(lin)==3:
			if category and region and usagetype:
				csv_appender.append([category, region, usagetype]+[x[0] for x in sorted(purifieddict[key], key=lambda x: float(x[2]))])
	return [csv_appender, category, region, usagetype]

def get_report(filename, subcat_str):
    filename = filename.replace('.csv', '')
    aws_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename+'.csv')
    report_file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename.replace('_rowitems', '')+'_moltres_report.xlsx')
    # os.system('python main.py --input {} --output {} --subcats {}'.format(aws_file_path, report_file_path, "'{"+subcat_str+"}'"))
    os.system('python main.py --input {} --output {} '.format(aws_file_path, report_file_path, "'{"+subcat_str+"}'"))
    return report_file_path

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method=='GET':
        return render_template('upload.html')
    if request.method == 'POST':
        print(dict(request.form))
        # print(['suds_bool', 'suds_bool' in dict(request.form), 'box_compute', 'box_compute' in dict(request.form), 'heavy_compute', 'heavy_compute' in dict(request.form), 'spot_compute', 'spot_compute' in dict(request.form), 'persistentdisk', 'persistentdisk' in dict(request.form), 'cloudstorage', 'cloudstorage' in dict(request.form), 'loadbalancer', 'loadbalancer' in dict(request.form), 'cloudnat', 'cloudnat' in dict(request.form), 'idleaddress', 'idleaddress' in dict(request.form), 'cloudsql', 'cloudsql' in dict(request.form), 'egress', 'egress' in dict(request.form), 'support', 'support' in dict(request.form)])
        subcat_str = '"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},"{}":{},'.format('suds_bool', 'suds_bool' in dict(request.form), 'box_compute', 'box_compute' in dict(request.form), 'heavy_compute', 'heavy_compute' in dict(request.form), 'spot_compute', 'spot_compute' in dict(request.form), 'persistentdisk', 'persistentdisk' in dict(request.form), 'cloudstorage', 'cloudstorage' in dict(request.form), 'loadbalancer', 'loadbalancer' in dict(request.form), 'cloudnat', 'cloudnat' in dict(request.form), 'idleaddress', 'idleaddress' in dict(request.form), 'cloudsql', 'cloudsql' in dict(request.form), 'egress', 'egress' in dict(request.form), 'support', 'support' in dict(request.form))
        # print(json.loads('{'+subcat_str+'}'))
        # check if the post request has the file part
        company_name = dict(request.form)['company'].lower().replace(' ','').replace('.', '')
        requester = dict(request.form)['email']
        print(company_name, requester)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = company_name+'_rowitems.csv'

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            download_path = get_report(filename, subcat_str)
            # print(os.listdir('bill_examples'))
            # print(os.listdir('reports'))
            # print(os.listdir('xml_files'))
            # print(os.listdir('csv_files'))
            return send_file(download_path, as_attachment=True)
            # return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''' 

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__': app.run(debug=True)