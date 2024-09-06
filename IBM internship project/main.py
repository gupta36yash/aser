from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import processing
import numpy as np

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'wav'}  # Allowed audio file extensions

# Ensure the upload folder exists
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()=='wav'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST']) # send file from user to flask
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)
        
        #model
        arr=processing.preprocess(filename)
        os.remove(filename)
        try:
            output=processing.model(arr)
        except:
            return jsonify({"Invalid":"Clip needs to longer"}),400  
        d1={
            "Female Angry":float("{:.1f}".format(output[0][0])),
            "Female Disgust":float("{:.1f}".format(output[0][1])),
            "Female Fear":float("{:.1f}".format(output[0][2])),
            "Female Happy":float("{:.1f}".format(output[0][3])),
            "Female Neutral":float("{:.1f}".format(output[0][4])),
            "Female Sad":float("{:.1f}".format(output[0][5])),
            "Female Surprise":float("{:.1f}".format(output[0][6])),
            
            "Male Angry":float("{:.1f}".format(output[0][7])),
            "Male Disgust":float("{:.1f}".format(output[0][8])),
            "Male Fear":float("{:.1f}".format(output[0][9])),
            "Male Happy":float("{:.1f}".format(output[0][10])),
            "Male Neutral":float("{:.1f}".format(output[0][11])),
            "Male Sad":float("{:.1f}".format(output[0][12])),
            "Male Surprise":float("{:.1f}".format(output[0][13])),
            }
        
        keys = list(d1.keys())
        values = list(d1.values())
        sorted_value_index = np.argsort(values)[::-1]
        sd = {keys[i]: values[i] for i in sorted_value_index[0:3]} 
        
        print(sd)
        return jsonify(sd),200    
    return jsonify({"error": "Invalid file format"}), 400

@app.route('/status', methods=['GET']) # get result to user (this really shouldn't be needed but let it remain for now) 
def get_status():
    response = {
        "status": "Server is running",
        "details": "This is a placeholder response for GET requests."
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
