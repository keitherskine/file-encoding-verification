import csv
import os

from flask import request, render_template, redirect, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/vrf/<state>/<runcode>')
def vrf_state_bareruncode(state, runcode):
    return redirect(url_for('vrf_source_file', state=state, runcode=runcode))

@app.route('/vrf/<state>/<runcode>/', methods=['POST', 'GET'])
def vrf_source_file(state, runcode):
    print(state, runcode)
    print('request.method: {}'.format(request.method))
    print('request.url   : {}'.format(request.url))
    print('request.form  : {}'.format(request.form))
    print('request.args  : {}'.format(request.args))
    print('request.json  : {}'.format(request.json))

    if request.method == 'POST':

        all_files = os.listdir(os.path.join(app.config['VRF_DATA_DIR'], state, runcode))
        text_files = [f for f in all_files if f.endswith(r'.txt')]

        data = []
        with open(os.path.join(os.path.join(app.config['VRF_DATA_DIR'],
                               state, runcode, request.form['filename'])),
                  'r', encoding=request.form['encoding'], errors='replace') as file:
            csv_reader = csv.reader(file, delimiter=request.form['delimiter'])
            line_num = 0
            for row in csv_reader:
                data.append(row)
                line_num += 1
                if line_num >= 10: break

        return render_template('vrf_source_file.html',
                               state=state,
                               runcode=runcode,
                               files=sorted(text_files),
                               filename=request.form['filename'],
                               encoding=request.form['encoding'],
                               delimiter=request.form['delimiter'],
                               data=data)

    elif request.method == 'GET':

        all_files = os.listdir(os.path.join(app.config['VRF_DATA_DIR'], state, runcode))
        text_files = [f for f in all_files if f.endswith(r'.txt')]
        # default to the voters file, whether it exists or not
        return render_template('vrf_source_file.html',
                               state=state,
                               runcode=runcode,
                               files=sorted(text_files),
                               filename='{}_{}_Source_VotersFile.txt'.format(state, runcode))
    else:
        return "Hello, World!"
