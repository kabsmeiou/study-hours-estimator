from flask import Flask, render_template, redirect, url_for, request, jsonify

from flask_wtf import CSRFProtect
import secrets
import pickle

# for dmatrix conversion
import xgboost as xgb

# form for the student details
from src.form_handler import StudentForm

app = Flask(__name__)
key = secrets.token_urlsafe(16)
app.secret_key = key

# Flask-WTF requires this line
csrf = CSRFProtect(app)

# get the xgb model(study hours estimator)
model_file=f'study_hestimator.bin'

with open(model_file, 'rb') as f_in:
    model, dv = pickle.load(f_in)

@app.route("/")
def redirect_form():
    return redirect(url_for('student_form'))

@app.route("/estimate")
def predict(student_data):
    data_dictionary = student_data
    # remove unneeded data
    del data_dictionary['name']
    del data_dictionary['csrf_token']
    del data_dictionary['submit']

    # one hot encoding on the dictionary(student data)
    X = dv.transform([data_dictionary]) # feature
    X_dmatrix = xgb.DMatrix(X)
    # use the model to predict with the features and round it to the nearest integer
    y = round(model.predict(X_dmatrix)[0]) # hours variable

    # return "50+" if y>=50, "You don't need to study" if <= 0
    study_hours = {}
    
    if y >= 50:
        study_hours = {
            "study_hours": "50+"
        }
        return jsonify(study_hours)

    if y <= 0:
        study_hours = {
            "study_hours": "You don't need to study"
        }
        return jsonify(study_hours)

    study_hours = {
        "study_hours": str(y-2) + ' - ' + str(y+2)
    }

    return jsonify(study_hours)

@app.route("/student_form", methods=['GET', 'POST'])
def student_form():
    form = StudentForm()
    
    # initially set result variables to None
    # this means that the user hasn't submitted anything yet
    # proceed to handle if the submit button is clicked.
    # if the form is submitted, pass the predicted result to the template
    result = None

    # input types
    categorical_features = ['parental_involvement', 'access_to_resources',
                            'extracurricular_activities', 'motivation_level', 'internet_access',
                            'family_income', 'teacher_quality', 'school_type', 'peer_influence',
                            'learning_disabilities', 'parental_education_level',
                            'distance_from_home', 'gender']
    numerical_features = ['hours_studied', 'attendance', 'sleep_hours', 'previous_scores', 'tutoring_sessions', 'physical_activity']

    # categories
    basic_information = ['name', 'gender', 'school_type']
    school_related = ['attendance', 'previous_scores', 'tutoring_sessions', 'extracurricular_activities']
    environment = ['teacher_quality', 'internet_access', 'access_to_resources',
                    'distance_from_home', 'parental_involvement']
    personal_info = ['sleep_hours', 'motivation_level', 'physical_activity', 'peer_influence', 'learning_disabilities']
    family_situation = ['family_income', 'parental_education_level']
    
    if form.validate_on_submit():
        try:
            # predict the study hours using form data
            prediction_response = predict(form.data)

            result = prediction_response.json.get('study_hours', "No result available")
            # print(form.data)
        except Exception as e:
            result = f"Error during prediction: {e}"

    return render_template('index.html',
                            title='Study Hours Estimator',
                            header='Study hours estimator',
                            form=form, result=result,
                            categorical_features=categorical_features,
                            numerical_features=numerical_features,
                            basic_information=basic_information, school_related=school_related,
                            environment=environment,
                            personal_info=personal_info, family_situation=family_situation)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
