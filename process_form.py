from flask import Flask, request
import requests
import json
import numpy as np
import pandas as pd
from keras.models import load_model                                                         

app = Flask(__name__)

@app.route('/process_form', methods=['POST'])


def process_form():

    model = load_model('mymodel.hd5/')

    X = {}
    X['age'] = request.form['age']
    X['sex'] = request.form['sex']
    X['cp'] = request.form['cp']
    X['trestbps'] = request.form['trestbps']
    X['chol'] = request.form['chol']
    X['fbs'] = request.form['fbs']
    X['restecg'] = request.form['restecg']
    X['thalach'] = request.form['thalach']
    X['exang'] = request.form['exang']
    X['oldpeak'] = request.form['oldpeak']
    X['slope'] = request.form['slope']
    X['ca'] = request.form['ca']
    X['thal'] = request.form['thal']



    normal_range = {
        'age': "[20, 70]",
        'Gender':"Male (1). Female (0).",
        'Chest Pain Type (cp)': " *Typical Angina: 1.  *Atypical Angina: 2.  *Non-Anginal Pain: 3.  *Asymptomatic: 4",
        'Resting Blood Pressure (trestbps)': "*Normal range: Typically around 90/60 mm Hg to 120/80 mm Hg. *Optimal range: Below 120/80 mm Hg.",
        'Serum Cholesterol (chol):': "*Normal range: Below 200 mg/dL. *Desirable range: Below 200 mg/dL.",
        'Fasting Blood Sugar (fbs)': "*Normal range: Typically less than 100 mg/dL. *Prediabetes range: Between 100 and 125 mg/dL. *Diabetes range: 126 mg/dL or higher on two separate tests.",
        'Resting Electrocardiographic Results (restecg)': "*Normal range: 0 (normal). *ST-T wave abnormality range: 1 (having ST-T wave abnormality). *Left ventricular hypertrophy range: 2 (showing probable or definite left ventricular hypertrophy).",
        'Maximum Heart Rate Achieved (thalach)': "*Normal range: The maximum heart rate achieved can vary depending on factors such as age and fitness level. However, a general estimate is around 60-85% of the maximum heart rate based on age. For example, for a 30-year-old, the estimated maximum heart rate would be around 190 beats per minute (bpm), and the normal range during exercise would be approximately 114-162 bpm (60-85Percent of 190 bpm).",
        'Exercise-Induced Angina (exang)': "*Normal range: 0 (no exercise-induced angina). *Presence of exercise-induced angina range: 1 (exercise-induced angina present).",
        'ST Depression Induced by Exercise Relative to Rest (oldpeak)': "*Normal range: The interpretation of ST depression depends on various factors. However, in general, an ST depression of 0.5 to 1 mm is considered mild, while greater than 1 mm is considered significant.",
        'Slope of the Peak Exercise ST Segment (slope)':"*Upsloping range: 1 (upsloping slope of the peak exercise ST segment). *Flat range: 2 (flat slope of the peak exercise ST segment). *Downsloping range: 3 (downsloping slope of the peak exercise ST segment).",
        'Number of Major Vessels Colored by Fluoroscopy (ca)': "*Normal range: The number of major vessels ranges from 0 to 3. In a healthy individual, the presence of major vessels colored by fluoroscopy would typically be 0.",
        'Thalassemia (thal)': "*Normal range: 3 (normal thalassemia value). *Fixed Defect range: 6 (fixed defect thalassemia value). *Reversible Defect range: 7 (reversible defect thalassemia value)."
    }


    
    new_x_array = np.array(list(map(float,X.values()))).reshape(1, -1)
    
    prediction = model.predict(new_x_array)
    
    if prediction[0][0] > 0.5:
        data = X
        result = "The patient have the heart disease."
    else:
        data = X
        result = "The patient do not have heart disease."
    

    data = {'Result': result,'Your_Data': data, 'Normal_Range': normal_range }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1/myapp/wp-json/myplugin/v1/process_form_response', json=json_data, headers=headers)

  
    
    
    return json_data

    

if __name__ == '__main__':
    app.run(debug=True)